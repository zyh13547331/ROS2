import rclpy
from rclpy.node import Node
from tf2_ros import TransformListener,Buffer #坐标监听器
from tf_transformations import euler_from_quaternion #四元数转欧拉角
import math #角度转弧度函数

class TF(Node):
    def __init__(self):
        super().__init__('listen_tf')
        self.buffer = Buffer()
        self.listener = TransformListener(self.buffer,self)
        self.timer = self.create_timer(1,self.get_tf)
        

    def get_tf(self):
        #定时获取坐标关系
        try:
            result = self.buffer.lookup_transform('base_link','bottle_link',
                                                  rclpy.time.Time(seconds = 0.0),rclpy.duration.Duration(seconds=1.0))
            transform = result.transform
            self.get_logger().info(f'平移：{transform.translation}')
            self.get_logger().info(f'选装：{transform.rotation}')
            rotation_euler = euler_from_quaternion(
                transform.rotation.x,
                transform.rotation.y,
                transform.rotation.z,
                transform.rotation.w,
            )
            self.get_logger().info(f'旋转RPY:{rotation_euler}')
        except Exception as e:
            self.get_logger().warn(f'坐标变换失败原因：{str(e)}')


def main():
    rclpy.init()
    node = TF()
    rclpy.spin(node)
    rclpy.shutdown()
