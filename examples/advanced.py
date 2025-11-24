import time

from looptick import LoopTick  # (可选项) 帧率计算 pip install looptick

from xrinput import XRRuntime, CommandLinePanel, Visualizer, PoseTransform

if __name__ == "__main__":

    print("初始化 OpenXR")

    xr_device = XRRuntime()  # 初始化 xr 设备

    panel = CommandLinePanel(title="XR 控制器状态")  # 创建 CLI 显示面板

    visualizer = Visualizer()  # 创建可视化器实例
    xr2bot = PoseTransform()

    loop= LoopTick()   # 创建帧率计算实例

    try:
        for i in range(100000):
            time.sleep(0.001)
            loop.tick()
            hz = loop.get_avg_hz()

            xr_data = xr_device.read_input()
            panel_data = {
                "会话状态": xr_device.session_state.name,
                "帧计数": i,
                "帧率": hz,
            }
            panel_data.update(xr_data)
            panel.update(panel_data)

            # rprint(panel_data)  # 打印数据

            left_pos = xr_data.get("left_pos") 
            left_rot = xr_data.get("left_rot")
            right_pos = xr_data.get("right_pos") 
            right_rot = xr_data.get("right_rot")
            hmd_pos = xr_data.get("hmd_pos")
            hmd_rot = xr_data.get("hmd_rot")

            if left_pos and left_rot and right_pos and right_rot and hmd_pos and hmd_rot:
                left_pose = left_pos + left_rot
                right_pose = right_pos + right_rot
                hmd_pose = hmd_pos + hmd_rot

                left_pose_robot = xr2bot.pose(left_pose)
                right_pose_robot = xr2bot.pose(right_pose)
                hmd_pose_robot = xr2bot.pose(hmd_pose)


                visualizer.update([left_pose_robot, right_pose_robot, hmd_pose_robot])
                
    except KeyboardInterrupt:
        print("退出程序")
    finally:
        xr_device.close()