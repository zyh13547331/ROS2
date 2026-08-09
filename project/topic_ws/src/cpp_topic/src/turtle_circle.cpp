#include <rclcpp/rclcpp.hpp>
#include <geometry_msgs/msg/twist.hpp>
#include <chrono>

using namespace std::chrono_literals;

class turtle_circle: public rclcpp::Node
{
private:
    rclcpp::TimerBase::SharedPtr timer_;
    rclcpp::Publisher<geometry_msgs::msg::Twist>::SharedPtr publisher_;   

public:
    explicit turtle_circle(const std::string &node_name):Node(node_name) /*创建发布者的智能指针*/
    {
        publisher_ = this ->create_publisher<geometry_msgs::msg::Twist>("/turtle1/cmd_vel", 10);
        timer_ = this -> create_wall_timer(1000ms,std::bind(&turtle_circle::timer_callback,this));
    }

    void timer_callback(){
        auto msg = geometry_msgs::msg::Twist();
        msg.linear.x = 1.0;
        msg.angular.z = 0.5;
        publisher_ ->publish(msg);
    }
};

int main(int argc, char* argv[]){
    rclcpp::init(argc, argv);
    auto node = std::make_shared<turtle_circle>("turtlr_circle");

    rclcpp::spin(node);
    rclcpp::shutdown();

}


