#include "rclcpp/rclcpp.hpp"

class PersonNode : public rclcpp::Node
{
private:
/*声明*/
    std::string name_;
    int age_;  

public:
    PersonNode(const std::string &node_name,const std::string &name,const int &age)
    :Node(node_name), name_(name), age_(age)
    /*调用父类构造函数等用于python中的super().__init__()*/
    {
        this->name_ = name;
        this->age_ = age;
    };

    void eat(const std::string &food)
    {
          RCLCPP_INFO(this->get_logger(), "我是%s,今年%d岁,我正在吃%s", this->name_.c_str(), this->age_, food.c_str());
    };
};

int main(int argc, char *argv[])
{
    rclcpp::init(argc, argv);
    auto node = std::make_shared<PersonNode>("person_node", "张三", 18);
    RCLCPP_INFO(node->get_logger(),"Hello, CPP_NODE!");
    node->eat("苹果");
    rclcpp::spin(node);
    rclcpp::shutdown();
    return 0;
}