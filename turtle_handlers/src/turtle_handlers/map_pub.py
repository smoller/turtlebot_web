import rospy
from nav_msgs.msg import OccupancyGrid

if __name__ == '__main__':
    pub = rospy.Publisher('map', OccupancyGrid, queue_size=1)
    rospy.init_node('test_map_pub', anonymous=True)
    r = rospy.Rate(1)
    map_msg = OccupancyGrid()
    map_msg.info.height = map_msg.info.width = 800
    flag = True

    while not rospy.is_shutdown():
        map_msg.data = [0,100,0,100] if flag else [100,0,100,0]
        map_msg.data = map_msg.data * 800 * 200
        pub.publish(map_msg)
        flag = not flag
        r.sleep()
