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

def rad2deg(rad):
    return rad*180/pi

class ImuControl(object):
    def __init__(self):
        """1. check imu is over threshold"""
        self.sub_imu_data = rospy.Subscribe("/imu/data", Imu, self.define_state)
        self.speed_client = rospy.ServiceProxy("imu_control", Trigger)
        self.is_FirstTime = True # first: going up(True). seceond: going down(False)
        self.p_current = None
        self.p_last = 0
        self.imu_gradient = None
        self.stable = None
        self.zero_to_max = None
        self.max_to_zero = None
        self.signal_box = np.array([False, False, False, False, False], dtype=np.bool)

    def define_state(self, imu):
        quater = np.array([imu.orientation.x, imu.orientation.y, imu.orientation.z, imu.orientation.w])
        (_, p_rad ,_) = euler_from_quaternion(quater)
        self.p_current = rad2deg(p_rad)

        self.imu_gradient = self.p_current - self.p_last # del t is constant so dont count it
        
        self.p_last = self.p_current

        if self.is_FirstTime:
            if abs(self.imu_gradient) < 1:
                self.stable = True
                self.signal_box[0] = self.stable
                if self.signal_box[1]:
                    self.signal_box[2] = self.stable

                if self.signal_box[3]:
                    self.signal_box[4] = self.stable

            elif self.imu_gradient < 0 :
                self.zero_to_max = True
                self.signal_box[1] = self.zero_to_max

            elif self.imu_gradient > 0 :
                self.max_to_zero = True
                self.signal_box[3] = self.max_to_zero

            if self.signal_box[0] & self.signal_box[1] & self.signal_box[2] & self.signal_box[3] & self.signal_box[4] :
                # make cmd_vel half speed.
                t = Trigger()
                rospy.loginfo("wating for server")
                rospy.wait_for_service("imu_control")
                rospy.loginfo("connected")
                result = self.speed_client(t)
                if result.success == True:
                    self.is_FirstTime = False
                    self.signal_box = np.array([False,False, False, False, False])

                else:
                    pass

        else:
            if abs(self.imu_gradient) < 1:
                self.stable = True
                self.signal_box[0] = self.stable
                if self.signal_box[1]:
                    self.signal_box[2] = self.stable

                if self.signal_box[3]:
                    self.signal_box[4] = self.stable

            elif self.imu_gradient > 0 :
                self.zero_to_max = True
                self.signal_box[1] = self.zero_to_max

            elif self.imu_gradient < 0 :
                self.max_to_zero = True
                self.signal_box[3] = self.max_to_zero

            if self.signal_box[0] & self.signal_box[1] & self.signal_box[2] & self.signal_box[3] & self.signal_box[4] :
                # make cmd_vel zero speed.
                t = Trigger()
                rospy.loginfo("wating for server")
                rospy.wait_for_service("control_cmd_vel")
                rospy.loginfo("connected")
                result = self.speed_client(t)
                if result.success == True:
                    rospy.signal_shutdown("It has all processed. So closing")
                else:
                    pass

    def spin(self):
        rospy.spin()

if __name__ == '__main__':
