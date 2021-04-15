import launch
import launch.actions
import launch_ros.actions

def generate_launch_description():
    return launch.LaunchDescription([
        launch.actions.DeclareLaunchArgument(
            'node_prefix',
            default_value=[launch.substitutions.EnvironmentVariable('USER'), '_'],
            description='Prefix for node names'
        ),
        launch_ros.actions.Node(
            package='ksr_robot20', executable='teleop_keyboard', output='screen',
            name=[launch.substitutions.LaunchConfiguration('node_prefix'), 'teleop_keyboard']
        ),
    ])