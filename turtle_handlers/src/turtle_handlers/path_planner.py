from math import sin, cos

import rospy
from sensor_msgs.msg import LaserScan
from nav_msgs.msg import OccupancyGrid
from heapq import heappush, heappop # for priority queue
import math

import numpy as np

class node:
    xPos = 0 
    yPos = 0 
    distance = 0
    priority = 0 
    def __init__(self, xPos, yPos, distance, priority):
        self.xPos = xPos
        self.yPos = yPos
        self.distance = distance
        self.priority = priority
    def __lt__(self, other):
        return self.priority < other.priority
    def updatePriority(self, xDest, yDest):
        self.priority = self.distance + self.estimate(xDest, yDest) * 10 
    def nextMove(self): 
        self.distance += 10
    def estimate(self, xDest, yDest):
        xd = xDest - self.xPos
        yd = yDest - self.yPos
        d = math.sqrt(xd * xd + yd * yd)
        return(d)


class PathPlanner:

	def __init__(self, maps='/map'):
		self.grid = None
		self._grid_height = self._grid_width = 0
		
		self.route = None
		
		self.update = 0
		self.path = None
		self.dest = None;
		self.subMap = rospy.Subscriber(maps, OccupancyGrid, self._callbackMap)

	def _callbackMap(self, data):
		if self.update == 0:
			self._grid_width, self._grid_height = data.info.width, data.info.height
			self.grid = data
		self.update = (self.update+1)%10; 

	def createPath(self, pos, point = [1024,1024]):
		the_map=np.reshape(np.array(self.grid.data, dtype=np.uint8), 
                               (self._grid_height, self._grid_width))
		n=self._grid_width 
		m=self._grid_height 
		
		#possible directions
		dirs=4
		dx = [1, 0, -1, 0]
   		dy = [0, 1, 0, -1]
 		xA=int(pos.pose.position.x/0.025+1024)
 		yA=int(pos.pose.position.y/0.025+1024)
 		xB=point[0]
 		yB=point[1]
		closed_nodes_map = [] # map of closed (tried-out) nodes
		open_nodes_map = [] # map of open (not-yet-tried) nodes
		dir_map = [] # map of dirs
		row = [0] * n
		for i in range(m): # create 2d arrays
		    closed_nodes_map.append(list(row))
		    open_nodes_map.append(list(row))
		    dir_map.append(list(row))

		pq = [[], []] # priority queues of open (not-yet-tried) nodes
		pqi = 0 # priority queue index
		# create the start node and push into list of open nodes
		n0 = node(xA, yA, 0, 0)
		n0.updatePriority(xB, yB)
		heappush(pq[pqi], n0)
		open_nodes_map[yA][xA] = n0.priority # mark it on the open nodes map

		# A* search
		while len(pq[pqi]) > 0:
		    # get the current node w/ the highest priority
		    # from the list of open nodes
		    n1 = pq[pqi][0] # top node
		    n0 = node(n1.xPos, n1.yPos, n1.distance, n1.priority)
		    x = n0.xPos
		    y = n0.yPos
		    heappop(pq[pqi]) # remove the node from the open list
		    open_nodes_map[y][x] = 0
		    closed_nodes_map[y][x] = 1 # mark it on the closed nodes map

		    # quit searching when the goal is reached
		    # if n0.estimate(xB, yB) == 0:
		    if x == xB and y == yB:
		        # generate the path from finish to start
		        # by following the dirs
		        path = []
		        while not (x == xA and y == yA):
		            j = dir_map[y][x]
		            path.append([x,y])
		            x += dx[j]
		            y += dy[j]
		        path.reverse()
		        return path

		    # generate moves (child nodes) in all possible dirs
		    for i in range(dirs):
		        xdx = x + dx[i]
		        ydy = y + dy[i]
		        if not (xdx < 0 or xdx > n-1 or ydy < 0 or ydy > m - 1
		                or the_map[ydy][xdx] == 1 or closed_nodes_map[ydy][xdx] == 1):
		            # generate a child node
		            m0 = node(xdx, ydy, n0.distance, n0.priority)
		            m0.nextMove()
		            m0.updatePriority(xB, yB)
		            # if it is not in the open list then add into that
		            if open_nodes_map[ydy][xdx] == 0:
		                open_nodes_map[ydy][xdx] = m0.priority
		                heappush(pq[pqi], m0)
		                # mark its parent node direction
		                dir_map[ydy][xdx] = (i + dirs / 2) % dirs
		            elif open_nodes_map[ydy][xdx] > m0.priority:
		                # update the priority
		                open_nodes_map[ydy][xdx] = m0.priority
		                # update the parent direction
		                dir_map[ydy][xdx] = (i + dirs / 2) % dirs
		                # replace the node
		                # by emptying one pq to the other one
		                # except the node to be replaced will be ignored
		                # and the new node will be pushed in instead
		                while not (pq[pqi][0].xPos == xdx and pq[pqi][0].yPos == ydy):
		                    heappush(pq[1 - pqi], pq[pqi][0])
		                    heappop(pq[pqi])
		                heappop(pq[pqi]) # remove the target node
		                # empty the larger size priority queue to the smaller one
		                if len(pq[pqi]) > len(pq[1 - pqi]):
		                    pqi = 1 - pqi
		                while len(pq[pqi]) > 0:
		                    heappush(pq[1-pqi], pq[pqi][0])
		                    heappop(pq[pqi])       
		                pqi = 1 - pqi
		                heappush(pq[pqi], m0) # add the better node instead
		return '' # if no route found
