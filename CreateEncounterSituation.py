# -*- coding: utf-8 -*-
"""
Created on Mon Apr 20 10:04:52 2020

@author: jfzhang
"""
"""
This function is used for creating multi-ship encounter situations that have collision risk
"""
import random
import numpy as np
import matplotlib.pyplot as plt


#random.seed(10) #random seeds

SPEED_MIN = 5  #the minimum value of ship velocity 
SPEED_MAX = 10 #the maximum value of ship velocity
DCPA_THRE = 200 #the threshold of DCPA, m
D_MIN = 5*1852  #the minimum distance between ships in the initial encounter situations


def GenEncounterPoint():#Generate the encounter points of ships
    r = random.uniform(0, DCPA_THRE)
    c = random.uniform(0,360)
    pos_encounter = [r * np.sin(c * np.pi / 180), r * np.cos(c * np.pi / 180)]
    return np.array(pos_encounter)

def CalMinDistance(pos):#Calculate the minimum distance between the ships
    d_min = np.linalg.norm(pos[0]-pos[1])
    for i in range(len(pos)):
        for j in range(i+1, len(pos)):
            d_temp = np.linalg.norm(pos[i]-pos[j])
            if d_min > d_temp:
                d_min = d_temp
    return d_min

def CreateEncounterSituation(n_ships):   
    pos =    [] #The array that stores the positions of the encounter ships
    course = [] #The array that stores the courses of the encounter ships
    speed =  [] #The array that stores the speeds of the encounter ships
     
    for i in range(n_ships):
        pos_temp = GenEncounterPoint()
        course_temp = np.array(random.uniform(0,360))
        speed_temp = np.array(random.uniform(SPEED_MIN,SPEED_MAX))
        pos.append(pos_temp)
        course.append(course_temp)
        speed.append(speed_temp)
    
    t = D_MIN / (max(speed)*2)
    D_temp = random.uniform(1,2)*1852
    #The minimum distance between the ships in the initial stage
    D_min = 0
    while D_min < D_temp:
        t += 10
        for i in range(n_ships):
            pos[i] = np.array([pos[i][0] - t * speed[i] * np.sin(course[i] * np.pi / 180), 
                              pos[i][1] - t * speed[i] * np.cos(course[i] * np.pi/180)])
        D_min = CalMinDistance(pos)

    return pos, course, speed