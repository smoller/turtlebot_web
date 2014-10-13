import sys
import rospy

import cv2
import numpy as np

from nav_msgs.msg import OccupancyGrid

class MapSubscriber:
    """subscribes to a ROS map topic and returns data"""

    def __init__(self, topic='/map', active=True):
        self.topic = topic
        self.cv_image = None
        self.grid = None
        self._grid_height = self._grid_width = 0

        if active: self._activate()
        
    def _activate(self):
        self.map_sub = rospy.Subscriber(self.topic, OccupancyGrid, self._callback, queue_size=1)

    def _deactivate(self):
        self.map_sub = None
        
    def _callback(self, data):
        self._grid_width, self._grid_height = data.info.width, data.info.height
        self.grid = np.reshape(np.array(data.data, dtype=np.uint8), 
            (self._grid_height, self._grid_width))

    def get_map(self):
        return self.grid

    def get_map_cv2(self):
        if self.grid is None: return None
        return np.array([[(el,0,0) for el in row] for row in self.grid], np.uint8) 

    def get_map_image(self, enc='.png'):
        cv_image = self.get_map_cv2()
        return cv2.imencode(enc, cv_image)[1]

if __name__ == '__main__':
    rospy.init_node('test_map_sub')
    sub = MapSubscriber()
    cv2.namedWindow('map')

    r = rospy.Rate(1)
    while not rospy.is_shutdown():
        r.sleep()

        image = sub.get_map_cv2()
        if image is not None:
            cv2.imshow('map', image)
            cv2.waitKey(1)
