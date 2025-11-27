import random
from typing import List, Tuple, Sequence, Union
from dataclasses import dataclass


@dataclass(slots=True)
class Box3D:
    """三维空间盒体（长方体）边界定义与操作, 用于机械臂运动空间限制"""

    x_min: float
    x_max: float
    y_min: float
    y_max: float
    z_min: float
    z_max: float

    def __init__(self, x_range: Sequence, y_range: Sequence, z_range: Sequence):
        """
        初始化Box3D实例，使用范围列表形式传入参数
        示例: Box3D(x_range=[0, 10], y_range=[0, 5], z_range=[-2, 2])
        """
        self.x_min, self.x_max = x_range[0], x_range[1]
        self.y_min, self.y_max = y_range[0], y_range[1]
        self.z_min, self.z_max = z_range[0], z_range[1]
        self.__post_init__()

    def __post_init__(self):
        # 保证边界合法
        assert self.x_min <= self.x_max, "x_min 必须 <= x_max"
        assert self.y_min <= self.y_max, "y_min 必须 <= y_max"
        assert self.z_min <= self.z_max, "z_min 必须 <= z_max"

    def clamp(
        self, point: Union[Tuple[float, float, float], Sequence[float]]
    ) -> List[float]:
        """将点限制在盒体范围内"""
        x, y, z = point
        x = max(self.x_min, min(x, self.x_max))
        y = max(self.y_min, min(y, self.y_max))
        z = max(self.z_min, min(z, self.z_max))
        return [x, y, z]

    def contains(
        self, point: Union[Tuple[float, float, float], Sequence[float]]
    ) -> bool:
        """判断点是否在盒体内部（含边界）"""
        x, y, z = point
        return (
            self.x_min <= x <= self.x_max
            and self.y_min <= y <= self.y_max
            and self.z_min <= z <= self.z_max
        )

    def random_point(self) -> Sequence[float]:
        """生成盒体内的随机点"""
        x = random.uniform(self.x_min, self.x_max)
        y = random.uniform(self.y_min, self.y_max)
        z = random.uniform(self.z_min, self.z_max)
        return x, y, z


if __name__ == "__main__":
    x_range = (-1, 1)
    Y_range = (-1, 1)
    z_range = (0.02, 1)

    limit_box = Box3D(x_range, Y_range, z_range)

    points = [
        [0.5, 0.5, 0.5],
        [0.5, 10.6, 0.5],
        [0.5, 0.6, 0.5],
        [0.5, 0.1, 0.5],
        [0.5, 0.5, -0.6],
        [0.5, 0.5, -0.6],
    ]

    for point in points:
        limited = limit_box.clamp(point)
        print(f"{point} -> {limited}: fixed: {point != limited}")
