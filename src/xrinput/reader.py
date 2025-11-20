"""
输入读取模块

负责:
- 同步动作集
- 按动作名称读取按键 / 摇杆 / 扳机状态
- 读取控制器 pose（位置 + 四元数）
"""

from __future__ import annotations

import ctypes
from typing import Any, Dict, Optional

import xr

from .config import ACTION_CONFIG, POSE_ACTION_NAME
from .core import XRContext


class XRInputReader:
    """
    封装所有输入读取逻辑

    使用方式:
    - 先调用 sync_actions() 同步状态
    - 然后用 read_all() 或 read_action_state() 获取具体值
    """

    def __init__(self, context: XRContext):
        self.ctx = context
        self.data_template = self._create_data_template()

    def _create_data_template(self) -> Dict[str, Any]:
        """
        创建数据模板字典，包含所有可能的键，初始值为None
        """
        template: Dict[str, Any] = {}
        
        for name, cfg in ACTION_CONFIG.items():
            # 特殊处理 pose
            if cfg["type"] == xr.ActionType.POSE_INPUT and name == POSE_ACTION_NAME:
                for side in ("left", "right"):
                    template[f"{name}_{side}_pos"] = None
                    template[f"{name}_{side}_rot"] = None
                continue

            # 其他类型输入
            if cfg.get("subaction"):
                # 双手各自的数据
                template[f"{name}_left"] = None
                template[f"{name}_right"] = None
            else:
                template[name] = None
                
        return template

    # 同步当前动作状态（必须每帧调用一次）
    def sync_actions(self) -> None:
        """
        同步所有动作状态
        """
        active_action_set = xr.ActiveActionSet(
            action_set=self.ctx.action_set,
            subaction_path=xr.NULL_PATH,  # type: ignore
        )
        xr.sync_actions(
            session=self.ctx.session,
            sync_info=xr.ActionsSyncInfo(
                count_active_action_sets=1,
                active_action_sets=ctypes.pointer(active_action_set),
            ),
        )

    # 读取某个动作的状态
    def read_action_state(
        self,
        name: str,
        subaction_path: Optional[str] = None,
    ) -> Any:
        """
        读取单个动作状态

        参数:
        - name: 动作名称（即 ACTION_CONFIG 的 key）
        - subaction_path: 可选，子路径，如 "/user/hand/left"

        返回:
        - 布尔 / float / (x, y) 元组
        """
        action = self.ctx.button_actions[name]
        t = self.ctx.action_types[name]

        if subaction_path:
            get_info = xr.ActionStateGetInfo(
                action=action,
                subaction_path=xr.string_to_path(self.ctx.instance, subaction_path),
            )
        else:
            get_info = xr.ActionStateGetInfo(action=action)

        try:
            if t == xr.ActionType.BOOLEAN_INPUT:
                return xr.get_action_state_boolean(
                    self.ctx.session, get_info
                ).current_state

            if t == xr.ActionType.FLOAT_INPUT:
                return xr.get_action_state_float(
                    self.ctx.session, get_info
                ).current_state

            if t == xr.ActionType.VECTOR2F_INPUT:
                v = xr.get_action_state_vector2f(
                    self.ctx.session, get_info
                ).current_state
                return (v.x, v.y)

        except xr.XrException:
            # 出错时返回 None，避免中断整个循环
            return None

        return None

    # 读取 pose（左右手）
    def read_pose(self, side: str) -> Dict[str, Any]:
        """
        读取控制器姿态

        参数:
        - side: "left" 或 "right"

        返回:
        - 字典:
          {
            "pos": (x, y, z) 或 None,
            "rot": (x, y, z, w) 或 None,
          }
        """
        space = self.ctx.pose_spaces.get(side)
        if space is None:
            return {"pos": None, "rot": None}

        try:
            state = xr.locate_space(
                space=space,
                base_space=self.ctx.reference_space,
                time=self.ctx.time_converter.get_xr_time(),
            )
            pos = state.pose.position
            rot = state.pose.orientation

            return {
                "pos": (pos.x, pos.y, pos.z),
                "rot": (rot.x, rot.y, rot.z, rot.w),
            }
            # return {
            #     "pos": (
            #         round(pos.x, 3),
            #         round(pos.y, 3),
            #         round(pos.z, 3),
            #     ),
            #     "rot": (
            #         round(rot.x, 3),
            #         round(rot.y, 3),
            #         round(rot.z, 3),
            #         round(rot.w, 3),
            #     ),
            # }
        except Exception:
            return {"pos": None, "rot": None}

    # 一次性读取所有动作
    def read_all(self) -> Dict[str, Any]:
        """
        自动读取 ACTION_CONFIG 中定义的所有输入

        返回:
        - dict, key 为动作名 / 动作名_左右等
        """
        # 使用预创建的模板副本，避免每次都重新创建
        data: Dict[str, Any] = self.data_template.copy()

        for name, cfg in ACTION_CONFIG.items():
            # 特殊处理 pose
            if cfg["type"] == xr.ActionType.POSE_INPUT and name == POSE_ACTION_NAME:
                for side in ("left", "right"):
                    pose = self.read_pose(side)
                    data[f"{side}_pos"] = pose["pos"]
                    data[f"{side}_rot"] = pose["rot"]
                continue

            # 其他类型输入
            if cfg.get("subaction"):
                # 双手各自的数据
                data[f"{name}_left"] = self.read_action_state(
                    name, "/user/hand/left"
                )
                data[f"{name}_right"] = self.read_action_state(
                    name, "/user/hand/right"
                )
            else:
                data[name] = self.read_action_state(name)

        return data
