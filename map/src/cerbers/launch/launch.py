import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import Command, LaunchConfiguration
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue


def generate_launch_description():
    # 获取默认urdf路径
    urdf_path = get_package_share_directory('cerbers')
    default_urdf_path = os.path.join(urdf_path, 'urdf', 'cerbers.urdf')
    default_rviz_path = os.path.join(urdf_path,'rviz','display.rviz')

    # 声明urdf的目录参数，方便修改
    action_declear_arg_mode_path = DeclareLaunchArgument(
        name='model',
        default_value=str(default_urdf_path),
        description='加载模型文件路径'
    )

    # 文件路径获取内容并转换为参数对象，传入 robot_state_publisher
    robot_description = ParameterValue(
        Command(['xacro ', LaunchConfiguration('model')]),
        value_type=str
    )

    action_robot_set_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        parameters=[{'robot_description': robot_description}]
    )

    action_joint_set_publisher = Node(
        package='joint_state_publisher',
        executable='joint_state_publisher',
    )

    action_rviz_node = Node(
        package='rviz2',
        executable='rviz2',
        arguments=['-d',default_rviz_path]
    )

    return LaunchDescription([
        action_declear_arg_mode_path,
        action_robot_set_publisher,
        action_joint_set_publisher,
        action_rviz_node
    ])