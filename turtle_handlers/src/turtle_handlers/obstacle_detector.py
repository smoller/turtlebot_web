from math import sin, cos
import rospy

from sensor_msgs.msg import LaserScan

class ObstacleDetector():
    def __init__(self, topic='scan'):
        self.readings = []
        self.detected = False
        self._obs_thd = 0.2
        self._width = 0.5

        rospy.init_node('obstacle_detector', anonymous=True)
        self.sub = rospy.Subscriber(topic, LaserScan, self._callback)

    def _callback(self, data):
        noisy_ranges = data.ranges
        angle_min, angle_increment = data.angle_min, data.angle_increment

        # eliminate bad readings (NaN)
        ranges = [x for x in noisy_ranges if x > 0]
        angles = [angle_min + i*angle_increment for i, j in enumerate(ranges) 
                  if j > 0]

        self.readings = self.polar_to_cartesian(ranges, angles)
        self.detected = any([y < self.thd for x, y in self.readings 
                             if abs(x) < self._width])

    def is_obstacle(self):
        return self.detected

    @staticmethod
    def polar_to_cartesian(ranges, angles):
        return [(r*cos(a), r*sin(a)) for (r, a) in zip(ranges, angles)]

if __name__ == '__main__':
    print(ObstacleDetector.polar_to_cartesian([1, 1, 1], [0, 0.5, 1]))
