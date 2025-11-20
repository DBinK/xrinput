import pyvista as pv
import numpy as np
from scipy.spatial.transform import Rotation as R


class Visualizer:
    def __init__(self, range_meters=1.0):
        self.range_meters = range_meters

        self.plotter = pv.Plotter(window_size=[900, 700])
        self.plotter.show(interactive_update=True)

        box = pv.Cube(center=(0, 1, 0),
                      x_length=2 * range_meters,
                      y_length=2 * range_meters,
                      z_length=2 * range_meters)
        self.plotter.add_mesh(box, style="wireframe", color="gray")

        _ = self.plotter.add_axes(line_width=2) # type: ignore

        self.objects = []
        self.colors = ["blue", "red", "green"]

        self.plotter.camera.position = (2, 2, 2)
        self.plotter.camera.focal_point = (0, 1, 0)
        self.plotter.camera.up = (0, 1, 0)

    def _create_object(self):
        sphere = pv.Sphere(radius=0.03)
        actor_point = self.plotter.add_mesh(sphere, color=(1, 1, 1))

        line_x = self.plotter.add_lines(np.zeros((2, 3)), color="red", width=4)
        line_y = self.plotter.add_lines(np.zeros((2, 3)), color="green", width=4)
        line_z = self.plotter.add_lines(np.zeros((2, 3)), color="blue", width=4)

        return dict(point=actor_point, axes=[line_x, line_y, line_z])

    def _update_object(self, obj, pose, color="white"):
        x, y, z, qx, qy, qz, qw = pose

        obj["point"].SetPosition(x, y, z)

        # 🔥 正确的颜色设置方式（关键！）
        r, g, b = pv.Color(color).float_rgb
        obj["point"].GetProperty().SetColor(r, g, b)

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
