#!/usr/bin/env python

from crazyflie_py.crazyswarm_py import Crazyswarm
from crazyflie_py.uav_trajectory import Trajectory
import numpy as np

swarm = Crazyswarm()
timeHelper = swarm.timeHelper
allcfs = swarm.allcfs

print(allcfs.crazyfliesById)
cf1 = allcfs.crazyfliesById[80]
cf2 = allcfs.crazyfliesById[81]
cf3 = allcfs.crazyfliesById[82]

traj1 = Trajectory()
traj1.loadcsv("./new_trajectories/poli_traj_cf1.csv")

traj2 = Trajectory()
traj2.loadcsv("./new_trajectories/poli_traj_cf2.csv")

traj3 = Trajectory()
traj3.loadcsv("./new_trajectories/poli_traj_cf3.csv")

allcfs.setParam('usd.logging', 1)

#cf.takeoff(1.0, 2.0)
timeHelper.sleep(2.5)

cf1.uploadTrajectory(0, 0, traj1)
cf2.uploadTrajectory(0, 0, traj2)
cf3.uploadTrajectory(0, 0, traj3)


cf1.startTrajectory(0, timescale=1.0)
cf2.startTrajectory(0, timescale=1.0)
cf3.startTrajectory(0, timescale=1.0)


timeHelper.sleep(20)

#cf.land(0.05, 2.0)
timeHelper.sleep(2.5)
