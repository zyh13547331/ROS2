#include <rclcpp/rclcpp.hpp>
#include <geometry_msgs/msg/twist.hpp>
#include <chrono>
#include <turtlesim/msg/pose.hpp>

using namespace std::chrono_literals;

class turtle_ctrl: public rclcpp::Node
{
private:
    // rclcpp::TimerBase::SharedPtr timer_;
    rclcpp::Publisher<geometry_msgs::msg::Twist>::SharedPtr publisher_;   
    rclcpp::Subscription<turtlesim::msg::Pose>::SharedPtr subscriper_;
    double target_x_ {3.0};
    double target_y_ {3.0};
    double k_ {1.0}; /*比例系数*/
    double max_speed_ {3.0};


public:
    explicit turtle_ctrl(const std::string &node_name):Node(node_name) /*创建发布者的智能指针*/
    {
        publisher_ = this ->create_publisher<geometry_msgs::msg::Twist>("/turtle1/cmd_vel", 10);
        // timer_ = this -> create_wall_timer(1000ms,std::bind(&turtle_ctrl::timer_callback,this));
        subscriper_ = this ->create_subscription<turtlesim::msg::Pose>("/turtle1/pose", 10, 
            std::bind(&turtle_ctrl::pose_callback, this, std::placeholders:: _1));

    }

    void pose_callback(const turtlesim::msg::Pose::SharedPtr pose){

        auto current_x = pose ->x;
        auto current_y = pose ->y;

        auto msg = geometry_msgs::msg::Twist();

        RCLCPP_INFO(get_logger(),"curent x:%f\ny:%f",current_x, current_y);

        /*计算距离和角度差*/
        auto distance = std::sqrt(
            (target_x_ - current_x)*(target_x_ - current_x)+
            (target_y_ - current_y)*(target_y_ - current_y)
        );

        auto angle = std::atan2((target_x_ - current_x),(target_y_ - current_y)) - pose ->theta;

        if(distance >0.1){
            if(fabs(angle)>0.2){
                msg.angular.z = fabs(angle);
            }else{
                msg.linear.x = k_*distance;
            }
        }

        if(msg.linear.x > max_speed_){
            msg.linear.x = max_speed_;
        }
            
        publisher_ ->publish(msg);
    }

    // void timer_callback(){
    //     auto msg = geometry_msgs::msg::Twist();
    //     msg.linear.x = 1.0;
    //     msg.angular.z = 0.5;
    //     publisher_ ->publish(msg);
    // }
};

int main(int argc, char* argv[]){
    rclcpp::init(argc, argv);
    auto node = std::make_shared<turtle_ctrl>("turtle_ctrl");

    rclcpp::spin(node);
    rclcpp::shutdown();

}


