"""
xrinput 包入口

提供:
- XRRuntime: 统一封装 OpenXR 初始化与读取流程
- ControlPanel: 终端中控面板
"""

from .runtime import XRRuntime
from .panel import ControlPanel

__all__ = [
    "XRRuntime",
    "ControlPanel",
]
