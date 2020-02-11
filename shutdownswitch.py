#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import os
import pigpio

if __name__ == '__main__':

    pi = pigpio.pi()

    if not pi.connected:
        exit()

    # 定数定義
    SWITCH_GPIO  = 14    # スイッチ制御GPIO番号

    # GPIO設定
    pi.set_mode(SWITCH_GPIO, pigpio.INPUT)
    pi.set_pull_up_down(SWITCH_GPIO, pigpio.PUD_DOWN)

    try:
        pushtime = 0
        while True:
            # スイッチが押されたらカウンティング開始
            if pi.read(SWITCH_GPIO) == 1:
                pushtime += 1
                print(pushtime)

                # カウントが50（5秒経過）になったらシャットダウン
                if pushtime >= 50:
                    os.system("sudo shutdown -h now")
            else:
                # スイッチが離されたらカウンティングリセット
                pushtime = 0

            time.sleep(0.1)
    except KeyboardInterrupt:
        pi.stop()
