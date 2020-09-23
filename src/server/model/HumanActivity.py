import numpy as np
import random
# import server.model.CPA as CPA
import CPA


""" 
工具包 涉及人的工作内容及概率化的结果
1.(1.0)只有一艘主船决策，两个人员角色，观察者OOW和决策者master
       角色1:OOW——观测及确认风险，确认风险后事件树产生新的节点，将信息传递给决策者
       角色2:master——决策者，根据当前状态判断本船是让路船还是直航船，作出相应决策
2.(2.0)两艘船都有决策，此时加入两船之间的沟通和理解
3.(3.0)按照IDAC模型细化每一个角色的内容
4.(4.0)增加远程驾驶船舶远程控制中心操作员的行为 

-> 当前版本为1.0版
"""


def ProbDeciEngie(ShipStatus):
    """ 
    : ShipStatus : 船舶的状态数据，数据格式如下所示.
    ：return : DeciProb 决策的结果，字典，格式如下给出.
    """
    # 虽然后面又在船的数据中加入了VOImgID 一项，但并不影响到这里的操作
    # ShipStatus = [
    #     {'time': 300, 'VMid': '2003231533468776', 'shipid': '10086', 'lon': 122.32665399999998, 'lat': 31.210672, 'speed': 1, 'heading': 90, 'interval': 100}, 
    #     {'time': 300, 'VMid': '2003231533468776', 'shipid': '10010', 'lon': 122.326654, 'lat': 32.110672, 'speed': 0, 'heading': 270, 'interval': 100}
    #     ]
    # firstly calculate risk value between two ships.
    # secondly if value bigger than some threshold, decision was touched off.
    # thirdly goes into decide function to generate a decition result and return it as a dictionary.
    
    # 测试： 
    # print("ShipStatus: ", ShipStatus)

    pos1 = [ShipStatus[0]['lon'], ShipStatus[0]['lat']]
    heading1 = ShipStatus[0]['heading']
    speed1 = ShipStatus[0]['speed']

    pos2 = [ShipStatus[1]['lon'], ShipStatus[1]['lat']]
    heading2 = ShipStatus[1]['heading']
    speed2 = ShipStatus[1]['speed']

    DeciProb = OOW(pos1, heading1, speed1, pos2, heading2, speed2)
    print(DeciProb)
    return DeciProb


def OOW(pos1, heading1, speed1, pos2, heading2, speed2):
    """
    OOW——观测及确认风险，确认风险后事件树产生新的节点，将信息传递给决策者
    输入：     
        pos1:     本船的位置，格式为 [lon, lat]
        heading1: 本船的航艏向，°
        speed1:   本船的航速，m/s
        pos2:     目标船的位置，格式为 [lon, lat]
        heading2: 目标船的航艏向，°
        speed2:   目标船的航速，m/s
    输出：
        确认风险——产生新的节点，计算方法如下
        否认风险——不产生新的节点，继续前进
    计算过程：
        1.根据输入状态计算DCPA和TCPA
        2.random产生当前OOW的风险阈值(RiskThreshold=[0,1))值越大，对风险的容忍越高，
        3.目前认为DCPA和TCPA在风险认知中占有同等重要的比重，各占0.5，因此当前的风险值采用计算式：
          RiskCurrent=0.5*((Dmax-DCPA)/(Dmax-D0))+0.5*((Tmax-TCPA)/(Tmax-T0))
          其中，D0,T0分别为DCPA和TCPA危险的标准阈值，即认为小于这个值就非常紧急，必须决策了；
               Dmax,Tmax分别为DCPA和TCPA安全的标准阈值，即认为大于这个值就是安全的；
          上式的计算采取简单的线性关系，风险随着DCPA和TCPA的减小而增加
        4.分支概率计算
          计算出当前环境的RiskCurrent和本船的RiskThreshold后，
              
          如果RiskCurrent>RiskThreshold，本船主要认为有风险，本船有报警概率
             报警的概率：  
             PrAlert=(RiskCurrent-RiskThreshold)/RiskThreshold
             (if PrAlert>0.99,PrAlert=0.99)
             不报警的概率：1-PrAlert
          反之，如果RiskCurrent<RiskThreshold，本船认为没有风险，不产生分支

     """

    # 1.计算DCPA和TCPA
    DCPA = CPA.ComputeDCPA(pos1, heading1, speed1, pos2, heading2, speed2)
    TCPA = CPA.ComputeTCPA(pos1, heading1, speed1, pos2, heading2, speed2)
    MET = 0
    FLAG = 0
    if TCPA < 0:
        # 两船已经错过，或者已经碰撞
        # 反馈标志，将使得全局虚拟机结束
        MET = 1

    # 2.random产生当前OOW的风险阈值
    RiskThreshold = 0.5 + 0.5 * random.random() # (0, 1)
    # 3. 计算RiskCurrent
    # D0,T0分别为DCPA和TCPA危险的标准阈值，即认为小于这个值就非常紧急，必须决策了;
    # Dmax,Tmax分别为DCPA和TCPA安全的标准阈值，即认为大于这个值就是安全的;
    # D和T的单位分别为 米 和 秒
    Dmax = 1852
    # Dmax = 1852 
    D0 = 200
    Tmax = 1800
    # T0 = 600
    T0 = 300
    RiskCurrent=0.5*((Dmax-DCPA)/(Dmax-D0))+0.5*((Tmax-TCPA)/(Tmax-T0))
    # print("RiskCurrent: ", RiskCurrent)
    # 4.分支概率计算
    # 先计算 Master决策出的概率
    DeciProb = Master(pos1, heading1, speed1, pos2, heading2, speed2)
    """     
    此时DeciProb的内容和格式为:
    DeciProb = {
        "GoHead": GH,
        "TurnLeft": TL,
        "TurnRight": TR
    } 
    """
    # print("当前风险值：", RiskCurrent, "  风险阈值：", RiskThreshold)
    # print("Current risk value: ", RiskCurrent, "  risk threshold: ", RiskThreshold)

    if RiskCurrent > RiskThreshold:
        PrAlert = (RiskCurrent-RiskThreshold)/(1-RiskThreshold)

        if PrAlert > 0.999999:
            PrAlert = 0.999999
        # PrAlert归一化处理
        # PrAlert = (RiskCurrent-RiskThreshold)/RiskCurrent
        # print("PrAlert: ", PrAlert)
        # Master做出了决策
        FLAG = 1
        DeciProb["FLAG"] = FLAG # 添加一个键值对 标识已经做出决策
        DeciProb["MET"] = MET # 添加一个键值对 标识是否汇遇
        # 船将直行的概率=当前的概率+ Master未决策的概率
        DeciProb["GoHead"] = DeciProb["GoHead"] * PrAlert + 1-PrAlert
        DeciProb["TurnLeft"] = DeciProb["TurnLeft"] * PrAlert
        DeciProb["TurnRight"] = DeciProb["TurnRight"] * PrAlert
    else:
        PrAlert = 0
        # Master没有做出决策，船将直行
        FLAG = 0
        DeciProb["FLAG"] = FLAG
        DeciProb["MET"] = MET
        # DeciProb["GoHead"] = 1
        # DeciProb["TurnLeft"] = 0
        # DeciProb["TurnRight"] = 0
    DeciProb['message'] = {
        'DCPA': DCPA,
        'TCPA': TCPA,
        'PrAlert': PrAlert,
        'RiskCurrent': RiskCurrent,
        'RiskThreshold': RiskThreshold
    }

    return DeciProb


def Master(pos1, heading1, speed1, pos2, heading2, speed2):
    """
    Master——考虑风险和经济性的避碰决策
    输入：     
        pos1:     本船的位置，格式为 [lon, lat]
        heading1: 本船的航艏向，°
        speed1:   本船的航速，m/s
        pos2:     目标船的位置，格式为 [lon, lat]
        heading2: 目标船的航艏向，°
        speed2:   目标船的航速，m/s
    输出：
        决策内容：考虑风险消解和经济性的避碰方案
        创建新的分支

    计算过程：
        1.根据输入状态计算DCPA和TCPA
        2.判断本船为让路船还是直航船
        3.船舶每次决策都以5°为单位，每次转5°
         3.1.直航船的决策：
               左转5°(-5°),概率0.3
               直航，概率0.6
               右转5°(+5°),概率0.1
         3.2.让路船的决策：
               左转5°(-5°),概率0.1
               直航，概率0.3
               右转5°(+5°),概率0.6
     """
    # 将目标船的坐标转换成以本船为坐标原点的坐标系中
    pos2_temp0 = [pos2[0]-pos1[0], pos2[1]-pos1[1]]

    # 将转化后的目标船的坐标通过旋转，进一步转化为本船航向指向y轴正向的坐标系中
    pos2_temp = coord_conv(pos2_temp0[0], pos2_temp0[1], heading1)

    # 将目标船的航向转化为以本船航向为y轴正向的坐标系中
    # heading2_temp = heading2-heading1
    # if heading2_temp < 0:
    #     heading2_temp = heading2_temp+360

    if pos2_temp[0] > 0:    # x>0即目标船在本船坐标系的第一或第四象限，即在本船的右侧，本船为让路船
        # print("我是让路船...")
        TR = 0.6
        GH = 0.3
        TL = 0.1
    else: # 否则本船为直航船
        # 目标在左边，他让路，我直航，我应该直着走或者左转，目标都是尽快从他船头过
        # print("我是直航船...")
        TR = 0.1
        GH = 0.6
        TL = 0.3
    MasterDeciProb = {
        "GoHead": GH,
        "TurnLeft": TL,
        "TurnRight": TR
    }
    return MasterDeciProb


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


def conv(ship1, ship2, theta):
    # 先平移坐标系 再旋转坐标系
    x = ship2.lon - ship1.lon
    y = ship2.lat - ship1.lat
    x_0 = x*np.cos(theta * np.pi / 180)-y*np.sin(theta * np.pi / 180)
    y_0 = x*np.sin(theta * np.pi / 180)+y*np.cos(theta * np.pi / 180)
    # 如果y_0>0, 对方船在1 4象限 我是让路船
    return x_0

def calc_delta_angle(alpha1, alpha2):
    delta = abs(alpha1 - alpha2)
    if delta <= 180:
        return delta
    else:
        return abs(360 - delta)

def HLD(a1, v1, pos1, a2, v2, pos2):
    """
    Human-Like Decition
    : a1: alpha, the course of ship1,
    : v1: the velocity of ship1,
    : pos1: the position of ship1, pos looks like [123.21, 31.32],
    : a2: alpha, the course of ship2,
    : v2: the velocity of ship2,
    : pos2: the position of ship2, pos looks like [123.21, 31.32]
    """
    deltav = 0.05
    v1delta = deltav * v1 # delta v1
    v1new = v1 # new v1

    tc = 0
    deltat = 10

    Dthre = 1852 # DCPA 阈值, 1海里 = 1.852 KM
    # Dthre = 1000 # DCPA 阈值, 1海里 = 1.852 KM
    # DCPA = 0
    DCPA = CPA.ComputeDCPA(pos1, a1, v1, pos2, a2, v2)
    print('Current DCPA: ', DCPA)
    if DCPA < Dthre:
        break_flag_1 = False
        # 让路船先减速, 判断能否有效避碰（DCPA> Dthre）
        for i in range(0, int(0.5/deltav), 1):
            v1new = v1 - i * v1delta
            for j in range(0, int(100/deltat), 1):
                tc = j * deltat
                DCPA = CPA.ComputeDynamicDCPA(pos1, a1, v1, pos2, a2, v2, tc, v1new)
                print('减速中, DCPA, tc: ', DCPA, tc)
                if DCPA > Dthre:
                    break_flag_1 = True
                    break
            if break_flag_1 == True:
                print('减速阶段已成功避碰.')
                break
            v1new = v1 # 回正v1
        
        # 如果充分减速（速度减至0.5*v1）后仍不能有效避碰（DCPA>Dthre），则开始计算右转
        Athre = 45
        deltaa = 5
        if DCPA < Dthre:
            print('预测通过减速无法成功避碰，准备转向...')
            DCPA = 0
            v1new = 0.5 * v1
            tc = 0
            a1_temp = a1
            break_flag_2 = False
            for i in range(0, int(Athre / deltaa), 1):
                a1_temp = a1_temp + i * deltaa
                for j in range(0, int(100/deltat), 1):
                    tc = j * deltat
                    DCPA = CPA.ComputeDynamicDCPA(pos1, a1_temp, v1, pos2, a2, v2, tc, v1new)
                    # DCPA = CPA.JDCPA()
                    print('转向中，DCPA, alpha, tc:', DCPA, a1_temp, tc)
                    if DCPA > Dthre:
                        break_flag_2 = True
                        break
                if break_flag_2 == True:
                    print('转向阶段成功避碰')
                    break
                a1_temp = a1 # 回正a1
            # 判断充分右转后能否避碰
            if DCPA < Dthre:
                # 避碰失败 怎么办
                print('避碰失败.')
                # TODO
                return 0, 0, v1
                # tc, a1_temp, v1new
                pass
            else:
                # 避碰成功
                return tc, a1_temp, v1new
        else: 
            return tc, 0, v1new
    else:
        # DCPA > Dthre
        return 0, 0, v1


def AHLD(my_ship, target_ship):
    """
    Advanced Human-Like Decition
    : my_ship: looks like a ship object, 
    : target_ship: looks like [ship1, ship2, ...]
    target ship is the ship in my ship's radar range
    """
    critical_angle = 22.5
    stand_on_ship = []
    for ship in target_ship:
        # delta_lon = my_ship.lon - ship.lon
        delta_lon = conv(my_ship, ship, my_ship.heading)
        # if delta_lon < 0: # 本船是让路船 目标船是直航船
        if delta_lon > 0: # 本船是让路船 目标船是直航船
            stand_on_ship.append(ship)

    GW1_vc_max = 0
    GW1_tc_max = 0
    GW2_tc_max = 0
    GW2_ac_max = 0
    has_ship = False
    if len(stand_on_ship) > 0: # 有船
        has_ship = True
        # 这里已经更新了 stand_on_ship, 下面判断夹角
        GW1 = [] # 小角度
        GW2 = [] # 大角度
        for ship in stand_on_ship:
            delta = calc_delta_angle(my_ship.heading, ship.heading)
            if delta < critical_angle:
                GW1.append(ship)
            else:
                GW2.append(ship)
        # 到此已经全部的船分组为小角度和大角度两组
        # 下面开始算小角度的
        GW1_vc = []
        GW1_tc = []
        for ship in GW1:
            # 计算本船与其决策结果 减速阶段
            vc, tc = A1(my_ship, ship)
            GW1_vc.append(vc)
            GW1_tc.append(tc)

        if len(GW1_vc) > 0:
            GW1_vc_max = max(GW1_vc)
        if len(GW1_tc) > 0:
            GW1_tc_max = max(GW1_tc)
        # 下面开始算大角度的 
        GW2_tc = []
        GW2_ac = []
        for ship in GW2:
            # 计算本船与其决策结果 转向阶段
            tc2, ac2 = A2(my_ship, ship, GW1_vc_max)
            GW2_tc.append(tc2)
            GW2_ac.append(ac2)

        if len(GW2_tc) > 0:
            GW2_tc_max = max(GW2_tc)
        if len(GW2_ac) > 0:
            GW2_ac_max = max(GW2_ac)
    else: # 无船
        pass
    
    return has_ship, GW1_vc_max, GW2_ac_max, GW2_tc_max

def A1(my_ship, target_ship):
    '''
    : my_ship: an instance of ship class, 
    : target_ship: an instance of ship class.
    '''
    v1, a1, pos1 = my_ship.speed, my_ship.heading, [my_ship.lon, my_ship.lat]
    v2, a2, pos2 = target_ship.speed, target_ship.heading, [target_ship.lon, target_ship.lat]
    deltav = 0.05
    v1delta = deltav * v1 # delta v1
    v1new = v1 # new v1

    tc = 0 # 运行的时间
    deltat = 10
    # TODO 注意 Dthre或许换为经纬度值
    Dthre = 1852 # DCPA 阈值, 1海里 = 1.852 KM
    # Dthre = 1000 # DCPA 阈值, 1海里 = 1.852 KM
    DCPA = CPA.ComputeDCPA(pos1, a1, v1, pos2, a2, v2)
    print('Current DCPA: ', DCPA)
    if DCPA < Dthre:
        JDCPA = 9999
        break_flag_1 = False
        # 让路船先减速, 判断能否有效避碰（DCPA> Dthre）
        for i in range(0, int(0.5/deltav), 1):
            v1new = v1 - i * v1delta
            for j in range(0, int(100/deltat), 1):
                tc = j * deltat
                # DCPA = CPA.ComputeDynamicDCPA(pos1, a1, v1, pos2, a2, v2, tc, v1new)
                tc2, a2new, v2new = 0, target_ship.original_heading, target_ship.original_speed
                if len(target_ship.decision_content) > 0:
                    v2new = target_ship.original_speed - target_ship.decision_content[0]
                    a2new = target_ship.original_heading + target_ship.decision_content[1]
                    tc2 = target_ship.decision_content[2]
                t2new = target_ship.applied_decision_lenth * target_ship.interval
                JDCPA = CPA.JDCPA(
                    target_ship.decision_status,
                    [my_ship.lon, my_ship.lat], my_ship.original_heading, my_ship.original_speed, 
                    [target_ship.lon, target_ship.lat], target_ship.original_heading, target_ship.original_speed, 
                    tc, v1new, my_ship.original_heading, 
                    t2new, tc2, a2new, v2new
                )
                print('减速中, JDCPA, tc: ', JDCPA, tc)
                if JDCPA > Dthre:
                    break_flag_1 = True
                    break
            if break_flag_1 == True:
                print('减速阶段成功避碰GW1.')
                break
        # TODO 这一快还要捋一捋
    vc = v1 - v1new # 速度的该变量
    return vc, tc

def A2(my_ship, target_ship, GW1_vc_max):
    v1, a1, pos1 = my_ship.speed, my_ship.heading, [my_ship.lon, my_ship.lat]
    v2, a2, pos2 = target_ship.speed, target_ship.heading, [target_ship.lon, target_ship.lat]
    v1new = v1 - GW1_vc_max
    a1new = a1
    Athre = 45
    deltaa = 5
    deltat = 10
    Dthre = 500 # TODO 注意是否要米和经纬度转换
    Dthre2 = 800
    DCPA = CPA.ComputeDCPA(pos1, a1, v1, pos2, a2, v2)
    tc = 0 # 转向阶段走的时间
    if DCPA < Dthre:
        # print('预测通过减速无法成功避碰，准备转向...')
        JDCPA = 9999
        break_flag_2 = False
        for i in range(0, int(Athre / deltaa), 1):
            a1new = a1 + i * deltaa # TODO 错了 改了
            for j in range(0, int(100/deltat), 1):
                tc = j * deltat
                tc2, a2new, v2new = 0, target_ship.original_heading, target_ship.original_speed
                if len(target_ship.decision_content) > 0:
                    # print('target ship original speed, target ship decition content[0]', target_ship.original_speed, target_ship.decision_content[0])
                    v2new = target_ship.original_speed - target_ship.decision_content[0]
                    a2new = target_ship.original_heading + target_ship.decision_content[1]
                    tc2 = target_ship.decision_content[2]
                t2new = target_ship.applied_decision_lenth * target_ship.interval
                JDCPA = CPA.JDCPA(
                    target_ship.decision_status,
                    [my_ship.lon, my_ship.lat], my_ship.original_heading, my_ship.original_speed, 
                    [target_ship.lon, target_ship.lat], target_ship.original_heading, target_ship.original_speed, 
                    tc, v1new, a1new, 
                    t2new, tc2, a2new, v2new
                )
                # print('转向中，DCPA, alpha, tc:', JDCPA, a1new, tc)
                if JDCPA > Dthre2:
                    break_flag_2 = True
                    break
            if break_flag_2 == True:
                print('time:{} myship:{} 与target ship:{} 转向阶段成功避碰GW2, JDCPA:{}'.format(my_ship.tick, my_ship.id, target_ship.id, JDCPA))
                break       
        if JDCPA < Dthre2:
            # 避碰失败 怎么办
            print('time:{} myship:{} 与target ship:{} GW2避碰失败, JDCPA:{}.'.format(my_ship.tick, my_ship.id, target_ship.id, JDCPA))
            # TODO
    #         return tc, a1-a1new
    #         # tc, a1new, v1new
    #         pass
    #     else:
    #         # 避碰成功
    #         return tc, a1-a1new
    # else: 
    #     return tc, a1-a1new
    return tc, a1new - a1


# mtc, ma, mv = HLD(10, 9.8, [123, 35], 350, 10.2, [123.1, 35])
# mtc, ma, mv = HLD(10, 9.8, [122.995, 34.995], 350, 10, [123.051, 35.001])
# print(mtc, ma, mv)


