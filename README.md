# irctl
https://beebotte.com の MQTTでGoogle Home からの IFTTT Webhookを受けて部屋のリモコンライトをつけたり消したりする例

「ねぇGoogle 部屋の電気消して！」

# ファイル
Python3で実装されています。

 - irctl.py
	 - メイン実装
 - irsender.py
	 - irrp.pyからIRコマンドを送る部分だけ抜き出したクラス
	 - irrp.py は http://abyz.me.uk/rpi/pigpio/code/irrp_py.zip から入手
- irctl.service
	- systemdでデーモン起動する際の設定例ファイル
- codes
	- わたしの家についてる蛍光灯のコード(サンプル)

# Beebotteの設定について
チャンネルHomeControllerでリソースlightを前提にしているので、必要に応じて変えてください。トークンは環境変数から読むようにしてあるので、irctl.serviceで設定してください。

また、実装では手抜きしてあってhttpでBeebotteに繋がります。httpsにしたいひとはポート変えて証明書をMQTTクライアントに読ませてください。

# IFTTTの設定について
参考文献2そのままなので略

# IR送信部について
RasPiのGPIO(実装は17)にトランジスタ一個噛ませてIrLEDを直結するという手抜き実装。いろんな例があるのでここでは深入しません。

# 参考文献
以下のQiita記事を元に作ってます。

 1. 格安スマートリモコンの作り方 ( https://qiita.com/takjg/items/e6b8af53421be54b62c9 )
	- pigpio を使うあたり
 2.  Google AssistantとRaspberry Piで自宅の家電を操作する ( https://qiita.com/104ki/items/9dcfe03246099d03d4dd )
	 - IFTTTの設定はまるまるこのまま。MQTTまわりとスクリプトのなかみはここから

# かいたひと
書いただけともいう。
walkure at 3pf.jp