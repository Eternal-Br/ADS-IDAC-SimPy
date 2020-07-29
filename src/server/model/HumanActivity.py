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
# def DeltaLat2DeltaMeter(DeltaLat):
#     """ 
#     将纬度差转换为距离差(单位:米), 0.1纬度取1852m.
#     : DeltaLat: 纬度差,
#     : return DeltaMeter.
#     """
#     DeltaMeter = DeltaLat * 18520
#     return DeltaMeter

# def DeltaLon2DeltaMeter(DeltaLon, CurrentLat):
#     """ 
#     将纬度差转换为距离差(单位:米), 0.1维度取1852m.
#     : DeltaLat: 纬度差,
#     : CurrentLat: 当前实际纬度,
#     : return DeltaMeter.
#     """
#     DeltaMeter = DeltaLon * 111 * np.cos(CurrentLat) * 1000
#     return DeltaMeter


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


def A1(a1, v1, pos1, a2, v2, pos2):
    """
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
    DCPA = 0
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
            tc, a1_temp, v1new
            pass
        else:
            # 避碰成功
            return tc, a1_temp, v1new
    else: 
        return tc, 0, v1new



mtc, ma, mv = A1(10, 9.8, [123, 35], 350, 10.2, [123.1, 35])


