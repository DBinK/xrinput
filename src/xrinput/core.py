"""
核心模块

负责:
- OpenXR 实例 / 会话初始化
- 时间转换函数（无头模式需要）
- 动作集 / 动作 / 绑定 / 空间 的创建
"""

from __future__ import annotations

import ctypes
import platform
import time
from dataclasses import dataclass
from typing import Dict, Tuple

import xr

from xrinput.log import logger
from .config import (
    ACTION_CONFIG,
    CONTROLLER_SUBACTION_PATHS,
    get_enabled_extensions,
)


class TimeConverter:
    """
    OpenXR 时间转换器封装

    - Windows: 使用 xrConvertWin32PerformanceCounterToTimeKHR
    - Linux: 使用 xrConvertTimespecTimeToTimeKHR
    """

    def __init__(self, instance: xr.Instance):
        self.instance = instance

        if platform.system() == "Windows":
            import ctypes.wintypes

            self._pc_time = ctypes.wintypes.LARGE_INTEGER()
            self._kernel32 = ctypes.WinDLL("kernel32")
            self._func = ctypes.cast(
                xr.get_instance_proc_addr(
                    instance=self.instance,
                    name="xrConvertWin32PerformanceCounterToTimeKHR",
                ),
                xr.PFN_xrConvertWin32PerformanceCounterToTimeKHR,
            )
            self._mode = "win32"
        else:
            # Linux / 其他平台使用 timespec
            self._timespec_time = xr.timespec()
            self._func = ctypes.cast( # type: ignore
                xr.get_instance_proc_addr(
                    instance=self.instance,
                    name="xrConvertTimespecTimeToTimeKHR",
                ),
                xr.PFN_xrConvertTimespecTimeToTimeKHR,
            )
            self._mode = "timespec"

    def get_xr_time(self) -> xr.Time:
        """
        返回当前的 XrTime
        """

        xr_time = xr.Time()

        if self._mode == "win32":
            self._kernel32.QueryPerformanceCounter(ctypes.byref(self._pc_time))
            result = self._func(
                self.instance,
                ctypes.pointer(self._pc_time),
                ctypes.byref(xr_time),
            )
        else:
            current_time_s = time.time()
            self._timespec_time.tv_sec = int(current_time_s)
            self._timespec_time.tv_nsec = int(
                (current_time_s - self._timespec_time.tv_sec) * 1_000_000_000
            )
            result = self._func(
                self.instance,
                ctypes.pointer(self._timespec_time),
                ctypes.byref(xr_time),
            )

        result = xr.check_result(result)
        if result.is_exception():
            raise result
        return xr_time


@dataclass
class XRContext:
    """
    OpenXR 运行上下文

    将常用对象集中封装，方便在 reader / runtime 中传递
    """

    instance: xr.Instance
    system: xr.SystemId
    session: xr.Session
    action_set: xr.ActionSet
    button_actions: Dict[str, xr.Action]
    action_types: Dict[str, xr.ActionType]
    pose_spaces: Dict[str, xr.Space]
    view_space: xr.Space
    reference_space: xr.Space
    time_converter: TimeConverter


def create_instance() -> xr.Instance:
    """
    创建 OpenXR 实例
    """
    extensions = get_enabled_extensions()
    print(f"正在初始化 OpenXR 实例, 启用扩展: {extensions}")
    instance = xr.create_instance(
        xr.InstanceCreateInfo(
            enabled_extension_names=extensions,
        )
    )
    return instance


def get_system(instance: xr.Instance) -> xr.SystemId:
    """
    获取系统 ID
    """
    try:
        system = xr.get_system(
            instance,
            xr.SystemGetInfo(form_factor=xr.FormFactor.HEAD_MOUNTED_DISPLAY),
        )
        return system
    except Exception as e:
        logger.exception(f"获取系统 ID 失败, 请检查VR设备是否连接PC: {e}")
        exit(1)


def create_session(instance: xr.Instance, system: xr.SystemId) -> xr.Session:
    """
    创建无图形绑定的 Session（适用于 headless）
    """
    session = xr.create_session(
        instance,
        xr.SessionCreateInfo(
            system_id=system,
            next=None,
        ),
    )
    return session


def create_action_set(instance: xr.Instance) -> xr.ActionSet:
    """
    创建动作集
    """
    action_set = xr.create_action_set(
        instance=instance,
        create_info=xr.ActionSetCreateInfo(
            action_set_name="quest3_input",
            localized_action_set_name="Quest 3 Input",
            priority=0,
        ),
    )
    return action_set


def create_actions(
    instance: xr.Instance,
    action_set: xr.ActionSet,
) -> Tuple[Dict[str, xr.Action], Dict[str, xr.ActionType]]:
    """
    根据 ACTION_CONFIG 创建所有动作对象
    """
    button_actions: Dict[str, xr.Action] = {}
    action_types: Dict[str, xr.ActionType] = {}

    for name, cfg in ACTION_CONFIG.items():
        sub_paths = None
        count_sub = 0

        # 如果带有子动作（左右手）
        if cfg.get("subaction"):
            sub_paths = (xr.Path * 2)(
                xr.string_to_path(instance, CONTROLLER_SUBACTION_PATHS[0]),
                xr.string_to_path(instance, CONTROLLER_SUBACTION_PATHS[1]),
            )
            count_sub = 2

        action = xr.create_action(
            action_set=action_set,
            create_info=xr.ActionCreateInfo(
                action_type=cfg["type"],
                action_name=name,
                localized_action_name=cfg["localized"],
                count_subaction_paths=count_sub,
                subaction_paths=sub_paths,
            ),
        )

        button_actions[name] = action
        action_types[name] = cfg["type"]

    return button_actions, action_types


def suggest_bindings(instance: xr.Instance, button_actions: Dict[str, xr.Action]) -> None:
    """
    为 Oculus Touch 控制器注册绑定
    """
    print("正在配置 Oculus Touch 控制器输入绑定...")

    oculus_bindings = []

    for name, cfg in ACTION_CONFIG.items():
        action = button_actions[name]
        for path in cfg["paths"]:
            oculus_bindings.append(
                xr.ActionSuggestedBinding(
                    action=action,
                    binding=xr.string_to_path(instance, path),
                )
            )

    xr.suggest_interaction_profile_bindings(
        instance=instance,
        suggested_bindings=xr.InteractionProfileSuggestedBinding(
            interaction_profile=xr.string_to_path(
                instance, "/interaction_profiles/oculus/touch_controller"
            ),
            count_suggested_bindings=len(oculus_bindings),
            suggested_bindings=(xr.ActionSuggestedBinding * len(oculus_bindings))(
                *oculus_bindings
            ),
        ),
    )

    print("✓ Oculus Touch 控制器绑定成功")


def attach_action_set(session: xr.Session, action_set: xr.ActionSet) -> None:
    """
    将动作集附加到会话
    """
    xr.attach_session_action_sets(
        session=session,
        attach_info=xr.SessionActionSetsAttachInfo(
            action_sets=[action_set],
        ),
    )


def create_pose_spaces(
    session: xr.Session,
    instance: xr.Instance,
    button_actions: Dict[str, xr.Action],
) -> Dict[str, xr.Space]:
    """
    为 pose 动作创建左右手空间
    """
    pose_action = button_actions["hand_pose"]
    pose_spaces: Dict[str, xr.Space] = {}

    for side in ("left", "right"):
        space = xr.create_action_space(
            session=session,
            create_info=xr.ActionSpaceCreateInfo(
                action=pose_action,
                subaction_path=xr.string_to_path(
                    instance, f"/user/hand/{side}"
                ),
            ),
        )
        pose_spaces[side] = space

    return pose_spaces


def create_reference_space(session: xr.Session) -> xr.Space:
    """
    创建参考空间（使用 STAGE）
    """
    reference_space = xr.create_reference_space(
        session=session,
        create_info=xr.ReferenceSpaceCreateInfo(
            reference_space_type=xr.ReferenceSpaceType.STAGE,
        ),
    )
    return reference_space

def create_view_space(session: xr.Session) -> xr.Space:
    """
    创建视图空间（用于获取HMD位置）
    """
    view_space = xr.create_reference_space(
        session=session,
        create_info=xr.ReferenceSpaceCreateInfo(
            reference_space_type=xr.ReferenceSpaceType.VIEW,
            pose_in_reference_space=xr.Posef(),  # 默认姿势
        ),
    )
    return view_space

def create_time_converter(instance: xr.Instance) -> TimeConverter:
    """
    创建时间转换器
    """
    return TimeConverter(instance)


def create_context() -> XRContext:
    """
    一次性完成所有初始化，返回 XRContext

    建议在程序启动时仅调用一次
    """
    instance = create_instance()
    system = get_system(instance)
    session = create_session(instance, system)
    action_set = create_action_set(instance)
    button_actions, action_types = create_actions(instance, action_set)
    suggest_bindings(instance, button_actions)
    attach_action_set(session, action_set)
    pose_spaces = create_pose_spaces(session, instance, button_actions)
    reference_space = create_reference_space(session)
    view_space = create_view_space(session)
    time_converter = create_time_converter(instance)

    context = XRContext(
        instance=instance,
        system=system,
        session=session,
        action_set=action_set,
        button_actions=button_actions,
        action_types=action_types,
        pose_spaces=pose_spaces,
        view_space=view_space,
        reference_space=reference_space,
        time_converter=time_converter,
    )

    return context
