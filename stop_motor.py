# -*- coding: utf-8 -*-
"""
モータが止まらなくなった場合、このモジュールを実行して停止させることができる。
myconfig.py を使用するため、Donkeycarアプリケーションディレクトリ上からしか
実行できない。
"""

def stop_motor(use_debug=False):
    """
    TB6612 上のSTBYピンを0にセットする。
    引数：
        use_debug   デバッグフラグ（デフォルトFalse）
    戻り値：
        なし
    """
    import donkeycar as dk
    cfg = dk.load_config()
    import pigpio
    pgio = pigpio.pi()

    from parts import PIGPIO_OUT

    # TB6612 STBY ピン初期化
    stby = PIGPIO_OUT(pin=cfg.TB6612_STBY_GPIO, pgio=pgio, debug=use_debug)
    stby.run(0)
    stby.shutdown()
    print('Set Stop on STBY pin')
    pgio.stop()

if __name__ == '__main__':
    stop_motor(use_debug=True)