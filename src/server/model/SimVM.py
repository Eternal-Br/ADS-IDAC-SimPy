#-------------------------------------------------------------------------------
# Name:        SimVM
# Purpose:     实现一个线程安全仿真环境，其中包含多条自主航行船舶、观测者、环境数据
#
# Author:      Youan
# Helper:      Bruce
# Created:     27-01-2020
# Copyright:   (c) Youan 2020
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import sys
sys.path.append(".")
sys.path.append("..")
import math, random, time, copy, uuid, threading
import CPA, TransBCD, DrawVoAreas, opt_db
import HumanActivity as HA
import CreateEncounterSituation

class SimShip:
    # 仿真船舶决策类，实现一步决策
    def __init__(self, SimVMID, ShipID, Tick = 0, Lon = 0.0, Lat = 0.0, Speed = 0.0, Heading = 0.0, TimeRatio = 10):
        # super().__init__(self, SimShipRegistered)
        self.VMid     = SimVMID   # 所属虚拟机
        self.id       = ShipID    #船舶的ID号码
        self.lon      = Lon       #船舶经度坐标
        self.lat      = Lat       #船舶纬度坐标
        self.speed    = Speed     #船舶速度,m/s
        self.heading  = Heading   #船艏向，°，正北方向为 0，顺时针旋转为正
        self.interval = TimeRatio #一次离散步长所对应的时间间隔
        self.tick     = Tick      #当前虚拟时钟
        self.VOImgID = None
        self.DCPA  = -1
        self.TCPA = -1
        pass

    def __RunOneStep(self):
        # time.sleep(0.1)
        # 创建一个以"__"双下划线开始的方法时，这意味着这个方法不能被重写，它只允许在该类的内部中使用

        # 简单计算，详细有待航海学相关内容
        # lon, lat: 起始坐标
        # speed: 航速，待统一转换，初步单位为 m/s
        # heading: 航向角，以正北为基准顺时针度量到航向线的角度
        # distance：本周期内，船舶行走的距离长度，初步单位为米
        # math.radians()将角度转换为弧度
        # 返回值：新的坐标点
        distance = self.speed * self.interval  # 单位为米
        # xx = self.lon + distance * math.sin(math.radians(self.heading))
        # yy = self.lat + distance * math.cos(math.radians(self.heading))

        x_com = distance * math.sin(math.radians(self.heading))
        y_com = distance * math.cos(math.radians(self.heading))
        xx = TransBCD.DeltaMeter2DeltaLon(x_com, self.lat)
        yy = TransBCD.DeltaMeter2DeltaLat(y_com)
        x = self.lon + xx
        y = self.lat + yy

        # heading, speed 不做出改变
        # print(self.lon, self.lat, self.speed, self.heading, distance, xx, yy)
        return x, y

    def __TurnLeft(self):
        # time.sleep(0.1)
        distance = self.speed * self.interval  # 单位为米
        # xx = self.lon + distance * math.sin(math.radians(self.heading - 5))
        # yy = self.lat + distance * math.cos(math.radians(self.heading - 5))

        x_com = distance * math.sin(math.radians(self.heading - 10))
        y_com = distance * math.cos(math.radians(self.heading - 10))
        xx = TransBCD.DeltaMeter2DeltaLon(x_com, self.lat)
        yy = TransBCD.DeltaMeter2DeltaLat(y_com)
        x = self.lon + xx
        y = self.lat + yy
        # TODO: 调用船舶动力学模型计算船舶位置等状态信息
        return x, y
        pass
    
    def __TurnRight(self):
        # time.sleep(0.1)
        distance = self.speed * self.interval  # 单位为米
        # xx = self.lon + distance * math.sin(math.radians(self.heading + 5))
        # yy = self.lat + distance * math.cos(math.radians(self.heading + 5))
        x_com = distance * math.sin(math.radians(self.heading + 10))
        y_com = distance * math.cos(math.radians(self.heading + 10))
        xx = TransBCD.DeltaMeter2DeltaLon(x_com, self.lat)
        yy = TransBCD.DeltaMeter2DeltaLat(y_com)
        x = self.lon + xx
        y = self.lat + yy
        # TODO: 调用船舶动力学模型计算船舶位置等状态信息
        return x, y
        pass


    def DecitionCore(self, func):
        self.lon, self.lat = func()
        self.tick = self.tick + self.interval

    def RunOneDecision(self, RunFlag):
        if self.id == '10086': # 目前只有主船决策
            if RunFlag == 2:
                self.DecitionCore(self.__TurnLeft)
                # print('\nFlag2 This Ship.time: ', self.tick)
                # TODO: 之后是否要修正方向, 当前在转行函数中自动修正
            elif RunFlag == 3:
                self.DecitionCore(self.__TurnRight)
                # TODO: 之后是否要修正方向, 当前在转行函数中自动修正
            else:
                self.DecitionCore(self.__RunOneStep)
        else:
            self.DecitionCore(self.__RunOneStep)
            pass

    def GetShipStatus(self):
        shipStatus = {} # 创建一个空字典
        shipStatus['time'] = self.tick
        shipStatus['VMid'] = self.VMid
        shipStatus['shipid'] = self.id
        shipStatus['lon'] = self.lon
        shipStatus['lat'] = self.lat
        shipStatus['speed'] = self.speed
        shipStatus['heading'] = self.heading
        shipStatus['interval'] = self.interval
        shipStatus['VOImgID'] = self.VOImgID
        shipStatus['DCPA'] = self.DCPA
        shipStatus['TCPA']  = self.TCPA
        return shipStatus

class SimVM:
    # SimShipRegistered = []
    # __Times = 10
    # __GoHead = True
    # __RunFlag = 0 # 测试决策
    # __METFlag = 0 # 标识是否已经相遇，相遇则此虚拟机停止运行
    # __SimData = []
    # __NextStepData = {}


    def __init__(self, id, interval = 0.5, timeratio = 10):
        # 定义虚拟机内船舶清单
        # ShipStatus内存数据表，一台VM带一个
        # 初始化参数 其中的私有变量可以改为公有
        self.id = id # VMID
        self.interval = interval
        self.timeratio = timeratio
        self.SimShipRegistered = []
        self.__Times = 10
        self.__RunFlag = 0 # 测试决策
        self.__METFlag = 0 # 标识是否已经相遇，相遇则此虚拟机停止运行
        self.__SimData = []
        self.__NextStepData = {}
        self.DeciResult = {}
        # 定义和启动VM线程

    def GetNextStepData(self):
        return self.__NextStepData

    def SetShipStatus(self, StatusData):
        """ 
        将ShipStatus 复原 
        """
        StatusData = copy.deepcopy(StatusData)
        i = 0
        for ship in self.SimShipRegistered:
            ship.__init__(
                StatusData[i].get('VMid'),
                StatusData[i].get('shipid'),
                StatusData[i].get('time'),
                StatusData[i].get('lon'),
                StatusData[i].get('lat'),
                StatusData[i].get('speed'),
                StatusData[i].get('heading'),
                StatusData[i].get('interval')
                )
            i += 1
        pass

    def GetMetFlag(self):
        return self.__METFlag

    def GetSimData(self):
        # time.sleep(0.1)
        return self.__SimData

    def addShip(self, ShipID, Tick = 0, Lon = 0.0, Lat = 0.0, Speed = 0.0, Heading = 0.0):
        # 注册船舶
        ship = SimShip(self.id, ShipID, Tick, Lon, Lat, Speed, Heading, self.timeratio)
        self.SimShipRegistered.append(ship)
        # SimShipRegistered.append(ship)

    # def delShip(self, ship):
    #     # 移除注册船舶 By ship object
    #     self.SimShipRegistered.remove(ship)
    #     # SimShipRegistered.remove(ship)

    # def delShip(self, shipid):
    def delShip(self,):
        # 移除注册船舶 By shipid
        for ship in self.SimShipRegistered:
            if ship.VMid == self.id:
                self.SimShipRegistered.remove(ship)
            # if ship.id == shipid:
            #     self.SimShipRegistered.remove(ship)

    def RunOneTime(self, ):
        for ship in self.SimShipRegistered:
            ship.RunOneDecision(self.__RunFlag)
        thisShipStatus = self.GetShipStatus()
        # print("请注意下面进入决策引擎的数据和数量，正常情况列表中应该只有2条数据: ")
        # print(thisShipStatus, '\n')
        DeciResult = HA.ProbDeciEngie(thisShipStatus)
        # print(DeciResult)
        self.__SimData.append(self.GetShipStatus())
        # print("FLAG: ", DeciResult["FLAG"], "\n")
        return DeciResult

    def GetShipStatus(self):
        # time.sleep(0.1)
        foo = []
        for ship in self.SimShipRegistered:
        # for ship in SimShipRegistered:
            # print(ship.GetShipStatus())
            foo.append(ship.GetShipStatus())
        return foo
        pass


    def StoreVOImgDataAndAddID2ShipStatus(self):
        ShipStatus = self.GetShipStatus()
        pos1 = [ShipStatus[0]['lon'], ShipStatus[0]['lat']]
        heading1 = ShipStatus[0]['heading']
        speed1 = ShipStatus[0]['speed']

        pos2 = [ShipStatus[1]['lon'], ShipStatus[1]['lat']]
        heading2 = ShipStatus[1]['heading']
        speed2 = ShipStatus[1]['speed']
        # imgID 由 '11'和36位的uuid拼接而成
        imgID = '11' + str(uuid.uuid5(uuid.NAMESPACE_URL, str(time.time())))
        b64ImgData = DrawVoAreas.GenVOImgB64(pos1, heading1, speed1, pos2, heading2, speed2, imgID)
        # 将 b64压缩编码后的数据存入数据库，一次连接存储一条，有待优化
        # TODO:有待优化数据库操作
        opt_db.insert_into_voimg(imgID, self.id, b64ImgData)
        return imgID


    def RunMultiTime(self):
        self.__GoHead = True
        # self.__RunFlag = True # 测试决策
        while self.__GoHead:
            if self.__Times == 0:
                self.__GoHead = False
            if self.__Times > 0:
                self.__Times = self.__Times - 1
            if self.__GoHead:
                # 调用上面的函数，存储图片数据，返回图片的ID
                imgID = self.StoreVOImgDataAndAddID2ShipStatus()
                # 目前只有主船决策，两艘船的VOImg 图一样，向每一艘船中添加VOImgID
                # 更好的方案应该是...不，不是...>这玩意儿就应该在虚拟机层面操作.

                thisDeciResult = self.RunOneTime() # 更新之后的
                for ship in self.SimShipRegistered:
                    ship.VOImgID = imgID # 向每一艘船中添加VOImgID
                    # 加入DCPA/TCPA的数据回传
                    ship.DCPA = thisDeciResult['message']['DCPA']
                    ship.TCPA = thisDeciResult['message']['TCPA']

                self.DeciResult = copy.deepcopy(thisDeciResult)
                self.__METFlag = thisDeciResult["MET"]
                if self.__METFlag == 1:
                    self.Stop()
                    # print("Attention:船已汇遇，当前虚拟机{}已经停止运行!\n".format(self.id))
                else:
                    self.__RunFlag = thisDeciResult["FLAG"]
                    # self.__RunFlag, DeciProb = self.RunOneTime() # 原来的
                    if thisDeciResult["FLAG"] == 1: 
                        self.Stop()
                        self.NextStep(thisDeciResult)
                    

    def NextStep(self, DeciProb):
        """
        系统决策：给出每个概率对应的下一步结果，经过组装之后以
        目前只有单船决策，即主船决策
        NextStepData = {
            "GoHead": {"prob": prob1, "status": ShipStatus1},
            "TurnLeft": {"prob": prob2, "status": ShipStatus2},
            "TurnRight": {"prob": prob3, "status": ShipStatus3}
        }
        的形式append到 self.__SimData 中,

        传入参数格式：
        DeciProb = {
            "FLAG": FLAG,
            "GoHead": GH,
            "TurnLeft": TL,
            "TurnRight": TR
        }
        其中GH, TL, TR均为概率数值,进入这里的FLAG 均为1，在这里已经没有用
        """
        DeciProb = copy.deepcopy(DeciProb)
        OldShipStatus = copy.deepcopy(self.GetShipStatus()) # ShipStatus
        # print('\nOldShipData: ', OldShipStatus)

        ShipStatus2 = self.RunNextStep(2)
        # TurnLeft = {"probability": DeciProb.get("TurnLeft"), "status": ShipStatus2}
        TurnLeft = {"probability": DeciProb.get("TurnLeft"), "status": OldShipStatus + ShipStatus2}
        # print('\nTurnLeft: ', TurnLeft)
        self.SetShipStatus(OldShipStatus)

        ShipStatus1 = self.RunNextStep(1)
        # GoHead = {"probability": DeciProb["GoHead"], "status": ShipStatus1}
        GoHead = {"probability": DeciProb["GoHead"], "status": OldShipStatus + ShipStatus1}
        # print('Prob: ', DeciProb["GoHead"])
        # print('\nGoHead: ', GoHead)
        self.SetShipStatus(OldShipStatus) # 将shipStatus 复原

        ShipStatus3 = self.RunNextStep(3)
        # TurnRight = {"probability": DeciProb.get("TurnRight"), "status": ShipStatus3}
        TurnRight = {"probability": DeciProb.get("TurnRight"), "status": OldShipStatus + ShipStatus3}
        # print('\nTurnRight: ', TurnRight)
        self.SetShipStatus(OldShipStatus)
        # print('\nAfterTurnRight ShipStatus: ', self.GetShipStatus())

        NextStepData = {
            "TurnLeft": TurnLeft,
            "GoHead": GoHead,
            "TurnRight": TurnRight
        }
        self.__NextStepData = copy.deepcopy(NextStepData)
        pass

    def RunNextStep(self, tempflag):
        """ 
        在功能上与RunOneTime相似，但又与之不同，单独作用一次，独立计算每种情况下的下一步的状态 
        """
        # ship1 = self.SimShipRegistered[0]
        # ship2 = self.SimShipRegistered[1]
        for ship in self.SimShipRegistered:
            ship.RunOneDecision(tempflag)

        SomeShipStatus = self.GetShipStatus()
        # print('\nThis SomeShipStatus: ', SomeShipStatus)
        return SomeShipStatus
        pass

    def Run(self, initStatus4DrawLines, Times = 0):
    # def Run(self, Times = 0):
        if initStatus4DrawLines == 'random':
            #TODO
            pass
        else:
            self.__SimData.append(initStatus4DrawLines) # 先将上一次仿真的结束状态添加到状态列表
        # 调用上面的函数，存储图片数据，返回图片的ID
        iimgID = self.StoreVOImgDataAndAddID2ShipStatus()
        # 目前只有主船决策，两艘船的VOImg 图一样，向每一艘船中添加VOImgID
        # 更好的方案应该是...不，不是...>这玩意儿就应该在虚拟机层面操作.
        for ship in self.SimShipRegistered:
            ship.VOImgID = iimgID # 向每一艘船中添加VOImgID
        self.__SimData.append(self.GetShipStatus()) # 再将当前的起始状态添加到状态列表
        # 启动线程
        self.__Times = Times
        self.__VMThread = threading.Thread(target=self.RunMultiTime(), args=(self,))
        self.__VMThread.start()
        # 这里改为单线程测试
        # self.RunMultiTime()

    def Stop(self):
        self.__GoHead = False
        # self.delShip()
        pass


# 这个函数用于外部调用
def RunVM(initData, initStatus4DrawLines='random', interval = 0.2, timeRatio = 100, runTimes = -1):
# def RunVM(initData, interval = 0.2, timeRatio = 100, runTimes = -1):
    """ 
    : initData: data that init ships in this VM, and initData looks like :
    initData = {
        ship0: {
            ShipID: "10086",
            Tick: 0,
            Lon: 123,
            Lat: 35,
            Speed: 10,
            Heading: 90
        },
        ship1: {ShipID: "10010", Tick: 0, Lon: 123.1, Lat: 35.01, Speed: 7, Heading: 90}
    }
    : interval = 0.2,
    : timeRatio = 100,
    : runTimes = -1 : running times, -1 to loop,
    : return: VMData
    """
    GenVMID = time.strftime("%y%m%d%H%M%S") + str(random.randint(1000, 9999))
    # print("VMID: ", GenVMID)
    VM = SimVM(id = GenVMID, interval = interval, timeratio = timeRatio)

    if initStatus4DrawLines == 'random':
        n_ships = 2
        pos, course, speed = CreateEncounterSituation.Create(n_ships)
        for i in range(n_ships):
            VM.addShip(ShipID='STRI'+'-{}'.format(i), Lon=pos[i][0], Lat=pos[i][1], Speed=speed[i], Heading=course[i])
    else: 
        VM.addShip(
            ShipID = initData["ship0"]["ShipID"], 
            Tick = initData["ship0"]["Tick"],
            Lon = initData["ship0"]["Lon"],
            Lat = initData["ship0"]["Lat"],
            Speed = initData["ship0"]["Speed"],
            Heading = initData["ship0"]["Heading"]
        ) # 主船
        VM.addShip(ShipID = initData["ship1"]["ShipID"], Tick = initData["ship1"]["Tick"], Lon = initData["ship1"]["Lon"], Lat = initData["ship1"]["Lat"], Speed = initData["ship1"]["Speed"], Heading = initData["ship1"]["Heading"]) # 目标船，客船
    
    # VM.addShip(
    #     ShipID = initData["ship0"]["ShipID"], 
    #     Tick = initData["ship0"]["Tick"],
    #     Lon = initData["ship0"]["Lon"],
    #     Lat = initData["ship0"]["Lat"],
    #     Speed = initData["ship0"]["Speed"],
    #     Heading = initData["ship0"]["Heading"]
    # ) # 主船
    # VM.addShip(ShipID = initData["ship1"]["ShipID"], Tick = initData["ship1"]["Tick"], Lon = initData["ship1"]["Lon"], Lat = initData["ship1"]["Lat"], Speed = initData["ship1"]["Speed"], Heading = initData["ship1"]["Heading"]) # 目标船，客船

    VM.Run(initStatus4DrawLines, runTimes)
    # VM.Run(runTimes)
    # VMData = {"VMID": VM.id, "SimData": VM.GetSimData(), "NextStepData": VM.GetNextStepData(), "MET": VM.GetMetFlag()}
    # print('\nVMData: ', VMData)
    # return VMData
    return VM


# 这个函数用于内部测试
def SimTest():
    GenVMID = time.strftime("%y%m%d%H%M%S") + str(random.randint(1000, 9999))
    # print("VMID: ", GenVMID)
    VM = SimVM(id = GenVMID, interval = 0.2, timeratio = 100)
    VM.addShip(ShipID='10086', Lon=123, Lat=35.01, Speed=10, Heading=135) # 主船
    VM.addShip(ShipID='10010', Lon=123.1, Lat=35, Speed=7, Heading=270) # 目标船，客船
    VM.Run(8)
    # VMData = {"VMID": VM.id, "SimData": VM.GetSimData(), "NextStepData": VM.GetNextStepData(), "MET": VM.GetMetFlag()}
    VMData = {"VMID": VM.id, "SimData": VM.GetSimData(), "NextStepData": VM.GetNextStepData(), "MET": VM.GetMetFlag(), 'DeciResult': VM.DeciResult}
    # print('\nVMData: ', VMData)


# 这个函数用于内部测试随机生成初始条件情况下的仿真
def SimTestRandomInit():
    GenVMID = time.strftime("%y%m%d%H%M%S") + str(random.randint(1000, 9999))
    # print("VMID: ", GenVMID)
    VM = SimVM(id = GenVMID, interval = 0.2, timeratio = 100)
    n_ships = 2
    pos, course, speed = CreateEncounterSituation.Create(n_ships)
    # print(
    #     pos, type(pos), type(pos[0]), '\n', 
    #     course, type(course), '\n', 
    #     speed, type(speed), '\n'
    # )
    for i in range(n_ships):
        VM.addShip(ShipID='STRI'+'-{}'.format(i), Lon=pos[i][0], Lat=pos[i][1], Speed=speed[i], Heading=course[i])
    VM.Run(8)
    VMData = {"VMID": VM.id, "SimData": VM.GetSimData(), "NextStepData": VM.GetNextStepData(), "MET": VM.GetMetFlag()}
    # print('\nVMData: ', VMData)


# ShipStatus内存数据表，一台VM带一个
# SimItemRegistered = []
# SimShipRegistered = []

# class SimItem(object):
#     # 仿真实体基础类，实现注册和注销
#     def __init__(self, RegisteredList = SimItemRegistered):
#         __RegisterList = RegisteredList

#     def Register():
#         __RegisterList.append(self)
#         pass

#     def unRegister():
#         __RegisterList.remove(self)
#         pass

#     def RunOneDecision():
#         pass


def main():
    SimTest()
    # SimTestRandomInit()
    pass

if __name__ == '__main__':
    main()
