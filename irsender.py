#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# excerpt from http://abyz.me.uk/rpi/pigpio/code/irrp_py.zip

import pigpio
import time
import os
import json

from logging import getLogger, NullHandler


class IRSender:
    def __init__(self, host, gpio, logger=None):
        self.__host = host
        self.__gpio = gpio
        if(logger == None):
            defLogger = getLogger(__name__)
            defLogger.addHandler(NullHandler())
            self.__logger = defLogger
        else:
            self.__logger = logger

    def load(self, file):
        try:
            f = open(file, "r")
        except:
            self.__logger.error('cannot open: {}'.format(FILE))
            return False

        self.__records = json.load(f)
        f.close()
        self.__logger.info('Load command:{}'.format(
            ','.join(self.__records.keys())))

        return True

    def __carrier(self, frequency, micros):
        """
        Generate carrier square wave.
        """
        wf = []
        cycle = 1000.0 / frequency
        cycles = int(round(micros / cycle))
        on = int(round(cycle / 2.0))
        sofar = 0
        for c in range(cycles):
            target = int(round((c + 1) * cycle))
            sofar += on
            off = target - sofar
            sofar += off
            wf.append(pigpio.pulse(1 << self.__gpio, 0, on))
            wf.append(pigpio.pulse(0, 1 << self.__gpio, off))
        return wf

    def __emit_ircode(self, code, pi):
        pi.set_mode(self.__gpio, pigpio.OUTPUT)
        pi.wave_clear()

        marks_wid = {}
        spaces_wid = {}

        wave = [0] * len(code)

        for i in range(0, len(code)):
            ci = code[i]
            if i & 1:  # Space
                if ci not in spaces_wid:
                    pi.wave_add_generic([pigpio.pulse(0, 0, ci)])
                    spaces_wid[ci] = pi.wave_create()
                wave[i] = spaces_wid[ci]
            else:  # Mark
                if ci not in marks_wid:
                    pi.wave_add_generic(self.__carrier(38.0, ci))
                    marks_wid[ci] = pi.wave_create()
                wave[i] = marks_wid[ci]

        # Send
        pi.wave_chain(wave)

        while pi.wave_tx_busy():
            time.sleep(0.002)

        # clear
        for i in marks_wid.values():
            pi.wave_delete(i)

        for i in spaces_wid.values():
            pi.wave_delete(i)

        pi.wave_clear()

    def emit_cmd(self, code):
        pi = pigpio.pi(self.__host)
        if not pi.connected:
            self.__logger.fatal('cannot connect pigpio')
            return False

        if code not in self.__records:
            self.__logger.error('cannot find cmd: {}'.format(cmd))
            return False

        self.__emit_ircode(self.__records[code], pi)

        pi.stop()  # Disconnect from Pi.

        return True
        