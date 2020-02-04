#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import commands
import pigpio

if __name__ == '__main__':

    pi = pigpio.pi()

    if not pi.connected:
        exit()

    # 定数定義
    coolfan_gpio  = 4    # ファン制御GPIO番号
    thermal_min   = 40   # 最低CPU温度
    thermal_max   = 70   # 最大CPU温度
    fan_duty_min  = 40   # 最小Duty値
    fan_duty_max  = 100  # 最大Duty値
    fan_frequency = 10   # 周波数値

    # duty計算用
    thermal_range = thermal_max - thermal_min
    duty_range = fan_duty_max - fan_duty_min

    # GPIO設定
    pi.set_mode(coolfan_gpio, pigpio.OUTPUT)
    pi.set_PWM_range(coolfan_gpio, fan_duty_max)
    pi.set_PWM_frequency(coolfan_gpio, fan_frequency)

    # duty値保持
    duty_now = 0

    try:
        while True:
            # 現在温度を取得
            tmp = commands.getoutput("cat /sys/class/thermal/thermal_zone0/temp")
            thermal = float(tmp) / 1000

            # duty値を計算
            duty = 0
            if thermal >= thermal_max:
                duty = 100
            elif thermal >= thermal_min:
            	duty = round((thermal - thermal_min) / thermal_range * duty_range + fan_duty_min)

            # duty値が変更されていれば設定
            if duty_now != duty:
                pi.set_PWM_dutycycle(coolfan_gpio, duty)
                duty_now = duty

            time.sleep(1)

    except KeyboardInterrupt:
        pi.set_PWM_dutycycle(coolfan_gpio, 0)
        pi.stop()
