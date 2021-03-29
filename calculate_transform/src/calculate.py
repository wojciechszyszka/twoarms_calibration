#!/usr/bin/env python
import yaml
import rospy
import scipy
import os
from scipy.spatial.transform import Rotation as R

rospy.init_node('calculate_tranform')
while rospy.get_time() == 0.0:
    pass

left_path = os.path.join(os.path.expanduser('~'), '.ros', 'easy_handeye', 'left_eye_on_base.yaml')
right_path = os.path.join(os.path.expanduser('~'), '.ros', 'easy_handeye', 'right_eye_on_base.yaml')
final_path = os.path.join(os.path.expanduser('/'), 'putarms_ws', 'src', 'twoarms_calibration', 'universal_robot', 'ur_description', 'urdf', 'final_transform.yaml')

with open(left_path, 'r') as leftyaml:
    left_list = yaml.load(leftyaml)

with open(right_path, 'r') as rightyaml:
    right_list = yaml.load(rightyaml)

left_rotation = R.from_quat([left_list['transformation']['qx'], left_list['transformation']['qy'], left_list['transformation']['qz'], left_list['transformation']['qw']])
right_rotation = R.from_quat([right_list['transformation']['qx'], right_list['transformation']['qy'], right_list['transformation']['qz'], right_list['transformation']['qw']])
final_rotation = right_rotation*left_rotation


final_x = -(left_list['transformation']['x'] - right_list['transformation']['x'])
final_y = -(left_list['transformation']['y'] - right_list['transformation']['y'])
final_z = -(left_list['transformation']['z'] - right_list['transformation']['z'])

final_tranforamation = {'x': final_x, 'y': final_y, 'z': final_z, 'r': float(final_rotation.as_euler('xyz')[0]), 'p': float(final_rotation.as_euler('xyz')[1]), 'v': float(final_rotation.as_euler('xyz')[2])}

print(final_tranforamation)

with open(final_path, 'w') as file:
    documents = yaml.dump(final_tranforamation, file)

rospy.spin()