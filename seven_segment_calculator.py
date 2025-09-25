#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
七段顯示器數學計算器（雙色LED版）
支援加減乘除運算，結果會在七段顯示器上逐位顯示
使用紅綠雙色LED指示正常/錯誤狀態
"""

import RPi.GPIO as GPIO
import time
import re

# 設定 GPIO 模式
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# 定義七段顯示器的 GPIO 接腳
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
GREEN_LED_PIN = 20  # 綠色LED - 正常狀態
RED_LED_PIN = 21    # 紅色LED - 錯誤狀態

# 數字和符號對應的段位配置
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
    9: {'a': True,  'b': True,  'c': True,  'd': True,  'e': False, 'f': True,  'g': True},
    '-': {'a': False, 'b': False, 'c': False, 'd': False, 'e': False, 'f': False, 'g': True},  # 負號
    'E': {'a': True,  'b': False, 'c': False, 'd': True,  'e': True,  'f': True,  'g': True}   # 錯誤顯示
}

def setup_gpio():
    """初始化 GPIO 設定"""
    # 設定七段顯示器接腳
    for segment, pin in SEGMENTS.items():
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin, GPIO.LOW)
    
    # 設定雙色LED指示燈接腳
    GPIO.setup(GREEN_LED_PIN, GPIO.OUT)
    GPIO.setup(RED_LED_PIN, GPIO.OUT)
    GPIO.output(GREEN_LED_PIN, GPIO.LOW)
    GPIO.output(RED_LED_PIN, GPIO.LOW)
    print(f"GPIO 初始化完成")
    print(f"   綠色LED接腳：{GREEN_LED_PIN}")
    print(f"   紅色LED接腳：{RED_LED_PIN}")

def green_led_on():
    """開啟綠色LED"""
    GPIO.output(GREEN_LED_PIN, GPIO.HIGH)
    GPIO.output(RED_LED_PIN, GPIO.LOW)  # 確保紅色LED關閉

def red_led_on():
    """開啟紅色LED"""
    GPIO.output(RED_LED_PIN, GPIO.HIGH)
    GPIO.output(GREEN_LED_PIN, GPIO.LOW)  # 確保綠色LED關閉

def all_leds_off():
    """關閉所有LED"""
    GPIO.output(GREEN_LED_PIN, GPIO.LOW)
    GPIO.output(RED_LED_PIN, GPIO.LOW)

def green_led_blink(times=3, duration=0.3):
    """綠色LED閃爍 - 表示正常/成功"""
    print(f"綠色LED閃爍 {times} 次")
    for i in range(times):
        green_led_on()
        time.sleep(duration)
        all_leds_off()
        if i < times - 1:  # 最後一次不要停留
            time.sleep(duration)

def red_led_blink(times=5, duration=0.15):
    """紅色LED閃爍 - 表示錯誤/警告"""
    print(f"紅色LED閃爍 {times} 次")
    for i in range(times):
        red_led_on()
        time.sleep(duration)
        all_leds_off()
        if i < times - 1:  # 最後一次不要停留
            time.sleep(duration)

def startup_led_sequence():
    """系統啟動LED序列"""
    print("系統啟動指示...")
    # 綠色閃爍1次表示系統正常啟動
    green_led_blink(1, 1.0)
    time.sleep(0.5)

def ready_to_display_sequence():
    """準備顯示結果的LED序列"""
    print("準備顯示指示...")
    # 綠色快速閃爍2次表示準備開始
    green_led_blink(2, 0.3)
    time.sleep(0.5)

def display_complete_sequence():
    """顯示完成的LED序列"""
    print("顯示完成指示...")
    # 綠色慢速閃爍3次表示成功完成
    green_led_blink(3, 0.25)

def error_led_sequence():
    """錯誤指示LED序列"""
    print("錯誤指示...")
    # 紅色快速閃爍5次表示錯誤
    red_led_blink(5, 0.1)

def warning_led_sequence():
    """警告指示LED序列（數字太長等）"""
    print("警告指示...")
    # 紅色中速閃爍3次表示警告
    red_led_blink(3, 0.2)

def goodbye_led_sequence():
    """退出告別LED序列"""
    print("退出指示...")
    # 綠色和紅色交替閃爍
    for i in range(3):
        green_led_on()
        time.sleep(0.3)
        red_led_on()
        time.sleep(0.3)
    all_leds_off()

def display_character(char):
    """顯示指定字符（數字或符號）"""
    if char == '.':
        # 小數點處理（如果有額外的小數點LED）
        return
    
    if char not in DIGIT_PATTERNS:
        print(f"無法顯示字符：{char}")
        return
    
    pattern = DIGIT_PATTERNS[char]
    
    # 設定各段的狀態
    for segment, pin in SEGMENTS.items():
        if pattern[segment]:
            GPIO.output(pin, GPIO.HIGH)
        else:
            GPIO.output(pin, GPIO.LOW)

def clear_display():
    """清空顯示器"""
    for pin in SEGMENTS.values():
        GPIO.output(pin, GPIO.LOW)

def display_number_sequence(number_str, delay=1.5):
    """逐個顯示數字序列，包含LED指示"""
    print(f"準備顯示結果：{number_str}")
    print("-" * 40)
    
    # 1. 準備顯示 - 綠色LED閃爍
    ready_to_display_sequence()
    
    # 2. 開啟綠色LED，表示正在正常顯示結果
    green_led_on()
    print("正在顯示結果...")
    print("七段顯示器顯示：", end="")
    
    # 3. 逐個顯示每個字符
    for i, char in enumerate(number_str):
        if char == '.':
            print(".", end="")
            continue
            
        if char == '-':
            print("-", end="", flush=True)
            display_character('-')
            time.sleep(delay)
        elif char.isdigit():
            print(char, end="", flush=True)
            display_character(int(char))
            time.sleep(delay)
        
        # 在字符間短暫清空（但保持綠色LED亮著）
        if i < len(number_str) - 1:
            clear_display()
            time.sleep(0.3)
    
    print()  # 換行
    
    # 4. 顯示完成 - 綠色LED閃爍表示成功結束
    time.sleep(0.5)
    clear_display()
    display_complete_sequence()
    print("-" * 40)

def safe_evaluate(expression):
    """安全地計算數學表達式"""
    try:
        # 移除空格
        expression = expression.replace(" ", "")
        
        # 檢查是否只包含數字和基本運算符
        if not re.match(r'^[0-9+\-*/().]+$', expression):
            return None, "表達式包含不支援的字符"
        
        # 防止除零錯誤
        if '/0' in expression.replace(' ', ''):
            return None, "除零錯誤"
        
        # 計算結果
        result = eval(expression)
        
        # 檢查結果是否為數字
        if not isinstance(result, (int, float)):
            return None, "計算結果不是數字"
        
        return result, None
        
    except ZeroDivisionError:
        return None, "除零錯誤"
    except SyntaxError:
        return None, "語法錯誤"
    except Exception as e:
        return None, f"計算錯誤：{str(e)}"

def format_result(result):
    """格式化結果為適合顯示的字符串"""
    if isinstance(result, float):
        # 如果是整數，不顯示小數點
        if result.is_integer():
            return str(int(result))
        else:
            # 保留兩位小數，去除尾隨零
            return f"{result:.2f}".rstrip('0').rstrip('.')
    else:
        return str(result)

def display_error():
    """顯示錯誤，包含紅色LED指示"""
    print("計算錯誤")
    
    # 紅色LED快速閃爍表示錯誤
    error_led_sequence()
    
    # 紅色LED亮起並顯示錯誤字符E
    red_led_on()
    print("錯誤狀態 - 七段顯示器顯示：E")
    display_character('E')
    time.sleep(2)
    clear_display()
    all_leds_off()

def show_welcome_message():
    """顯示歡迎訊息"""
    print("=" * 70)
    print("七段顯示器數學計算器（雙色LED版）")
    print("=" * 70)
    print("新功能：雙色LED指示系統")
    print()
    print("LED指示說明：")
    print("   綠色LED：正常操作")
    print("      • 系統啟動：長閃爍1次")
    print("      • 準備顯示：快速閃爍2次")
    print("      • 正在顯示：持續亮起")
    print("      • 顯示完成：慢速閃爍3次")
    print()
    print("   紅色LED：錯誤/警告")
    print("      • 計算錯誤：快速閃爍5次")
    print("      • 數字太長：中速閃爍3次")
    print("      • 錯誤狀態：持續亮起")
    print()
    print("   退出程式：綠紅交替閃爍")
    print()
    print("支援運算：+ (加法), - (減法), * (乘法), / (除法)")
    print("範例：")
    print("   3 + 5")
    print("   10 - 3")
    print("   6 * 7")
    print("   15 / 3")
    print("   (2 + 3) * 4")
    print("-" * 70)
    print("輸入 'q' 或 'quit' 退出程式")
    print("=" * 70)

def main():
    """主程式"""
    try:
        setup_gpio()
        show_welcome_message()
        
        # 啟動提示
        startup_led_sequence()
        print("系統就緒！七段顯示器和雙色LED已初始化")
        clear_display()
        
        while True:
            print()
            # 獲取用戶輸入
            expression = input("請輸入數學運算式：").strip()
            
            # 檢查退出指令
            if expression.lower() in ['q', 'quit', '退出']:
                print("感謝使用，再見！")
                goodbye_led_sequence()
                break
            
            # 檢查空輸入
            if not expression:
                print("請輸入有效的運算式")
                warning_led_sequence()
                continue
            
            print(f"計算：{expression}")
            
            # 計算結果
            result, error = safe_evaluate(expression)
            
            if error:
                print(f"錯誤：{error}")
                display_error()
                continue
            
            # 格式化結果
            result_str = format_result(result)
            
            # 顯示結果
            print(f"答案：{result_str}")
            
            # 檢查結果長度（七段顯示器通常顯示較短的數字）
            if len(result_str.replace('-', '').replace('.', '')) > 6:
                print("數字太長，僅在終端顯示")
                warning_led_sequence()
                continue
            
            # 在七段顯示器上顯示結果（包含綠色LED指示）
            display_number_sequence(result_str)
            
            # 完成後短暫停留
            time.sleep(1)
    
    except KeyboardInterrupt:
        print("\n\n程式被使用者中斷")
    
    except Exception as e:
        print(f"發生未預期的錯誤：{e}")
        display_error()
    
    finally:
        print("清理 GPIO 並退出...")
        clear_display()
        all_leds_off()
        GPIO.cleanup()
        print("清理完成")

if __name__ == "__main__":
    main()