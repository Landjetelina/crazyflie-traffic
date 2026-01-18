#from crazyflie_interfaces.srv._takeoff import Takeoff
from crazyflie_py.crazyswarm_py import Crazyswarm

import csv


if __name__ == "__main__":
    swarm = Crazyswarm()
    timeHelper = swarm.timeHelper
    allcfs = swarm.allcfs

    allcfs.land(targetHeight=0.05, duration=2.0)
    timeHelper.sleep(2.5)