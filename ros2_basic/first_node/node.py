import rclpy
from rclpy.node import Node

def main():
    rclpy.init() #初始化工作，分配资源
    node = Node('python_node') #创建一个名为'python_node'的节点
    node.get_logger().info('Python Node!') #打印日志信息
    node.get_logger().warn('Python Node!') #打印日志信息
    rclpy.spin(node) #运行节点
    rclpy.shutdown() #关闭节点，释放资源

if __name__ == '__main__':
    main()