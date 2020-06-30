# -*- coding: utf-8 -*-
"""
Created on Mon Jun 22 15:28:32 2020

@author: jfzhang
"""
import numpy as np
import math
import CreateEncounterSituation
import matplotlib.pyplot as plt


class Ship(object): 
    def __init__(self, lon, lat, speed, course):
        super().__init__()
        self.lon       = lon       #longitude
        self.lat       = lat       #latitude
        self.speed     = speed     #velocity,m/s
        self.course   = course     #course(°). The north direction is 0, increase in clockwise direction
        
        #destination of the ship, 10 nm from the start point
        self.dest = [self.lon + 10 * 1851* np.sin(self.course * np.pi / 180),
                     self.lat + 10 * 1851* np.cos(self.course * np.pi / 180)]
        self.status = 'None'       #The status of ship, Giveway or Standon
        self.standon = []          #The target ships that own ship should give way to
        self.giveway = []          #The target ships that own ship should stand on
        self.targets = []          #All the target ships
        
        self.RUDDER_MAX = 30       #the maximum rudder angle,30°
        self.K         = 0.0579    #Turning ability parameter
        self.T         = 69.9784   #Rudder gain
        self.delta     = 0.0       #rudder angle, the positive is turning right, negative is turning left
        self.gama_old  = 0.0       #angular velocity at previous moment, degree/second
        self.gama      = 0.0       #angular velocity at present moment, degree/second
           
    def TurnRight(self,):
        if self.delta <= self.RUDDER_MAX - 2:
            self.delta += 2
        
    def TurnLeft(self,):
        if self.delta >= -self.RUDDER_MAX + 2:
            self.delta -= 2
    
    #Compute the DCPA with target ship   
    def ComputeDCPA(self, x_target, y_target, speed, course):
        #x_target, y_target are the longitude and latitude of target ship
        #speed is the velocity of target ship, m/s
        #course is the course of target ship, °

        #speed vector of own ship
        x_1 = self.speed * np.sin(self.course * np.pi /180)
        y_1 = self.speed * np.cos(self.course * np.pi /180)
        
        #speed vector of target ship
        x_2 = speed * np.sin(course * np.pi /180)
        y_2 = speed * np.cos(course * np.pi /180)
        
        #relative speed vector
        x = x_1 - x_2
        y = y_1 - y_2
        
        #relative position between the two ships
        pos_own = np.array([self.lon, self.lat])
        pos_target = np.array([x_target, y_target])        
        pos = pos_target - pos_own
        
        #The projection of relative position on relative speed
        p_x = np.array([y * (y * pos[0] - x * pos[1]) / (x **2 + y ** 2),\
                        -x*(y * pos[0] - x * pos[1]) / (x ** 2 + y ** 2)])

        d = np.linalg.norm(p_x-pos)  #the distance between two positions
        t = 0 
        if x * pos[0]+y * pos[1] > 0: #The two ships are approaching each other
            t = d / (x**2+y**2)**0.5
        pos1=np.array([pos_own[0]+self.speed*np.sin(self.course * np.pi /180) * t,\
                       pos_own[1]+self.speed*np.cos(self.course * np.pi /180) * t])
        pos2=np.array([pos_target[0]+speed*np.sin(course * np.pi /180) * t,\
                       pos_target[1]+speed*np.cos(course * np.pi /180) * t])
        DCPA = np.linalg.norm(pos1-pos2)
        if x*x_2 + y*y_2 > 0:#Own ship is crossing from ahead of target ship
            DCPA = -DCPA
        return DCPA
    
    #Compute the TCPA between two ships. A negative value means that two ships are far away between each other
    def ComputeTCPA(self, x_target, y_target, speed, course):
        #x_target, y_target are the longitude and latitude of target ship
        #speed is the velocity of target ship,m/s
        #course is the course of target ship，°
        
        #speed vector of own ship
        x_1 = self.speed * np.sin(self.course * np.pi /180)
        y_1 = self.speed * np.cos(self.course * np.pi /180)
        
        #speed vector of target ship
        x_2 = speed * np.sin(course * np.pi /180)
        y_2 = speed * np.cos(course * np.pi /180)
        
        #relative speed vector
        x = x_1 - x_2
        y = y_1 - y_2
        
        #relative position between the two ships
        pos_own = np.array([self.lon,self.lat])
        pos_target = np.array([x_target, y_target])        
        pos = pos_target - pos_own
        
        #The projection of relative position on relative speed
        p_x = np.array([y * (y * pos[0] - x * pos[1]) / (x **2 + y ** 2),\
                        -x*(y * pos[0] - x * pos[1]) / (x ** 2 + y ** 2)])

        d = np.linalg.norm(p_x-pos)  #the distance between two positions
        TCPA = 0 #initialize
        if x * pos[0]+y * pos[1] <= 0: #The two ships are moving away from each other, TCPA is negative
            TCPA = -d / (x**2+y**2)**0.5
        else:#The two ships are approaching each other, TCPA is positive
            TCPA = d / (x**2+y**2)**0.5
        return TCPA

    def collision_risk(self, Ship):
        x_target = Ship.lon
        y_target = Ship.lat
        speed = Ship.speed
        course = Ship.course
        DCPA = ComputeDCPA(self, x_target, y_target, speed, course)
        if abs(DCPA)<1000:
            return True
        else:
            return False

    def update(self):
        #update the angulat velocity
        gama_temp = self.gama_old + (self.K * self.delta - self.gama_old) / self.T
        self.gama_old = self.gama
        self.gama = gama_temp
        #update ship course and position
        self.course += self.gama
        self.lon += self.speed * np.sin(self.course * np.pi / 180)
        self.lat += self.speed * np.cos(self.course * np.pi / 180)
    
    #predict the position, course and speed with specific operations
    #turning_angle: the turning angle on the basis of present rudder angle
    #time:forward prediction time，s
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
        return lon_t,lat_t,course_t
    
    #Calculate the reward under different decisions
    def calculate_rewards(self, turning_angle, time, Ship):
        lon_own, lat_own, course_own = self.predict_forward(turning_angle, time)
        #偏离目标点的程度，用角度表示
        vec_course_dest = [self.dest[0] - lon_own, self.dest[1] - lat_own]#本船指向目的地的向量
        vec_course_own = [np.sin(course_own*np.pi/180), np.cos(course_own*np.pi/180)]#本船航向向量
        course_diff = 180/np.pi * math.acos(min(1,((vec_course_dest[0]*vec_course_own[0] + vec_course_dest[1]*
                                             vec_course_own[1])/np.linalg.norm(vec_course_dest))))
        #print(self.course, course_own)
                
        lon_temp, lat_temp, course_temp = Ship.predict_forward(0, time)
        DCPA_temp = ComputeDCPA(lon_own, lat_own, self.speed, course_own, 
                                    lon_temp, lat_temp, Ship.speed, course_temp)#The DCPA after taking operation
        TCPA_temp = self.ComputeTCPA(lon_temp, lat_temp, Ship.speed, course_temp)#The TCPA after taking operation
        if TCPA_temp >0:
            if abs(DCPA_temp) < 1000: #Has collision risk
                r_safe = 0.5 * (DCPA_temp+1000) / 2000
                r_course = 0
                if turning_angle > 0:
                    r_COLREG = 0
                else:
                    r_COLREG = -0.2 #COLREG violation penalty
            else:#No collision risk
                r_safe = 0.5
                r_course = 0.5 * np.exp(-course_diff/25) #偏离航向程度相关奖励
                r_COLREG = 0
        else:
            r_safe = 0.5
            r_course = 0.5 * np.exp(-course_diff/25) #偏离航向程度相关奖励
            r_COLREG = 0
        
        return r_safe + r_course + r_COLREG
    
    #用于确定本船的角色，Standon为直航船，Giveway是让路船
    #输入参数Ship为目标船
    def determine_status(self, Ship):
        self.targets.append(Ship)
        
        lon_temp = self.lon.copy()
        lat_temp = self.lat.copy()
        #平移，使本船位于原点
        lon_temp = Ship.lon - lon_temp
        lat_temp = Ship.lat - lat_temp
        #顺时针旋转self.course
        lon_t = lon_temp*np.cos(self.course * np.pi / 180)-lat_temp*np.sin(self.course * np.pi / 180)
        lat_t = lon_temp*np.sin(self.course * np.pi / 180)+lat_temp*np.cos(self.course * np.pi / 180)
        #v_355 = [-np.sin(5 * np.pi / 180), np.cos(5 * np.pi / 180)]#参考航向
        if lon_t > 0: #目标船位于本船右侧
            if lat_t > 0:  #目标船位于第一象限
                self.standon.append(Ship)
            else:  #目标船位于第四象限
                if math.atan(abs(lat_t/lon_t))*180/np.pi < 22.5: #相对舷角<112.5°
                    self.standon.append(Ship)
                else:
                    self.giveway.append(Ship)
        else:#目标船位于二、三象限
            if lat_t > 0 and math.atan(abs(lat_t/lon_t))*180/np.pi > 85:#对遇状态
                self.standon.append(Ship)
            else:#本船为直航船
                self.giveway.append(Ship)
        if self.standon: #if not null
            self.status = 'Giveway'
        else:
            self.status = 'Standon'
            

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
    if x*x_2 + y*y_2 > 0:#Own ship is crossing from ahead of target ship
        DCPA = -DCPA
    return DCPA


def plot_situation(pos, course, speed):
    fig = plt.figure()
    ax = fig.add_subplot(111)
    for i in range(n_ships):
        ax.plot(pos[i][0],pos[i][1],'.')
       
        ax.arrow(pos[i][0], pos[i][1], speed[i]*np.sin(course[i] * np.pi/180)*50, 
                speed[i]*np.cos(course[i] * np.pi/180)*50,
                 length_includes_head=True,# show arrow head
                 head_width=40, head_length=200, fc='r', ec='b')

#Initialize the encounter ships
n_ships = 4 #number of encounter ships
pos, course, speed = CreateEncounterSituation.CreateEncounterSituation(n_ships)

ship_list = []
for i in range(n_ships):
    ship_temp = Ship(pos[i][0],pos[i][1],speed[i],course[i])
    ship_list.append(ship_temp)
#determine the status of all the ships: Giveway or Standon
for i in range(n_ships):
    for j in range(n_ships):
        if i is not j:
            ship_list[i].determine_status(ship_list[j])

TIME = 1500 #Simulation time
pos_ships = np.zeros((TIME,n_ships,2), dtype = np.float)#record the trajectories of the ships

DCPA = np.arange(TIME*n_ships*n_ships).reshape(TIME, n_ships, n_ships)#The DCPA between pairwise ships at each time point
TCPA = np.arange(TIME*n_ships*n_ships).reshape(TIME, n_ships, n_ships)#The TCPA between pairwise ships at each time point
RUDDER = np.arange(TIME*n_ships).reshape(TIME, n_ships) #The ship rudder angle between pairwise ships at each time point
for time in range(TIME):
    for i in range(n_ships):
        #########################################
        #Collect the data
        pos_ships[time][i][0]=ship_list[i].lon
        pos_ships[time][i][1]=ship_list[i].lat
        RUDDER[time][i] = ship_list[i].delta
        for j in range(i+1, n_ships):
            DCPA[time][i][j] = ship_list[i].ComputeDCPA(ship_list[j].lon, ship_list[j].lat, ship_list[j].speed, ship_list[j].course)
            TCPA[time][i][j] = ship_list[i].ComputeTCPA(ship_list[j].lon, ship_list[j].lat, ship_list[j].speed, ship_list[j].course)
        #########################################
        
        
        if time%10 ==0:# make decision every 10 seconds
            if ship_list[i].status == 'Giveway':
                ## calculate the rewards of turning right, turning left and standon, respectively
                ## Consider all the target ships that the own ship should give way
                r_left = 10
                r_right = 10
                r_head = 10
                for ship in ship_list[i].targets:                    
                    ship_temp = ship
                    if ship_list[i].delta >= -ship_list[i].RUDDER_MAX + 2:#说明还可以继续向左转舵
                        r_left_temp  = ship_list[i].calculate_rewards(-2, 100, ship_temp)
                    else:#不能继续向左转舵
                        r_left_temp = 0
                        
                    if ship_list[i].delta <= ship_list[i].RUDDER_MAX - 2:#说明还可以继续向右转舵
                        r_right_temp = ship_list[i].calculate_rewards(2,100, ship_temp)
                    else:#不能继续向右转舵
                        r_right_temp = 0
                        
                    r_head_temp  = ship_list[i].calculate_rewards(0,100, ship_temp)
                    if r_left > r_left_temp:
                        r_left = r_left_temp
                    if r_right > r_right_temp:
                        r_right = r_right_temp
                    if r_head > r_head_temp:
                        r_head = r_head_temp
                    
                #print('r_right', r_right, 'r_head', r_head, 'r_left', r_left)
                if r_left > r_right and r_left > r_head:
                    ship_list[i].TurnLeft()
                    print('Ship {} at Time: {} turn left'.format(i, time))
                    print(ship_list[i].delta)
                if r_right >= r_left and r_right > r_head:
                    ship_list[i].TurnRight()
                    print('Ship {} at Time: {} turn right'.format(i, time))
                    print(ship_list[i].delta)
        ship_list[i].update()

#print('time: ', np.arange(0, TIME))
fig = plt.figure()
fig.tight_layout()
ax1 = fig.add_subplot(221) #show the trajectories
ax2 = fig.add_subplot(222) #show the DCPA between ships
ax3 = fig.add_subplot(223)
ax4 = fig.add_subplot(224)
for time in range(TIME):
    ax1.cla()   # 清除键
    for i in range(n_ships):
        pos_x = []
        pos_y = []
        for j in range(time):
            pos_x.append(pos_ships[j][i][0])
            pos_y.append(pos_ships[j][i][1])
        ax1.plot(pos_x, pos_y, '-')
    ax1.set_title('T = {} s'.format(time))
    
    ax2.cla()
    time_x = np.arange(0,time)
    for i in range(n_ships):
        for j in range(i+1, n_ships):
            ax2.plot(time_x, DCPA[0:time,i,j], '-')
    ax2.set_xlabel('Time (s)')
    ax2.set_ylabel('DCPA (m)')
    ax2.set_xlim(0,TIME)

    ax3.cla()
    for i in range(n_ships):
        for j in range(i+1, n_ships):
            ax3.plot(time_x, TCPA[0:time,i,j], '-')
    ax3.set_xlabel('Time (s)')
    ax3.set_ylabel('TCPA (s)')
    ax3.set_xlim(0,TIME)
    
    ax4.cla()
    for i in range(n_ships):
        ax4.plot(time_x, RUDDER[0:time,i], '-')  
    ax4.set_xlim(0,TIME)
    ax4.set_xlabel('Time (s)') 
    ax4.set_ylabel('Rudder angle (°)')         
    plt.pause(0.0001)
