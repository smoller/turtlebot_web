import rospy
from geometry_msgs.msg import Twist

from obstacle_detector import ObstacleDetector
from path_planner import PathPlanner

class TurtleTeleOp(object):

    def __init__(self, topic='cmd_vel_mux/input/navi', obstacle_detect=False):
        rospy.init_node('turtlebot_move', anonymous=True)
        self.pub = rospy.Publisher(topic, Twist, queue_size=1)
        self.twist = Twist()
        self.path = PathPlanner()

        self._max_speed = 0.5 # m/s
        self._max_omega = 0.5 # rad/s
        self._range = (-1, 1)

    def set_move(self, speed, omega):
        self.twist.linear.x, self.twist.angular.z = speed, omega

    def move(self, x, y):
        # receive range in [-1, 1]
        speed = self._clamp(y, *self._range) * self._max_speed
        omega = self._clamp(x, *self._range) * self._max_omega

        self.set_move(speed, omega)
        self.publish()

	def moveToWaypoint(position, waid):
		route = path.createPath()
		i=0
		for dest in route:
			print [int(self.pos.pose.position.x/0.05+1024),int(self.pos.pose.position.y/0.05+1024)]
			print dest
			self.dest = dest;
			i = i+1
			if i<5: continue
			i=0
			pos = self.pos.pose.position
			yaw = self._getYaw()
			curPos = [((pos.x/0.05)+1024),((pos.y/0.05)+1024)]
			hip=0
			ac = dest[0]-curPos[0]
			oc = dest[1]-curPos[1]
			yaw = round(yaw,2)
			angle = round(math.atan2(oc, ac),2)
			print "angle"
			print angle * 180 / 3.14
			print "yaw"
			print yaw * 180 / 3.14

			if angle>yaw or abs(angle-self._getYaw())>3.14 :
				while(abs(angle-self._getYaw())>0.04):
					move(2*abs(angle-self._getYaw()), 0)
			else:
				while(abs(angle-self._getYaw())>0.04):
					move(-2*abs(angle-self._getYaw()), 0)	
			
			print "after"
			print yaw
			while(math.sqrt(math.pow((self.pos.pose.position.y/0.05)+1024-dest[1],2)+pow((self.pos.pose.position.x/0.05)+1024-dest[0],2))>2):
				self.mover.move(0, 0.3)	
				
    def stop(self):
        self.publish(Twist())

    def publish(self):
        self.pub.publish(self.twist)

    def _clamp(self, n, minn, maxn):
        return max(min(maxn, n), minn)
