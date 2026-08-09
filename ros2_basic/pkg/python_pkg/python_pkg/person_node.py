import rclpy
from rclpy.node import Node

"""
类： PersonNode
属性：
    name : str, 姓名
    age : int, 年龄
方法：
    eat : 吃东西
"""

class PersonNode(Node):
    def __init__(self,node_name: str, name: str, age: int) -> None:
        super().__init__(node_name)
        self.node_name = node_name
        self.name = name
        self.age = age

    def eat(self, food: str):
        """
        方法：吃东西
        :food : str, 吃的东西
        """
        #print(f"{self.name},{self.age}岁, is eating {food}")

        self.get_logger().info(f"{self.name},{self.age}岁, is eating {food}")


def main():
    rclpy.init()
    rclpy.spin_once()
    node = PersonNode('yu', 'yuhao9', 21)
    node.eat('banana')
    node = PersonNode('hao', 'yuhao8', 20)
    node.eat('apple')
    rclpy.shutdown()