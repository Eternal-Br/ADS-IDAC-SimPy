"""

Potential Field based path planner

author: Atsushi Sakai (@Atsushi_twi)

Ref:
https://www.cs.cmu.edu/~motionplanning/lecture/Chap4-Potential-Field_howie.pdf

"""

import numpy as np
import matplotlib.pyplot as plt

# Parameters
KP = 30.0  # attractive potential gain 引力势增益
ETA = 0.000007  # repulsive potential gain 斥力势增益
# AREA_WIDTH = 30.0  # potential area width [m] 势场区域宽度
AREA_WIDTH = 0.04  # potential area width [m] 势场区域宽度

show_animation = True


def calc_potential_field(gx, gy, ox, oy, reso, rr):
    """
    计算势场
    : gx: goal x position, 目标位置x坐标,
    : gy: goal y posotion, 目标位置y坐标,
    : ox: obstacle x position list, 障碍物x坐标集合,
    : oy: obstacle y position list, 障碍物y坐标集合,
    : reso: grid_size, 格子的大小
    : rr: robot_radius
    """
    minx = min(ox) - AREA_WIDTH / 2.0
    miny = min(oy) - AREA_WIDTH / 2.0
    maxx = max(ox) + AREA_WIDTH / 2.0
    maxy = max(oy) + AREA_WIDTH / 2.0
    xw = int(round((maxx - minx) / reso))
    yw = int(round((maxy - miny) / reso))

    # calc each potential
    # 初始化每个点的势场
    pmap = [[0.0 for i in range(yw)] for i in range(xw)]

    for ix in range(xw):
        x = ix * reso + minx
        for iy in range(yw):
            y = iy * reso + miny
            # 计算某一点的引力势和斥力势
            ug = calc_attractive_potential(x, y, gx, gy)
            uo = calc_repulsive_potential(x, y, ox, oy, rr)
            # 人工势场等于二者叠加
            uf = ug + uo
            pmap[ix][iy] = uf

    return pmap, minx, miny


def calc_attractive_potential(x, y, gx, gy):
    """
    计算引力势
    : x: current position x,
    : y: current position y,
    : gx: goal position x,
    : gy: goal position y
    """
    # hypot为欧几里得范数，即两点间的欧氏距离
    return 0.5 * KP * np.hypot(x - gx, y - gy)


def calc_repulsive_potential(x, y, ox, oy, rr):
    """
    计算斥力势
    : x: current position x,
    : y: current position y,
    : ox: obstacle x position list, 障碍物x坐标集合,
    : oy: obstacle y position list, 障碍物y坐标集合,
    : rr: robot radius
    """
    # search nearest obstacle 搜索最近的障碍物
    minid = -1
    dmin = float("inf") # 表示正无穷大
    for i in range(len(ox)):
        d = np.hypot(x - ox[i], y - oy[i])
        if dmin >= d:
            dmin = d
            minid = i

    # calc repulsive potential 计算斥力势
    dq = np.hypot(x - ox[minid], y - oy[minid])

    if dq <= rr: 
        if dq <= 0.1:
            dq = 0.1
        print(0.5 * ETA * (1.0 / dq - 1.0 / rr) ** 2)
        return 0.5 * ETA * (0.7 / dq - 1.0 / rr) ** 2
    else:
        return 0.0


def get_motion_model():
    # what is motion model? And what is it used for?
    # dx, dy
    motion = [[1, 0],
              [0, 1],
              [-1, 0],
              [0, -1],
              [-1, -1],
              [-1, 1],
              [1, -1],
              [1, 1]]

    return motion


def potential_field_planning(sx, sy, gx, gy, ox, oy, reso, rr):
    """ 
    : reso: grid_size, 格子的大小
    : rr: robot_radius
    """
    # calc potential field
    # pmap: 势场地图, minx, miny: 左下角坐标
    pmap, minx, miny = calc_potential_field(gx, gy, ox, oy, reso, rr)

    # search path
    d = np.hypot(sx - gx, sy - gy)
    ix = round((sx - minx) / reso)
    iy = round((sy - miny) / reso)
    gix = round((gx - minx) / reso)
    giy = round((gy - miny) / reso)

    if show_animation:
        draw_heatmap(pmap)
        plt.plot(ix, iy, "*k")
        plt.plot(gix, giy, "*m")

    rx, ry = [sx], [sy]
    motion = get_motion_model()
    while d >= reso:
        minp = float("inf")
        minix, miniy = -1, -1
        for i in range(len(motion)):
            inx = int(ix + motion[i][0])
            iny = int(iy + motion[i][1])
            if inx >= len(pmap) or iny >= len(pmap[0]):
                p = float("inf")  # outside area
            else:
                p = pmap[inx][iny]
            if minp > p:
                minp = p
                minix = inx
                miniy = iny
        ix = minix
        iy = miniy
        xp = ix * reso + minx
        yp = iy * reso + miny
        d = np.hypot(gx - xp, gy - yp)
        rx.append(xp)
        ry.append(yp)

        if show_animation:
            plt.plot(ix, iy, ".r")
            plt.pause(0.01)

    print("Goal!!")

    return rx, ry


def draw_heatmap(data):
    data = np.array(data).T
    # plt.pcolor(data, vmax=100.0, cmap=plt.cm.Blues)
    plt.pcolor(data, vmax=1.0, cmap=plt.cm.Blues)


def main():
    print("potential_field_planning start...")

    sx = 0.0  # start x position [m]
    sy = 10.0  # start y positon [m]
    gx = 30.0  # goal x position [m]
    gy = 30.0  # goal y position [m]
    grid_size = 0.5  # potential grid size [m]
    robot_radius = 5.0  # robot radius [m]

    ox = [15.0, 5.0, 20.0, 25.0]  # obstacle x position list [m]
    oy = [25.0, 15.0, 26.0, 25.0]  # obstacle y position list [m]

    if show_animation:
        plt.grid(True)
        plt.axis("equal")

    # path generation
    rx, ry = potential_field_planning(
        sx, sy, gx, gy, ox, oy, grid_size, robot_radius)

    print(rx)
    print(ry)

    if show_animation:
        plt.show()

# 举个栗子🌰
def test():
    print("potential_field_planning start...")

    sx = 0.0  # start x position [m]
    sy = 0.0  # start y positon [m]
    gx = 0.03854167  # goal x position [m]
    gy = 0.03333333  # goal y position [m]
    grid_size = 0.001  # potential grid size [m]
    robot_radius = 0.0025  # robot radius [m]

    ox = [0.01327084, 0.026020]  # obstacle x position list [m]
    oy = [0.01366667, 0.01950]  # obstacle y position list [m]

    if show_animation:
        plt.grid(True)
        plt.axis("equal")

    # path generation
    rx, ry = potential_field_planning(
        sx, sy, gx, gy, ox, oy, grid_size, robot_radius)

    # print(rx)
    # print(ry)

    if show_animation:
        plt.show()


if __name__ == '__main__':
    print(__file__ + " start!!")
    # main()
    test()
    print(__file__ + " Done!!")
