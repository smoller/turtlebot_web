import rospy
from geometry_msgs.msg import Twist,PoseStamped
from tf.transformations import euler_from_quaternion
import tf
import math

from path_planner import PathPlanner
from obstacle_detector import ObstacleDetector

class TurtleTeleOp(object):

	def __init__(self, topic='cmd_vel_mux/input/navi', scan='scan', pos='slam_out_pose', obstacle_detect=False):
		rospy.init_node('turtlebot_move', anonymous=True)
		
		self.pub = rospy.Publisher(topic, Twist, queue_size=1)
		self.subPos = rospy.Subscriber(pos, PoseStamped, self._callbackPos)
		
		self.obstacleDetector = ObstacleDetector()
		
		self.twist = Twist()
		self.dest = [1024,1024]
		self.path = PathPlanner()
		self.pos = None

		self._max_speed = 0.5 # m/s
		self._max_omega = 0.5 # rad/s
		self._range = (-1, 1)

	def set_move(self, speed, omega):
		self.twist.linear.x, self.twist.angular.z = speed, omega

	def _callbackPos(self, data):
		self.pos = data
		print math.sqrt(math.pow((self.pos.pose.position.y/0.025)+1024-self.dest[1],2)+pow((self.pos.pose.position.x/0.025)+1024-self.dest[0],2))
		
	def move(self, x, y):
		# receive range in [-1, 1]
		speed = self._clamp(y, *self._range) * self._max_speed
		omega = self._clamp(x, *self._range) * self._max_omega

		self.set_move(speed, omega)
		self.publish()

	def _callbackScan(self, data):
		print("scan")
		
	def moveToWaypoint(self, position, waid):
		print("destination",position)
		print("Current", [int(self.pos.pose.position.x/0.025+1024),int(self.pos.pose.position.y/0.025+1024)])
		route = self.path.createPath(self.pos, position)
		print "path created"
		print route
		i=0
		for dest in route:
			self.dest = dest;
			i = i+1
			if i<10: continue
			print("destination",dest)
			print("Current", [int(self.pos.pose.position.x/0.025+1024),int(self.pos.pose.position.y/0.025+1024)])
			i=0
			pos = self.pos.pose.position
			yaw = self._getYaw()
			curPos = [((pos.x/0.025)+1024),((pos.y/0.025)+1024)]
			hip=0
			ac = dest[0]-curPos[0]
			oc = dest[1]-curPos[1]
			yaw = round(yaw,2)
			angle = round(math.atan2(oc, ac),2)

			if angle>yaw or 5>abs(angle-self._getYaw())>3.14 :
				while(abs(angle-self._getYaw())>0.06):
					self.move(2*abs(angle-self._getYaw()), 0)
			else:
				while(abs(angle-self._getYaw())>0.06):
					self.move(-2*abs(angle-self._getYaw()), 0)	
		
			while(20>math.sqrt(math.pow((self.pos.pose.position.y/0.025)+1024-dest[1],2)+pow((self.pos.pose.position.x/0.025)+1024-dest[0],2))>3):
				self.move(0, 0.3)	
			
			#if self.obstacleDetector.is_obstacle() == True :
			#	return False;
		
		print "done"
		return True;
	def stop(self):
		self.publish(Twist())

	def publish(self):
		self.pub.publish(self.twist)

	def _clamp(self, n, minn, maxn):
		return max(min(maxn, n), minn)
		
	def _getYaw(self):
		(roll, pitch, yaw) = euler_from_quaternion([self.pos.pose.orientation.x,self.pos.pose.orientation.y, self.pos.pose.orientation.z, self.pos.pose.orientation.w])
		return yaw
