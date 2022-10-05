cmake_minimum_required(VERSION 3.0.2)
project(emg_tcp)

find_package(catkin REQUIRED COMPONENTS
  roscpp
  rospy
  std_msgs
)

catkin_package(
)

include_directories(
  include
  ${catkin_INCLUDE_DIRS}
)

link_directories(
  lib
)




add_dependencies(${catkin_EXPORTED_TARGETS})



catkin_install_python(PROGRAMS src/delsys_emg.py
  DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
)
