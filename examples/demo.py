from xrinput import XRRuntime, ControlPanel
import time

from rich import print as rprint

if __name__ == "__main__":
    xr_device = XRRuntime()
    panel = ControlPanel(title="Quest 3 控制器状态")
    panel.start()

    try:
        for i in range(600):
            data = xr_device.read_input(i)
            rprint(data)
            panel_data = {
                "会话状态": xr_device.session_state.name,
                "帧计数": i,
            }
            panel_data.update(data)
            # panel.update(panel_data)
            time.sleep(0.1)
    finally:
        xr_device.close()