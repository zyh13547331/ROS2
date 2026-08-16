import launch
import launch_ros

def generate_launch_description():
    #产生launch描述
    action_static = launch_ros.actions.Node(
        package='python_tf',
        executable='static_tf',
        output='screen'
    )
    action_dynamic = launch_ros.actions.Node(
        package='python_tf',
        executable='dynamic_tf',
        output='log'
    )
    action_lisenter = launch_ros.actions.Node(
        package='python_tf',
        executable='tf_lisenter',
        output='both'
    )

    return launch.LaunchDescription([
        # 动作
        action_static,
        action_dynamic,
        action_lisenter,
    ])