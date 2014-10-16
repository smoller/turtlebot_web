#!/usr/bin/env python2

import rospy
from nav_msgs.msg import OccupancyGrid

if __name__ == '__main__':
    pub = rospy.Publisher('map', OccupancyGrid, queue_size=1)
    rospy.init_node('test_map_pub', anonymous=True)
    r = rospy.Rate(1)
    map_msg = OccupancyGrid()
    map_msg.info.height = map_msg.info.width = 800
    flag = True

    map_msg.data = [0] * map_msg.info.height * map_msg.info.width
    while not rospy.is_shutdown():
        data_len = len(map_msg.data)
        if flag: map_msg.data = [100 if i < data_len/2 else 0 for i in xrange(data_len)]
        else:    map_msg.data = [100 if i > data_len/2 else 0 for i in xrange(data_len)]

        pub.publish(map_msg)
        flag = not flag
        r.sleep()
