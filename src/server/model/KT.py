# import numpy as np
from math import exp
from matplotlib import pyplot as plt


L = 100
B = 30
K_s = 0.45
T_s = 9
v_max = 25*1852/3600

K = K_s*v_max/L
T = T_s*L/v_max

delta_0 = 30 # ship steering angle
r_1 = [0] #angular velocity from the nomoto model
r_2 = [0] #angular velocity from iterative update

course_1 = [0]
course_2 = [0]
t_max = 1000

delta = [30 for _ in range(500)] + [-30 for _ in range(500)]

for t in range(1, t_max):
    r_1.insert(t, K * delta_0 * (1-exp(-(t/T))))
    r_2.insert(t, r_2[t-1] + (K * delta[t] - r_2[t-1]) / T)
    
    course_1.insert(t, course_1[t-1] + r_1[t-1])
    course_2.insert(t, course_2[t-1] + r_2[t-1])
    pass

plt.plot([i for i in range(1000)], r_2, 'r^')
plt.plot([i for i in range(1000)], r_1, 'bo')
plt.grid()
plt.show()


# ----------------测试
self.RUDDER_MAX = 30       #最大操舵角度为30°
self.K         = 0.0579        #船舶旋回性指数
self.T         = 69.9784   #船舶追随性指数
self.delta     = 0.0         #船舶当前时刻的操舵角度,向右为正，向左为负
self.gama_old  = 0.0         #船舶上一时刻角速度
self.gama      = 0.0         #船舶当前时刻角速度


self.K         = 0.0579        #船舶旋回性指数
self.T         = 69.9784   #船舶追随性指数

def update(self):
    #更新船舶角速度
    gama_temp = self.gama_old + (self.K * self.delta - self.gama_old) / self.T
    self.gama_old = self.gama
    self.gama = gama_temp
    #更新船舶航向和位置
    self.course += self.gama
    self.lon += self.speed * np.sin(self.course * np.pi / 180)
    self.lat += self.speed * np.cos(self.course * np.pi / 180)
    

gama_t = gama_old + (self.K * delta_t - gama_old) / self.T
gama_old = gama
gama = gama_t

course_t += gama_old
lon_t += self.speed * np.sin(course_t * np.pi / 180)
lat_t += self.speed * np.cos(course_t * np.pi / 180)
