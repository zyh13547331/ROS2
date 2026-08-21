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
    # 🔧 修复：补全 .world 后缀，避免 Gazebo 加载默认空地图
    default_world_path = os.path.join(pkg_share, 'world', 'cust_world')
    gazebo_ros_share = get_package_share_directory('gazebo_ros')

    # 声明 urdf 路径参数，方便修改
    action_declare_arg_model = DeclareLaunchArgument(
        name='model',
        default_value=str(default_xacro_path),
        description='加载模型文件路径'
    )

    # xacro 转 URDF 字符串，传给 robot_state_publisher
    robot_description = ParameterValue(
        Command(['xacro ', LaunchConfiguration('model')]),
        value_type=str
    )

    # ============================================================
    # 1. robot_state_publisher（必须加 use_sim_time: true）
    # ============================================================
    action_robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        parameters=[{
            'robot_description': robot_description,
            'use_sim_time': True,   # 🔧 关键修复：使用仿真时间
        }]
    )

    # ============================================================
    # 2. 启动 Gazebo，加载自定义世界
    # ============================================================
    action_launch_gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(gazebo_ros_share, 'launch', 'gazebo.launch.py')
        ),
        launch_arguments={'world': str(default_world_path)}.items()
    )

    # ============================================================
    # 3. 把机器人模型生成到 Gazebo 中（加初始坐标防叠罗汉）
    # ============================================================
    action_spawn_entity = Node(
        package='gazebo_ros',
        executable='spawn_entity.py',
        arguments=[
            '-topic', 'robot_description',
            '-entity', 'cerbers',
            '-x', '0.0',
            '-y', '0.0',
            '-z', '0.05',   # 抬高一点避免陷入地面
        ],
        output='screen'
    )

    # ============================================================
    # 4. 控制器加载（分步进行，保证顺序）
    # ============================================================

    # 4.1 第一步：先加载 joint_state_broadcaster（必须最先加载）
    def load_joint_state_broadcaster():
        return ExecuteProcess(
            cmd=[
                'ros2', 'run', 'controller_manager', 'spawner',
                'cerbers_joint_state_broadcaster',
                '--controller-manager-timeout', '60'
            ],
            output='screen'
        )

    # 4.2 第二步：再加载 diff_drive_controller（依赖 joint_states）
    def load_diff_drive_controller():
        return ExecuteProcess(
            cmd=[
                'ros2', 'run', 'controller_manager', 'spawner',
                'cerbers_diff_drive_controller',
                '--controller-manager-timeout', '60'
            ],
            output='screen'
        )

    # 4.3 使用 TimerAction 分阶段加载
    # 阶段1：等待 Gazebo 和 spawn_entity 完成（8秒后加载 joint_state_broadcaster）
    action_load_controllers_step1 = TimerAction(
        period=8.0,
        actions=[load_joint_state_broadcaster()]
    )

    # 阶段2：再等 4 秒（即总共 12 秒），加载 diff_drive_controller
    action_load_controllers_step2 = TimerAction(
        period=12.0,
        actions=[load_diff_drive_controller()]
    )

    # ============================================================
    # 5. 返回启动描述
    # ============================================================
    return LaunchDescription([
        action_declare_arg_model,
        action_robot_state_publisher,
        action_launch_gazebo,
        action_spawn_entity,
        action_load_controllers_step1,
        action_load_controllers_step2,
    ])