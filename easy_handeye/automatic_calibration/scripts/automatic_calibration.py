#!/usr/bin/env python
from easy_handeye.handeye_client import HandeyeClient
import rospy
import sys
import rospy
import rospkg

class AutomaticMovements():
    NOT_INITED_YET = 0
    BAD_PLAN = 1
    GOOD_PLAN = 2
    MOVED_TO_POSE = 3
    BAD_STARTING_POSITION = 4
    GOOD_STARTING_POSITION = 5
    SAMPLE_TOOK = 6
    MOVEMENT_FAILED = 7

    def __init__(self):
        self.handeye_client = HandeyeClient()
        self.state = AutomaticMovements.NOT_INITED_YET
        self.samples_taken = 0
        self.current_target_pose = -1  # -1 is home
        self.target_poses = None


    def handle_check_pose(self):
        check_pose_result = self.handeye_client.check_starting_pose()
        if check_pose_result.can_calibrate:
            print('{} Good starting pose'.format(rospy.get_namespace()))
            self.state = AutomaticMovements.GOOD_STARTING_POSITION
        else:
            print('{} Bad starting pose'.format(rospy.get_namespace()))
            self.state = AutomaticMovements.BAD_STARTING_POSITION
        self.current_target_pose = check_pose_result.target_poses.current_target_pose_index
        self.target_poses = check_pose_result.target_poses.target_poses
        self.plan_was_successful = None
        print(self.current_target_pose)

    def handle_next_pose(self):
        next_pose_result = self.handeye_client.select_target_pose(self.current_target_pose+1)
        self.current_target_pose = next_pose_result.target_poses.current_target_pose_index
        self.target_poses = next_pose_result.target_poses.target_poses
        self.plan_was_successful = None

        self.state = AutomaticMovements.GOOD_STARTING_POSITION
        print("{} Current target pose {}".format(rospy.get_namespace(), self.current_target_pose))


    def handle_plan(self):
        plan_result = self.handeye_client.plan_to_selected_target_pose()
        self.plan_was_successful = plan_result.success
        if self.plan_was_successful :
            print("{} Plan successful".format(rospy.get_namespace()))
            self.state = AutomaticMovements.GOOD_PLAN
        else:
            print("{} Plan failed".format(rospy.get_namespace()))
            self.state = AutomaticMovements.BAD_PLAN

    def handle_execute(self):
        if self.plan_was_successful:
            execution_result = self.handeye_client.execute_plan()
            if execution_result.success:
                self.state = AutomaticMovements.MOVED_TO_POSE
                print("{} Execution successful".format(rospy.get_namespace()))
            else:
                self.state = AutomaticMovements.MOVEMENT_FAILED
                print("{} Execution failed".format(rospy.get_namespace()))

    def handle_take_sample(self):
        sample_list = self.handeye_client.take_sample()
        self.samples_taken += 1
        print("{} Sample {} taken ".format(rospy.get_namespace(), self.samples_taken))
        self.state = AutomaticMovements.SAMPLE_TOOK

    def handle_compute_calibration(self):
        result = self.handeye_client.compute_calibration()
        if result.valid:
            print("{} Calibration successful".format(rospy.get_namespace()))
        else:
            print("{} Calibration failed".format(rospy.get_namespace()))
                
    def handle_save_calibration(self):
        self.handeye_client.save()
        print("{} Calibration saved".format(rospy.get_namespace()))

    def handle_logic(self):
        if self.state == AutomaticMovements.NOT_INITED_YET:
               self.handle_check_pose()
        while self.samples_taken < 18:
            if self.state == AutomaticMovements.SAMPLE_TOOK:
                self.handle_next_pose()
            if self.state == AutomaticMovements.GOOD_STARTING_POSITION:
                self.handle_plan()
            if self.state == AutomaticMovements.GOOD_PLAN:
                self.handle_execute()
            if self.state == AutomaticMovements.MOVED_TO_POSE:
                rospy.sleep(1.)
                self.handle_take_sample()
        self.handle_compute_calibration()
        self.handle_save_calibration()
