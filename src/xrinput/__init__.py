"""
xrinput 包入口

提供:
- XRRuntime: 统一封装 OpenXR 初始化与读取流程
- ControlPanel: 终端中控面板
"""
# 核心模块
from .core.xr_runtime import XRRuntime

# 监控模块
from .monitor.log import logger
from .monitor.panel import CommandLinePanel
from .monitor.visualizer import Visualizer

# 数据处理模块
from .processing.filters import LowPassFilter
from .processing.pose_mapper import PoseMapper
from .processing.pose_transform import PoseTransform

# 通信模块
from .comm.zmq_pub import ZMQPublisher
from .comm.zmq_sub import ZMQSubscriber

__all__ = [
    "XRRuntime",

    "logger",
    "CommandLinePanel",
    "Visualizer",

    "PoseMapper",
    "PoseTransform",
    "LowPassFilter",

    "ZMQPublisher",
    "ZMQSubscriber",
]
