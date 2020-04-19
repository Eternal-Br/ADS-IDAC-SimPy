# #     # def plottrace(self, point):
# #     #     # 使用matplotlib之pyplot绘制船舶轨迹
# #     #     # point = 38
# #     #     def initial(ax):
# #     #         ax.axis("equal") #设置图像显示的时候XY轴比例
# #     #         ax.set_xlabel('Horizontal Position')
# #     #         ax.set_ylabel('Vertical Position')
# #     #         ax.set_title('Vessel trajectory')
# #     #         plt.grid(True) #添加网格
# #     #         return ax

# #     #     es_time = np.zeros([point])
# #     #     fig=plt.figure()
# #     #     ax=fig.add_subplot(1,1,1)
# #     #     ax = initial(ax)

# #     #     # test
# #     #     ax2 = fig.add_subplot(1,1,1)
# #     #     ax2 = initial(ax2)

# #     #     plt.ion()  #interactive mode on 动态绘制


# #     #     # IniObsX=0000
# #     #     # IniObsY=4000
# #     #     # IniObsAngle=135
# #     #     # IniObsSpeed=10*math.sqrt(2)   #米/秒
# #     #     # print('开始仿真')
# #     #     obsX = []
# #     #     obsX2 = []
# #     #     # obsY = [4000,]
# #     #     obsY = []
# #     #     obsY2 = []
# #     #     for t in range(point):
# #     #         # t0 = time.time()
# #     #         #障碍物船只轨迹
# #     #         # obsX.append(IniObsX+IniObsSpeed*math.sin(IniObsAngle/180*math.pi)*t)
# #     #         obsX.append(sim_res.SHIP1POS[t][0])
# #     #         obsX2.append(sim_res.SHIP2POS[t][0])
# #     #         # obsY.append(IniObsY+IniObsSpeed*math.cos(IniObsAngle/180*math.pi)*t)
# #     #         obsY.append(sim_res.SHIP1POS[t][1])
# #     #         obsY2.append(sim_res.SHIP2POS[t][1])
# #     #         plt.cla()
# #     #         ax = initial(ax)
# #     #         ax.plot(obsX,obsY,'-g',marker='*')  #散点图

# #     #         # test
# #     #         ax2 = initial(ax2)
# #     #         ax2.plot(obsX2, obsY2, '-r', marker='o')
# #     #         risk_value_text = 'Risk value: ' + str(sim_res.RISKVALUE[t])
# #     #         plt.text(0, 7, risk_value_text)
# #     #         plt.pause(0.5)
# #     #         # es_time[t] = 1000*(time.time() - t0)

# #     #     plt.pause(0)
# #     #     # return es_time
# #     #     pass

# # l =[
# # {'mmsi': '413234579', 'lon': 1.1246919270816962, 'lat': 4.998444950514175, 'speed': 5, 'heading': 1.4290123809632689, 'timestamp': 1579090464736},
# # {'mmsi': '413637543', 'lon': 4.000000000000001, 'lat': 75.0, 'speed': 5, 'heading': 180.0, 'timestamp': 1579090464736},
# # {'mmsi': '413234579', 'lon': 1.3739982203982506, 'lat': 9.992225719842436, 'speed': 5, 'heading': 2.8580247619265378, 'timestamp': 1579090464736},
# # {'mmsi': '413637543', 'lon': 4.000000000000002, 'lat': 70.0, 'speed': 5, 'heading': 180.0, 'timestamp': 1579090464736},
# # {'mmsi': '413234579', 'lon': 1.8702173911353093, 'lat': 14.967541441944203, 'speed': 5, 'heading': 5.695628760003613, 'timestamp': 1579090464736},
# # {'mmsi': '413637543', 'lon': 4.000000000000003, 'lat': 65.0, 'speed': 5, 'heading': 180.0, 'timestamp': 1579090464736},
# # {'mmsi': '413234579', 'lon': 2.612132572393715, 'lat': 19.912191264107378, 'speed': 5, 'heading': 8.533232758080688, 'timestamp': 1579090464736},
# # {'mmsi': '413637543', 'lon': 4.0000000000000036, 'lat': 60.0, 'speed': 5, 'heading': 180.0, 'timestamp': 1579090464736},
# # {'mmsi': '413234579', 'lon': 3.716411250463177, 'lat': 24.788723700292046, 'speed': 5, 'heading': 12.759299424665802, 'timestamp': 1579090464736},
# # {'mmsi': '413637543', 'lon': 4.000000000000004, 'lat': 55.0, 'speed': 5, 'heading': 180.0, 'timestamp': 1579090464736},
# # {'mmsi': '413234579', 'lon': 5.177048477945394, 'lat': 29.570620697268566, 'speed': 5, 'heading': 16.985366091250917, 'timestamp': 1579090464736},
# # {'mmsi': '413637543', 'lon': 4.000000000000005, 'lat': 50.0, 'speed': 5, 'heading': 180.0, 'timestamp': 1579090464736},
# # {'mmsi': '413234579', 'lon': 7.096918029476489, 'lat': 34.18734040991128, 'speed': 5, 'heading': 22.580054122906034, 'timestamp': 1579090464736},
# # {'mmsi': '413637543', 'lon': 4.000000000000006, 'lat': 45.0, 'speed': 5, 'heading': 180.0, 'timestamp': 1579090464736},
# # {'mmsi': '413234579', 'lon': 9.457729087997743, 'lat': 38.594898820864415, 'speed': 5, 'heading': 28.17474215456115, 'timestamp': 1579090464736},
# # {'mmsi': '413637543', 'lon': 4.000000000000007, 'lat': 40.0, 'speed': 5, 'heading': 180.0, 'timestamp': 1579090464737},
# # {'mmsi': '413234579', 'lon': 12.33407559960147, 'lat': 42.68471920141722, 'speed': 5, 'heading': 35.11849378253092, 'timestamp': 1579090464737},
# # {'mmsi': '413637543', 'lon': 4.000000000000008, 'lat': 35.0, 'speed': 5, 'heading': 180.0, 'timestamp': 1579090464737},
# # {'mmsi': '413234579', 'lon': 15.683763371985261, 'lat': 46.39680646164461, 'speed': 5, 'heading': 42.06224541050069, 'timestamp': 1579090464737},
# # {'mmsi': '413637543', 'lon': 4.000000000000009, 'lat': 30.0, 'speed': 5, 'heading': 180.0, 'timestamp': 1579090464737},
# # {'mmsi': '413234579', 'lon': 19.532755012637075, 'lat': 49.58824240024536, 'speed': 5, 'heading': 50.335782348966696, 'timestamp': 1579090464737},
# # {'mmsi': '413637543', 'lon': 4.00000000000001, 'lat': 25.0, 'speed': 5, 'heading': 180.0, 'timestamp': 1579090464737},
# # {'mmsi': '413234579', 'lon': 23.800932659502035, 'lat': 52.192596365205254, 'speed': 5, 'heading': 58.609319287432704, 'timestamp': 1579090464737},
# # {'mmsi': '413637543', 'lon': 4.000000000000011, 'lat': 20.0, 'speed': 5, 'heading': 180.0, 'timestamp': 1579090464737},
# # {'mmsi': '413234579', 'lon': 28.443155609841064, 'lat': 54.04995095691508, 'speed': 5, 'heading': 68.19363873966773, 'timestamp': 1579090464737},
# # {'mmsi': '413637543', 'lon': 4.0000000000000115, 'lat': 15.0, 'speed': 5, 'heading': 180.0, 'timestamp': 1579090464737},
# # {'mmsi': '413234579', 'lon': 33.329828234157475, 'lat': 55.10845493081246, 'speed': 5, 'heading': 77.77795819190277, 'timestamp': 1579090464737},
# # {'mmsi': '413637543', 'lon': 4.000000000000012, 'lat': 10.0, 'speed': 5, 'heading': 180.0, 'timestamp': 1579090464737},
# # {'mmsi': '413234579', 'lon': 38.328449271128534, 'lat': 55.225876090534065, 'speed': 5, 'heading': 88.65432891349755, 'timestamp': 1579090464737},
# # {'mmsi': '413637543', 'lon': 4.000000000000013, 'lat': 5.0, 'speed': 5, 'heading': 180.0, 'timestamp': 1579090464737},
# # {'mmsi': '413234579', 'lon': 43.25943440039857, 'lat': 54.39799587279855, 'speed': 5, 'heading': 99.53069963509233, 'timestamp': 1579090464737},
# # {'mmsi': '413637543', 'lon': 4.000000000000014, 'lat': 0.0, 'speed': 5, 'heading': 180.0, 'timestamp': 1579090464737},
# # {'mmsi': '413234579', 'lon': 47.90572109010106, 'lat': 52.550830477633994, 'speed': 5, 'heading': 111.68065805343934, 'timestamp': 1579090464737},
# # {'mmsi': '413637543', 'lon': 4.000000000000015, 'lat': -5.0, 'speed': 5, 'heading': 180.0, 'timestamp': 1579090464737},
# # {'mmsi': '413234579', 'lon': 52.05915653762326, 'lat': 49.76713258036388, 'speed': 5, 'heading': 123.83061647178636, 'timestamp': 1579090464737},
# # {'mmsi': '413637543', 'lon': 4.000000000000016, 'lat': -10.0, 'speed': 5, 'heading': 180.0, 'timestamp': 1579090464737},
# # {'mmsi': '413234579', 'lon': 55.45405968754069, 'lat': 46.09635165490936, 'speed': 5, 'heading': 137.23596286101656, 'timestamp': 1579090464737},
# # {'mmsi': '413637543', 'lon': 4.000000000000017, 'lat': -15.0, 'speed': 5, 'heading': 180.0, 'timestamp': 1579090464737}
# # ]

# import time, copy
# import random
# # for i in range(10):
# #     print(
# #         "ImgID: ", str(round(time.time()*1000)) + str(random.randint(100, 999))
# #     )
# # for i in range(10):
# #     print("VMID: ", time.strftime("%y%m%d%H%M%S") + str(random.randint(1000, 9999)))

# # 1584706734732171
# # 2003202036233914
# """ 
# /res/VOImg/
#     VMID/
#         ImgID 
# """

# # test deepcopy
# data = {
#     "data": [
#         {
#         "name": "1000",
#         "value": "1000-value",
#     }, {
#         "name": "1001",
#         "value": "1001-value",
#     }],
#     "ID": 10086
# }

# olddata = copy.deepcopy(data)

# print("data:    ", data)
# print("olddata: ", olddata)

# data["data"][0]["value"] = "2000-value"

# print("\n更改后\ndata:    ", data)
# print("olddata: ", olddata)

# data = copy.deepcopy(olddata)
# print("\nnew data: ", data)

# delta1 = [30 for _ in range(5)]
# delta2 = [-30 for _ in range(5)]
# delta = delta1 + delta2
# print(delta)

# coding: utf-8

# import os

# current_dir= os.path.dirname(__file__)
# print("current_dir: ", current_dir)

# parent_dir= os.path.dirname(current_dir)  # 获得current_dir所在的目录,
# print("parent_dir: ", parent_dir)

# parent_parent_dir= os.path.dirname(parent_dir)  # 获得parent_dir所在的目录
# print(parent_parent_dir)

# NextStepData = {
#     'GoHead': {'probability': 0.5132643909682215, 'status': [{'time': 500, 'VMid': '2003291529531708', 'shipid': '10086', 'lon': 123.05499051838406, 'lat': 35.001, 'speed': 10, 'heading': 90, 'interval': 100}, {'time': 500, 'VMid': '2003291529531708', 'shipid': '10010', 'lon': 123.06150710756154, 'lat': 35.0, 'speed': 7, 'heading': 270, 'interval': 100}]}, 
#     'TurnLeft': {'probability': 0.06953365843311121, 'status': [{'time': 500, 'VMid': '2003291529531708', 'shipid': '10086', 'lon': 123.05494866727916, 'lat': 35.00178433893761, 'speed': 10, 'heading': 90, 'interval': 100}, {'time': 500, 'VMid': '2003291529531708', 'shipid': '10010', 'lon': 123.06153640297696, 'lat': 34.99945096274367, 'speed': 7, 'heading': 270, 'interval': 100}]}, 
#     'TurnRight': {'probability': 0.41720195059866727, 'status': [{'time': 500, 'VMid': '2003291529531708', 'shipid': '10086', 'lon': 123.05499051838406, 'lat': 35.001, 'speed': 10, 'heading': 90, 'interval': 100}, {'time': 500, 'VMid': '2003291529531708', 'shipid': '10010', 'lon': 123.06150710756154, 'lat': 35.0, 'speed': 7, 'heading': 270, 'interval': 100}]}
#     }
# for item in NextStepData:
#     print(item, NextStepData[item])

# 测试多线程
# import threading

# class VM:
#     __Data = []
#     def __init__(self, VMID, tick):
#         self.id = VMID
#         self.tick = tick
#         self.__selfdata = []

#     def run(self):
#         self.__Data.append(self.tick)
#         self.__selfdata.append(self.tick)

# VM1 = VM(10086, 100)
# VM2 = VM(10010, 50)
# VM1.run()
# VM2.run()

# mytu = (0,1,2)
# print(mytu[2])

# import uuid, time
# print(uuid.uuid5(uuid.NAMESPACE_URL, str(time.time())))
# 81b19b9a-a4cb-531e-b725-741fe2cf890c