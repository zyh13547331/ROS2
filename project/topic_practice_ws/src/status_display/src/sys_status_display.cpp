#include <QApplication>
#include <QLabel>
#include <QString>
#include <rclcpp/rclcpp.hpp>
#include <status_interfaces/msg/system_status.hpp>

using SystemStatus = status_interfaces::msg::SystemStatus;

class SystemStatusDisplay : public rclcpp::Node
{
private:

    rclcpp::Subscription<SystemStatus>::SharedPtr subscription_;
    QLabel *label_;
public:
    SystemStatusDisplay() : Node("system_status_display")
    {
        label_ = new QLabel();
        subscription_ = this->create_subscription<SystemStatus>(
        "system_status", 10,[&](const SystemStatus::SharedPtr msg)->void{
            label_->setText(get_qstr_from_msg(msg));
        });
        label_->setText(get_qstr_from_msg(std::make_shared<SystemStatus>()));
        label_->show();

    };

    QString get_qstr_from_msg(const SystemStatus::SharedPtr msg){
        std::stringstream show_str;
        show_str <<"======== System Status Display ========\n";
        show_str <<"Time: " << msg->stamp.sec << "\n";
        show_str <<"Host: " << msg->host_name << "\n";
        show_str <<"CPU Usage: " << msg->cpu_percent << "%\n";
        show_str <<"Memory Usage: " << msg->memory_percent << "%\n";
        show_str <<"Memory Total: " << msg->memory_total << "MB\n";
        show_str <<"Memory Available: " << msg->memory_available << "MB\n";
        show_str <<"Net Sent: " << msg->net_sent << "MB/s\n";
        show_str <<"Net Recv: " << msg->net_recv << "MB/s\n";
        show_str <<"========================================\n";
        return QString::fromStdString(show_str.str());
    };
};

int main(int argc, char *argv[])
{
    rclcpp::init(argc, argv);
    QApplication app(argc, argv);
    auto node = std::make_shared<SystemStatusDisplay>();

    std::thread spin_thread([&]()->void{
        rclcpp::spin(node);
    });

    spin_thread.detach();

    app.exec();
    return 0;
}