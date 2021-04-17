#!/bin/bash
source /opt/ros/foxy/setup.bash
export RMW_IMPLEMENTATION=rmw_fastrtps_cpp
export ROS_DOMAIN_ID=30

#Modify paths to match local installation
source /home/yuki/projects/KSRWorkspace/install/setup.bash

ros2 launch ksr_robot20 robot.launch.py

PID=$!
wait "$PID"