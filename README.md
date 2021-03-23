# Description
This repository contains modified packages and instructions how to automaticly calibrate two UR3 robot arms with RealSense camera using ROS.

# Installation
- install [RealSense for ROS](https://github.com/IntelRealSense/realsense-ros)

- clone this repository into your catkin workspace:
```
cd ~/catkin_ws/src  # replace with path to your workspace
git clone https://github.com/wojciechszyszka/twoarms_calibration.git
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

