#ifndef MOTION_CONTROL_HPP
#define MOTION_CONTROL_HPP

namespace motion_control{
    class MotionControl
    {
    private:
        /* data */
    public:
        virtual void start() = 0;
        virtual void stop() = 0;
    };
 
}

#endif