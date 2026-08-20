import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import (
    DeclareLaunchArgument,
    ExecuteProcess,
    IncludeLaunchDescription,
    TimerAction,
)
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import Command, LaunchConfiguration
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue


def generate_launch_description():
    # 获取功能包share路径
    pkg_share = get_package_share_directory('cerbers')

    # 默认 urdf 与 world 路径
    default_xacro_path = os.path.join(pkg_share, 'urdf', 'cerbers', 'cerbers.urdf.xacro')
    default_world_path = os.path.join(pkg_share, 'world', 'custom_room')
    gazebo_ros_share = get_package_share_directory('gazebo_ros')

    # 声明 urdf 路径参数，方便修改
    action_declear_arg_model = DeclareLaunchArgument(
        name='model',
        default_value=str(default_xacro_path),
        description='加载模型文件路径'
    )

    # xacro 转 URDF 字符串，传给 robot_state_publisher
    robot_description = ParameterValue(
        Command(['xacro ', LaunchConfiguration('model')]),
        value_type=str
    )

    # 模型 spawn 后自动加载并激活关节状态控制器。
    # 用 spawner（自带 --controller-manager-timeout 等待服务就绪），比 ros2 control CLI 更可靠
    action_load_joint_states_controller = ExecuteProcess(
        cmd=['ros2', 'run', 'controller_manager', 'spawner',
             'cerbers_joint_state_broadcaster',
             '--controller-manager-timeout', '60'],
        output='screen'
    )

    # action_load_effort_controller = ExecuteProcess(
    #     cmd=['ros2', 'run', 'controller_manager', 'spawner',
    #          'cerbers_effort_controller',
    #          '--controller-manager-timeout', '60'],
    #     output='screen'
    # )

    # 差速驱动控制器：接收 /cmd_vel 控制左右轮，发布 /odom
    action_load_diff_drive_controller = ExecuteProcess(
        cmd=['ros2', 'run', 'controller_manager', 'spawner',
             'cerbers_diff_drive_controller',
             '--controller-manager-timeout', '60'],
        output='screen'
    )



    # spawn_entity.py 是长驻进程、spawn 成功后不会退出，因此不能用 OnProcessExit 触发。
    # 改为延迟执行，spawner 内部的 timeout 会等到 gazebo_ros2_control 的 controller_manager 就绪
    action_delayed_load_controller = TimerAction(
        period=8.0,
        actions=[action_load_joint_states_controller, action_load_diff_drive_controller]
    )

    action_robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        parameters=[{'robot_description': robot_description}]
    )

    # 启动 Gazebo，加载自定义世界
    action_launch_gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(gazebo_ros_share, 'launch', 'gazebo.launch.py')
        ),
        launch_arguments={'world': str(default_world_path)}.items()
    )

    # 把机器人模型生成到 Gazebo 中
    action_spawn_entity = Node(
        package='gazebo_ros',
        executable='spawn_entity.py',
        arguments=['-topic', 'robot_description', '-entity', 'cerbers'],
        output='screen'
    )

    return LaunchDescription([
        action_declear_arg_model,
        action_robot_state_publisher,
        action_launch_gazebo,
        action_spawn_entity,
        action_delayed_load_controller,
    ])