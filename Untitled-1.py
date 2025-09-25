#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
七段顯示器數學計算器
支援加減乘除運算，結果會在七段顯示器上逐位顯示
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
    for segment, pin in SEGMENTS.items():
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin, GPIO.LOW)

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
    """逐個顯示數字序列"""
    print(f"七段顯示器顯示：", end="")
    
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
        
        # 在字符間短暫清空
        if i < len(number_str) - 1:
            clear_display()
            time.sleep(0.3)
    
    print()  # 換行

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
    """顯示錯誤"""
    print("七段顯示器顯示：E (錯誤)")
    display_character('E')
    time.sleep(2)

def show_welcome_message():
    """顯示歡迎訊息"""
    print("=" * 50)
    print("七段顯示器數學計算器")
    print("=" * 50)
    print("支援運算：+ (加法), - (減法), * (乘法), / (除法)")
    print("範例：")
    print("  3 + 5")
    print("  10 - 3")
    print("  6 * 7")
    print("  15 / 3")
    print("  (2 + 3) * 4")
    print("-" * 50)
    print("輸入 'q' 或 'quit' 退出程式")
    print("=" * 50)

def main():
    """主程式"""
    try:
        setup_gpio()
        show_welcome_message()
        
        # 啟動提示
        print("系統就緒！七段顯示器已初始化")
        clear_display()
        
        while True:
            print()
            # 獲取用戶輸入
            expression = input("請輸入數學運算式：").strip()
            
            # 檢查退出指令
            if expression.lower() in ['q', 'quit', '退出']:
                print("感謝使用，再見！")
                break
            
            # 檢查空輸入
            if not expression:
                print("請輸入有效的運算式")
                continue
            
            print(f"計算：{expression}")
            
            # 計算結果
            result, error = safe_evaluate(expression)
            
            if error:
                print(f"錯誤：{error}")
                display_error()
                clear_display()
                continue
            
            # 格式化結果
            result_str = format_result(result)
            
            # 顯示結果
            print(f" 答案：{result_str}")
            print("-" * 30)
            
            # 檢查結果長度（七段顯示器通常顯示較短的數字）
            if len(result_str.replace('-', '').replace('.', '')) > 6:
                print("數字太長，僅在終端顯示")
                continue
            
            # 在七段顯示器上顯示結果
            display_number_sequence(result_str)
            
            # 保持顯示一段時間
            time.sleep(2)
            clear_display()
    
    except KeyboardInterrupt:
        print("\n\n⏹程式被使用者中斷")
    
    except Exception as e:
        print(f"發生未預期的錯誤：{e}")
        display_error()
    
    finally:
        print("🧹 清理 GPIO 並退出...")
        clear_display()
        GPIO.cleanup()
        print("清理完成")

if __name__ == "__main__":
    main()