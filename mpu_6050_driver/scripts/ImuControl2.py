#!/usr/bin/env python  
import rospy
import tf_conversions
import tf2_ros
import geometry_msgs.msg
from sensor_msgs.msg import Temperature, Imu
from tf.transformations import euler_from_quaternion
from math import *
from std_srvs.srv import *
import numpy as np
from std_msgs.msg import Float32

def rad2deg(rad):
    return rad*180/pi

class ImuControl(object):
    def __init__(self):
        """1. check imu is over threshold"""
        self.sub_imu_data = rospy.Subscriber("/imu/data", Imu, self.define_state)
        self.imu_client = rospy.ServiceProxy("imu_control", Trigger)
        self.pub_gradient = rospy.Publisher("imu_gradient", Float32, queue_size=3)
        self.p = 1000
        self.stableStep = None
        self.upStep = None
        self.downStep = None
        self.signal_box = np.array([False, False, False], dtype=np.bool)
        self.data = Float32()

    def define_state(self, imu):
        quater = np.array([imu.orientation.x, imu.orientation.y, imu.orientation.z, imu.orientation.w])
        (_, p_rad ,_) = euler_from_quaternion(quater)
        self.p = rad2deg(p_rad)
        self.data.data = self.p
        self.pub_gradient.publish(self.data)
        # del t is constant so dont count it

    def main(self):
        is_FirstTime = True # first: going up(True). seceond: going down(False)
        while not rospy.is_shutdown():
            
            if is_FirstTime:
                if abs(self.p) < 5.:
                    rospy.loginfo("its stable")
                    self.stableStep = True
                    self.signal_box[0] = self.stableStep
                    if self.signal_box[1]:
                        self.signal_box[2] = self.stableStep

                elif self.p < -20:
                    rospy.loginfo("upstep")
                    self.upStep = True
                    self.signal_box[1] = True

                if self.signal_box[0] & self.signal_box[1] & self.signal_box[2]:
                    rospy.loginfo("its on the roof")
                    rospy.sleep(2)
                    self.signal_box[0] = self.signal_box[1] = self.signal_box[2] = False
                    is_FirstTime = False
                    res  = self.imu_client()

            else :
                if abs(self.p) < 5.:
                    rospy.loginfo("its stable")
                    self.stableStep = True
                    self.signal_box[0] = self.stableStep
                    if self.signal_box[1]:
                        self.signal_box[2] = self.stableStep

                elif self.p > 20:
                    rospy.loginfo("downstep")
                    self.downStep = True
                    self.signal_box[1] = self.downStep

                if self.signal_box[0] & self.signal_box[1] & self.signal_box[2]:
                    rospy.loginfo("its over.")
                    self.signal_box[0] = self.signal_box[1] = self.signal_box[2] = False
                    rospy.signal_shutdown("shutdown node")
                    res  = self.imu_client()

    def fnShutDown(self):
        rospy.loginfo("shutdown node")
        res = self.imu_client()

if __name__ == '__main__':
    rospy.init_node("imu_control", disable_signals=True)
    imu_control = ImuControl()
    imu_control.main()
