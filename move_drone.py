#!/usr/bin/env python

from crazyflie_py.crazyswarm_py import Crazyswarm
from crazyflie_py.uav_trajectory import Trajectory
import numpy as np

swarm = Crazyswarm()
timeHelper = swarm.timeHelper
allcfs = swarm.allcfs

print(allcfs.crazyfliesById)
cf = allcfs.crazyfliesById[1]

traj = Trajectory()
traj.loadcsv("poli_traj_cf1.csv")

allcfs.setParam('usd.logging', 1)

cf.takeoff(1.0, 2.0)
timeHelper.sleep(2.5)

cf.uploadTrajectory(0, 0, traj)
cf.startTrajectory(0, timescale=1.0)

timeHelper.sleep(traj.duration)

cf.land(0.05, 2.0)
timeHelper.sleep(2.5)
