from geometry_msgs.msg import PoseStamped
from nav2_simple_commander.robot_navigator import BasicNavigator
import rclpy
from tf_transformations import quaternion_from_euler
import math

def main():
    rclpy.init()
    nav = BasicNavigator()
    nav.waitUntilNav2Active()

    # 定义多个目标点
    goal_poses = []

    # 目标点 1
    pose1 = PoseStamped()
    pose1.header.frame_id = "map"
    pose1.header.stamp = nav.get_clock().now().to_msg()
    pose1.pose.position.x = -1.0
    pose1.pose.position.y = -1.0
    pose1.pose.position.z = 0.0
    q = quaternion_from_euler(0.0, 0.0, 0.0)
    pose1.pose.orientation.x = q[0]
    pose1.pose.orientation.y = q[1]
    pose1.pose.orientation.z = q[2]
    pose1.pose.orientation.w = q[3]
    goal_poses.append(pose1)

    # 目标点 2
    pose2 = PoseStamped()
    pose2.header.frame_id = "map"
    pose2.header.stamp = nav.get_clock().now().to_msg()
    pose2.pose.position.x = 2.0
    pose2.pose.position.y = 2.0
    pose2.pose.position.z = 0.0
    q = quaternion_from_euler(0.0, 0.0, 1.57)  # 90°
    pose2.pose.orientation.x = q[0]
    pose2.pose.orientation.y = q[1]
    pose2.pose.orientation.z = q[2]
    pose2.pose.orientation.w = q[3]
    goal_poses.append(pose2)

    # 目标点 3
    pose3 = PoseStamped()
    pose3.header.frame_id = "map"
    pose3.header.stamp = nav.get_clock().now().to_msg()
    pose3.pose.position.x = 0.0
    pose3.pose.position.y = 0.0
    pose3.pose.position.z = 0.0
    q = quaternion_from_euler(0.0, 0.0, 0.0)
    pose3.pose.orientation.x = q[0]
    pose3.pose.orientation.y = q[1]
    pose3.pose.orientation.z = q[2]
    pose3.pose.orientation.w = q[3]
    goal_poses.append(pose3)

    # 发送多点导航目标
    nav.followWaypoints(goal_poses)

    # 监控导航进度
    while not nav.isTaskComplete():
        feedback = nav.getFeedback()
        if feedback:
            nav.get_logger().info(f'导航中...\n路点编号：{feedback.current_waypoint}')
        # nav.cancelTask()

    nav.get_logger().info('所有目标点已到达')
    rclpy.shutdown()