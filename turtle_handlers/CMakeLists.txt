cmake_minimum_required(VERSION 2.8.3)
project(turtle_handlers)

find_package(catkin REQUIRED COMPONENTS
  rospy
  std_msgs
)

catkin_python_setup()

include_directories(
  ${catkin_INCLUDE_DIRS}
)
