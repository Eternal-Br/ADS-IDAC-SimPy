import numpy as np
import math
# from numpy import cos, pi
import TransBCD
# 工具包 计算本船与目标船的DCPA和TCPA


def ComputeDCPA(pos1, heading1, speed1, pos2, heading2, speed2):
    """     
    : pos1: 自己船的位置，格式为 [lon, lat]
    : heading1: 自己船的航艏向，°
    : speed1: 自己船的航速，m/s
    : pos2: 目标船的位置，格式为 [lon, lat]
    : heading2: 目标船的航艏向，°
    : speed2: 目标船的航速，m/s
    """
    # heading1 = -heading1
    # heading2 = -heading2

    #本船的速度向量
    x_1 = speed1 * np.sin(heading1 * np.pi /180)
    y_1 = speed1 * np.cos(heading1 * np.pi /180)
    
    #目标船的速度向量
    x_2 = speed2 * np.sin(heading2 * np.pi /180)
    y_2 = speed2 * np.cos(heading2 * np.pi /180)
    
    #相对速度向量
    x = x_1 - x_2
    y = y_1 - y_2
    # print("相对速度: ", x, y)
    
    #求两船相对位置坐标
    pos_own = np.array(pos1) # 修改
    pos_target = np.array(pos2)    # 修改    
    pos = pos_target - pos_own
    # print("pos: ", pos[0], pos[1])

    pos[0] = TransBCD.DeltaLon2DeltaMeter(pos[0], pos_own[1])
    pos[1] = TransBCD.DeltaLat2DeltaMeter(pos[1])
    # print("pos: ", pos[0], pos[1])

    #相对距离在相对速度上的投影
    p_x = np.array([y * (y * pos[0] - x * pos[1]) / (x **2 + y ** 2),\
                    -x*(y * pos[0] - x * pos[1]) / (x ** 2 + y ** 2)])

    d = np.linalg.norm(p_x-pos)  #两个坐标的距离
    # print("两个坐标的距离: ", d)
    t = 0 
    # print("x * pos[0] + y * pos[1]: ", x * pos[0] + y * pos[1])
    # if x * pos[0] + y * pos[1] > 0: # 说明两船逐渐靠近
    if x * pos[0] + y * pos[1] > 0: # 说明两条东西向航行的船逐渐靠近
        t = d / (x**2+y**2)**0.5
    # print("t: ", t)

    # 先将待计算的距离转换为坐标差值
    foo1 = TransBCD.DeltaMeter2DeltaLon(speed1*np.sin(heading1 * np.pi /180) * t, pos_own[1])
    foo2 = TransBCD.DeltaMeter2DeltaLat(speed1*np.cos(heading1 * np.pi /180) * t)
    bar1 = TransBCD.DeltaMeter2DeltaLon(speed2*np.sin(heading2 * np.pi /180) * t, pos_target[1])
    bar2 = TransBCD.DeltaMeter2DeltaLat(speed2*np.cos(heading2 * np.pi /180) * t)

    # 带入计算
    pos1=np.array([pos_own[0] + foo1,\
                    pos_own[1] + foo2])
    pos2=np.array([pos_target[0] + bar1,\
                    pos_target[1] + bar2])
    # pos1=np.array([pos_own[0]+speed1*np.sin(heading1 * np.pi /180) * t,\
    #                 pos_own[1]+speed1*np.cos(heading1 * np.pi /180) * t])
    # pos2=np.array([pos_target[0]+speed2*np.sin(heading2 * np.pi /180) * t,\
    #                 pos_target[1]+speed2*np.cos(heading2 * np.pi /180) * t])
    deltapos = pos1-pos2
    # print("转换前deltapos: ", deltapos)
    deltapos[0] = TransBCD.DeltaLon2DeltaMeter(deltapos[0], pos_own[1])
    deltapos[1] = TransBCD.DeltaLat2DeltaMeter(deltapos[1])
    # print("\ndeltapos: ", deltapos)
    DCPA = np.linalg.norm(deltapos)
    # print("DCPA: ", DCPA)
    return DCPA


#计算本船与目标船的TCPA,如果返回值为负数，则说明两条船舶逐渐远离
def ComputeTCPA(pos1, heading1, speed1, pos2, heading2, speed2):
    """     
    : pos1: 自己船的位置，格式为 [lon, lat]
    : heading1: 自己船的航艏向，°
    : speed1: 自己船的航速，m/s
    : pos2: 目标船的位置，格式为 [lon, lat]
    : heading2: 目标船的航艏向，°
    : speed2: 目标船的航速，m/s
     """
    # heading1 = -heading1
    # heading2 = -heading2
    
    #本船的速度向量
    x_1 = speed1 * np.sin(heading1 * np.pi /180)
    y_1 = speed1 * np.cos(heading1 * np.pi /180)
    
    #目标船的速度向量
    x_2 = speed2 * np.sin(heading2 * np.pi /180)
    y_2 = speed2 * np.cos(heading2 * np.pi /180)
    
    #相对速度向量
    x = x_1 - x_2
    y = y_1 - y_2
    # print("相对速度: ", x, y)
    
    #求两船相对位置坐标
    pos_own = np.array(pos1)
    pos_target = np.array(pos2) 
    pos = pos_target - pos_own


    # pos[0] = TransBCD.DeltaLon2DeltaMeter(pos[0], pos_own[0]) # 这里有问题，应该是下面一句
    pos[0] = TransBCD.DeltaLon2DeltaMeter(pos[0], pos_own[1])
    pos[1] = TransBCD.DeltaLat2DeltaMeter(pos[1])

    #相对距离在相对速度上的投影
    p_x = np.array([y * (y * pos[0] - x * pos[1]) / (x **2 + y ** 2),\
                  - x * (y * pos[0] - x * pos[1]) / (x ** 2 + y ** 2)])

    d = np.linalg.norm(p_x-pos)  #两个坐标的距离
    # print("this d: ", d)
    TCPA = 0 #初始化TCPA        
    if x * pos[0]+y * pos[1] <= 0: #说明两船逐渐远离
        TCPA = -d / (x**2+y**2)**0.5
    else:
        TCPA = d / (x**2+y**2)**0.5
    # print("TCPA: ", TCPA)
    return TCPA


def ComputeDynamicDCPA(pos1, heading1, speed1, pos2, heading2, speed2, tc, speed1new):
    """     
    动态DCPA, 先根据传入参数时间参数t，计算t时刻后船舶的状态，再计算当时状态下的DCPA
    : pos1: 自己船的位置，格式为 [lon, lat]
    : heading1: 自己船的航艏向，°
    : speed1: 自己船的航速，m/s
    : pos2: 目标船的位置，格式为 [lon, lat]
    : heading2: 目标船的航艏向，°
    : speed2: 目标船的航速，m/s
    : t: 时间参数, s
    """

    # 20200717 Bruce 修改 动态DCPA

    #本船的原始速度向量
    x_1 = speed1 * np.sin(heading1 * np.pi /180)
    y_1 = speed1 * np.cos(heading1 * np.pi /180)

    #本船的当前速度向量
    x_1_d = speed1new * np.sin(heading1 * np.pi /180)
    y_1_d = speed1new * np.cos(heading1 * np.pi /180)

    #目标船的速度向量
    x_2 = speed2 * np.sin(heading2 * np.pi /180)
    y_2 = speed2 * np.cos(heading2 * np.pi /180)


    # 从这里开始插入，更新t时刻后船的位置，
    # ship1用当前速度，ship2用原始速度
    delta_x_1 = x_1_d * tc
    delta_y_1 = y_1_d * tc
    delta_x_2 = x_2 * tc
    delta_y_2 = y_2 * tc

    # 将距离差值转化为经纬度差值
    temp_x_1 = TransBCD.DeltaMeter2DeltaLon(delta_x_1, pos1[1])
    temp_y_1 = TransBCD.DeltaMeter2DeltaLat(delta_y_1)
    temp_x_2 = TransBCD.DeltaMeter2DeltaLon(delta_x_2, pos2[1])
    temp_y_2 = TransBCD.DeltaMeter2DeltaLat(delta_y_2)

    # 更新位置 经纬度
    pos1 = [pos1[0]+temp_x_1, pos1[1]+temp_y_1]
    pos2 = [pos2[0]+temp_x_2, pos2[1]+temp_y_2]
    # 更新完成
    # 后续操作的 pos1, pos2 就是这里更新之后的


    # 这里开始回到原来写的函数， 后续计算用原始速度

    # 原始速度相对速度向量
    x = x_1 - x_2
    y = y_1 - y_2
    # print("相对速度: ", x, y)
    
    #求两船相对位置坐标
    pos_own = np.array(pos1) # 修改
    pos_target = np.array(pos2)    # 修改    
    pos = pos_target - pos_own
    # print("pos: ", pos[0], pos[1])

    pos[0] = TransBCD.DeltaLon2DeltaMeter(pos[0], pos_own[1])
    pos[1] = TransBCD.DeltaLat2DeltaMeter(pos[1])
    # print("pos: ", pos[0], pos[1])

    #相对距离在相对速度上的投影
    p_x = np.array([y * (y * pos[0] - x * pos[1]) / (x **2 + y ** 2),\
                    -x*(y * pos[0] - x * pos[1]) / (x ** 2 + y ** 2)])

    d = np.linalg.norm(p_x-pos)  #两个坐标的距离
    # print("两个坐标的距离: ", d)
    t = 0 
    # print("x * pos[0] + y * pos[1]: ", x * pos[0] + y * pos[1])
    # if x * pos[0] + y * pos[1] > 0: # 说明两船逐渐靠近
    if x * pos[0] + y * pos[1] > 0: # 说明两条东西向航行的船逐渐靠近
        t = d / (x**2+y**2)**0.5
    # print("t: ", t)

    # 先将待计算的距离转换为坐标差值
    foo1 = TransBCD.DeltaMeter2DeltaLon(speed1*np.sin(heading1 * np.pi /180) * t, pos_own[1])
    foo2 = TransBCD.DeltaMeter2DeltaLat(speed1*np.cos(heading1 * np.pi /180) * t)
    bar1 = TransBCD.DeltaMeter2DeltaLon(speed2*np.sin(heading2 * np.pi /180) * t, pos_target[1])
    bar2 = TransBCD.DeltaMeter2DeltaLat(speed2*np.cos(heading2 * np.pi /180) * t)

    # 带入计算
    pos1=np.array([pos_own[0] + foo1,\
                    pos_own[1] + foo2])
    pos2=np.array([pos_target[0] + bar1,\
                    pos_target[1] + bar2])
    # pos1=np.array([pos_own[0]+speed1*np.sin(heading1 * np.pi /180) * t,\
    #                 pos_own[1]+speed1*np.cos(heading1 * np.pi /180) * t])
    # pos2=np.array([pos_target[0]+speed2*np.sin(heading2 * np.pi /180) * t,\
    #                 pos_target[1]+speed2*np.cos(heading2 * np.pi /180) * t])
    deltapos = pos1-pos2
    # print("转换前deltapos: ", deltapos)
    deltapos[0] = TransBCD.DeltaLon2DeltaMeter(deltapos[0], pos_own[1])
    deltapos[1] = TransBCD.DeltaLat2DeltaMeter(deltapos[1])
    # print("\ndeltapos: ", deltapos)
    DCPA = np.linalg.norm(deltapos)
    # print("DCPA: ", DCPA)
    return DCPA

def JDCPA(target_ship_decision_status, pos1, a1, v1, pos2, a2, v2, tc1, v1new, a1new, t2new, tc2, a2new, v2new):
    def update_position(lon, lat, speed, heading, interval):
        distance = speed * interval # 单位为米
        x_com = distance * math.sin(math.radians(heading))
        y_com = distance * math.cos(math.radians(heading))
        xx = TransBCD.DeltaMeter2DeltaLon(x_com, lat)
        yy = TransBCD.DeltaMeter2DeltaLat(y_com)
        lon += xx
        lat += yy
        return lon, lat
    
    if target_ship_decision_status == False:
        # tc是本船转向后走的时间， v1new是本船在转向阶段的速度 v1是本船原始速度
        D0 = ComputeDynamicDCPA(pos1, a1, v1, pos2, a2, v2, tc1, v1new)
        return D0
    else:
        delta_t2 = tc2 - t2new
        if tc1 > delta_t2:
            # 对方先回正
            D1 = ComputeDCPA(pos1, a1new, v1new, pos2, a2new, v2new)
            pos2new = update_position(pos2[0], pos2[1], v2new, a2new, delta_t2)
            D2 = ComputeDCPA(pos1, a1new, v1new, pos2new, a2, v2)
            pos1new = update_position(pos1[0], pos1[1], v1new, a1new, tc1)
            D3 = ComputeDCPA(pos1new, a1, v1, pos2new, a2, v2)
        else:
            # 本船先回正
            D1 = ComputeDCPA(pos1, a1new, v1new, pos2, a2new, v2new)
            pos1new = update_position(pos1[0], pos1[1], v1new, a1new, tc1)
            D2 = ComputeDCPA(pos1new, a1, v1, pos2, a2new, v2new)
            pos2new = update_position(pos2[0], pos2[1], v2new, a2new, delta_t2)
            D3 = ComputeDCPA(pos1new, a1, v1, pos2new, a2, v2)
        return min(D1, D2, D3)


# @test
# mydcpa = ComputeDCPA([123, 35], 10, 9.8, [123.1, 35], 350, 10.2)
# print('原始MyDCPA: ', mydcpa)
# myddcpa10 = ComputeDynamicDCPA([123, 35], 10, 9.8, [123.1, 35], 350, 10.2, 20, 7)
# print('短时间减速DCPA: ', myddcpa10)
# myddcpa20 = ComputeDynamicDCPA([123, 35], 10, 9.8, [123.1, 35], 350, 10.2, 80, 7)
# print('长时间减速DCPA: ', myddcpa20)
# myddcpa30 = ComputeDynamicDCPA([123, 35], 20, 9.8, [123.1, 35], 350, 10.2, 80, 7)
# print('减速加转向DCPA: ', myddcpa30)
# mytcpa = ComputeTCPA([123, 35.1], 90, 10, [123.1, 35], 270, 7)
# print('MyTCPA: ', mytcpa)


# x = TransBCD.DeltaLon2DeltaMeter(123.31-123.2102, 30.3813)
# y =  TransBCD.DeltaLat2DeltaMeter(30.3813-30.1382)
# d1 = math.sqrt(x**2 +y**2)     
# dcpa = ComputeDCPA([123.2102, 30.1382], 168.4, 10, [123.31, 30.3813], 15.2, 10)
# print('d1: ', d1)
# print('DCPA: ', dcpa)