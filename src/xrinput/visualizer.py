import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from scipy.spatial.transform import Rotation as R

class Visualizer:
    def __init__(self, range_meters=1.0):
        """
        初始化控制器可视化器
        
        参数:
        range_meters: float, 可视化范围(以米为单位)，默认为1.0米
                     控制器将在[-range_meters, range_meters]的立方体空间内显示
        """
        # 保存范围参数
        self.range_meters = range_meters
        
        # 创建图形和3D轴
        self.fig = plt.figure(figsize=(10, 8))
        self.ax = self.fig.add_subplot(111, projection='3d')
        self.ax.set_title('VR Controllers 3D Visualization')
        self.ax.set_xlabel('X (meters)')
        self.ax.set_ylabel('Y (meters)')
        self.ax.set_zlabel('Z (meters)')
        
        # 设置固定的坐标轴范围
        self.ax.set_xlim(-self.range_meters, self.range_meters)
        self.ax.set_ylim(0, 2 * self.range_meters)  # Y轴从0开始到2倍范围
        self.ax.set_zlim(-self.range_meters, self.range_meters)
        
        # 初始化图形元素
        self.left_controller_scatter = None
        self.right_controller_scatter = None
        self.left_axes_lines = [[], [], []]  # X, Y, Z轴线条
        self.right_axes_lines = [[], [], []]  # X, Y, Z轴线条
        
        # 显示图形
        plt.ion()  # 开启交互模式
        plt.show()


    def update(self, left_controller:list, right_controller:list):
        """
        更新可视化界面
        
        参数:
        left_controller: [x,y,z] + [x, y, z, w] 7轴数据
        right_controller: [x,y,z] + [x, y, z, w] 7轴数据
        """
        # 清除旧的轴向线条
        for i in range(3):
            # 删除左控制器的轴线
            for line in self.left_axes_lines[i][:]:  # 使用[:]创建副本以避免迭代时修改列表
                if line in self.ax.lines:
                    line.remove()
            self.left_axes_lines[i].clear()
            
            # 删除右控制器的轴线
            for line in self.right_axes_lines[i][:]:  # 使用[:]创建副本以避免迭代时修改列表
                if line in self.ax.lines:
                    line.remove()
            self.right_axes_lines[i].clear()
        
        # 解析左控制器数据
        left_pos_data = left_controller[:3]  # 前三个元素是位置
        left_ori_data = left_controller[3:]  # 后四个元素是四元数方向
        
        # 更新左控制器
        # 绘制左控制器位置点
        if self.left_controller_scatter:
            self.left_controller_scatter.remove()
        self.left_controller_scatter = self.ax.scatter(
            left_pos_data[0], left_pos_data[1], left_pos_data[2], 
            c='blue', s=100, label='Left Controller'
        )
        
        # 绘制左控制器坐标轴
        self._draw_coordinate_system(
            (left_pos_data[0], left_pos_data[1], left_pos_data[2]),
            (left_ori_data[0], left_ori_data[1], left_ori_data[2], left_ori_data[3]),
            self.left_axes_lines,
            length=0.1
        )
        
        # 解析右控制器数据
        right_pos_data = right_controller[:3]  # 前三个元素是位置
        right_ori_data = right_controller[3:]  # 后四个元素是四元数方向
        
        # 更新右控制器
        # 绘制右控制器位置点
        if self.right_controller_scatter:
            self.right_controller_scatter.remove()
        self.right_controller_scatter = self.ax.scatter(
            right_pos_data[0], right_pos_data[1], right_pos_data[2], 
            c='red', s=100, label='Right Controller'
        )
        
        # 绘制右控制器坐标轴
        self._draw_coordinate_system(
            (right_pos_data[0], right_pos_data[1], right_pos_data[2]),
            (right_ori_data[0], right_ori_data[1], right_ori_data[2], right_ori_data[3]),
            self.right_axes_lines,
            length=0.1
        )
        
        # 添加图例
        # 只在第一次添加图例，避免重复
        if not self.ax.get_legend():
            self.ax.legend()
        
        # 更新图形
        self.fig.canvas.draw()
        self.fig.canvas.flush_events()


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

# 示例用法
if __name__ == "__main__":
    # 创建可视化器实例，设置范围为1米
    visualizer = Visualizer(range_meters=1.0)
    
    # 示例数据 - 直接使用7元素数组格式：[x, y, z, qx, qy, qz, qw]
    # 分别代表位置(x, y, z)和四元数方向(x, y, z, w)
    left_controller_data = [0.151, 0.909, -0.752, 0.435, -0.074, -0.450, 0.777]
    right_controller_data = [0.309, 0.905, -0.823, 0.493, 0.330, 0.317, 0.740]
    
    # 更新可视化
    visualizer.update(left_controller_data, right_controller_data)
    
    # 保持窗口开启
    plt.ioff()
    plt.show()