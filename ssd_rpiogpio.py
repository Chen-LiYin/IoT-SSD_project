#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
七段顯示器測試程式
顯示數字 0-9
加入雙色LED除錯功能
"""

import RPi.GPIO as GPIO
import time

# 設定 GPIO 模式
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# 定義七段顯示器的 GPIO 接腳
# 你可以根據實際接線修改這些接腳編號
SEGMENTS = {
    'a': 18,  # 上橫線
    'b': 23,  # 右上豎線
    'c': 24,  # 右下豎線
    'd': 25,  # 下橫線
    'e': 8,   # 左下豎線
    'f': 7,   # 左上豎線
    'g': 12   # 中間橫線
}

# LED 指示燈接腳
GREEN_LED_PIN = 20  # 綠色LED - 正常輸入
RED_LED_PIN = 21    # 紅色LED - 錯誤輸入

# 數字對照的段位配置（True = 點亮，False = 熄滅）
DIGIT_PATTERNS = {
    0: {'a': True,  'b': True,  'c': True,  'd': True,  'e': True,  'f': True,  'g': False},
    1: {'a': False, 'b': True,  'c': True,  'd': False, 'e': False, 'f': False, 'g': False},
    2: {'a': True,  'b': True,  'c': False, 'd': True,  'e': True,  'f': False, 'g': True},
    3: {'a': True,  'b': True,  'c': True,  'd': True,  'e': False, 'f': False, 'g': True},
    4: {'a': False, 'b': True,  'c': True,  'd': False, 'e': False, 'f': True,  'g': True},
    5: {'a': True,  'b': False, 'c': True,  'd': True,  'e': False, 'f': True,  'g': True},
    6: {'a': True,  'b': False, 'c': True,  'd': True,  'e': True,  'f': True,  'g': True},
    7: {'a': True,  'b': True,  'c': True,  'd': False, 'e': False, 'f': False, 'g': False},
    8: {'a': True,  'b': True,  'c': True,  'd': True,  'e': True,  'f': True,  'g': True},
    9: {'a': True,  'b': True,  'c': True,  'd': True,  'e': False, 'f': True,  'g': True}
}

def setup_gpio():
    """初始化 GPIO 設定"""
    # 設定七段顯示器接腳
    for segment, pin in SEGMENTS.items():
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin, GPIO.LOW)
    
    # 設定雙色LED接腳
    GPIO.setup(GREEN_LED_PIN, GPIO.OUT)
    GPIO.setup(RED_LED_PIN, GPIO.OUT)
    GPIO.output(GREEN_LED_PIN, GPIO.LOW)
    GPIO.output(RED_LED_PIN, GPIO.LOW)
    
    print("GPIO 初始化完成")
    print(f"綠色LED接腳：{GREEN_LED_PIN}")
    print(f"紅色LED接腳：{RED_LED_PIN}")

def green_led_on():
    """開啟綠色LED"""
    GPIO.output(GREEN_LED_PIN, GPIO.HIGH)
    GPIO.output(RED_LED_PIN, GPIO.LOW)

def red_led_on():
    """開啟紅色LED"""
    GPIO.output(RED_LED_PIN, GPIO.HIGH)
    GPIO.output(GREEN_LED_PIN, GPIO.LOW)

def all_leds_off():
    """關閉所有LED"""
    GPIO.output(GREEN_LED_PIN, GPIO.LOW)
    GPIO.output(RED_LED_PIN, GPIO.LOW)

def red_led_blink(times=3, duration=0.2):
    """紅色LED閃爍 - 表示錯誤"""
    print(f"錯誤指示：紅色LED閃爍 {times} 次")
    for i in range(times):
        red_led_on()
        time.sleep(duration)
        all_leds_off()
        time.sleep(duration)

def green_led_blink(times=1, duration=0.3):
    """綠色LED閃爍 - 表示正確"""
    for i in range(times):
        green_led_on()
        time.sleep(duration)
        all_leds_off()
        time.sleep(duration)

def display_digit(digit):
    """顯示指定數字"""
    if digit not in DIGIT_PATTERNS:
        print(f"錯誤：不支援的數字 {digit}")
        return
    
    pattern = DIGIT_PATTERNS[digit]
    
    # 設定各段的狀態
    for segment, pin in SEGMENTS.items():
        if pattern[segment]:
            GPIO.output(pin, GPIO.HIGH)  # 點亮
        else:
            GPIO.output(pin, GPIO.LOW)   # 熄滅
    
    print(f"顯示數字：{digit}")

def clear_display():
    """清空顯示器"""
    for pin in SEGMENTS.values():
        GPIO.output(pin, GPIO.LOW)

def test_all_segments():
    """測試所有段位（顯示數字8）"""
    print("測試所有段位...")
    for pin in SEGMENTS.values():
        GPIO.output(pin, GPIO.HIGH)
    time.sleep(2)
    clear_display()

def countdown_demo():
    """倒數計時示範 9 -> 0"""
    print("倒數計時示範：9 -> 0")
    for i in range(9, -1, -1):
        display_digit(i)
        time.sleep(1)
    clear_display()

def countup_demo():
    """正數計時示範 0 -> 9"""
    print("正數計時示範：0 -> 9")
    for i in range(10):
        display_digit(i)
        time.sleep(1)
    clear_display()

def main():
    """主程式"""
    try:
        print("七段顯示器測試程式啟動")
        print("GPIO 接腳配置：")
        for segment, pin in SEGMENTS.items():
            print(f"  段 {segment.upper()}: GPIO {pin}")
        
        setup_gpio()
        
        # 測試所有段位
        test_all_segments()
        
        # 顯示 0-9 每個數字
        print("\n顯示數字 0-9：")
        for digit in range(10):
            display_digit(digit)
            time.sleep(1.5)
        
        clear_display()
        time.sleep(0.5)
        
        # 倒數計時展示
        countdown_demo()
        
        # 互動模式
        print("\n互動模式")
        print("輸入數字 0-9 顯示（輸入 'q' 退出）：")
        while True:
            user_input = input("請輸入數字 0-9：").strip()
            
            if user_input.lower() == 'q':
                print("退出程式")
                green_led_blink(2, 0.3)
                break
            
            try:
                digit = int(user_input)
                if 0 <= digit <= 9:
                    # 正確輸入 - 綠色LED短暫亮起
                    green_led_on()
                    display_digit(digit)
                    time.sleep(0.3)
                    all_leds_off()
                else:
                    # 數字超出範圍 - 紅色LED閃爍
                    print(f"錯誤：請輸入 0-9 之間的數字")
                    red_led_blink(3, 0.2)
                    clear_display()
            except ValueError:
                # 非數字輸入 - 紅色LED閃爍
                print("錯誤：請輸入有效的數字")
                red_led_blink(3, 0.2)
                clear_display()
            
            except Exception as e:
                print(f"發生錯誤：{e}")
                red_led_blink(5, 0.1)
    
    except KeyboardInterrupt:
        print("\n程式被使用者中斷")
    
    except Exception as e:
        print(f"發生錯誤：{e}")
        red_led_blink(5, 0.1)
    
    finally:
        print("清理 GPIO 並退出...")
        clear_display()
        all_leds_off()
        GPIO.cleanup()
        print("清理完成")

if __name__ == "__main__":
    main()