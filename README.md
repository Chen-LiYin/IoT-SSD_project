# IoT Assignment 1 - Raspberry Pi + 7-Segment Display (SSD)

113423037 資管碩二 陳俐吟 Jerry

# Part A

Determine your SSD is CC or CA (and find the common pin)

-   Common Cathode(共陰極)
    ![Alt text](<photo/截圖 2025-09-29 下午2.26.25.png>)
-   Common pin
    ![Alt text](<photo/截圖 2025-09-29 下午2.32.44.png>)
    ![![Alt text](image.png)](<photo/截圖 2025-09-29 下午2.35.04.png>)

# PartB

## Programmer Test

1.  展示 0–9 序列

    影片連結：https://youtube.com/shorts/fpBC6WQZfhE?feature=share

    內容說明：
    先進行 0-9 的序列展示，以及 9-0 倒數展示，並且透過 LED 輔助結果

    -   綠色 LED 指示（正常輸入）：
        -   當輸入正確的 0-9 數字時 → 綠色 LED 會短暫亮起
        -   程式正常退出時 → 綠色 LED 閃爍 2 次
    -   紅色 LED 指示（錯誤輸入）：
        -   輸入非數字字元（如字母、符號）→ 紅色 LED 閃爍 3 次
        -   輸入超出範圍的數字（如 10、-1）→ 紅色 LED 閃爍 3 次
        -   發生其他錯誤 → 紅色 LED 快速閃爍 5 次

## Bouns

2.  算式計算機

    影片連結：https://youtube.com/shorts/nsMCnQI8oF4?feature=share

    內容說明：

    輸入算式可以顯示結果，透過 LED 輔助正確或正在展示的結果，以及錯誤的 LED 回報。

    -   綠色 LED （ 正常操作）：
        -   系統啟動：長閃爍 1 次
        -   準備顯示：快速閃爍 2 次
        -   正在顯示：持續亮起
        -   顯示完成：慢速閃爍 3 次
    -   紅色 LED（錯誤/警告）：

        -   計算錯誤：快速閃爍 5 次（如：除以零、語法錯誤）
        -   數字太長：中速閃爍 3 次（結果超過 6 位數）
        -   空輸入警告：中速閃爍 3 次
        -   錯誤狀態顯示：持續亮起（顯示"E"時）

    -   小數點會與數字一起顯示:
        ```
        例如顯示 3.14 時：
        顯示數字 3 + 小數點亮起
        顯示數字 1
        顯示數字 4
        ```
    -   範例的算式：
        ```
        5 - 8
        10 / 3
        (2 + 3) * 4
        ```

**接線位置**

```
七段顯示器：
- a段：GPIO 18
- b段：GPIO 23
- c段：GPIO 24
- d段：GPIO 25
- e段：GPIO 8
- f段：GPIO 7
- g段：GPIO 12
- DP（小數點）：GPIO 16

LED指示燈：
- 綠色LED：GPIO 20 → 電阻 → GND
- 紅色LED：GPIO 21 → 電阻 → GND
```

![Alt text](<photo/截圖 2025-09-29 下午6.28.39.png>)
