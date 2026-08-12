#include <rclcpp/rclcpp.hpp>
#include <geometry_msgs/msg/twist.hpp>
#include <turtlesim/msg/pose.hpp>
#include <face/srv/partol.hpp>
#include <cmath>
#include <algorithm>

using Partol = face::srv::Partol;

class turtle_service: public rclcpp::Node
{
private:
    rclcpp::Service<Partol>::SharedPtr service;
    rclcpp::Publisher<geometry_msgs::msg::Twist>::SharedPtr publisher;
    rclcpp::Subscription<turtlesim::msg::Pose>::SharedPtr subscriper;

    void pose_callback(const turtlesim::msg::Pose::SharedPtr pose){
        auto message = geometry_msgs::msg::Twist();

        double dx = target_x - pose->x;
        double dy = target_y - pose->y;
        double distance = std::sqrt(dx*dx + dy*dy);

        // 计算目标角度并归一化到 [-PI, PI]
        double target_angle = std::atan2(dy, dx);
        double angle_diff = target_angle - pose->theta;
        while (angle_diff > M_PI)  angle_diff -= 2 * M_PI;
        while (angle_diff < -M_PI) angle_diff += 2 * M_PI;

        if (distance > 0.1) {
            message.linear.x = k * distance;   // 距离越近速度越小
            message.angular.z = k * angle_diff;
        } else {
            message.linear.x = 0.0;            // 到达目标点停下
            message.angular.z = 0.0;
        }

        // 限速
        message.linear.x  = std::clamp(message.linear.x,  -max_speed, max_speed);
        message.angular.z = std::clamp(message.angular.z, -max_speed, max_speed);

        publisher->publish(message);
    }
    double target_x {3.0};
    double target_y {3.0};
    double k {1.0}; /*比例系数*/
    double max_speed {3.0};

public:
    turtle_service():Node("turtle_service"){
        publisher = this->create_publisher<geometry_msgs::msg::Twist>("turtle1/cmd_vel",10);
        subscriper = this->create_subscription<turtlesim::msg::Pose>("turtle1/pose",10,std::bind(&turtle_service::pose_callback,this,std::placeholders::_1));
        service = this->create_service<Partol>("turtle_service",
            [&](const Partol::Request::SharedPtr req, Partol::Response::SharedPtr res){
                if((0<req->target_x && req->target_x<11) && 
                    (0<req->target_y && req->target_y<11))
                {
                    res->result = Partol::Response::SUCCESS;
                    this->target_x = req->target_x;
                    this->target_y = req->target_y;
                }else{
                    res->result = Partol::Response::FAIL;
                }
        });
    }

    
};


int main(int argc, char* argv[]){
    rclcpp::init(argc, argv);
    auto node = std::make_shared<turtle_service>();
    rclcpp::spin(node);
    rclcpp::shutdown();
    return 0;
}