# Description
This repository contains modified packages and instructions how to use hand-eye calibration to automatically calibrate two UR3 robot arms with RealSense camera using ROS Melodic.

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

# Usage

The Tsai's hand-eye calibration can be used in two ways: eye-in-hand and eye-on-base. Since two arms are used, the more convenient variant is eye-on-base.

- Place the camera (tracking system) in a fixed position. Make sure it can see both arms.
- Place different AprilTags on the end effector of each arm. The tags can be found [here](https://github.com/AprilRobotics/apriltag-imgs). The default group is 'tag36h11'. It can be changed in the 'apriltag_ros/apriltag_ros/config/settings.yaml'. Scale up the images in your favorite editor and print them out. Remember to measure the size of the tag. Change the size and ID of the tag in 'apriltag_ros/apriltag_ros/config/tags.yaml'. 
- Position the robots, so that the tags are facing the camera.
- Set robots IP in 'two_putarms/launch/calibrate.launch'
- Run
```
roslaunch two_putarms calibration.launch
```



