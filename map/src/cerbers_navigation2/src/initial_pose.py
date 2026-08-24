#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 发布初始位姿到 /initialpose，供 Nav2 AMCL 定位使用，
# 省去在 RViz 中手动点击 "2D Pose Estimate"。
#
# 参数（可通过 launch 传入）：
#   x   : 初始位姿 x (m)
#   y   : 初始位姿 y (m)
#   yaw : 初始位姿朝向 (rad)
#
# 逻辑：每秒检查一次，一旦检测到 AMCL 订阅 /initialpose 就发布一次并退出；
#       若 10 秒内始终没有订阅者，则兜底发布一次后退出。
import math

import rclpy
from geometry_msgs.msg import PoseWithCovarianceStamped
from rclpy.node import Node


class InitialPosePublisher(Node):
    def __init__(self):
        super().__init__('initial_pose_publisher')

        self.declare_parameter('x', 0.0)
        self.declare_parameter('y', 0.0)
        self.declare_parameter('yaw', 0.0)

        self.publisher_ = self.create_publisher(
            PoseWithCovarianceStamped, '/initialpose', 10)

        self._count = 0
        self.timer_ = self.create_timer(1.0, self.publish_initial_pose)

    def publish_initial_pose(self):
        self._count += 1

        # 等待 AMCL 订阅 /initialpose（最多等 10 秒）
        if self.publisher_.get_subscription_count() == 0 and self._count < 10:
            self.get_logger().info(
                '等待 AMCL 订阅 /initialpose ...', throttle_duration_sec=2.0)
            return

        x = self.get_parameter('x').value
        y = self.get_parameter('y').value
        yaw = self.get_parameter('yaw').value

        msg = PoseWithCovarianceStamped()
        msg.header.frame_id = 'map'
        msg.header.stamp = self.get_clock().now().to_msg()

        msg.pose.pose.position.x = x
        msg.pose.pose.position.y = y
        msg.pose.pose.position.z = 0.0

        msg.pose.pose.orientation.x = 0.0
        msg.pose.pose.orientation.y = 0.0
        msg.pose.pose.orientation.z = math.sin(yaw / 2.0)
        msg.pose.pose.orientation.w = math.cos(yaw / 2.0)

        # 协方差：位置 0.25 m²，朝向 0.06 rad²
        msg.pose.covariance[0] = 0.25
        msg.pose.covariance[7] = 0.25
        msg.pose.covariance[35] = 0.06

        self.publisher_.publish(msg)
        self.get_logger().info(
            f'已发布初始位姿 -> x={x:.3f}, y={y:.3f}, yaw={yaw:.3f}')

        self.timer_.cancel()


def main(args=None):
    rclpy.init(args=args)
    node = InitialPosePublisher()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
