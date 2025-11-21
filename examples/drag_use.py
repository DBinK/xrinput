import time

from scipy.spatial.transform import Rotation as R

from xrinput import XRRuntime, PoseMapper, Visualizer
from xrinput.utils import convert_pose

if __name__ == "__main__":

    # 初始化
    xr_device = XRRuntime()  # 初始化 xr 设备
    mapper = PoseMapper()
    visualizer = Visualizer()

    # 初始化参考姿态（只需一次）
    init_pos  = [0.0, 0.0, 0.0]
    init_quat = [0.0, 0.0, 0.0, 1.0]

    mapper.init_reference(init_pos, init_quat)

    try:
        while True:

            xr_data = xr_device.read_input()

            if xr_data is None:
                time.sleep(0.005)
                continue
            
            raw_pos = xr_data.get("right_pos") 
            raw_orient = xr_data.get("right_rot")
            trigger = xr_data.get("trigger_right")
            grip = xr_data.get("grip_right")
            
            if raw_pos is None or raw_orient is None or trigger is None or grip is None: 
                continue

            raw_pose = raw_pos+raw_orient

            vr_pose   = convert_pose(raw_pose)
            vr_pos     = vr_pose[:3]
            vr_quat    = vr_pose[3:]

            # 1. 松开按钮 → 停止拖拽
            if trigger <= 0.5:
                mapper.stop_drag()

            # 2. 按下按钮且尚未开始拖拽 → 开始拖拽
            elif trigger > 0.5 and not mapper.dragging:
                mapper.start_drag(vr_pos, vr_quat)

            # 3. 按住按钮 → 持续更新姿态
            elif trigger > 0.5 and mapper.dragging:
                mapper.update(vr_pos, vr_quat)

            # 4. 获取映射后的目标姿态
            target_pos, target_ori = mapper.get_target()
            
            if target_pos is not None and target_ori is not None:
                target_pose = target_pos + target_ori
                visualizer.update( [target_pose, vr_pose] )

            time.sleep(0.001)

    except KeyboardInterrupt:
        print("退出程序")
    finally:
        xr_device.close()