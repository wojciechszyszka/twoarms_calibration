#!/usr/bin/env python

import rospy
import rospkg
from automatic_calibration import AutomaticMovements


def main():
    rospy.init_node('auto_calibration')
    while rospy.get_time() == 0.0:
        pass

    am = AutomaticMovements()
    am.handle_logic()

    rospy.spin()


if __name__ == '__main__':
    main()