#!/usr/bin/env python
import sys
import rospy
import actionlib
from sensactu.msg import RotationAction, RotationGoal, RotationResult, RotationFeedback

rospy.init_node('action_actuator')
client = actionlib.SimpleActionClient('fake/position', RotationAction)
client.wait_for_server()

goal = RotationGoal()
goal.orientation = int(' '.join(sys.argv[1:]))
client.send_goal(goal)
client.wait_for_result()
print('Rotation: %f'%(client.get_result().final_orientation))
