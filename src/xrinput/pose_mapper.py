# -*- coding: utf-8 -*-
# pose_mapper.py
# 基于 VR 拖拽方式的姿态映射器
# 用于: 初始化物体姿态 + 使用 VR 手柄拖拽物体(输出绝对位姿)

from scipy.spatial.transform import Rotation as R
import numpy as np


class PoseMapper:
    """
    VR → 物体(如机械臂末端) 的姿态映射器

    设计理念:
    - init_reference(obj_pos, obj_quat): 初始化物体初始姿态(只需调用一次)
    - start_drag(vr_pos, vr_quat): 开始拖拽(按下按钮时调用一次)
    - update(vr_pos, vr_quat): 拖拽期间持续更新
    - stop_drag(): 停止拖拽
    - get_target(): 获取当前维护的目标姿态

    整个类内部持续维护 "current_t, current_R" 作为目标姿态
    """

    def __init__(self):
        self.ref_R = None
        self.ref_t = None

        self.rel_R = None
        self.rel_t = None

        self.current_R = None
        self.current_t = None

        self.ref_inited = False
        self.dragging = False

    # ------------------ 1. 初始化物体世界姿态 ------------------
    def init_reference(self, obj_pos, obj_quat):
        self.ref_R = R.from_quat(obj_quat)
        self.ref_t = np.array(obj_pos)

        self.current_R = self.ref_R
        self.current_t = self.ref_t.copy()

        self.ref_inited = True

    # ------------------ 2. 正式开始拖拽 ------------------
    def start_drag(self, vr_pos, vr_quat):
        assert self.ref_inited and self.current_R is not None and self.current_t is not None, "必须先调用 init_reference()"

        R_vr = R.from_quat(vr_quat)

        # 计算抓取瞬间的相对姿态
        self.rel_R = R_vr.inv() * self.current_R
        self.rel_t = R_vr.inv().apply(self.current_t - vr_pos)

        self.dragging = True

    # ------------------ 3. 停止拖拽 ------------------
    def stop_drag(self):
        self.dragging = False

    # ------------------ 4. 拖拽期间持续更新 ------------------
    def update(self, vr_pos, vr_quat):
        assert self.dragging and self.rel_R is not None and self.rel_t is not None and self.current_R is not None, "必须先调用 start_drag()"

        R_vr = R.from_quat(vr_quat)

        # 计算新的绝对姿态
        self.current_R = R_vr * self.rel_R
        self.current_t = vr_pos + R_vr.apply(self.rel_t)

        return self.current_t.tolist(), self.current_R.as_quat().tolist()

    # ------------------ 5. 获取当前维护的目标姿态 ------------------
    def get_target(self):
        if self.current_t is None or self.current_R is None:
            return None, None
        return self.current_t.tolist(), self.current_R.as_quat().tolist()



if __name__ == "__main__":
    import time
    import math
    
    def generate_test_data(t):
        """生成基于时间t的测试数据"""
        # 位置数据：使用sin函数创建平滑的周期性运动
        pos = [
            0.5 + 0.1 * math.sin(t),
            0.2 + 0.1 * math.sin(2 * t),
            0.3 + 0.1 * math.cos(t)
        ]
        
        # 四元数数据：绕Y轴旋转
        angle = 0.5 * math.sin(t)
        quat = R.from_euler('y', angle).as_quat()
        
        return pos, quat
    
    # 创建姿态映射器实例
    mapper = PoseMapper()
    
    # 初始化物体姿态（固定位置）
    obj_pos = [0.5, 0.2, 0.3]
    obj_quat = [0, 0, 0, 1]  # 单位四元数
    
    mapper.init_reference(obj_pos, obj_quat)
    
    print("PoseMapper 循环演示")
    print("=" * 50)
    print(f"初始物体位置: {obj_pos}")
    print(f"初始物体姿态: {obj_quat}")
    print("=" * 50)
    
    # 模拟VR控制器运动的循环
    for i in range(50):
        # 生成基于时间的测试数据
        t = i * 0.2
        
        # 生成VR控制器姿态
        vr_pos, vr_quat = generate_test_data(t)
        
        # 第一帧需要调用 start_drag
        if i == 0:
            print(f"\n第 {i+1} 帧 - 开始拖拽:")
            print(f"  VR控制器位置: {vr_pos}")
            print(f"  VR控制器姿态: {vr_quat}")
            mapper.start_drag(vr_pos, vr_quat)
        else:
            # 后续帧调用 update 更新姿态
            mapper.update(vr_pos, vr_quat)
        
        # 获取并打印当前目标姿态
        target_pos, target_quat = mapper.get_target()
        print(f"第 {i+1} 帧 - 目标姿态:")
        print(f"  物体位置: {target_pos}")
        print(f"  物体姿态: {target_quat}")
        
        # 控制演示速度
        time.sleep(0.1)
    
    print("\n演示完成!")
