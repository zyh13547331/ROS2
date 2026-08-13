#include <rclcpp/rclcpp.hpp>
#include <face/srv/partol.hpp>
#include <cmath>
#include <chrono>
#include <ctime>
#include <rcl_interfaces/msg/parameter.hpp>
#include <rcl_interfaces/msg/parameter_value.hpp>
#include <rcl_interfaces/msg/parameter_type.hpp>
#include <rcl_interfaces/srv/set_parameters.hpp>

using SetP = rcl_interfaces::srv::SetParameters;
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
    /*创建客户端，返回结果*/
    SetP::Response::SharedPtr call_set_parameter(const rcl_interfaces::msg::Parameter &param){
        auto parma_client = this->create_client<SetP>("/turtle_service/set_parameters");
        //检测服务端是否上线
        while(!parma_client->wait_for_service(1s)){
            if(!rclcpp::ok()){
                RCLCPP_ERROR(this->get_logger(),"请求失败！");
                return nullptr;
            }
            RCLCPP_INFO(this->get_logger(),"等待服务上线中...");
        }
        //构造请求对象
        auto request = std::make_shared<SetP::Request>();
        request->parameters.push_back(param);
        //发送请求
        auto future = parma_client->async_send_request(request);
        rclcpp::spin_until_future_complete(this->get_node_base_interface(),future);
        auto response = future.get();
        return response;
    }

    /*更新参数*/
    void update_server_param(double k){
        //创建参数对象
        auto param = rcl_interfaces::msg::Parameter();
        param.name = "k";
        //创建参数值
        auto param_value = rcl_interfaces::msg::ParameterValue();
        param_value.type = rcl_interfaces::msg::ParameterType::PARAMETER_DOUBLE;
        param_value.double_value = k;
        param.value = param_value;
        //请求参数并处理
        auto response = this->call_set_parameter(param);
        if(response == NULL){
            RCLCPP_INFO(this->get_logger(),"参数更新失败");
            return;
        }
        for(auto result:response->results){
            if(result.successful == false){
                RCLCPP_INFO(this->get_logger(),"参数更新失败,原因:%s",result.reason.c_str());
            }else{
                RCLCPP_INFO(this->get_logger(),"参数更新成功");
            }
        }
    }
    
};


int main(int argc, char* argv[]){
    rclcpp::init(argc, argv);
    auto node = std::make_shared<turtle_client>();
    node->update_server_param(4.0);
    rclcpp::spin(node);
    rclcpp::shutdown();
    return 0;
}