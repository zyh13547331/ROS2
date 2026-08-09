import rclpy
from rclpy.node import Node
import requests
from example_interfaces.msg import String
from queue import Queue

class NovelPubNode(Node):
    def __init__(self, node_name):
        super().__init__(node_name)
        self.get_logger().info(f'{node_name}, start!')
        self.novel_queue = Queue() # 创建队列
        self.novel_publisher = self.create_publisher(String, 'novel', 15) #创建发布者
        self.create_timer(5, self.timer_callback)
        

    def timer_callback(self):
        if self.novel_queue.qsize() > 0:
            line = self.novel_queue.get()
            msg = String()
            msg.data = line
            self.novel_publisher.publish(msg)
            self.get_logger().info(f'发布了：{msg}')


    def download(self, url):
        response = requests.get(url)
        if response.status_code != 200:
            self.get_logger().error(f'下载失败，状态码：{response.status_code}')
            return
        response.encoding = 'utf-8'
        text = response.text
        self.get_logger().info(f'下载{url},{len(text)}')
        for line in text.splitlines():
            self.novel_queue.put(line)



def main():
    rclpy.init()
    novel_node = NovelPubNode('novel_pub')
    novel_node.download('http://0.0.0.0:8000/novel1.txt')
    rclpy.spin(novel_node)
    rclpy.shutdown()