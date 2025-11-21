# xrinput

一个简单的捕获 VR 输入的 Python 库, 使用简单的 API 获取 VR 设备上的所有数据

参考 Wiki: https://zread.ai/DBinK/xrinput

```shell
╭───────────────────── Quest 3 控制器状态 ─────────────────────╮
│ ┏━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓ │
│ ┃ 项目                    ┃ 值                             ┃ │
│ ┡━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩ │
│ │ 会话状态                │ FOCUSED                        │ │
│ │ 帧计数                  │ 9458                           │ │
│ │ 帧率                    │ 59.518                         │ │
│ │ a_click                 │ 0                              │ │
│ │ a_touch                 │ 0                              │ │
│ │ b_click                 │ 0                              │ │
│ │ b_touch                 │ 0                              │ │
│ │ x_click                 │ 0                              │ │
│ │ x_touch                 │ 0                              │ │
│ │ y_click                 │ 0                              │ │
│ │ y_touch                 │ 0                              │ │
│ │ trigger_left            │ 0.000                          │ │
│ │ trigger_right           │ 0.000                          │ │
│ │ trigger_touch_left      │ 0                              │ │
│ │ trigger_touch_right     │ 0                              │ │
│ │ grip_left               │ 0.000                          │ │
│ │ grip_right              │ 0.000                          │ │
│ │ thumbstick_left         │ (0.000, 0.000)                 │ │
│ │ thumbstick_right        │ (0.000, 0.000)                 │ │
│ │ thumbstick_click_left   │ 0                              │ │
│ │ thumbstick_click_right  │ 0                              │ │
│ │ thumbstick_touch_left   │ 0                              │ │
│ │ thumbstick_touch_right  │ 0                              │ │
│ │ menu                    │ 0                              │ │
│ │ system                  │ 0                              │ │
│ │ left_pos                │ [-0.169, 1.053, -0.320]        │ │
│ │ left_rot                │ [0.322, -0.109, -0.677, 0.653] │ │
│ │ right_pos               │ [-0.019, 1.265, -0.552]        │ │
│ │ right_rot               │ [0.520, 0.167, 0.378, 0.748]   │ │
│ │ hmd_pos                 │ [-0.027, 1.228, -0.074]        │ │
│ │ hmd_rot                 │ [-0.418, 0.115, 0.045, 0.900]  │ │
│ └─────────────────────────┴────────────────────────────────┘ │
╰──────────────────────────────────────────────────────────────╯
                 
```

# 快速开始

配置 ALVR 和 SteamVR , 让 SteamVR 能串流到头显上

安装

```shell
pip install git+https://github.com/DBinK/xrinput.git[all]
```

## 基本使用
读取 XR 设备上的数据 [base.py](examples/base.py) :

```python
# base.py
# pip install rich

import time

from rich import print  # (可选项) 推荐使用 rich 打印更美观

from xrinput import XRRuntime

if __name__ == "__main__":

    print("初始化 OpenXR")

    xr_device = XRRuntime()

    while True:
        
        xr_data = xr_device.read_input()
        print(xr_data)

        time.sleep(0.01)
        
```

不出意外, 终端会打印出 VR 设备上的所有数据, 类似:

```shell
{
    'a_click': 0,
    'a_touch': 0,
    'b_click': 0,
    'b_touch': 0,
    'x_click': 0,
    'x_touch': 0,
    'y_click': 0,
    'y_touch': 0,
    'trigger_left': 0.0,
    'trigger_right': 0.0,
    'trigger_touch_left': 0,
    'trigger_touch_right': 0,
    'grip_left': 0.0,
    'grip_right': 0.0,
    'thumbstick_left': (0.0, 0.0),
    'thumbstick_right': (0.0, 0.0),
    'thumbstick_click_left': 0,
    'thumbstick_click_right': 0,
    'thumbstick_touch_left': 0,
    'thumbstick_touch_right': 0,
    'menu': 0,
    'system': 0,
    'left_pos': [
        -0.1724829375743866,
        1.0524146556854248,
        -0.31398871541023254
    ],
    'left_rot': [
        0.3271861970424652,
        -0.14018674194812775,
        -0.643242597579956,
        0.6778907179832458
    ],
    'right_pos': [
        0.08515229821205139,
        1.125990390777588,
        -0.44476109743118286
    ],
    'right_rot': [
        0.5003969073295593,
        0.0631144717335701,
        0.5167505741119385,
        0.6918007731437683
    ],
    'hmd_pos': [
        -0.05926784873008728,
        1.201049566268921,
        -0.014041170477867126
    ],
    'hmd_rot': [
        -0.2635272443294525,
        0.01641845889389515,
        -0.07385121285915375,
        0.9616807103157043
    ]
}
```
