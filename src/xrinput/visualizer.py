import pyvista as pv
import numpy as np
from scipy.spatial.transform import Rotation as R


class Visualizer:
    def __init__(self, range_meters=2.0):
        self.range_meters = range_meters

        self.plotter = pv.Plotter(window_size=[900, 700])
        self.plotter.show(interactive_update=True)

        box = pv.Cube(
            center=(0, 0, 0),
            x_length=range_meters,
            y_length=range_meters,
            z_length=range_meters,
        )
        self.plotter.add_mesh(box, style="wireframe", color="gray")

        ground = pv.Plane(
            center=(0, 0, 0),  # 地面在 Z = 0
            direction=(0, 0, 1),  # 法线指向 +Z，上方向
            i_size=range_meters,
            j_size=range_meters,
            i_resolution=10,
            j_resolution=10,
        )
        self.plotter.add_mesh(ground, color="#B4B4B4", show_edges=True, opacity=1.0)

        _ = self.plotter.add_axes(line_width=2)  # type: ignore

        self.objects = []
        self.colors = ["blue", "red", "green"]

        self.plotter.camera.position = (2, 2, 2)
        self.plotter.camera.focal_point = (0, 1, 0)
        self.plotter.camera.up = (0, 1, 0)

        self._draw_world_axes()

    def _draw_world_axes(self):
        L = self.range_meters * 0.5  # 全局坐标轴长度

        # X 轴: 红色
        x_axis = np.array([[0, 0, 0], [L, 0, 0]], dtype=np.float32)
        self.plotter.add_lines(x_axis, color="red", width=4)
        self.plotter.add_point_labels(
            [(L, 0, 0)], ["X"], text_color="red", font_size=20, point_size=0, shape=None
        )

        # Y 轴: 绿色
        y_axis = np.array([[0, 0, 0], [0, L, 0]], dtype=np.float32)
        self.plotter.add_lines(y_axis, color="green", width=4)
        self.plotter.add_point_labels(
            [(0, L, 0)],
            ["Y"],
            text_color="green",
            font_size=20,
            point_size=0,
            shape=None,
        )

        # Z 轴: 蓝色
        z_axis = np.array([[0, 0, 0], [0, 0, L]], dtype=np.float32)
        self.plotter.add_lines(z_axis, color="blue", width=4)
        self.plotter.add_point_labels(
            [(0, 0, L)],
            ["Z"],
            text_color="blue",
            font_size=20,
            point_size=0,
            shape=None,
        )

    def _create_object(self):
        sphere = pv.Sphere(radius=0.03)
        actor_point = self.plotter.add_mesh(sphere, color=(1, 1, 1))

        line_x = self.plotter.add_lines(np.zeros((2, 3)), color="red", width=4)
        line_y = self.plotter.add_lines(np.zeros((2, 3)), color="green", width=4)
        line_z = self.plotter.add_lines(np.zeros((2, 3)), color="blue", width=4)

        # 🌟 地板连接线（Z=0 到物体位置）
        line_floor = self.plotter.add_lines(np.zeros((2, 3)), color="orange", width=2)

        return dict(
            point=actor_point,
            axes=[line_x, line_y, line_z],
            floor_line=line_floor,
        )

    def _update_object(self, obj, pose, color="white"):
        x, y, z, qx, qy, qz, qw = pose

        # 球体
        obj["point"].SetPosition(x, y, z)
        r, g, b = pv.Color(color).float_rgb
        obj["point"].GetProperty().SetColor(r, g, b)

        # 🌟 更新地板线
        floor_pts = np.array([[x, y, 0], [x, y, z]], dtype=np.float32)
        obj["floor_line"].GetMapper().GetInput().points = floor_pts

        # 坐标轴
        rot = R.from_quat([qx, qy, qz, qw])
        axis_vecs = rot.apply(np.eye(3) * 0.15)
        p0 = np.array([x, y, z])

        for i, axis in enumerate(obj["axes"]):
            pts = np.vstack([p0, p0 + axis_vecs[i]]).astype(np.float32)
            axis.GetMapper().GetInput().points = pts

    def update(self, poses):
        while len(self.objects) < len(poses):
            self.objects.append(self._create_object())

        for i, pose in enumerate(poses):
            color = self.colors[i % len(self.colors)]
            self._update_object(self.objects[i], pose, color)

        self.plotter.update()
