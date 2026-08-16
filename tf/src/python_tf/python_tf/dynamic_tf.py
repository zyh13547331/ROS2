import rclpy
from rclpy.node import Node
from tf2_ros import TransformBroadcaster #动态坐标发布器
from geometry_msgs.msg import TransformStamped #消息接口
from tf_transformations import quaternion_from_euler #欧拉角转四元数
import math #角度转弧度函数

class TF(Node):
    def __init__(self):
        super().__init__('dynamic_tf')
        self.broadcaster = TransformBroadcaster(self)
        self.timer = self.create_timer(3.0,self.publish_tf)
        #self.publish_static_tf()

    def publish_tf(self):
        #发布TF，从camera_link到bottle_link之间的坐标关系
        transform = TransformStamped()
        transform.header.frame_id = 'camera_link'
        transform.header.stamp = self.get_clock().now().to_msg()
        transform.child_frame_id = 'bottle_link'

        transform.transform.translation.x =0.3
        transform.transform.translation.y =0.2
        transform.transform.translation.z =0.5
        #欧拉角转四元数x,y,z,w
        q = quaternion_from_euler(math.radians(180),0,0)
        #旋转部分赋值
        transform.transform.rotation.x = q[0]  
        transform.transform.rotation.y = q[1]
        transform.transform.rotation.z = q[2]
        transform.transform.rotation.w = q[3]
        #发布动态坐标
        self.broadcaster.sendTransform(transform)
        self.get_logger().info(f"发布静态TF:{transform}")


def main():
    rclpy.init()
    node = TF()
    rclpy.spin(node)
    rclpy.shutdown()
