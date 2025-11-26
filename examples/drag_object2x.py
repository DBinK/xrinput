import time

from looptick import LoopTick

from xrinput import XRRuntime, PoseMapper, Visualizer, LowPassFilter, PoseTransform
from xrinput.comm.zmq_pub import ZMQPublisher
from xrinput.monitor.panel import CommandLinePanel

INIT_POS  =   [0.21054126, 0.00141549, 0.22679673] 
INIT_QUAT =  [  -0.47771874, -0.4777191, -0.5213261, -0.5213333 ]

UNIT_POS = [0,0,0]
UNIT_QUAT = [0,0,0,1]

if __name__ == "__main__":

    # 初始化 xr 设备
    xr_device = XRRuntime() 
    
    # 可视化
    panel = CommandLinePanel(title="XR 控制器状态")  # 创建 CLI 显示面板
    visualizer = Visualizer()

    # 数据处理
    xr2bot = PoseTransform()  # 变换为机器人坐标系下的姿态
    left_lowpass = LowPassFilter(alpha=0.3)
    right_lowpass = LowPassFilter(alpha=0.3)
    
    # 创建手柄映射器
    left_mapper = PoseMapper()
    right_mapper = PoseMapper()

    # 创建数据发布器
    pub = ZMQPublisher()

    # 创建帧率计算实例
    loop= LoopTick()   # 创建帧率计算实例

    # 初始化左右物体的参考姿态
    left_init_pos  = INIT_POS  # 左边的物体
    left_init_quat = INIT_QUAT
    
    right_init_pos = INIT_POS    # 右边的物体
    right_init_quat = INIT_QUAT

    # left_init_pos  =  UNIT_POS  # 左边的物体
    # left_init_quat =  UNIT_QUAT
    
    # right_init_pos = UNIT_POS     # 右边的物体
    # right_init_quat = UNIT_QUAT

    left_target_pose = None
    right_target_pose = None

    # 对齐手柄和被操作物体初始位置
    left_mapper.init_reference(left_init_pos, left_init_quat)
    right_mapper.init_reference(right_init_pos, right_init_quat)

    try:
        while True:
            xr_data = xr_device.read_input()

            if xr_data is None:
                time.sleep(0.005)
                continue

            # 获取左右手的位置、方向和触发器状态
            left_raw_pos = xr_data.get("left_pos") 
            left_raw_orient = xr_data.get("left_rot")
            left_trigger = xr_data.get("trigger_left")
            
            right_raw_pos = xr_data.get("right_pos") 
            right_raw_orient = xr_data.get("right_rot")
            right_trigger = xr_data.get("trigger_right")

            # 确保数据有效
            if (
                left_raw_pos is None
                or left_raw_orient is None
                or left_trigger is None
                or right_raw_pos is None
                or right_raw_orient is None
                or right_trigger is None
            ):
                time.sleep(0.005)
                continue

            # 转换左右手姿态到机器人坐标系
            left_raw_pose = left_raw_pos + left_raw_orient
            left_vr_pose = xr2bot.pose(left_raw_pose)
            left_vr_pos = left_vr_pose[:3]
            left_vr_quat = left_vr_pose[3:]
            
            right_raw_pose = right_raw_pos + right_raw_orient
            right_vr_pose = xr2bot.pose(right_raw_pose)
            right_vr_pos = right_vr_pose[:3]
            right_vr_quat = right_vr_pose[3:]

            # 处理左手拖拽逻辑
            # 1. 松开按钮 → 停止拖拽
            if left_trigger <= 0.5:
                left_mapper.stop_drag()
            # 2. 按下按钮且尚未开始拖拽 → 开始拖拽
            elif left_trigger > 0.5 and not left_mapper.dragging:
                left_mapper.start_drag(left_vr_pos, left_vr_quat)
            # 3. 按住按钮 → 持续更新姿态
            elif left_trigger > 0.5 and left_mapper.dragging:
                left_mapper.update(left_vr_pos, left_vr_quat)

            # 处理右手拖拽逻辑
            # 1. 松开按钮 → 停止拖拽
            if right_trigger <= 0.5:
                right_mapper.stop_drag()
            # 2. 按下按钮且尚未开始拖拽 → 开始拖拽
            elif right_trigger > 0.5 and not right_mapper.dragging:
                right_mapper.start_drag(right_vr_pos, right_vr_quat)
            # 3. 按住按钮 → 持续更新姿态
            elif right_trigger > 0.5 and right_mapper.dragging:
                right_mapper.update(right_vr_pos, right_vr_quat)

            ## 复位逻辑
            # 按下A键和X键 → 重置目标姿态
            a_click = xr_data.get("a_click") 
            x_click = xr_data.get("x_click") 

            if a_click == 1 and x_click == 1: 
                # left_mapper.set_target(UNIT_POS, UNIT_QUAT)
                # right_mapper.set_target(UNIT_POS, UNIT_QUAT)
                left_mapper.set_target(left_init_pos, left_init_quat)
                right_mapper.set_target(right_init_pos, right_init_quat)
            
            ## 处理姿态数据
            # 获取映射后的目标姿态
            left_target_pos, left_target_ori = left_mapper.get_target()
            right_target_pos, right_target_ori = right_mapper.get_target()
            
            # 装填所有需要可视化的姿态
            all_poses = []
            
            # 添加左手控制的物体姿态
            if left_target_pos is not None and left_target_ori is not None:
                left_target_pose = left_target_pos + left_target_ori
                # left_target_pose = left_target_pos + left_target_ori
                # left_target_pose = left_target_pos + left_target_ori
                left_target_pose = left_lowpass.update(left_target_pose)
                all_poses.append(left_target_pose)
                
            # 添加右手控制的物体姿态
            if right_target_pos is not None and right_target_ori is not None:
                right_target_pose = right_target_pos + right_target_ori
                # right_target_pose = right_target_pos + right_target_ori
                # right_target_pose = right_target_pos + right_target_ori
                right_target_pose = right_lowpass.update(right_target_pose)
                all_poses.append(right_target_pose)
                
            # 添加左右手控制器的姿态用于可视化参考
            all_poses.append(left_vr_pose)
            all_poses.append(right_vr_pose)

            # 计算帧率
            loop.tick()
            
            if all_poses:
                # 更新可视化显示
                panel_dict = {
                    "会话状态": xr_device.session_state.name,
                    "帧率": loop.get_avg_hz(),
                    "left_target_pose": left_target_pose,
                    "right_target_pose": right_target_pose,
                }
                panel_dict.update(xr_data)           # 添加输入数据
                panel.update(panel_dict)       # 更新CLI面板数据
                visualizer.update(all_poses)  # 更新可视化显示

                # 发送数据
                pub.send(panel_dict)

            time.sleep(0.001)  # 休眠1ms, 避免CPU占用过高

    except KeyboardInterrupt:
        print("退出程序")
    finally:
        xr_device.close()