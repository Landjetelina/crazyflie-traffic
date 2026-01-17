from matplotlib import pyplot as plt
from crazyflie_py.crazyswarm_py import Crazyswarm

import csv


if __name__ == "__main__":
    swarm = Crazyswarm()
    timeHelper = swarm.timeHelper
    allcfs = swarm.allcfs

    print(range(1, len(allcfs.crazyfliesById) + 1))
    poses = []
    xs = []
    ys = []
    zs = []
    set_t = False
    t = []
    for n in range(1, len(allcfs.crazyfliesById) + 1):
        xi = []
        yi = []
        zi = []
        with open(f"timed_traj_cf{n}.csv", "r") as f:

            csvFile = csv.reader(f)
            
            skip = True
            for line in csvFile:
                if skip:
                    #print(line)
                    skip = False
                    continue
                
                if not set_t:
                    t.append(float(line[0]))
                xi.append(float(line[1]))
                yi.append(float(line[2]))
                zi.append(float(line[3]))
            set_t = True
        xs.append(xi)
        ys.append(yi)
        zs.append(zi)

    #print(len(t))
    plt.figure()
    plt.title("X koordinate")
    for n in range(0, len(allcfs.crazyfliesById)):
        plt.plot(t, xs[n], label=f"cf_{n+1}")
    
    plt.xlabel("t / s")
    plt.ylabel("x / m")
    plt.legend(loc="best")
    plt.savefig("xs_in_time.png")

    plt.figure()
    plt.title("Y koordinate")
    for n in range(0, len(allcfs.crazyfliesById)):
        plt.plot(t, ys[n], label=f"cf_{n+1}")
    
    plt.xlabel("t / s")
    plt.ylabel("y / m")
    plt.legend(loc="best")
    plt.savefig("ys_in_time.png")

    plt.figure()
    plt.title("Z koordinate")
    for n in range(0, len(allcfs.crazyfliesById)):
        plt.plot(t, zs[n], label=f"cf_{n+1}")
    
    plt.xlabel("t / s")
    plt.ylabel("z / m")
    plt.legend(loc="best")
    plt.savefig("zs_in_time.png")
    
        



                