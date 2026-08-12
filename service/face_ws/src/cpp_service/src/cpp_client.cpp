#include <rclcpp/rclcpp.hpp>
#include <face/srv/partol.hpp>
#include <cmath>
#include <chrono>
#include <ctime>

using namespace std::chrono_literals; // 可使用10s， 100ms时间
using Partol = face::srv::Partol;

class turtle_client: public rclcpp::Node
{
private:
    rclcpp::Client<Partol>::SharedPtr client;
    rclcpp::TimerBase::SharedPtr timer;

public:
    turtle_client():Node("turtle_client"){
        srand(time(NULL));/*初始化随机数种子*/
        client = this->create_client<Partol>("turtle_service");
        /*等待服务上线*/
        timer = this->create_wall_timer(10s, [&]()->void{
            while(!this->client->wait_for_service(1s))
            {
                if(!rclcpp::ok()){
                    RCLCPP_INFO(this->get_logger(),"client exit");
                    return;
                }
                RCLCPP_INFO(this->get_logger(),"waiting for service");
            }
            /*构造对象*/
            auto request = std::make_shared<Partol::Request>();
            request->target_x = rand()%15;
            request->target_y = rand()%15;
            RCLCPP_INFO(this->get_logger(),"目标点(x,y):%f,%f",request->target_x,request->target_y);
            /*发送请求(异步)*/
            this->client->async_send_request(request, [&](rclcpp::Client<Partol>::SharedFuture result_future)
            ->void{
                auto response = result_future.get();
                if(response->result == Partol::Response::SUCCESS){
                    RCLCPP_INFO(this->get_logger(),"请求点成功!");
                }else{
                    RCLCPP_INFO(this->get_logger(),"请求点失败!");
                }
            });

        });
        
    }
    
};


int main(int argc, char* argv[]){
    rclcpp::init(argc, argv);
    auto node = std::make_shared<turtle_client>();
    rclcpp::spin(node);
    rclcpp::shutdown();
    return 0;
}