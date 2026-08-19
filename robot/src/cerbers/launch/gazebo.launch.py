import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
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
    ])