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
        self._grid_width, self._grid_height = data.width, data.height
        self.grid = np.reshape(np.array(data.data, dtype=np.uint8), (data.height, data.width))
