#include <rclcpp/rclcpp.hpp>
#include <iostream>

int main(int argc, char * argv[])
{
    rclcpp::init(argc , argv); //初始化工作，分配资源
    auto node = std::make_shared<rclcpp::Node>("cpp_node"); //创建一个名为'cpp_node'的节点
    RCLCPP_INFO(node -> get_logger(), "C++ Node!"); //打印日志信息
    rclcpp::spin(node); //运行节点
    rclcpp::shutdown(); //关闭节点，释放资源
  return 0;
}