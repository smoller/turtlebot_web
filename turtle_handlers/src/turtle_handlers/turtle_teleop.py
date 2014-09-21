import rospy

from geometry_msgs.msg import Twist

class TurtleTeleOp(object):

    def __init__(self, topic='cmd_vel_mux/input/navi'):
        rospy.init_node('turtlebot_move', anonymous=True)
        self.pub = rospy.Publisher(topic, Twist, queue_size=1)
        self.twist = Twist()
        self.speed = self.omega = 0

        self._max_speed = 0.4 # m/s
        self._max_omega = 0.3 # rad/s
        self._range = (-1, 1)

    def set_move(self, speed, omega):
        self.speed, self.omega = speed, omega

    def move(self, y, x):
        # receive range in [-1, 1]
        speed = self._clamp(y, *self._range) * self._max_speed
        omega = self._clamp(x, *self._range) * self._max_omega

        self.set_move(speed, omega)
        self.publish()

    def stop(self):
        self.publish(Twist())

    def publish(self):
        self.pub.publish(self.twist)

    def _clamp(self, n, minn, maxn):
        return max(min(maxn, n), minn)
