import rclpy
from geometry_msgs.msg import PoseStamped,Pose
from nav2_simple_commander.robot_navigator import BasicNavigator,TaskResult
from rclpy.node import Node
from tf2_ros import TransformListener,Buffer #坐标监听器
from tf_transformations import euler_from_quaternion,quaternion_from_euler
import math #角度转弧度函数

class PartolNode(BasicNavigator):
    def __init__(self, node_name='partol_node'):
        super().__init__(node_name)
        #声明参数
        self.declare_parameter('initial_point',[0.0, 0.0, 0.0])
        self.declare_parameter('target_point',[0.0, 0.0, 0.0, -1.0, 1.0, -1.57])
        self.initial_point = self.get_parameter('initial_point').value
        self.target_point = self.get_parameter('target_point').value
        self.buffer = Buffer()
        self.listener = TransformListener(self.buffer, self)

    def get_pose_by_xyyaw(self, x, y, yaw):
        """返回PoseStamp对象"""
        pose = PoseStamped()
        pose.header.frame_id = 'map'
        pose.pose.position.x = x
        pose.pose.position.y = y
        q = quaternion_from_euler(0, 0, yaw)
        pose.pose.orientation.x = q[0] 
        pose.pose.orientation.y = q[1]
        pose.pose.orientation.z = q[2]
        pose.pose.orientation.w = q[3]
        return pose

    def init_robot_pose(self):
        """初始化机器人位姿"""
        self.initial_point = self.get_parameter('initial_point').value
        init_pose = self.get_pose_by_xyyaw(self.initial_point[0],self.initial_point[1],self.initial_point[2])
        self.setInitialPose(init_pose)
        self.waitUntilNav2Active()

    def get_target_point(self):
        """通过参数获取目标点集合"""
        self.target_point = self.get_parameter('target_point').value
        points = [
            (self.target_point[i], self.target_point[i+1], self.target_point[i+2]) 
            for i in range(0, len(self.target_point), 3)]
        self.get_logger().info(f'获取目标点{points}')
        return points

    def nav_to_pose(self,target_point):
        """导航到目标点"""
        self.goToPose(target_point)
        while not self.isTaskComplete():
            feedback = self.getFeedback()
            self.get_logger().info(f'距离目标点:{feedback.distance_remaining}')
        result = self.getResult()
        self.get_logger().info(f'导航结果:{result}')

    def get_current_pose(self):
        """获取机器人当前位置"""
        while rclpy.ok():
            try:
                result = self.buffer.lookup_transform('map', 'base_footprint',
                                                    rclpy.time.Time(seconds=0.0),rclpy.time.Duration(second=1.0))
                transform = result.transform
                return transform
            except Exception as e:
                self.get_logger().warn(f'获取坐标变化呢失败：原因{str(e)}')

def main():
    rclpy.init()
    partol = PartolNode()
    # rclpy.spin(partol)
    partol.init_robot_pose()
    
    while rclpy.ok():
        points = partol.get_target_point()
        for point in points:
            x,y,yaw = point[0], point[1], point[2]
            target_pose = partol.get_pose_by_xyyaw(x, y, yaw)
            partol.nav_to_pose(target_pose)