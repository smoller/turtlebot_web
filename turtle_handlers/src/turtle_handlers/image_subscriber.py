import sys
import rospy

import cv2

from std_msgs.msg import String
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError

class ImageSubscriber:
    """subscribes to a ROS image topic and returns data"""

    def __init__(self, topic='/camera/rgb/image_color', active=False):
        self.topic = topic
        self.bridge = CvBridge()
        self.cv_image = None
        if active: self._activate()
        
    def _activate(self):
        self.image_sub = rospy.Subscriber(self.topic, Image, self._callback, queue_size=1)

    def _deactivate(self):
        self.image_sub = None
        
    def _callback(self, data):
        try:
            self.cv_image = self.bridge.imgmsg_to_cv2(data, "bgr8")
        except CvBridgeError as e:
            print e

    def photo(self, enc='.png'):
        """take a single image and return it"""
        try:
            msg = rospy.wait_for_message(self.topic, Image, timeout=10)
        except rospy.exceptions.ROSException:
            return None

        self._callback(msg)

        return cv2.imencode(enc, self.cv_image)[1]
