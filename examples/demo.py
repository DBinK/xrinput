from xrinput import XRRuntime, ControlPanel, Visualizer
import time

from rich import print as rprint

if __name__ == "__main__":
    xr_device = XRRuntime()

    panel = ControlPanel(title="Quest 3 控制器状态")
    panel.start()

    visualizer = Visualizer()

    try:
        for i in range(600):
            vr_data = xr_device.read_input(i)
            # rprint(data)
            panel_data = {
                "会话状态": xr_device.session_state.name,
                "帧计数": i,
            }
            panel_data.update(vr_data)
            panel.update(panel_data)

            # rprint(panel_data)  # 打印数据

            left_pos = vr_data.get("left_pos") 
            left_rot = vr_data.get("left_rot")
            right_pos = vr_data.get("right_pos") 
            right_rot = vr_data.get("right_rot")
            hmd_pos = vr_data.get("hmd_pos")
            hmd_rot = vr_data.get("hmd_rot")

            if left_pos and left_rot and right_pos and right_rot and hmd_pos and hmd_rot:
                left_pose = left_pos + left_rot
                right_pose = right_pos + right_rot

                hmd_pose = hmd_pos + hmd_rot
                visualizer.update([left_pose, right_pose, hmd_pose])

            # print("左手位置:", left_pos, left_rot)
            # print("右手位置:", right_pos, right_rot)
            # print("头位置:", hmd_pos, hmd_rot)

    except KeyboardInterrupt:
        print("退出程序")
    finally:
        xr_device.close()