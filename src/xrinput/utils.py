import numpy as np
from scipy.spatial.transform import Rotation as rot

def convert_pos_to_robot(xr_pos: list[float]):
    """
    将 OpenXR / Quest 坐标转换到 Robot 坐标系
    xr_pos: [x, y, z]
    返回: [x_r, y_r, z_r]
    """
    xq, yq, zq = xr_pos
    # Quest: +x右 +y上 +z后 → Robot: +x前 +y左 +z上
    return [-zq, -xq, yq]


def convert_rot_to_robot(xr_quat: list[float]):
    """
    将 OpenXR / Quest 四元数转换到 Robot 四元数
    xr_quat: [x, y, z, w]
    返回: [xr, yr, zr, wr]
    """
    # Quest→Robot 坐标轴旋转矩阵（按 x/y/z 列）
    R_mat = np.array([
        [ 0, -1,  0],   # Robot x
        [ 0,  0,  1],   # Robot y
        [-1,  0,  0]    # Robot z
    ])

    R_q = rot.from_matrix(R_mat).as_quat()
    robot_rot = rot.from_quat(R_q) * rot.from_quat(xr_quat)
    return robot_rot.as_quat().tolist()

def convert_pose(xr_pose: list[float]) -> list[float]:
    """
    将 OpenXR / Quest 姿态转换到 Robot 姿态
    xr_pose: [x, y, z, qx, qy, qz, qw]
    返回: [x_r, y_r, z_r, qx_r, qy_r, qz_r, qw_r]
    """
    robot_pos = convert_pos_to_robot(xr_pose[:3])
    robot_rot = convert_rot_to_robot(xr_pose[3:])
    return robot_pos + robot_rot

def round_list(_list: list[float], precision: int = 3) -> list[float]:
    """ 列表元素四舍五入 """
    return [round(x, precision) for x in _list]


if __name__ == "__main__":
    vr_xyz = [0.1, 0.2, 0.3]
    robot_xyz = convert_pos_to_robot(vr_xyz)
    print(robot_xyz)

    # 用 ZYX 欧拉角（yaw, pitch, roll）生成四元数
    yaw, pitch, roll = 0.0, 0.2, 0.1  # 单位：弧度

    # 生成四元数 (xyzw)
    q_quest = rot.from_euler('ZYX', [yaw, pitch, roll]).as_quat()

    q_r = convert_rot_to_robot(q_quest)
    print(q_r)