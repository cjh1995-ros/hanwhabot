현재 사용하는 센서들 list

motor
camera
hc-sr04
imu

필요한 tf list

odom -> base_footprint, 

imu_link
mag_link
joint_state?(모터용)
joint_state_header_frame_id = base_link

# 처음에 연결 안될 경우 대비해서 하는 역할. 연결 되면 필요 없어짐.
void updateTFPrefix(bool isConnected)
{
  sprintf(odom_header_frame_id, "odom"); 
  sprintf(odom_child_frame_id, "base_footprint");  

  sprintf(imu_frame_id, "imu_link");
  sprintf(mag_frame_id, "mag_link");
  sprintf(joint_state_header_frame_id, "base_link");
}
odom_header_frame_id = odom.header.frame_id
odom_child_frame_id = odom.child_frame_id
imu_frame_id = img_msg.header.frame_id
mag_frame_id = mag_msg.header.frame_id
joint_state_header_frame_id = joint_states.header.frame_id


# publishDriveInformation 
void updateTF(geometry_msgs::TransformStamped& odom_tf)
{
  odom_tf.header = odom.header;
  odom_tf.child_frame_id = odom.child_frame_id;
  odom_tf.transform.translation.x = odom.pose.pose.position.x;
  odom_tf.transform.translation.y = odom.pose.pose.position.y;
  odom_tf.transform.translation.z = odom.pose.pose.position.z;
  odom_tf.transform.rotation      = odom.pose.pose.orientation;
}


when publish Drive info, plz use same stamp

strcmp = 두 string 비교해서 같으면 0, 다르면 1 or -1
