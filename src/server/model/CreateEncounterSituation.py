# -*- coding: utf-8 -*-
"""
Created on Mon Apr 20 10:04:52 2020

@author: jfzhang
"""
import random
import numpy as np
import matplotlib.pyplot as plt
import math

class Ship(object): 
    def __init__(self, lon, lat, speed, course):
        super().__init__()
        self.lon       = lon       #船舶经度坐标
        self.lat       = lat       #船舶纬度坐标
        self.speed     = speed     #船舶速度,m/s
        self.course   = course     #船艏向，°，正北方向为0，顺时针旋转为正
        
        #船舶目标点，距离起点10海里
        self.dest = [self.lon + 10 * 1851* np.sin(self.course * np.pi / 180),
                     self.lat + 10 * 1851* np.cos(self.course * np.pi / 180)]
        self.status = 'None' #船舶角色，让路船或直航船
        self.standon = [] #记录本船是直航船的目标船
        self.giveway = [] #记录本船需要让路的船舶
        self.targets = []#记录所有目标船舶
        
        self.RUDDER_MAX = 30       #最大操舵角度为30°
        self.K         = 0.0579        #船舶旋回性指数
        self.T         = 69.9784   #船舶追随性指数
        self.delta     = 0.0         #船舶当前时刻的操舵角度,向右为正，向左为负
        self.gama_old  = 0.0         #船舶上一时刻角速度
        self.gama      = 0.0         #船舶当前时刻角速度
           
    def TurnRight(self,):
        if self.delta <= self.RUDDER_MAX - 5:
            self.delta += 5
        
    def TurnLeft(self,):
        if self.delta >= -self.RUDDER_MAX + 5:
            self.delta -= 5
    
    #计算本船与目标船的DCPA    
    def ComputeDCPA(self, x_target, y_target, speed, course):
        #x, y是目标船的经度坐标和纬度坐标
        #speed是目标船的速度,m/s
        #course是目标船的航向，°
        # TODO: 将本函数内的self作用变量换成参数变量作用变量
        #本船的速度向量
        x_1 = self.speed * np.sin(self.course * np.pi /180)
        y_1 = self.speed * np.cos(self.course * np.pi /180)
        
        #目标船的速度向量
        x_2 = speed * np.sin(course * np.pi /180)
        y_2 = speed * np.cos(course * np.pi /180)
        
        #相对速度向量
        x = x_1 - x_2
        y = y_1 - y_2
        
        #求两船相对位置坐标
        pos_own = np.array([self.lon,self.lat])
        pos_target = np.array([x_target, y_target])        
        pos = pos_target - pos_own
        
        #相对距离在相对速度上的投影
        p_x = np.array([y * (y * pos[0] - x * pos[1]) / (x **2 + y ** 2),\
                        -x*(y * pos[0] - x * pos[1]) / (x ** 2 + y ** 2)])

        d = np.linalg.norm(p_x-pos)  #两个坐标的距离
        t = 0 
        if x * pos[0]+y * pos[1] > 0: #说明两船逐渐靠近
            t = d / (x**2+y**2)**0.5
        pos1=np.array([pos_own[0]+self.speed*np.sin(self.course * np.pi /180) * t,\
                       pos_own[1]+self.speed*np.cos(self.course * np.pi /180) * t])
        pos2=np.array([pos_target[0]+speed*np.sin(course * np.pi /180) * t,\
                       pos_target[1]+speed*np.cos(course * np.pi /180) * t])
        DCPA = np.linalg.norm(pos1-pos2)
        return DCPA
    
    #计算本船与目标船的TCPA,如果返回值为负数，则说明两条船舶逐渐远离
    def ComputeTCPA(self, x_target, y_target, speed, course):
        #x, y是目标船的经度坐标和纬度坐标
        #speed是目标船的速度,m/s
        #course是目标船的航向，°
        
        #本船的速度向量
        x_1 = self.speed * np.sin(self.course * np.pi /180)
        y_1 = self.speed * np.cos(self.course * np.pi /180)
        
        #目标船的速度向量
        x_2 = speed * np.sin(course * np.pi /180)
        y_2 = speed * np.cos(course * np.pi /180)
        
        #相对速度向量
        x = x_1 - x_2
        y = y_1 - y_2
        
        #求两船相对位置坐标
        pos_own = np.array([self.lon,self.lat])
        pos_target = np.array([x_target, y_target])        
        pos = pos_target - pos_own
        
        #相对距离在相对速度上的投影
        p_x = np.array([y * (y * pos[0] - x * pos[1]) / (x **2 + y ** 2),\
                        -x*(y * pos[0] - x * pos[1]) / (x ** 2 + y ** 2)])

        d = np.linalg.norm(p_x-pos)  #两个坐标的距离
        TCPA = 0 #初始化TCPA        
        if x * pos[0]+y * pos[1] <= 0: #说明两船逐渐远离
            TCPA = -d / (x**2+y**2)**0.5
        else:
            TCPA = d / (x**2+y**2)**0.5
        return TCPA
        
    def update(self):
        #更新船舶角速度
        gama_temp = self.gama_old + (self.K * self.delta - self.gama_old) / self.T
        self.gama_old = self.gama
        self.gama = gama_temp
        #更新船舶航向和位置
        self.course += self.gama
        self.lon += self.speed * np.sin(self.course * np.pi / 180)
        self.lat += self.speed * np.cos(self.course * np.pi / 180)
    
    #predict the position, course and speed with specific operations
    #turning_angle:舵角转向幅度，在原来舵角的基础上转的幅度
    #time:向前预测的时间，s
    def predict_forward(self, turning_angle, time):
        delta_t = self.delta + turning_angle        
        lon_t = self.lon.copy()
        lat_t = self.lat.copy()
        course_t = self.course.copy()
        
        gama_old = self.gama_old
        gama = self.gama
        for _ in range(time):
            gama_t = gama_old + (self.K * delta_t - gama_old) / self.T
            gama_old = gama
            gama = gama_t
            
            course_t += gama_old
            lon_t += self.speed * np.sin(course_t * np.pi / 180)
            lat_t += self.speed * np.cos(course_t * np.pi / 180)
        course_t %= 360.0
#        print('turning angle = ',turning_angle)
#        print('course_t = ', course_t)
#        print('gama = ', self.gama)
#        print('ship course = ', self.course)
        return lon_t,lat_t,course_t
    
    #计算不同操舵决策下的奖励值，选择奖励值最大的作为决策
    def calculate_rewards(self, turning_angle, time, Ship):
        lon_own, lat_own, course_own = self.predict_forward(turning_angle, time)
        course_dest = abs(course_own - self.course)
        r_course = np.exp(-course_dest/20) #偏离航向程度相关奖励
        
        lon_temp, lat_temp, course_temp = Ship.predict_forward(0, time)
        DCPA_temp = ComputeDCPA(lon_own, lat_own, self.speed, course_own, 
                                    lon_temp, lat_temp,Ship.speed, course_temp)
        
        r_safe = 1-np.exp(-DCPA_temp/250 + 1)#安全相关的奖励
        #print('DCPA = ', DCPA_temp,'r_course = ', r_course, 'r_safe = ', r_safe)
        
        return 0.3*r_course + 0.7*r_safe
    
    #用于确定本船的角色，Standon为直航船，Giveway是让路船
    #输入参数Ship为目标船
    def determin_status(self, Ship):
        self.targets.append(Ship)
        
        lon_t = self.lon.copy()
        lat_t = self.lat.copy()
        #平移，使本船位于原点
        lon_t = Ship.lon - lon_t
        lat_t = Ship.lat - lat_t
        #逆时针旋转self.course
        lon_t = lon_t*np.cos(self.course * np.pi / 180)-lat_t*np.sin(self.course * np.pi / 180)
        lat_t = lon_t*np.sin(self.course * np.pi / 180)+lat_t*np.cos(self.course * np.pi / 180)
        
        v_355 = [-np.sin(5 * np.pi / 180), np.cos(5 * np.pi / 180)]#参考航向
        if lon_t * v_355[1] - lat_t * v_355[0] > 0:#目标船逆时针旋转到355°时旋转角度<180°
            theta = math.acos((lon_t * v_355[0] + lat_t * v_355[1]) / np.linalg.norm([lon_t, lat_t]))
            if theta < 117.5 * np.pi / 180: #目标船时针旋转到355°时旋转角度<112.5°+5°，本船为让路船
                self.status = 'Giveway'
                self.standon.append(Ship)
            else:#目标船时针旋转到355°时旋转角度>112.5°+5°，本船为直航船
                self.status = 'Standon'
                self.giveway.append(Ship)
        else:#目标船逆时针旋转到355°时旋转角度>180°,本船为直航船
            self.status = 'Standon'
            self.giveway.append(Ship)       

def ComputeDCPA(x_own, y_own, speed_own, course_own, x_target, y_target, speed, course):
    #x, y是目标船的经度坐标和纬度坐标
    #speed是目标船的速度,m/s
    #course是目标船的航向，°
    # TODO: 将本函数内的self作用变量换成参数变量作用变量
    #本船的速度向量
    x_1 = speed_own * np.sin(course_own * np.pi /180)
    y_1 = speed_own * np.cos(course_own * np.pi /180)
    
    #目标船的速度向量
    x_2 = speed * np.sin(course * np.pi /180)
    y_2 = speed * np.cos(course * np.pi /180)
    
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
    pos1=np.array([pos_own[0]+speed_own*np.sin(course_own * np.pi /180) * t,\
                   pos_own[1]+speed_own*np.cos(course_own * np.pi /180) * t])
    pos2=np.array([pos_target[0]+speed*np.sin(course * np.pi /180) * t,\
                   pos_target[1]+speed*np.cos(course * np.pi /180) * t])
    DCPA = np.linalg.norm(pos1-pos2)
    return DCPA

SPEED_MIN = 5  #the minimum value of ship velocity 
SPEED_MAX = 10 #the maximum value of ship velocity
DCPA_THRE = 500 #the threshold of DCPA, m
D_MIN = 5*1852  #the minimum distance between ships in the initial encounter situations

def coord_conv(x, y, theta):
    # 国际海上避碰规则 COLREGs
    #  坐标系中某一个点(x1,y1)围绕某一点(Xr,Yr)旋转任意角度a后，得到一个新的坐标(x,y)，求(x,y)的通用公式
    #     逆时针旋转的公式为
    #     x=Xr+(x1-Xr)cosa-(y1-Yr)sina
    #     y=Yr+(x1-Xr)sina+(y1-Yr)cosa
    #  顺时针旋转，把a变成-a即可，为：
    #     x=Xr+(x1-Xr)cosa+(y1-Yr)sina
    #     y=Yr-(x1-Xr)sina+(y1-Yr)cosa
    x_0 = x*np.cos(theta * np.pi / 180)-y*np.sin(theta * np.pi / 180)
    y_0 = x*np.sin(theta * np.pi / 180)+y*np.cos(theta * np.pi / 180)
    return [x_0, y_0]

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

# def CreateEncounterSituation(n_ships):   
def Create(n_ships):   
    pos = [] #The array that stores the positions of the encounter ships
    course = []#The array that stores the courses of the encounter ships
    speed = []#The array that stores the speeds of the encounter ships
     
    for i in range(n_ships):
        pos_temp = GenEncounterPoint()
        course_temp = np.array(random.uniform(0,360))
        speed_temp = np.array(random.uniform(SPEED_MIN,SPEED_MAX))
        pos.append(pos_temp)
        course.append(course_temp)
        speed.append(speed_temp)
    # print('maxspeed: ', max(speed)*2)
    t = D_MIN / (max(speed)*2)
    D_temp = random.uniform(5,6)*1852#The minimum distance between the shipss in the initial stage
    D_min = 0
    while D_min < D_temp:
        t += 10
        for i in range(n_ships):
            pos[i] = np.array([pos[i][0] - t * speed[i] * np.sin(course[i] * np.pi / 180), 
                              pos[i][1] - t * speed[i] * np.cos(course[i] * np.pi/180)])
        D_min = CalMinDistance(pos)

    pos = [pos[0].tolist(), pos[1].tolist()]
    course = [course[0].tolist(), course[1].tolist()]
    speed = [speed[0].tolist(), speed[1].tolist()]
    # print(
    #     pos, type(pos), type(pos[0]), '\n', 
    #     course, type(course), '\n', 
    #     speed, type(speed), '\n'
    # )
    return pos, course, speed

# Create(2)
'''
def plot_situation(pos, course, speed):
    fig = plt.figure()
    ax = fig.add_subplot(111)
    for i in range(n_ships):
        ax.plot(pos[i][0],pos[i][1],'.')
       
        ax.arrow(pos[i][0], pos[i][1], speed[i]*np.sin(course[i] * np.pi/180)*50, 
                speed[i]*np.cos(course[i] * np.pi/180)*50,
                 length_includes_head=True,# 增加的长度包含箭头部分
                 head_width=40, head_length=200, fc='r', ec='b')


n_ships = 2
pos, course, speed = CreateEncounterSituation(n_ships)

ship_list = []
for i in range(n_ships):
    ship_temp = Ship(pos[i][0], pos[i][1],speed[i],course[i])
    ship_list.append(ship_temp)
    print(f'pos[{i}]: ', pos[i])

ship_list[0].determin_status(ship_list[1])
ship_list[1].determin_status(ship_list[0])

# 2020年6月4日 21点： 张老师说：
# calculate_rewards(0,200, ship_temp)
# 这个地方改成200，三个地方都改，船舶的转向次数就会减少，没有出现一下左转一下右转的情况了
# 就相当于往前预测200s，之前是往前预测100s

#r_left  = ship_list[0].calculate_rewards(5, 100, ship_list[1])
#print('reward = ',r_left)

pos1 = []
pos2 = []
for time in range(1500):
    for i in range(n_ships):
        if ship_list[i].status == 'Giveway':
            ship_temp = ship_list[i].standon[0]
            #print('Giveway ship is: ',ship_temp)
            r_left  = ship_list[i].calculate_rewards(-5, 100, ship_temp)
            r_right = ship_list[i].calculate_rewards(5,100, ship_temp)
            r_head  = ship_list[i].calculate_rewards(0,100, ship_temp)
            #print(r_left, r_right, r_head)
            if r_left > r_right and r_left > r_head:
                ship_list[i].TurnLeft()
                print('Time: ', time)
                print('Turn left')
            if r_right >= r_left and r_right > r_head:
                ship_list[i].TurnRight()
                print('Time: ', time)
                print('Turn right')
        ship_list[i].update()
        if i == 0:
            pos1.append([ship_list[i].lon, ship_list[i].lat])
        else:
            pos2.append([ship_list[i].lon, ship_list[i].lat])
pos1 = np.array(pos1)
pos2 = np.array(pos2)


fig, ax = plt.subplots()
x1 = []
y1 = []
x2 = []
y2 = []
for i in range(len(pos1)):
    x1.append(pos1[i][0])
    y1.append(pos1[i][1])  # 每迭代一次，将i放入y1中画出来
    x2.append(pos2[i][0])
    y2.append(pos2[i][1])
    ax.cla()   # 清除键
    plt.plot(x1, y1, '-')
    plt.plot(x2, y2, '-')
    plt.pause(0.01)
#fig, ax = plt.subplots()
#plt.plot(pos1[:,0],pos1[:,1],'-')
#plt.plot(pos2[:,0],pos2[:,1],'--')
'''