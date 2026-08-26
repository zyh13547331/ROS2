from geometry_msgs.msg import PoseStamped
from nav2_simple_commander.robot_navigator import BasicNavigator
import rclpy
from tf_transformations import quaternion_from_euler
import math

def main():
    rclpy.init()
    nav = BasicNavigator()  #节点
    init_pose = PoseStamped()
    init_pose.header.frame_id = "map"
    init_pose.header.stamp = nav.get_clock().now().to_msg()
    # 1. 位置（决定机器人在哪）
    init_pose.pose.position.x = 0.0   
    init_pose.pose.position.y = 0.0  
    init_pose.pose.position.z = 0.0

    # 2. 方向（决定车头朝哪）
    q = quaternion_from_euler(0.0, 0.0, -2.900024)  
    init_pose.pose.orientation.x = q[0]     
    init_pose.pose.orientation.y = q[1]   
    init_pose.pose.orientation.z = q[2]    
    init_pose.pose.orientation.w = q[3]    

    nav.setInitialPose(init_pose)
    nav.waitUntilNav2Active() #等待导航
    rclpy.spin(nav)
    rclpy.shutdown()

   