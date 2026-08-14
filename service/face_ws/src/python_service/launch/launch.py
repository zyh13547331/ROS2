import launch
import launch_ros

def generate_launch_description():
    #声明launch的参数
    action_declare_arg_background_g = launch.actions.DeclareLaunchArgument('launch_arg_background',default_value=150)
    #将launch参数手动传输给节点

    #产生launch描述
    action_turtlesim_node = launch_ros.actions.Node(
        package='turtlesim',
        executable='turtlesim_node',
        parameters=[{'background_g':
                     launch.substitutions.LaunchConfiguration('launch_arg_background', default='150')}],
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
        action_declare_arg_background_g,
        action_turtlesim_node,
        action_turtlesim_client,
        action_turtlesim_service,
    ])