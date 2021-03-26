# Description
This repository contains modified packages and instructions how to use hand-eye calibration to automatically calibrate two UR3 robot arms with RealSense camera using ROS Melodic.
## Used packages
- [AprilTag](https://github.com/AprilRobotics/apriltag.git)
- [apriltag_ros](https://github.com/AprilRobotics/apriltag_ros.git)
- [ROS-Industrial Universal Robot](https://github.com/ros-industrial/universal_robot.git) 
- [Universal_Robots_ROS_Driver](https://github.com/UniversalRobots/Universal_Robots_ROS_Driver.git)
- [easy_handeye](https://github.com/IFL-CAMP/easy_handeye.git)
- [ROS Wrapper for Intel® RealSense™ Devices](https://github.com/IntelRealSense/realsense-ros.git)
# Installation
- install [RealSense for ROS](https://github.com/IntelRealSense/realsense-ros)
- install OpenCV
```
pip install opencv-python
```
- clone this repository into your catkin workspace:
```
cd ~/catkin_ws/src  # replace with path to your workspace
git clone https://github.com/wojciechszyszka/twoarms_calibration.git
```
- source your distro
```
source /opt/ros/melodic/setup.bash 
```

- satisfy dependencies
```
cd ..  # now we are inside ~/catkin_ws
rosdep install -iyr --from-paths src
```

- build
```
catkin_make_isolated
```

- source your workspace
```
source devel_isolated/setup.bash
```
# Usage

The Tsai's hand-eye calibration can be used in two ways: eye-in-hand and eye-on-base. Since two arms are used, the more convenient variant is eye-on-base.

- Place different AprilTags on the end effector of each arm. The tags can be found [here](https://github.com/AprilRobotics/apriltag-imgs). The default group is 'tag36h11'. It can be changed in the 'apriltag_ros/apriltag_ros/config/settings.yaml'. 
``` yaml
tag_family:        'tag36h11' # options: tagStandard52h13, tagStandard41h12, tag36h11, tag25h9, tag16h5, tagCustom48h12, tagCircle21h7, tagCircle49h12 
```
Scale up the images in your favorite editor and print them out. Remember to measure the size of the tag. Change the size and ID of the tag in 'apriltag_ros/apriltag_ros/config/tags.yaml'. 
``` yaml
standalone_tags:
  [
    {id: 0, size: 0.044, name: 'leftTag'},
    {id: 1, size: 0.044, name: 'rightTag'}
  ]
  ```
- Place the camera (tracking system) in a fixed position. Make sure it can see both arms with ca. 40cm margin.
- Position the robots, so that the tags are facing the camera.
- Set IP adresses of robots in 'two_putarms/launch/calibrate.launch'
``` xml
  <arg name="left_robot_ip"           default="150.254.47.149" />
  <arg name="right_robot_ip"          default="150.254.47.193" />
```
- Run calibration launch file:
```
roslaunch two_putarms calibrate.launch
```
- Wait for robots to finish movements. Now the console should display transform between camera and each arm. The tranforms are saved.
- Exit the launch file and publish calculated tranforms in TF by running:
```
rosluanch two_putarms publish_calibration.launch
```



