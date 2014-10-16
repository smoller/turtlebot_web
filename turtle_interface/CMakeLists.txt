cmake_minimum_required(VERSION 2.8.3)
project(turtle_interface)

find_package(catkin REQUIRED COMPONENTS
  rospy
  std_msgs
  turtle_handlers
)

include_directories(
  ${catkin_INCLUDE_DIRS}
)
