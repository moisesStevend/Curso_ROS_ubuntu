#!/usr/bin/env python
import rospy
import actionlib
from std_msgs.msg import Float32
from fake_actuator import FakeActuator
from sensactu.srv import Light,LightResponse
from sensactu.msg import RotationAction, RotationFeedback, RotationResult


def volume_callback(msg):
    actuator.actuator.set_volume(min(100, max(0, int(msg.data * 100))))


def light_callback(request):
    actuator.actuator.toggle_light(request.on)
    return LightResponse(actuator.actuator.light_on())


def rotation_callback(goal):
    feedback = RotationFeedback()
    result = RotationResult()

    actuator.actuator.set_position(goal.orientation)
    success = True

    rate = rospy.Rate(10)
    while abs(goal.orientation - actuator.actuator.position()) > 0.01:
        if a.is_preempt_requested():
            success = False
            break

        feedback.current_orientation = actuator.actuator.position()
        a.publish_feedback(feedback)
        rate.sleep()

    result.final_orientation = actuator.actuator.position()
    if success:
        a.set_succeeded(result)
    else:
        a.set_preempted(result)
    

if __name__ == '__main__':
    
    actuator = FakeActuator() 
    rospy.init_node('fake_actuator')

    t = rospy.Subscriber('fake/volume', Float32, volume_callback)

    s = rospy.Service('fake/light', Light, light_callback)

    a = actionlib.SimpleActionServer('fake/position', RotationAction,
                                     execute_cb=rotation_callback,
                                     auto_start=False)
    a.start()
    rospy.spin()

