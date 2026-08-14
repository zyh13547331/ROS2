import launch
import launch_ros

def generate_launch_description():
    #产生launch描述
    action_turtlesim_node = launch_ros.actions.Node(
        package='turtlesim',
        executable='turtlesim_node',
        output='screen'
    )
    action_turtlesim_client = launch_ros.actions.Node(
        package='cpp_service',
        executable='cpp_client',
        output='log'
    )
    action_turtlesim_service = launch_ros.actions.Node(
        package='cpp_service',
        executable='cpp_node',
        output='both'
    )

    return launch.LaunchDescription([
        # 动作
        action_turtlesim_node,
        action_turtlesim_client,
        action_turtlesim_service,
    ])