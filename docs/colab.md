# Google Colaboratory を使ったトレーニング

* [ipynbファイル](../caterpillar.ipynb)

## Raspberry Pi上での操作

```bash
cd ~/caterpillar
ls data/
tar cvfz datas_YYYYMMDD_XX.tar.gz ./data
```

## ホストPC上での操作

### WinSCPでの操作

`/home/pi/caterpillar/datas_YYYYMMDD_XX.tar.gz` を　WinSCPでホストPC側へコピーする。

## Chrome 上での操作

* 自分のGoogleアカウントで GoogleDriveを開く
* 適当なフォルダで「＋新規」＞「その他」＞「Google Colaboratory」を選択
* ファイル名を適当に変更
* ランタイム＞ランタイムのタイプを変更
* ラインタイムのタイプをPython3に変更
* ハードウェアアクセラレータをGPUに変更
* 左横の「＞」を選択
* ファイルを選択
* アップロードを選択
* `datas_YYYYMMDD_XX.tar.gz` を選択しOK
* 中央のセルに以下のコードを書き込み、実行する

```bash
%cd /content/
git clone https://github.com/autorope/donkeycar -b 3.1.1
cd donkeycar
pip install .[pc]
pip install tensorflow-gpu==1.15.0
%cd /content/
git clone https://github.com/coolerking/caterpillar
cd caterpillar
git checkout master
mkdir models
tar xvfz ../datas_YYYYMMDD_XX.tar.gz
python manage_cat.py train --tub data/tub_X_YY_MM_DD/ --model models/cat_linear.h5 --type linear
# categorical を使いたい場合
#python manage_cat.py train --tub data/tub_X_YY_MM_DD/ --model models/cat_categorical.h5 --type categorical
```

* 終わったら、左のペインから作成したモデルファイルを選択し、ダウンロードする
