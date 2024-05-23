import os
from launch import LaunchDescription
from launch_ros.actions import Node
from moveit_configs_utils import MoveItConfigsBuilder
from launch.actions import DeclareLaunchArgument, GroupAction
from launch.substitutions import LaunchConfiguration
from launch.conditions import LaunchConfigurationEquals

def generate_launch_description():
    target_arg = DeclareLaunchArgument(
        "target", default_value="sim"
    )
    run_env_f  = LaunchConfiguration('target')


    sim_moveit_config = MoveItConfigsBuilder("name", package_name="my_moveit_config").to_moveit_configs()
    real_moveit_config = MoveItConfigsBuilder("name", package_name="real_moveit_config").to_moveit_configs()

    # MoveItCpp demo executable
    sim_moveit_pick_and_place_node = Node(
        name="pick_and_place",
        package="moveit2_scripts",
        executable="pick_and_place",
        output="screen",
        parameters=[
            sim_moveit_config.robot_description,
            sim_moveit_config.robot_description_semantic,
            sim_moveit_config.robot_description_kinematics,
            {'use_sim_time': True},
            {'target': run_env_f},
        ],
    )

    real_moveit_pick_and_place_node = Node(
        name="pick_and_place",
        package="moveit2_scripts",
        executable="pick_and_place",
        output="screen",
        parameters=[
            real_moveit_config.robot_description,
            real_moveit_config.robot_description_semantic,
            real_moveit_config.robot_description_kinematics,
            {'use_sim_time': False},
            {'target': run_env_f},
        ],
    )

    return LaunchDescription(
        [
            target_arg,
            GroupAction(
                condition=LaunchConfigurationEquals('target', 'sim'),
                actions = [
                    sim_moveit_pick_and_place_node
                ]
            ),
            GroupAction(
                condition=LaunchConfigurationEquals('target', 'real'),
                actions = [
                    real_moveit_pick_and_place_node
                ]
            )
        ]
    )