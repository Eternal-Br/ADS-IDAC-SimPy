import math
import copy
import TransBCD
import CPA
import time
import random
import HumanActivity as HA

class SimShip:
    def __init__(self, SimVMID, ShipID, SVM, Tick = 0, Lon = 0.0, Lat = 0.0, Speed = 0.0, Heading = 0.0, TimeRatio = 10, ):
        self.VMid     = SVM.id   # 所属虚拟机
        self.id       = ShipID    #船舶的ID号码
        self.lon      = Lon       #船舶经度坐标
        self.lat      = Lat       #船舶纬度坐标
        self.speed    = Speed     #船舶速度,m/s
        self.heading  = Heading   #船艏向，°，正北方向为 0，顺时针旋转为正
        self.interval = TimeRatio #一次离散步长所对应的时间间隔
        self.tick     = Tick      #当前虚拟时钟
        # self.VOImgID = None
        self.DCPA  =  9999
        self.TCPA = 9999
        self.simVM = SVM
        self.original_speed = Speed
        self.original_heading = Heading
        self.radar_range = 0.07 # TODO 注意 米和经纬度
        self.decision_status = False
        self.decision_content = [] # 决策内容 [GW1_vc_max, GW2_ac_max, GW2_tc_max]
        self.instructions_queue = [] # 指令队列
        self.full_decision_length = 0
        self.applied_decision_lenth = 0
        self.collision = False
        self.ship_prob = 1

    def turn_left(self):
        self.heading -= 5
    
    def turn_right(self):
        self.heading += 5
    
    def go_ahead(self):
        distance = self.speed * self.interval # 单位为米
        x_com = distance * math.sin(math.radians(self.heading))
        y_com = distance * math.cos(math.radians(self.heading))
        xx = TransBCD.DeltaMeter2DeltaLon(x_com, self.lat)
        yy = TransBCD.DeltaMeter2DeltaLat(y_com)
        self.lon += xx
        self.lat += yy
        self.tick += self.interval
        print('current time {}, ship {} 已前进，当前位置'.format(self.tick, self.id), self.lon, self.lat)

    def instructions_mapping(self, instruction_code):
        if instruction_code == 1001:
            self.turn_left()
        elif instruction_code == 1002:
            self.turn_right()
        else:
            self.go_ahead()

    def set_original_status(self):
        self.speed = self.original_speed
        self.heading = self.original_heading

    def execute_instruction(self):
        ins = self.instructions_queue
        if len(ins) > 0:
            # 当前还处在执行决策阶段 指令还没执行完毕
            this_ins = ins
            for step in this_ins:
                self.instructions_mapping(step)
            self.instructions_queue = ins[1:] #更新
            self.applied_decision_lenth += 1
            if self.applied_decision_lenth == self.full_decision_length:
                self.set_original_status()
        else:
            self.go_ahead()
        
    def detect_ship_in_radar_range(self):
        ship_in_range = []
        for ship in self.simVM.SimShipRegistered:
            if ship.id == self.id:
                pass
            else:
                dis = math.hypot(self.lon - ship.lon, self.lat - ship.lat)
                if dis < self.radar_range:
                    ship_in_range.append(ship)
                else:
                    pass
        return ship_in_range

    def get_decision_probability(self, DCPA):
        return math.exp(DCPA * 1.05 * (-1) / 1000)

    def get_ship_status(self):
        shipStatus = {} # 创建一个空字典
        shipStatus['time'] = self.tick
        shipStatus['VMid'] = self.VMid
        shipStatus['shipid'] = self.id
        shipStatus['lon'] = self.lon
        shipStatus['lat'] = self.lat
        shipStatus['speed'] = self.speed
        shipStatus['heading'] = self.heading
        shipStatus['interval'] = self.interval
        # shipStatus['VOImgID'] = self.VOImgID
        shipStatus['DCPA'] = self.DCPA
        shipStatus['TCPA']  = self.TCPA
        # shipStatus['simVM'] = self.simVM
        shipStatus['original_speed'] = self.original_speed
        shipStatus['original_heading'] = self.original_heading
        shipStatus['radar_range'] = self.radar_range
        shipStatus['decision_status'] = self.decision_status
        shipStatus['decision_content'] = self.decision_content
        shipStatus['instructions_queue'] = self.instructions_queue
        shipStatus['full_decision_length'] = self.full_decision_length
        shipStatus['applied_decision_lenth'] = self.applied_decision_lenth
        shipStatus['ship_prob'] = self.ship_prob
        return shipStatus


class SimVM:
    def __init__(self, id, interval = 0.5, timeratio = 10):
        # 定义虚拟机内船舶清单
        # ShipStatus内存数据表，一台VM带一个
        # 初始化参数 其中的私有变量可以改为公有
        self.id = id # VMID
        self.interval = interval
        self.timeratio = timeratio
        self.SimShipRegistered = []
        self.Times = 10
        self.RunFlag = 0 # 测试决策
        self.METFlag = 0 # 标识是否已经相遇，相遇则此虚拟机停止运行
        self.SimData = []
        self.NextStepData = {}
        self.DeciResult = {}
        self.count = 0
        self.VM_prob = 1 # 虚拟机分支的概率

    def addShip(self, ShipID, VM, Tick = 0, Lon = 0.0, Lat = 0.0, Speed = 0.0, Heading = 0.0):
        ship = SimShip(self.id, ShipID, self, Tick, Lon, Lat, Speed, Heading, self.timeratio)
        self.SimShipRegistered.append(ship)

    def delShip(self,):
        for ship in self.SimShipRegistered:
            if ship.VMid == self.id:
                self.SimShipRegistered.remove(ship)

    def get_all_ship_status(self):
        foo = []
        for ship in self.SimShipRegistered:
            foo.append(ship.get_ship_status())
        return foo

    def GetSimData(self):
        return self.SimData

    def stop(self):
        self.GoHead = False
        pass

    # def parse_decition(self, ship, decision,a_ship_decision):
    def parse_decition(self, ship):
        # decision looks like: [GW1_vc_max, GW2_ac_max, GW2_tc_max]
        # 注意 只有让路船会决策 故不存在左转的情况
        # 注意 只解析GW2_tc_max 不解析速度和角度的改变 
        # 因为假设速度和角度的改变不消耗时间 应在调用此函数之前或之后一次操作完成
        
        dt = 10
        ins = []
        print('ship id: ', ship.id)
        print('a_ship_decision, 标记:', ship.decision_content)
        GW2_tc_max =  ship.decision_content[2]
        for t in range(int(GW2_tc_max/dt)):
            ins.append(2001)
        return ins

    def pre_gen_branch_data(self, decision):
        # decision = {
        #     'deci_status': [{'id': ship.id, 'status': False}, {}, {}, {}],
        #     'result': [{'id': ship.id, 'result': []}, {}, {}, {}]
        #     'ship_status': [{}, {}, {}, {}]
        # }
        data1 = self.get_all_ship_status() # 保持状态的分支数据
        data2 = [] # 新分支的数据
        data1 = copy.deepcopy(self)
        data2 = copy.deepcopy(self)


        for ship in self.SimShipRegistered:
            temp_ins = []
            bar = copy.deepcopy(ship)
            break_flag = False
            for ds in decision['deci_status']:
                if ds['id'] == bar.id and ds['status'] == True: # 找到‘我’,且我做了新决策
                    # 去找‘我’的决策内容
                    for res in decision['result']:
                        if res['id'] == bar.id:
                            # 读决策结果 解析为指令
                            temp_ins = self.parse_decition(res['result']) 
                            bar.instructions_queue = temp_ins 

                            # 在此改变速度和方向 上面的解析指令中不解析速度和方向
                            bar.speed = bar.speed - res['result'][0] 
                            bar.heading = bar.heading - res['result'][1]
                            
                            break_flag = True
                            data2.append(bar.get_ship_status())
                            break
                if break_flag:
                    break
        # 继续 此处data2已经重新填好数据
        return data1, data2

    # def gen_branch_data(self, decision):
    def gen_branch_data(self, decision):
        # decision = {
        #     'deci_status': [{'id': ship.id, 'status': False}, {}, {}, {}],
        #     'result': [{'id': ship.id, 'result': []}, {}, {}, {}]
        #     'ship_status': [{}, {}, {}, {}]
        # }
        # decision = self.remove_duplicated_decision(decision)
        def GenVMID():
            return time.strftime("%y%m%d%H%M%S") + str(random.randint(1000, 9999))
        VM1 = copy.deepcopy(self)
        VM1.id = GenVMID()
        VM2 = copy.deepcopy(self)
        VM2.id = GenVMID()
        VM1.SimData = []
        VM2.SimData = []
        p = 1
        for ship in VM2.SimShipRegistered:
            p = p * ship.ship_prob
            temp_ins = []
            break_flag = False
            for ds in decision['deci_status']:
                if ds['id'] == ship.id and ds['status'] == True: # 找到‘我’,且我做了新决策
                    ship.decision_status = True # TODO 这里注意了 两船激活这一句
                    # 去找‘我’的决策内容
                    for res in decision['result']:
                        if res['id'] == ship.id:
                            # 读决策结果 解析为指令
                            # temp_ins = self.parse_decition(ship, decision, res['result']) 
                            temp_ins = self.parse_decition(ship) 
                            ship.instructions_queue = temp_ins
                            ship.full_decision_length = len(temp_ins)

                            # 在此改变速度和方向 上面的解析指令中不解析速度和方向
                            print('ship id:{},标记：'.format(ship.id), decision )
                            ship.speed = ship.original_speed - res['result'][0] 
                            ship.heading = ship.original_heading + res['result'][1]

                            break_flag = True
                            break
                if break_flag:
                    break
        VM2.VM_prob = p * self.VM_prob
        VM1.VM_prob = (1-p) * self.VM_prob
        return VM1, VM2

    def pre_remove_duplicated_decision(self, decision):
        # decision = {
        #     'deci_status': [{'id': ship.id, 'status': False}, {}, {}, {}],
        #     'result': [{'id': ship.id, 'result': []}, {}, {}, {}]
        #     'ship_status': [{}, {}, {}, {}]
        # }
        print('remove remove_duplicated_decision,decision: ', decision)
        if len(decision['result']) > 4:
            deci_status = decision['deci_status']  
            result = decision['result']
            foo_id = []
            foo = []
            deplicated_id = 0
            for ds in deci_status:
                id = ds['id']
                # status = ds['status']
                if id not in foo_id:
                    foo_id.append(id)
                    foo.append(ds)
                else:
                    deplicated_id = id
                    for item in foo:
                        if item['id'] == deplicated_id:
                            item['status'] = True
            bar = []  
            d = []  
            for res in result:
                res_id = res['id']
                res_result = res['result']
                if res_id == deplicated_id:
                    d.append(res)
                else:
                    bar.append(res)
            d0 = d[0]
            d1 = d[1]
            if len(d[0]['result']) > len(d[1]['result']):
                bar.append(d0)
            else:
                bar.append(d1)
                # if len(d1['result']) == 0:
                #     for item in foo:
                #         if item['id'] == deplicated_id:
                #             item['status'] = False
            decision['deci_status'] = foo
            decision['result'] = bar
        else:
            pass
        return decision

    def new_remove_duplicated_decision(self, temp_deci_status, temp_result):
        # temp_deci_status = [{'id': ship.id, 'status': True}, {'id': ship.id, 'status': False}, {'id': ship.id, 'status': True},...]
        # temp_result = [{'id': ship.id, 'result': [0, 40, 50]}, {'id': ship.id, 'result': []}, {'id': ship.id, 'result': [10, 50, 40]}, ...]
        # 注：这些id一定是相同的 是当前船的id
        print('new标记：temp_d, remp_r:', temp_deci_status, temp_result)
        if len(temp_deci_status) == 0 or len(temp_result) == 0:
            return False, []
        else:
            bar = False
            id = temp_deci_status[0]['id']
            for temp_d in temp_deci_status:
                if temp_d['status'] == True:
                    bar = True
                    break
            res = [[], [], []]
            for temp_r in temp_result:
                if len(temp_r['result']) > 0:
                    res[0].append(temp_r['result'][0])
                    res[1].append(temp_r['result'][1])
                    res[2].append(temp_r['result'][2])
            if len(res[0]) > 0: #有东西
                max_res = [max(res[0]), max(res[1]), max(res[2])]
            else:
                max_res = []
            # return {'id': id, 'status': bar}, {'id':id, 'result': max_res}
            return bar, max_res


    def Run(self, Times = 32):
        will_brance = False
        decision = {
            'deci_status': [],
            'result': [],
            'ship_status': []
        }
        self.GoHead = True
        self.SimData.append(self.get_all_ship_status()) # 再将当前的起始状态添加到状态列表
        self.Times = Times

        while self.Times > 0:
            print('进入多步运行', self.Times)
            self.Times -= 1
            will_brance, decision = self.RunOneTime() # 更新之后的
            # decision = self.remove_duplicated_decision(decision)
            if will_brance:
                # self.Time = 0    
                break       
        # 结束之后
        if will_brance:
            [VM1, VM2] = self.gen_branch_data(decision)
            # [VM1, VM2] = self.gen_branch_data()
            return True, self.SimData, [VM1, VM2]
        else:
            return False, self.SimData, []

    def judge_collision(self):
        for ship1 in self.SimShipRegistered:
            for ship2 in self.SimShipRegistered:
                if ship1.id == ship2.id:
                    pass
                else:
                    delta_lon = ship1.lon - ship2.lon
                    delta_lat = ship1.lat - ship2.lat
                    dis = math.hypot(TransBCD.DeltaLon2DeltaMeter(delta_lon, ship1.lat), TransBCD.DeltaLat2DeltaMeter(delta_lat))
                    if dis < 100:
                        ship1.collision = True
                        ship2.collision = True
            # break

    def calc_distance(self, ship1, ship2):
        delta_lon = ship1.lon - ship2.lon
        delta_lat = ship1.lat - ship2.lat
        return math.hypot(TransBCD.DeltaLon2DeltaMeter(delta_lon, ship1.lat), TransBCD.DeltaLat2DeltaMeter(delta_lat))        

    def RunOneTime(self, ):
        # 注：decision是本轮决策结果
        self.count += 1
        decision = {
            'deci_status': [],
            'result': [],
            'ship_status': []
        }
        original_decision_status = []
        # self.decision = {
        #     'deci_status': [],
        #     'result': [],
        #     'ship_status': []
        # } # 每次运行 先清理一下
        will_branch = False
        self.judge_collision()
        for ship in self.SimShipRegistered:
            original_decision_status.append(ship.decision_status)
            if ship.collision == False:
                if ship.decision_status:
                    # 如果ship已经做出决策
                    if ship.applied_decision_lenth < ship.full_decision_length:
                        ship.execute_instruction()
                    else:
                        ship.set_original_status()
                        ship.go_ahead()
                    decision['deci_status'].append({'id': ship.id, 'status': False})
                    decision['result'].append({'id': ship.id, 'result': []})
                    # decision['ship_status'].append({'id': ship.id, 'ship_status': ship.get_ship_status()})
                else:
                    # ship尚未做出决策
                    # count % 4意思是步长每4次运行一次
                    if self.count % 4 == 0:
                        ship.execute_instruction()
                        ship_in_range = ship.detect_ship_in_radar_range()
                        if len(ship_in_range) > 0:
                            temp_deci_status = []
                            temp_result = []
                            temp_ship_prob = [] # 记录船的决策
                            temp_ship_DCPA = [] # 记录船DCPA
                            temp_ship_TCPA = [] # 记录船TCPA
                            for target_ship in ship_in_range:
                                DCPA = CPA.ComputeDCPA([ship.lon, ship.lat], ship.heading, ship.speed, [target_ship.lon, target_ship.lat], target_ship.heading, target_ship.speed)
                                TCPA = CPA.ComputeTCPA([ship.lon, ship.lat], ship.heading, ship.speed, [target_ship.lon, target_ship.lat], target_ship.heading, target_ship.speed)
                                temp_ship_DCPA.append(DCPA)
                                temp_ship_TCPA.append(TCPA)
                                distance = self.calc_distance(ship, target_ship)
                                if abs(DCPA - distance) < 50:
                                    #  相遇TODO
                                    pass
                                else:
                                    p = ship.get_decision_probability(DCPA)
                                    temp_ship_prob.append(p)
                                    print('current time {}, my_ship {}, target_ship {}, DCPA {}, p {:.6f}:'.format(ship.tick, ship.id, target_ship.id, DCPA, p))
                                    if p > 0.8:
                                        has_ship, GW1_vc_max, GW2_ac_max, GW2_tc_max = HA.AHLD(ship, ship_in_range) # 算法2
                                        dr = [GW1_vc_max, GW2_ac_max, GW2_tc_max]
                                        if has_ship:
                                            temp_deci_status.append({'id': ship.id, 'status': True})
                                            temp_result.append({'id': ship.id, 'result': dr})
                                            # dr = [GW1_vc_max, GW2_ac_max, GW2_tc_max]
                                            # ship.decision_status = True # TODO 这里注意了
                                            # ship.decision_content = dr
                                            # self.decision['deci_status'].append({'id': ship.id, 'status': True})
                                            # self.decision['result'].append({'id': ship.id, 'result': dr})
                                        else:
                                            temp_deci_status.append({'id': ship.id, 'status': False})
                                            temp_result.append({'id': ship.id, 'result': []})
                                            # self.decision['deci_status'].append({'id': ship.id, 'status': False})
                                            # self.decision['result'].append({'id': ship.id, 'result': []})
                                    else:
                                        temp_deci_status.append({'id': ship.id, 'status': False})
                                        temp_result.append({'id': ship.id, 'result': []})
                                        # self.decision['deci_status'].append({'id': ship.id, 'status': False})
                                        # self.decision['result'].append({'id': ship.id, 'result': []})
                            # 解决关键问题 2020年8月4日23点25分
                            s, r = self.new_remove_duplicated_decision(temp_deci_status, temp_result)
                            decision['deci_status'].append({'id': ship.id, 'status': s})
                            decision['result'].append({'id': ship.id, 'result': r})
                            if s: # s为True 或者False # TODO 这里注意了
                                # 两船场景下 不在此更改 而在line238 gen_branch_data()中
                                # ship.decision_status = True
                                ship.decision_content = r
                            if len(temp_ship_prob) > 0:
                                ship.ship_prob = max(temp_ship_prob)
                            # 否则是相遇了 默认ship_prob就是1，不用处理
                            if len(temp_ship_DCPA) > 0:
                                ship.DCPA = max(temp_ship_DCPA)
                            if len(temp_ship_TCPA) > 0:
                                ship.TCPA = max(temp_ship_TCPA)                              
                        else:
                            # 领域内没有船
                            decision['deci_status'].append({'id': ship.id, 'status': False})
                            decision['result'].append({'id': ship.id, 'result': []})
                            # decision['ship_status'].append({'id': ship.id, 'ship_status': ship.get_ship_status()})
                            # 船舶不参与分支概率计算
                    else:
                        ship.go_ahead()
            else:
                # 船的状态表明已相遇
                ship.ship_prob = 1
                pass     
        for elem in decision['deci_status']:
            if elem['status'] == True:
                will_branch = True
                break

        self.SimData.append(self.get_all_ship_status())
        print('Run one time, will_branch: ', will_branch)
        return will_branch, decision
        # return will_branch


# def test():
#     GenVMID = time.strftime("%y%m%d%H%M%S") + str(random.randint(1000, 9999))
#     VM = SimVM(GenVMID, timeratio=10)
#     VM.addShip(ShipID='1', VM=VM, Tick=0, Lon=123, Lat=30.916667, Speed=18, Heading=0)
#     VM.addShip(ShipID='2', VM=VM, Tick=0, Lon=123.074551, Lat=31.0535, Speed=18, Heading=230)
#     VM.addShip(ShipID='3', VM=VM, Tick=0, Lon=123.074940, Lat=30.963, Speed=16, Heading=300)
#     VM.addShip(ShipID='4', VM=VM, Tick=0, Lon=122.950364, Lat=31.0425, Speed=13, Heading=135)
#     will_branch, my_self, gotten_VM = VM.Run(32)
#     return will_branch, my_self, gotten_VM, VM.SimShipRegistered[0].tick

# def main():
#     will_branch, VM, gotten_VM, tick = test()
#     print('will_branch: ', will_branch)
#     print('tick: ', tick)
#     if will_branch:
#         print('got_VM, VM1 id {}, VM2 id {}'.format(gotten_VM[0].id, gotten_VM[1].id))

# if __name__ == '__main__':
#     main()