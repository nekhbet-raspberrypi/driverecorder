#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import pigpio

class NeoPixel:
    # コンストラクタ
    def __init__(self, pi):
        self.pi = pi
        self.h = self.pi.spi_open(0, 3200000, 0)

    # デストラクタ
    def __del__(self):
        self.set_color(0)
        self.pi.spi_close(self.h)

    # LEDカラーセット関数
    def set_color(self, color):
        buf = bytearray(24)

        # 上位ビットから変換
        for pos in range(24):
            buf[23 - pos] = 0xF8 if color & (2 ** pos) else 0x80

        self.pi.spi_write(self.h, buf)
        time.sleep(10e-5)

# メイン
if __name__ == '__main__':
    pi = pigpio.pi()
    if not pi.connected:
        exit()

    pixels = NeoPixel(pi)

    # RGB test
    pixels.set_color(0x00000F)
    try:
        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        del pixels
        pi.stop()
