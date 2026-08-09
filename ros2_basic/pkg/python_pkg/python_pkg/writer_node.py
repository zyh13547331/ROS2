import rclpy
from rclpy.node import Node
from python_pkg.person_node import PersonNode

class WriterNode(PersonNode):
    def __init__(self, book: str) -> None:
        super().__init__('writer_node', 'Writer', 30)
        self.book = book

def main():
    rclpy.init()
    node = WriterNode('好书一本')
    node.get_logger().info(f"Writer is writing a book: {node.book}")
    node.eat('sandwich')
    rclpy.spin(node)
    rclpy.shutdown()