#include <iostream>
#include "motion_system/spin_motion_control.hpp"
namespace motion_control
{
    void SpinMotionControl::start()
    {
        // 实现旋转运动控制逻辑
        std::cout << "SpinMotionControl::start" << std::endl;
    }
    void SpinMotionControl::stop()
    {
        // 停止运动控制
        std::cout << "SpinMotionControl::stop" << std::endl;
    }
} 
#include "pluginlib/class_list_macros.hpp"
PLUGINLIB_EXPORT_CLASS(motion_control::SpinMotionControl, motion_control::MotionControl)