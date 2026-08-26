import launch
import launch_ros
from ament_index_python.packages import get_package_share_directory

def generate_launch_description():
    package_path = get_package_share_directory('cerbers_partol')
    config_path = package_path+'/config/partol.config.yaml'
    action_partol_node = launch_ros.actions.Node(
        package='cerbers_partol',
        executable='partol_node',
        output='screen',
        parameters=[config_path]
    )
    action_speaker = launch_ros.actions.Node(
        package='cerbers_partol',
        executable='speaker',
        output='screen',
        parameters=[config_path]
    )

    return launch.LaunchDescription([
        action_partol_node,
        action_speaker
    ])
