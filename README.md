# 楽しい工作シリーズ「ブルドーザ」のDonkeycar化

このリポジトリは、 [タミヤ 楽しい工作シリーズ No.104 ブルドーザー工作基本セット](https://store.shopping.yahoo.co.jp/shophoney/20190307213959-00071.html?sc_e=slga_pla) をDonkeyCar化した際のアプリケーションプログラムです。
工具や外装組み付け部品を除き、約22,500円(税込)で制作することができます。

* [Donkeycar Ver3.1.1](http://docs.donkeycar.com/) が前提です
　動作確認を行ったバージョンが上記です。

* Raspberry Pi 3B+ の使用が前提です
  pigpioパッケージを使用しているため Jetson では動作しません。

* Raspbean Streatch Lite の使用が前提です。
　動作確認を行ったバージョンが上記です。

## ブルドーザ本体の製作

* 以下の部品を調達してください。

| **部品名** | **参考単価** | **数量** | **用途** |
|:--|--:|--:|:--|
| [タミヤ 楽しい工作シリーズ No.104 ブルドーザー工作基本セット](https://store.shopping.yahoo.co.jp/shophoney/20190307213959-00071.html?sc_e=slga_pla) | 6,099円(税込) | 1セット | Donkey Car本体として |
| [Raspberry Pi 3B+](https://www.switch-science.com/catalog/3920/) | 5,670円(税込) | 1台 | Zeroを使用するとtensorflowが推論中内部エラーを出す |
| [Raspberry Pi用広角カメラモジュール](https://www.switch-science.com/catalog/3211/) | 4,773円(税込) | 1セット | 入力データ取得用として |
| [SANDISK SDSQUAC-016G-JN3MA ウルトラ microSDHC UHS-I カード 16GB](https://www.yodobashi.com/product/100000001003810858/) | 2,654円(税込) | 1枚 | Raspberry Pi用ストレージとして |
| [Maxell MPC-C2600BK モバイル充電バッテリー 2.600mAh ブラック](https://www.yodobashi.com/product/100000001002808783/) | 1,280円(税込) | 1台 | Raspberry Piバッテリとして(他の製品でも可) |
| [ELECOM JC-U3912Tワイヤレスコントローラ](https://www.elecom.co.jp/products/JC-U3912TBK.html) | 5,841円(税込) | 1台 | 手動運転デバイスとして、要単3電池✕2 |
|  [ELECOM TB-MAEMCBN010BKタブレット用OTGケーブル スタンダード microB-Aメス変換 USB2.0 ブラック 0.1m](https://www.yodobashi.com/product/100000001002965774/) | 500円(税込) | 1本 | コントローラドングル接続用 |
| [TB6612使用Dual DCモータドライブキット](http://akizukidenshi.com/catalog/g/gK-11219/) | 350円(税込) | 1セット | DCモータ＆モータ用電源とRaspberry Piをつなぐモータドライバとして |
| [ブレッドボード・ジャンパー延長ワイヤ（メスーメス）15cm赤　（10本入）](http://akizukidenshi.com/catalog/g/gP-03474/) | 330円(税込) | 1セット | モータドライブキットとRaspberry Piをつなぐ |
| [PANASONIC LR6NJ/2B アルカリ乾電池 EVOLTA NEO（エボルタ ネオ） 単3形 4本](https://www.yodobashi.com/product/100000001003469874/) | 304円(税込) | 2セット(4本) | JC-U3291TBK の電池として |
| [電池ボックス 単3×4本 リード線・フタ・スイッチ付](http://akizukidenshi.com/catalog/g/gP-00311/) | 110円(税込) | 1個 | モータ用電源として |
| [積層コンデンサ 0.1μF 50V 10本入り](絶縁ラジアルリード型積層セラミックコンデンサー０．１μＦ５０Ｖ５ｍｍ（１０個入）) | 100円(税抜)|1パック(3本×2モーター)|DCモータノイズ除去用|

> 上記には、 **本体に組み付けるための材料** を含んでいません。またはんだ・はんだごてをはじめとする工具類も含まれていません。

* モバイル充電バッテリをフル充電する
* ブルドーザー工作基本セットを同梱マニュアルに従い組み立てる（ドーザー部分は外してもよい）
* 各モータに0.1μF(50V)×3をパシコンとしてはんだ付け(ギアボックスに搭載する際に干渉しないようにする)
* DCモータドライブキットをはんだ付け、ピンコネクタは組付け易い位置（秋月サイトにある画像とは反対にピンヘッダをつける）にはんだづけ
* 電池ボックスのスイッチをOFFにしてアルカリ乾電池を装填、ケーブル先がばらばらにならないようはんだでまとめておく
* 2つのモータのケーブル端も同様にはんだづけ
* ２つのモータと電池ボックスをDCモータドライブキットのターミナルに接続

| 接続元 | 接続先 | 備考 |
|:------|:-------|:----|
| Raspberry Pi GPIO 16 | DCモータドライブキット AIN1 | ジャンパワイヤで接続 |
| Raspberry Pi GPIO 21 | DCモータドライブキット AIN2 | ジャンパワイヤで接続 |
| Raspberry Pi GPIO 20 | DCモータドライブキット PWMA | ジャンパワイヤで接続 |
| Raspberry Pi GPIO 16 | DCモータドライブキット BIN1 | ジャンパワイヤで接続 |
| Raspberry Pi GPIO 21 | DCモータドライブキット BIN2 | ジャンパワイヤで接続 |
| Raspberry Pi GPIO 20 | DCモータドライブキット PWMB | ジャンパワイヤで接続 |
| Raspberry Pi 5V | DCモータドライブキット VCC | ジャンパワイヤで接続 |
| Raspberry Pi GND | DCモータドライブキット GND | ジャンパワイヤで接続 |
| Raspberry Pi GPIO 04 | DCモータドライブキット STBY | ジャンパワイヤで接続 |
| 電池ボックスケーブル赤 | DCモータドライブキット　VM | 電池ボックスのスイッチがOFFであることを確認してから、ターミナルブロックに接続 |
| 電池ボックスケーブル黒 | DCモータドライブキット　PGND | 電池ボックスのスイッチがOFFであることを確認してから、ターミナルブロックに接続 |
| 左履帯駆動DCモータケーブル上 | DCモータドライブキット A01 | ターミナルブロックに接続 |
| 左履帯駆動DCモータケーブル下 | DCモータドライブキット A02 | ターミナルブロックに接続 |
| 右履帯駆動DCモータケーブル上 | DCモータドライブキット B02 | ターミナルブロックに接続 |
| 右履帯駆動DCモータケーブル下 | DCモータドライブキット B01 | ターミナルブロックに接続 |

* ジャンパ延長ワイヤとRaspberry Piを接続

> 結線の詳細は [こちら](./docs/circuit.md) を参照のこと

* Raspberry Piにカメラモジュールを接続
* 本体に組み付け
* Raspberry Pi にJC-U3912T USBアダプタを接続
* JC-U3912Tに電池を搭載する（使用前に下面の電源をONにすること）

## SDカードの準備

* micro SDカード (32GB)を入手して、フォーマットを実行
* [Raspbean ダウンロードサイト](https://www.raspberrypi.org/downloads/raspbian/) から Raspbean Streatch Lite のimg圧縮ファイルをダウンロードし、展開する（ほげほげ部は最新OS呼称）
* ImageWriterなどでimgファイルをmicro SDカードへ書き込み
* `wpa_supplicant.conf` を作成し、microSDカードへ保存(UTF-8/LF)、取り外す

```ini
country=US
ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
update_config=1

network={
    ssid="XXXXXXXXXXX"
    psk="xxxxxxxxxxxxxxxxxx"
}
```

* `ssh` というファイル名で0バイトファイルを作成し、microSDカードへ保存(UTF-8/LF)、取り外す

> `ssh` を作成しておくと、初期起動時点からにssh接続可能になる

## Raspbean Lite のセットアップ

### ホスト名変更および各種初期設定

* SDカードを刺し、HDMIケーブル経由でモニタ、USB経由でマウス＆キーボードを接続し、起動する
* IPアドレスを探し出し、ターミナルソフト経由でSSH接続する(pi/raspberry)
* `sudo vi /etc/dphys-swapfile` を実行し、`CONF_SWAPSIZE` と `CONF_MAXSWAP` を `4096` に変更し、保存する
* `sudo raspi-config` を実行し、以下の設定を行う

> * デフォルトパスワードの変更
> * Interfacing Options の Camera を有効化
> * Interfacing Options の I2C を有効化
> * Advanced Options の Exapand Filesystem を選択

* 終了すると再起動指示が出るので、従う

### OSパッケージ最新化および前提パッケージインストール

* 再起動したら、再度ターミナルソフトでSSHログイン
* 以下のコマンドを実行し、SSH接続可能にする

```bash
sudo apt update && sudo apt upgrade -y
sudo apt install build-essential python3 python3-dev python3-pip python3-virtualenv python3-numpy python3-picamera python3-pandas python3-rpi.gpio i2c-tools avahi-utils joystick libopenjp2-7-dev libtiff5-dev gfortran libatlas-base-dev libopenblas-dev libhdf5-serial-dev git ntp -y
sudo apt install libilmbase-dev libopenexr-dev libgstreamer1.0-dev libjasper-dev libwebp-dev libatlas-base-dev libavcodec-dev libavformat-dev libswscale-dev libqtgui4 libqt4-test -y
sudo apt install pigpio
sudo systemctl start pigpiod
sudo systemctl enable pigpiod
```

### Python環境構築

* 以下のコマンドを実行し、Python3環境を構築する。

```bash
cd ~/
mkdir projects
cd projects
python3 -m virtualenv -p python3 env --system-site-packages
echo "source env/bin/activate" >> ~/.bashrc
source ~/.bashrc
```

* 以下のコマンドを実行し、Donkeycarおよび関連パッケージをインストールする

```bash
cd ~/projects
git clone https://github.com/autorope/donkeycar -b 3.1.1
cd donkeycar
pip install -e .[pi]
pip install tensorflow==1.13.1
pip install pigpio
pip install opencv-python
```

### このリポジトリアプリケーションの展開

* 以下のコマンドを実行して、本リポジトリをダウンロードする

```bash
cd ~/projects
git clone https://github.com/coolerking/caterpillar
cd ~/
ln -s /home/pi/projects/caterpillar .
```

* 以下のコマンドを実行して、設定ファイルを変更する

```bash
cd ~/caterpillar
cp myconfig_cat.py myconfig.py
```

## 手動運転

1. DCモータ電源のスイッチON
2. ssh接続し、ユーザ名`pi`、パスワード`raspberry`でログイン
3. `cd ~/caterpillar` を実行する
4. (存在しない場合) `mkdir data` を実行し、tubデータ格納ディレクトリを作成する
5. USBワイヤレスアダプタを３秒以上押し込み、LEDを青点滅に変更（ペアリング開始）
6. PS4コントローラの充電をはずし（はずさなくても可能）、shareボタンを押しながらPSロゴボタンを3秒以上押し続け、コントローラ側のLEDが青点灯させる（ペアリング完了）
7. `python manage_cat.py drive` を実行する

* コントローラはプログラム実行前に電源ONにすること
* [JC-U3912Tの操作方法](./docs/jc_u3912t.md) はこちらを参照のこと

## 注意

### カメラの取り付け

カメラが動作しない場合は以下の項目を確認してください。

* `sudo raspi-config` でカメラを有効化したかどうか
* `raspistill -o test.jpg` で撮影できるかどうか
* `vcgencmd get_camera` の結果が両方 `1` かどうか

上記が動作しない場合は、カメラをつけ直ししてください。
Raspberry Piのカメラインターフェイスは、すぐにずれてしまうので注意してください。

### トレーニングおよび自動運転

Donkeycar上のアプリケーションディレクトリが `~/caterpillar` であること以外は、通常のDonkeycarと同じです。

### モーターの強制停止

プログラムが異常停止した場合、モータが回転したままとなることがあります。
そのような場合は、DCモータ電源（電池ボックス）をオフにしてください。

## ライセンス

本リポジトリのソースコードは、すべて [MITライセンス](./LISENSE) 準拠とします。
