#!/usr/bin/env python

from pathlib import Path
import time


from crazyflie_py import Crazyswarm
from crazyflie_py.uav_trajectory import Trajectory
import numpy as np
from geometry_msgs.msg import PoseStamped, Pose
import rclpy
from rclpy.node import Node

import csv


T = 15
N = 100


class Pose_Node(Node):
    def __init__(self, i, gx, gy, gz): # dron id i ciljna tocka

        super().__init__('follower_node')
        self.i = i
        self.x = 0
        self.y = 0
        self.z = 0
        self.yaw = 0

        self.gx = gx
        self.gy = gy
        self.gz = gz

        self.done = False

        self.subscription_cf = self.create_subscription(
            PoseStamped, f"cf_{i}/pose", self.cf_callback, 10
        )

    def cf_callback(self, msg):

        print(f"Listening cf_{self.i}.pose")
        self.x = msg.pose.position.x
        self.y = msg.pose.position.y
        self.z = msg.pose.position.z

        print(f"Drone cf_{self.i} initial pose: {self.x} {self.y} {self.z} ")
 
        dx = self.gx - self.x
        dy = self.gy- self.y
        dz = self.gz - self.z

        points = []

        for s in range(N+1):
            step = s/N
            sx = self.x + step*dx
            sy = self.y + step*dy
            sz = self.z + step*dz
            syaw = 0 
            st = T * s/N

            point =f"{st},{sx},{sy},{sz},{syaw}"
            points.append(point)
        
        with open(f"timed_traj_cf{self.i}.csv", "w") as f:
            f.write("t,x,y,z,yaw\n")
            for ps in points:
                f.write(f"{ps}\n")
        
        self.destroy_subscription(self.subscription_cf)
        time.sleep(7)
        rclpy.shutdown()
        print("\nAll trajectories generated!\n")


    
if __name__ == "__main__":
    #rclpy.init()
    swarm = Crazyswarm()
    timeHelper = swarm.timeHelper
    allcfs = swarm.allcfs
    # print(len(allcfs.crazyflies))
    #N = len(allcfs.crazyfliesById)

    # # print("Enter goal points:")
    # # p = input(" cf_1: ").split(" ")
    # # x, y, z, yaw = p[0], p[1], p[2], 0

    # print(f"{x} {y} {z} {yaw}")

    poses = []
    print("Enter goal poses:")
    for n in range(len(allcfs.crazyfliesById)):
        p = input(f" cf_{n+1}: ").split(" ")
        x, y, z = float(p[0]), float(p[1]), float(p[2])
        poses.append([x,y,z])

    nodes = []
    for n in range(len(allcfs.crazyfliesById)):        
        node = Pose_Node(n+1, poses[n][0], poses[n][1], poses[n][2])
        nodes.append(node)

    executor = rclpy.executors.MultiThreadedExecutor()
    for node in nodes:
        executor.add_node(node)
    executor.spin()



    