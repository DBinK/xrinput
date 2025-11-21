import numpy as np
from scipy.spatial.transform import Rotation as R


class PoseTransform:
    """
    XR → Robot / Robot → XR 坐标转换器
    可动态指定坐标系旋转矩阵，实现 XR 与 Robot 的姿态对齐。

    参数:
        R_mat: 3x3 ndarray, 表示 Robot = R_mat * XR
    """

    def __init__(self, R_mat=None):
        # 默认：你的 Quest → Robot 变换矩阵
        if R_mat is None:
            R_mat = np.array([
                [ 0,  0, -1],  # Robot X = -Quest Z
                [-1,  0,  0],  # Robot Y = -Quest X
                [ 0,  1,  0]   # Robot Z =  Quest Y
            ], dtype=float)

        self.R = np.array(R_mat, dtype=float)            # XR → Robot 旋转矩阵
        self.R_rot = R.from_matrix(self.R)               # 对应 Rotation 对象
        self.R_inv = self.R.T                            # Robot → XR 的矩阵
        self.R_inv_rot = R.from_matrix(self.R_inv)       # Rotation 对象

    # ------------------------------------------------
    # XR → Robot
    # ------------------------------------------------
    def pos(self, xr_pos):
        xr_pos = np.array(xr_pos)
        return (self.R @ xr_pos).tolist()

    def rot(self, xr_quat):
        xr_R = R.from_quat(xr_quat)
        robot_R = self.R_rot * xr_R
        return robot_R.as_quat().tolist()

    def pose(self, xr_pose):
        p = self.pos(xr_pose[:3])
        q = self.rot(xr_pose[3:])
        return p + q

    # ------------------------------------------------
    # Robot → XR
    # ------------------------------------------------
    def pos_inv(self, robot_pos):
        robot_pos = np.array(robot_pos)
        return (self.R_inv @ robot_pos).tolist()

    def rot_inv(self, robot_quat):
        robot_R = R.from_quat(robot_quat)
        xr_R = self.R_inv_rot * robot_R
        return xr_R.as_quat().tolist()

    def pose_inv(self, robot_pose):
        p = robot_pose[:3]
        q = robot_pose[3:]
        return self.pos_inv(p) + self.rot_inv(q)

    # ------------------------------------------------
    # 允许动态更新矩阵
    # ------------------------------------------------
    def set_matrix(self, R_mat):
        self.__init__(R_mat)   # 重新初始化全部缓存


# 测试
if __name__ == "__main__":
    cc = PoseTransform()

    xr_pose = [0.1, 0.2, 0.3, 0, 0.1, 0, 0.99]
    print("XR→Robot:", cc.pose(xr_pose))
    print("Robot→XR:", cc.pose_inv(cc.pose(xr_pose)))
