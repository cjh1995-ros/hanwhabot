cmake_minimum_required(VERSION 3.0.2)
project(hanwhabot_msgs)

find_package(catkin REQUIRED COMPONENTS
  actionlib
  actionlib_msgs
  message_generation
  std_msgs
  std_srvs
)

add_message_files(
  FILES
  DetectObstacle.msg
  DetectObstacles.msg
  ObstacleData.msg
#   Message2.msg
)

## Generate services in the 'srv' folder
add_service_files(
  FILES
  StartSignal.srv
  HandleSignal.srv
)

## Generate actions in the 'action' folder
# add_action_files(
#   FILES
#   Action1.action
#   Action2.action
# )

## Generate added messages and services with any dependencies listed here
generate_messages(
  DEPENDENCIES
  actionlib_msgs#   std_msgs
  std_msgs
  std_srvs
)

catkin_package(
  LIBRARIES hanwhabot_msgs
  CATKIN_DEPENDS actionlib actionlib_msgs message_runtime std_msgs
  DEPENDS system_lib
)

include_directories(
# include
  ${catkin_INCLUDE_DIRS}
)

