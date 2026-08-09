import rclpy
from status_interfaces.msg import SystemStatus
from rclpy.node import Node
import psutil
import platform

class SysStatusPub(Node):
    def __init__(self, node_name):
        super().__init__(node_name)
        self.publisher_ = self.create_publisher(SystemStatus, 'system_status', 10)
        self.timer = self.create_timer(1.0, self.publish_status)

    def publish_status(self):
        cpu_percent = psutil.cpu_percent(interval=1)
        memory_info = psutil.virtual_memory()
        net_io_counters = psutil.net_io_counters()

        msg = SystemStatus()
        msg.stamp = self.get_clock().now().to_msg()
        msg.host_name = platform.node()
        msg.cpu_percent = cpu_percent
        msg.memory_percent = memory_info.percent
        msg.memory_total = memory_info.total / 1024 / 1024  # Convert to MB
        msg.memory_available = memory_info.available /1024/1024  # Convert to MB
        msg.net_sent = net_io_counters.bytes_sent /1024/1024  # Convert to MB
        msg.net_recv = net_io_counters.bytes_recv /1024/1024  # Convert to MB   

        self.get_logger().info(f"发布：{str(msg)}")
        self.publisher_.publish(msg)

def main():
    rclpy.init()
    node = SysStatusPub('sys_status_pub')
    rclpy.spin(node)
    rclpy.shutdown()