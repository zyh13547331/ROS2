#ifndef SPIN_MOTION_CONTROL_HPP
#define SPIN_MOTION_CONTROL_HPP
#include "motion_control.hpp"

namespace motion_control{
    class SpinMotionControl : public MotionControl
    {
    private:
        /* data */
    public:
        void start() override;
        void stop() override;
    };
 
}

#endif