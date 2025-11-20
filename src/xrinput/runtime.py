"""
运行时模块

负责:
- 只在启动时调用一次的初始化逻辑
- Session 状态机处理
- 每帧数据读取调度

可直接从外部这样用:

    from xrinput import XRRuntime, ControlPanel

    rt = XRRuntime()
    panel = ControlPanel(title="Quest 3 控制器状态")
    panel.start()

    for i in range(600):
        data = rt.read_input(frame_index=i)
        panel.update(data)
        time.sleep(0.1)

"""

from __future__ import annotations

import ctypes
import time
from typing import Any, Dict

import xr

from .core import create_context, XRContext
from .reader import XRInputReader
from .panel import ControlPanel


class XRRuntime:
    """
    XR 运行时封装

    - 初始化时只运行一次 create_context()
    - 内部维护 session_state
    - 对外提供 read_input() 每帧调用
    """

    def __init__(self):
        # 一次性初始化所有 OpenXR 相关对象
        self.ctx: XRContext = create_context()
        self.reader = XRInputReader(self.ctx)

        # 会话状态
        self.session_state = xr.SessionState.UNKNOWN

        print("\n🎮 Quest 3 无头模式按键读取准备就绪")
        print("按键映射:")
        print("  左手: X/Y 按键, 左摇杆, 左扳机, 左握把, 菜单键")
        print("  右手: A/B 按键, 右摇杆, 右扳机, 右握把, 系统键")
        print("  同时监控所有按键的触摸事件")
        print("  调用 XRRuntime.read_input() 以按帧读取\n")

    # 处理所有待处理事件
    def _poll_events(self) -> None:
        """
        处理 OpenXR 事件, 更新 session_state
        """
        while True:
            try:
                event_buffer = xr.poll_event(self.ctx.instance)
                event_type = xr.StructureType(event_buffer.type)

                if event_type == xr.StructureType.EVENT_DATA_SESSION_STATE_CHANGED:
                    event = ctypes.cast(
                        ctypes.byref(event_buffer),
                        ctypes.POINTER(xr.EventDataSessionStateChanged),
                    ).contents
                    self.session_state = xr.SessionState(event.state)
                    print(f"📱 OpenXR 会话状态: {self.session_state.name}")

                    if self.session_state == xr.SessionState.READY:
                        xr.begin_session(
                            self.ctx.session,
                            xr.SessionBeginInfo(
                                primary_view_configuration_type=xr.ViewConfigurationType.PRIMARY_MONO,  # 单视图即可
                            ),
                        )
                    elif self.session_state == xr.SessionState.STOPPING:
                        xr.end_session(self.ctx.session)

                # 如果没有更多事件会抛 EventUnavailable
                break

            except xr.EventUnavailable:
                break

    # 单帧逻辑
    def read_input(self, frame_index: int) -> Dict[str, Any]:
        """
        执行一帧的逻辑:
        - 处理事件 / Session 状态
        - 若处于 FOCUSED, 则同步并读取所有输入

        返回:
        - dict, 可直接用于 ControlPanel.update()
        """
        self._poll_events()

        result_data: Dict[str, Any] = self.reader.data_template  # 从数据模板创建

        if self.session_state == xr.SessionState.FOCUSED:
            # 同步动作
            self.reader.sync_actions()

            # 读取所有输入
            try:
                all_inputs = self.reader.read_all()
                result_data.update(all_inputs)
            except Exception as e:
                result_data["错误"] = f"读取输入异常: {e}"

        elif self.session_state == xr.SessionState.IDLE:
            # 可根据需要添加提示逻辑
            if frame_index % 60 == 0:
                print("⏳ 等待头显激活...")

        return result_data

    # 资源清理
    def close(self) -> None:
        """
        销毁 Session 和 Instance

        建议在程序退出时调用
        """
        print("🧹 正在清理 XR 资源...")
        try:
            if self.ctx.session:
                xr.destroy_session(self.ctx.session)
        except Exception:
            pass

        try:
            if self.ctx.instance:
                xr.destroy_instance(self.ctx.instance)
        except Exception:
            pass

        print("✅ 清理完成")


if __name__ == "__main__":
    # 提供一个等价于原 btn.py 的简单示例循环 :contentReference[oaicite:2]{index=2}
    import traceback

    rt = None
    panel = None

    try:
        rt = XRRuntime()
        panel = ControlPanel(title="Quest 3 控制器状态")
        panel.start()

        # 运行 600 帧，大约 1 分钟（0.1s/帧）
        for frame_index in range(600):
            data = rt.read_input(frame_index)
            panel.update(data)
            time.sleep(0.1)

    except KeyboardInterrupt:
        print("\n👋 用户中断，正在退出...")
    except Exception as e:
        print(f"❌ 运行时发生错误: {e}")
        traceback.print_exc()
    finally:
        if rt is not None:
            rt.close()
