#!/usr/bin/env python  
import rospy
import tf_conversions
import tf2_ros
from tf.transformations import euler_from_quaternion
import geometry_msgs.msg
from sensor_msgs.msg import Temperature, Imu
import numpy as np
from math import pi

MAX_DEG = 90

def rad2deg(r_rad, p_rad, y_rad):
    r_deg = r_rad*180/pi
    p_deg = p_rad*180/pi
    y_deg = y_rad*180/pi
    return r_deg, p_deg, y_deg

def handle_imu_pose(msg):
    br = tf2_ros.TransformBroadcaster()
    t = geometry_msgs.msg.TransformStamped()

    t.header.stamp = rospy.Time.now()
    t.header.frame_id = "plane"
    t.child_frame_id = "imu_link"
    t.transform.translation.x = 0
    t.transform.translation.y = 0
    t.transform.translation.z = 0
    t.transform.rotation.x = msg.orientation.x
    t.transform.rotation.y = msg.orientation.y
    t.transform.rotation.z = msg.orientation.z
    t.transform.rotation.w = msg.orientation.w
    br.sendTransform(t)
    quat = np.array([msg.orientation.x, msg.orientation.y, msg.orientation.z, msg.orientation.w])
    r, p, y = euler_from_quaternion(quat)
    r, p, y = rad2deg(r, p, y)
    rospy.loginfo("r: %f, p: %f, y: %f"%(r, p, y))

if __name__ == '__main__':
      rospy.init_node('tf_broadcaster_imu')
      rospy.Subscriber('/imu/data', Imu, handle_imu_pose)
      rospy.spin()
