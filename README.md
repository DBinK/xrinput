# xrinput

一个简单的捕获 VR 输入的 Python 库, 使用简单的 API 获取 VR 设备上的所有数据

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
读取 XR 设备上的数据:

```python
# minimal.py
import time

from rich import print  # (可选项) 推荐使用 rich 打印更美观, pip install rich

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

## 可视化
提供一个基于 pyvista 的 3D 可视化类, 在 `xrinput.visualizer` 模块中

```shell
pip install git+https://github.com/DBinK/xrinput.git[viz]  # 加上 viz 选项
```
使用
```python
import math
import time

from scipy.spatial.transform import Rotation as R
from xrinput import Visualizer

# 创建可视化器实例
viz = Visualizer()

# 动画循环
try:
    while True:
        # 计算当前时间（相对于开始时间）
        t = time.time()
        
        # 创建动态姿态数据
        poses = []
        
        # 第一个对象： 绕Z轴运动
        x1 = 0.5 * math.sin(t)
        y1 = 1 * math.cos(t)
        z1 = 1

        rot1 = R.from_euler('z', 1)
        qx1, qy1, qz1, qw1 = rot1.as_quat()
        poses.append([x1, y1, z1, qx1, qy1, qz1, qw1])
        
        # 第二个对象： 绕自身Y轴旋转
        x2 = 1
        y2 = 1 
        z2 = 1
        # 围绕Y轴旋转
        rot2 = R.from_euler('y', t * 0.5)
        qx2, qy2, qz2, qw2 = rot2.as_quat()
        poses.append([x2, y2, z2, qx2, qy2, qz2, qw2])

        # 更新可视化器显示
        viz.update(poses)
        
        # 控制帧率
        time.sleep(0.02)
        
except KeyboardInterrupt:
    print("\n退出动画")
```

## CLI 显示面板
提供一个 CLI 显示面板, 在 `xrinput.ControllPanel` 中

```shell
pip install git+https://github.com/DBinK/xrinput.git[panel]  # 加上 panel 选项
```

```python
# panel_use.py

import random
import time 
from xrinput import ControlPanel

panel = ControlPanel(title="中控面板", float_precision=4)
panel.start()

data_dict = {
    "index": 0,
    "xr_name": "quest3",
    "xr_grip": 0.0,
    "xr_pos": [0.0, 0.0, 0.0]
}

index = 0

while True:

    index += 1
    
    data_dict = {
    "index": index,
    "xr_name": "quest3",
    "xr_grip": random.uniform(0, 1),
    "xr_pos": [random.uniform(-1, 1), random.uniform(-1, 1), random.uniform(-1, 1)]
    }   

    panel.update(data_dict)

    time.sleep(0.1)
```
    

可以不换行一直打印这个面板:
```shell
╭────────────────────────── 中控面板 ──────────────────────────╮
│ ┏━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓ │
│ ┃ 项目         ┃ 值                                        ┃ │
│ ┡━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩ │
│ │ index        │ 56                                        │ │
│ │ xr_name      │ quest3                                    │ │
│ │ xr_grip      │ 0.4087                                    │ │
│ │ xr_pos       │ [0.2979, -0.5602, -0.4286]                │ │
│ └──────────────┴───────────────────────────────────────────┘ │
╰──────────────────────────────────────────────────────────────╯
```

## 更多
更多请参考 [examples/all_api.py](examples/all_api.py) 中的代码