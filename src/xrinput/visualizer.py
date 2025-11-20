import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from scipy.spatial.transform import Rotation as R

class Visualizer:
    def __init__(self, range_meters=1.0):
        """
        初始化多物体可视化器
        
        参数:
        range_meters: float, 可视化范围(以米为单位)，默认为1.0米
                     物体将在[-range_meters, range_meters]的立方体空间内显示
        """
        # 保存范围参数
        self.range_meters = range_meters
        
        # 创建图形和3D轴
        self.fig = plt.figure(figsize=(10, 8))
        self.ax = self.fig.add_subplot(111, projection='3d')
        self.ax.set_title('VR Objects 3D Visualization')
        self.ax.set_xlabel('X (meters)')
        self.ax.set_ylabel('Y (meters)')
        self.ax.set_zlabel('Z (meters)')
        
        # 设置固定的坐标轴范围
        self.ax.set_xlim(-self.range_meters, self.range_meters)
        self.ax.set_ylim(0, 2 * self.range_meters)  # Y轴从0开始到2倍范围
        self.ax.set_zlim(-self.range_meters, self.range_meters)
        
        # 存储所有物体的图形元素
        self.objects_elements = []  # [(scatter, axes_lines), ...]
        
        # 显示图形
        plt.ion()  # 开启交互模式
        plt.show()

    def _draw_coordinate_system(self, position, orientation, axes_lines, length=0.1):
        """
        绘制坐标系
        
        参数:
        position: tuple, (x, y, z) 位置坐标
        orientation: tuple, (x, y, z, w) 四元数方向
        axes_lines: list, 存储轴线的列表
        length: float, 坐标轴长度
        """
        # 使用scipy处理四元数旋转
        rotation = R.from_quat(orientation)  # scipy使用(x, y, z, w)格式
        
        # 定义坐标轴方向 (X, Y, Z)
        axes = [
            np.array([length, 0, 0]),  # X轴 - 红色
            np.array([0, length, 0]),  # Y轴 - 绿色
            np.array([0, 0, length])   # Z轴 - 蓝色
        ]
        
        # 旋转坐标轴向量
        rotated_axes = rotation.apply(axes)
        
        # 绘制每条轴线
        colors = ['red', 'green', 'blue']
        for i, (axis, color) in enumerate(zip(rotated_axes, colors)):
            line = self.ax.plot(
                [position[0], position[0] + axis[0]],
                [position[1], position[1] + axis[1]],
                [position[2], position[2] + axis[2]],
                color=color, linewidth=2
            )[0]
            axes_lines[i].append(line)

    def _draw_single_pose(self, pose_data, color='blue', label=None):
        """
        绘制单个物体的位姿
        
        参数:
        pose_data: [x, y, z, qx, qy, qz, qw] 7轴数据
        color: 绘制颜色
        label: 标签
        """
        # 解析数据
        pos_data = pose_data[:3]  # 前三个元素是位置
        ori_data = pose_data[3:]  # 后四个元素是四元数方向
        
        # 绘制位置点
        scatter = self.ax.scatter(
            pos_data[0], pos_data[1], pos_data[2], 
            c=color, s=100, label=label
        )
        
        # 绘制坐标轴
        axes_lines = [[], [], []]  # X, Y, Z轴线条
        self._draw_coordinate_system(
            (pos_data[0], pos_data[1], pos_data[2]),
            (ori_data[0], ori_data[1], ori_data[2], ori_data[3]),
            axes_lines,
            length=0.1
        )
        
        return scatter, axes_lines

    def update(self, objects_data):
        """
        更新可视化界面，支持多个物体
        
        参数:
        objects_data: 包含多个7自由度数据的列表，每个元素为[x,y,z,qx,qy,qz,qw]
        """
        # 清除所有现有的图形元素
        for scatter, axes_lines in self.objects_elements:
            # 删除散点图
            if scatter:
                scatter.remove()
                
            # 删除坐标轴线条
            for i in range(3):
                for line in axes_lines[i][:]:
                    if line in self.ax.lines:
                        line.remove()
        
        # 清空存储的元素列表
        self.objects_elements.clear()
        
        # 为每个物体创建颜色和标签
        colors = ['blue', 'red', 'green', 'orange', 'purple', 'brown', 'pink', 'gray', 'olive', 'cyan']
        labels = [f'Object {i+1}' for i in range(len(objects_data))]
        
        # 绘制所有物体
        for i, obj_data in enumerate(objects_data):
            color = colors[i % len(colors)]
            label = labels[i]
            
            scatter, axes_lines = self._draw_single_pose(obj_data, color, label)
            self.objects_elements.append((scatter, axes_lines))
        
        # 添加图例
        self.ax.legend()
        
        # 更新图形
        self.fig.canvas.draw()
        self.fig.canvas.flush_events()

# 示例用法
if __name__ == "__main__":
    # 创建可视化器实例，设置范围为1米
    visualizer = Visualizer(range_meters=1.0)
    
    # 示例数据 - 多个7元素数组格式：[x, y, z, qx, qy, qz, qw]
    # 分别代表位置(x, y, z)和四元数方向(x, y, z, w)
    objects_data = [
        [0.151, 0.909, -0.752, 0.435, -0.074, -0.450, 0.777],  # Object 1
        [0.309, 0.905, -0.823, 0.493, 0.330, 0.317, 0.740],   # Object 2
        [0.0, 1.0, -0.5, 0.0, 0.0, 0.0, 1.0]                  # Object 3 (默认朝向)
    ]
    
    # 更新可视化
    visualizer.update(objects_data)
    
    # 保持窗口开启
    plt.ioff()
    plt.show()