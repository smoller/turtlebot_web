import rospy
from geometry_msgs.msg import Twist

from obstacle_detector import ObstacleDetector

class TurtleTeleOp(object):

    def __init__(self, topic='cmd_vel_mux/input/navi', obstacle_detect=True):
        rospy.init_node('turtlebot_move', anonymous=True)
        self.pub = rospy.Publisher(topic, Twist, queue_size=1)
        self.twist = Twist()

        self._max_speed = 0.4 # m/s
        self._max_omega = 0.3 # rad/s
        self._range = (-1, 1)
        self.obstacle_detect = obstacle_detect
        if obstacle_detect: obs_detector = ObstacleDetector()

    def set_move(self, speed, omega):
        self.twist.linear.x, self.twist.angular.z = speed, omega

    def move(self, x, y):
        # receive range in [-1, 1]
        speed = self._clamp(y, *self._range) * self._max_speed
        omega = self._clamp(x, *self._range) * self._max_omega

        # check for obstacles if obstacle detection enabled
        if self.obstacle_detect and self.obs_detector.is_obstacle():
            rospy.loginfo('obstacle detected!')
            if speed > 0:
                # only stop if move is invalid, ie. moving towards obstacle
                speed = omega = 0
                rospy.loginfo('invalid move!')

        self.set_move(speed, omega)
        self.publish()

    def stop(self):
        self.publish(Twist())

    def publish(self):
        self.pub.publish(self.twist)

    def _clamp(self, n, minn, maxn):
        return max(min(maxn, n), minn)
