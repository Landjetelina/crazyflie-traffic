#!/usr/bin/env python

from crazyflie_py.crazyswarm_py import Crazyswarm
from crazyflie_py.uav_trajectory import Trajectory
import numpy as np


def move_drones():
    swarm = Crazyswarm()
    timeHelper = swarm.timeHelper
    allcfs = swarm.allcfs

    print(allcfs.crazyfliesById)
    cf1 = allcfs.crazyfliesById[80]
    cf2 = allcfs.crazyfliesById[81]
    cf3 = allcfs.crazyfliesById[82]

    traj1 = Trajectory()
    traj1.loadcsv("./safe_trajectories/poli_traj_cf1.csv")

    traj2 = Trajectory()
    traj2.loadcsv("./safe_trajectories/poli_traj_cf2.csv")

    traj3 = Trajectory()
    traj3.loadcsv("./safe_trajectories/poli_traj_cf3.csv")

    allcfs.setParam('usd.logging', 1)

    #cf.takeoff(1.0, 2.0)
    timeHelper.sleep(2.5)
    cf1.goTo(
    [cf1.position[0],
    cf1.position[1],
    cf1.position[2]],
    0.0, 0.1
)
    cf2.goTo(
    [cf2.position[0],
    cf2.position[1],
    cf2.position[2]],
    0.0, 0.1
)
    cf3.goTo(
    [cf3.position[0],
    cf3.position[1],
    cf3.position[2]],
    0.0, 0.1
    )

    timeHelper.sleep(0.2)

    cf1.uploadTrajectory(0, 0, traj1)
    cf2.uploadTrajectory(0, 0, traj2)
    cf3.uploadTrajectory(0, 0, traj3)
    print("Trajectories uploaded")
    timeHelper.sleep(5.0)
    cf1.startTrajectory(0, timescale=1.0, relative=False)
    cf2.startTrajectory(0, timescale=1.0, relative=False)
    cf3.startTrajectory(0, timescale=1.0, relative=False)


    timeHelper.sleep(20)

    #cf.land(0.05, 2.0)

if __name__ == "__main__":
    move_drones()
