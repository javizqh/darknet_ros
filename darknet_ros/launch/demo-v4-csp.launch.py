import os

from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription, SetEnvironmentVariable
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node

def generate_launch_description():
  darknet_ros_share_dir = get_package_share_directory('darknet_ros')
  network_param_file = darknet_ros_share_dir + '/config/yolov4-csp.yaml'

  darknet_ros_launch = IncludeLaunchDescription(
    PythonLaunchDescriptionSource([darknet_ros_share_dir + '/launch/darknet_ros.launch.py']),
      launch_arguments={
        'network_param_file': network_param_file,
      }.items()
  )

  camera = Node(
    package="v4l2_camera",
    node_executable="v4l2_camera_node",
    # node_namespace="camera/rgb",
    parameters=[
      {'video_device'     : "/dev/video0"},
    ])
  
  return LaunchDescription([
    darknet_ros_launch,
    camera,
  ])