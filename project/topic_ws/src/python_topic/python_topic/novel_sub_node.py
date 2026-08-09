import espeakng
import rclpy
from rclpy.node import Node
import requests
from example_interfaces.msg import String
from queue import Queue
import threading
import time

class NovelSubNode(Node):
    def __init__(self, node_name):
        super().__init__(node_name)
        self.get_logger().info(f'{node_name}, start!')
        self.novel_queue = Queue()
        self.novel_subscriber = self.create_subscription(String, 'novel', self.novel_callback, 10)
        self.speek_thread = threading.Thread(target=self.speech_thread)
        self.speek_thread.start()

    def novel_callback(self, msg):
        self.novel_queue.put(msg.data)

    def speech_thread(self):
        speaker = espeakng.Speaker()
        speaker.voice = 'zh'

        while rclpy.ok(): #检测ROS上下文是否ok
            if self.novel_queue.qsize() > 0:
                text = self.novel_queue.get()
                self.get_logger().info(f"read:{text}")
                speaker.say(text)
                speaker.wait() #等待讲完

            else:
                #当前线程休眠1s
                time.sleep(1)

def main():
    rclpy.init()
    node = NovelSubNode("novel") 
    rclpy.spin(node)
    rclpy.shutdown()