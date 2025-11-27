class Box3D:
    """三维空间盒体（长方体）边界定义与操作，用于机械臂末端位置空间限制"""

    def __init__(self, x_range, y_range, z_range):
        # 使用范围定义边界
        self.x_min, self.x_max = x_range
        self.y_min, self.y_max = y_range
        self.z_min, self.z_max = z_range

        # 保证边界合法
        assert self.x_min <= self.x_max
        assert self.y_min <= self.y_max
        assert self.z_min <= self.z_max

    def clamp(self, point):
        """限制点在范围内"""
        x, y, z = point

        # 局部绑定，避免 repeatedly 属性查找
        xm, xM = self.x_min, self.x_max
        ym, yM = self.y_min, self.y_max
        zm, zM = self.z_min, self.z_max

        # 使用三元表达式避免 max/min 调用开销
        return [
            xM if x > xM else (xm if x < xm else x),
            yM if y > yM else (ym if y < ym else y),
            zM if z > zM else (zm if z < zm else z),
        ]

    def contains(self, point):
        """判断点是否在范围内（包含边界）"""
        x, y, z = point
        return (
            self.x_min <= x <= self.x_max
            and self.y_min <= y <= self.y_max
            and self.z_min <= z <= self.z_max
        )

    def random_point(self):
        """生成范围内随机点"""
        import random
        return (
            random.uniform(self.x_min, self.x_max),
            random.uniform(self.y_min, self.y_max),
            random.uniform(self.z_min, self.z_max),
        )


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
