from xrinput import XRRuntime, ControlPanel
import time

if __name__ == "__main__":
    rt = XRRuntime()
    panel = ControlPanel(title="Quest 3 控制器状态")
    panel.start()

    try:
        for i in range(600):
            data = rt.step(i)
            panel_data = {
                "会话状态": rt.session_state.name,
                "帧计数": i,
            }
            panel_data.update(data)
            panel.update(panel_data)
            time.sleep(0.1)
    finally:
        rt.close()