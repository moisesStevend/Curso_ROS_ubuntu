#!/usr/bin/env python

from math import pi

from fake_sensor import FakeSensor

import rospy
import tf
import time

from geometry_msgs.msg import Quaternion
from sensactu.srv import SensorFake,SensorFakeResponse


def make_quaternion(angle):
    q = tf.transformations.quaternion_from_euler(0, 0, angle)
    return Quaternion(*q)

def callback(request):
    global sensor
    angle = sensor.sensor.value() * 2 * pi / 100.0
    q = make_quaternion(angle)
    
    return SensorFakeResponse(q)

        
if __name__ == '__main__':
    global sensor
    sensor = FakeSensor()

    rospy.init_node('fake_sensor')
    service = rospy.Service('angle', SensorFake, callback)
    
    rospy.spin()
