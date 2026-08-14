import launch
import launch_ros
from ament_index_python.packages import get_package_share_directory

def generate_launch_description():
    #声明参数
    action_declare_startup_rqt = launch.actions.DeclareLaunchArgument('startup_rqt',
                                                                      default_value="False")

    startup_rqt = launch.substitutions.LaunchConfiguration('startup_rqt', default='False')

    #1.动作，包含其他launch（启动其他launch）
    multisim_launch_path = [get_package_share_directory('turtlesim'),'/launch/','multisim.launch.py']
    action_include_launch = launch.actions.IncludeLaunchDescription(
        launch.launch_description_sources.PythonLaunchDescriptionSource(
            multisim_launch_path
        )
    )
    #2.动作，打印数据
    action_log_info = launch.actions.LogInfo(msg=str(multisim_launch_path))

    #3.动作，执行进程
    action_topic_list = launch.actions.ExecuteProcess(
        condition = launch.conditions.IfCondition(startup_rqt),
        cmd=['rqt']
    )

    #4.动作,组织动作成组，多个动作成一组
    action_group = launch.actions.GroupAction([
        #5.动作，定时器
        launch.actions.TimerAction(period=2.0, actions=[action_include_launch]),
        launch.actions.TimerAction(period=4.0, actions=[action_topic_list]),
    ])

    return launch.LaunchDescription([
        # 动作
        action_log_info,
        action_group
    ])