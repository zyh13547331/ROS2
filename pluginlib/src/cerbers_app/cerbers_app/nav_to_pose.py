from geometry_msgs.msg import PoseStamped
from nav2_simple_commander.robot_navigator import BasicNavigator
import rclpy
from tf_transformations import quaternion_from_euler
import math

def main():
    rclpy.init()
    nav = BasicNavigator()  # 节点
    nav.waitUntilNav2Active() #等待导航
    goal_pose = PoseStamped()
    goal_pose.header.frame_id = "map"
    goal_pose.header.stamp = nav.get_clock().now().to_msg()
    # 1. 位置（决定机器人在哪）
    goal_pose.pose.position.x = 1.0   
    goal_pose.pose.position.y = 1.0  
    goal_pose.pose.position.z = 0.0

    # 2. 方向（决定车头朝哪）
    q = quaternion_from_euler(0.0, 0.0, 0.0)  
    goal_pose.pose.orientation.x = q[0]     
    goal_pose.pose.orientation.y = q[1]   
    goal_pose.pose.orientation.z = q[2]    
    goal_pose.pose.orientation.w = q[3]    


    nav.goToPose(goal_pose)
    while not nav.isTaskComplete():
        feedback = nav.getFeedback()
        if feedback:
            nav.get_logger().info(f'预计剩余距离 {feedback.distance_remaining:.2f} m')
        #nav.cancelTask()
    
    nav.get_logger().info('导航任务完成')
    rclpy.shutdown()

   