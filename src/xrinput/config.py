"""
配置模块

- 定义 OpenXR 扩展
- 定义动作配置 ACTION_CONFIG
- 定义控制器相关路径
"""

import platform
import xr


# 控制器子动作路径（左右手）
CONTROLLER_SUBACTION_PATHS = (
    "/user/hand/left",
    "/user/hand/right",
)

# pose 动作名称
POSE_ACTION_NAME = "pose"


def get_enabled_extensions() -> list[str]:
    """
    根据平台返回需要启用的 OpenXR 扩展列表
    """
    exts = [xr.MND_HEADLESS_EXTENSION_NAME]
    if platform.system() == "Windows":
        exts.append(xr.KHR_WIN32_CONVERT_PERFORMANCE_COUNTER_TIME_EXTENSION_NAME)
    else:
        exts.append(xr.KHR_CONVERT_TIMESPEC_TIME_EXTENSION_NAME)
    return exts


# 所有按键配置表
# 从原始示例代码 btn.py 拆分而来 :contentReference[oaicite:0]{index=0}
ACTION_CONFIG: dict = {
    "a_click": {
        "type": xr.ActionType.BOOLEAN_INPUT,
        "localized": "A Click",
        "paths": ["/user/hand/right/input/a/click"],
    },
    "a_touch": {
        "type": xr.ActionType.BOOLEAN_INPUT,
        "localized": "A Touch",
        "paths": ["/user/hand/right/input/a/touch"],
    },
    "b_click": {
        "type": xr.ActionType.BOOLEAN_INPUT,
        "localized": "B Click",
        "paths": ["/user/hand/right/input/b/click"],
    },
    "b_touch": {
        "type": xr.ActionType.BOOLEAN_INPUT,
        "localized": "B Touch",
        "paths": ["/user/hand/right/input/b/touch"],
    },
    # 左手按钮
    "x_click": {
        "type": xr.ActionType.BOOLEAN_INPUT,
        "localized": "X Click",
        "paths": ["/user/hand/left/input/x/click"],
    },
    "x_touch": {
        "type": xr.ActionType.BOOLEAN_INPUT,
        "localized": "X Touch",
        "paths": ["/user/hand/left/input/x/touch"],
    },
    "y_click": {
        "type": xr.ActionType.BOOLEAN_INPUT,
        "localized": "Y Click",
        "paths": ["/user/hand/left/input/y/click"],
    },
    "y_touch": {
        "type": xr.ActionType.BOOLEAN_INPUT,
        "localized": "Y Touch",
        "paths": ["/user/hand/left/input/y/touch"],
    },
    # 扳机（双手）
    "trigger": {
        "type": xr.ActionType.FLOAT_INPUT,
        "localized": "Trigger",
        "paths": [
            "/user/hand/left/input/trigger/value",
            "/user/hand/right/input/trigger/value",
        ],
        "subaction": True,
    },
    "trigger_touch": {
        "type": xr.ActionType.BOOLEAN_INPUT,
        "localized": "Trigger Touch",
        "paths": [
            "/user/hand/left/input/trigger/touch",
            "/user/hand/right/input/trigger/touch",
        ],
        "subaction": True,
    },
    # 握把
    "grip": {
        "type": xr.ActionType.FLOAT_INPUT,
        "localized": "Grip",
        "paths": [
            "/user/hand/left/input/squeeze/value",
            "/user/hand/right/input/squeeze/value",
        ],
        "subaction": True,
    },
    # 摇杆（二维）
    "thumbstick": {
        "type": xr.ActionType.VECTOR2F_INPUT,
        "localized": "Thumbstick",
        "paths": [
            "/user/hand/left/input/thumbstick",
            "/user/hand/right/input/thumbstick",
        ],
        "subaction": True,
    },
    "thumbstick_click": {
        "type": xr.ActionType.BOOLEAN_INPUT,
        "localized": "Thumbstick Click",
        "paths": [
            "/user/hand/left/input/thumbstick/click",
            "/user/hand/right/input/thumbstick/click",
        ],
        "subaction": True,
    },
    "thumbstick_touch": {
        "type": xr.ActionType.BOOLEAN_INPUT,
        "localized": "Thumbstick Touch",
        "paths": [
            "/user/hand/left/input/thumbstick/touch",
            "/user/hand/right/input/thumbstick/touch",
        ],
        "subaction": True,
    },
    # 左菜单、右系统
    "menu": {
        "type": xr.ActionType.BOOLEAN_INPUT,
        "localized": "Menu",
        "paths": ["/user/hand/left/input/menu/click"],
    },
    "system": {
        "type": xr.ActionType.BOOLEAN_INPUT,
        "localized": "System",
        "paths": ["/user/hand/right/input/system/click"],
    },
    # 控制器姿态（双手）
    POSE_ACTION_NAME: {
        "type": xr.ActionType.POSE_INPUT,
        "localized": "Controller Pose",
        "paths": [
            "/user/hand/left/input/grip/pose",
            "/user/hand/right/input/grip/pose",
        ],
        "subaction": True,
    },
}
