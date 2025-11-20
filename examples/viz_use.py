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