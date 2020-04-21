# -*- coding: utf-8 -*-
"""
Created on Mon Apr 20 10:04:52 2020

@author: jfzhang
"""
import random
import numpy as np
import matplotlib.pyplot as plt


def ComputeDCPA(x_own, y_own, speed_own, heading_own, x_target, y_target, speed, heading):
    #x, y是目标船的经度坐标和纬度坐标
    #speed是目标船的速度,m/s
    #heading是目标船的航向，°
    # TODO: 将本函数内的self作用变量换成参数变量作用变量
    #本船的速度向量
    x_1 = speed_own * np.sin(heading_own * np.pi /180)
    y_1 = speed_own * np.cos(heading_own * np.pi /180)
    
    #目标船的速度向量
    x_2 = speed * np.sin(heading * np.pi /180)
    y_2 = speed * np.cos(heading * np.pi /180)
    
    #相对速度向量
    x = x_1 - x_2
    y = y_1 - y_2
    
    #求两船相对位置坐标
    pos_own = np.array([x_own, y_own])
    pos_target = np.array([x_target, y_target])        
    pos = pos_target - pos_own
    
    #相对距离在相对速度上的投影
    p_x = np.array([y * (y * pos[0] - x * pos[1]) / (x **2 + y ** 2),\
                    -x*(y * pos[0] - x * pos[1]) / (x ** 2 + y ** 2)])

    d = np.linalg.norm(p_x-pos)  #两个坐标的距离
    t = 0 
    if x * pos[0]+y * pos[1] > 0: #说明两船逐渐靠近
        t = d / (x**2+y**2)**0.5
    pos1=np.array([pos_own[0]+speed_own*np.sin(heading_own * np.pi /180) * t,\
                   pos_own[1]+speed_own*np.cos(heading_own * np.pi /180) * t])
    pos2=np.array([pos_target[0]+speed*np.sin(heading * np.pi /180) * t,\
                   pos_target[1]+speed*np.cos(heading * np.pi /180) * t])
    DCPA = np.linalg.norm(pos1-pos2)
    
    return DCPA
def CreateEncounterSituation():
    SPEED_MIN = 5  #the minimum value of ship velocity
    SPEED_MAX = 10 #the maximum value of ship velocity
    DCPA_THRE = 500 #the threshold of DCPA, m
    D_MIN = 5*1852  #the minimum distance between ships in the initial encounter situations
    
    course1 = random.uniform(0,360)
    speed1 = random.uniform(SPEED_MIN,SPEED_MAX)
    
    course2 = random.uniform(0, 360)
    speed2 = random.uniform(SPEED_MIN,SPEED_MAX)
    
    #the encouner position of two ships
    pos_encounter1 = [0, 0]
    r = random.uniform(0, DCPA_THRE)
    c = random.uniform(0,360)
    pos_encounter2 = [r * np.sin(c * np.pi / 180), r * np.cos(c * np.pi / 180)]
    print('Encounter distance: ',np.linalg.norm(pos_encounter2))
    
    t = D_MIN / (speed1+speed2)
    
    pos1 = np.array([pos_encounter1[0] - t * speed1 * np.sin(course1 * np.pi / 180), 
            pos_encounter1[1] - t * speed1 * np.cos(course1 * np.pi/180)])
    
    pos2 = np.array([pos_encounter2[0] - t * speed2 * np.sin(course2 * np.pi/180), 
           pos_encounter2[1]-t * speed2 * np.cos(course2 * np.pi/180)])
    dist_temp = np.linalg.norm(pos1-pos2)
    D_temp = random.uniform(5,6)*1852
    while dist_temp < D_temp:
        t += 10
        pos1 = np.array([pos_encounter1[0] - t * speed1 * np.sin(course1 * np.pi/180), 
                         pos_encounter1[1] - t * speed1 * np.cos(course1 * np.pi/180)])
    
        pos2 = np.array([pos_encounter2[0] - t * speed2 * np.sin(course2 * np.pi/180), 
                         pos_encounter2[1] - t * speed2 * np.cos(course2 * np.pi/180)])
        dist_temp = np.linalg.norm(pos1-pos2)

    return pos1, course1, speed1, pos2, course2, speed2

def plot_situation():
    pos1, course1, speed1, pos2, course2, speed2 = CreateEncounterSituation()
    print('pos1: ', pos1)
    print('speed1: ', speed1)
    print('course1:', course1)

    print('pos2: ', pos2)
    print('speed2: ', speed2)
    print('course2:', course2)
    DCPA = ComputeDCPA(pos1[0], pos1[1], speed1, course1, pos2[0], pos2[1], speed2, course2)

    print('DCPA: ', DCPA)
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.plot(pos1[0],pos1[1],'o')
    ax.plot(pos2[0],pos2[1],'*')
   
    ax.arrow(pos1[0], pos1[1], speed1*np.sin(course1 * np.pi/180)*50, 
        speed1*np.cos(course1 * np.pi/180)*50,
        length_includes_head=True,# 增加的长度包含箭头部分
        head_width=20, head_length=100, fc='r', ec='b')
    ax.arrow(pos2[0], pos2[1], speed2*np.sin(course2 * np.pi/180)*50, 
            speed2*np.cos(course2 * np.pi/180)*50,
            length_includes_head=True,# 增加的长度包含箭头部分
            head_width=20, head_length=100, fc='r', ec='g')   
    plt.xlim(-12000, 12000)
    plt.ylim(-12000, 12000)
    plt.pause(0)

plot_situation()