#-------------------------------------------------------------------------------
# Name:        SimTree
# Purpose:     To management SimVM
#
# Author:      Bruce
#
# Created:     28-03-2020
# Copyright:   (c) Bruce 2020
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import sys
sys.path.append(".")
sys.path.append("..")
from treelib import Node, Tree
import pickle, json, copy, time, random
import SimVM
import opt_db


def store(data, filename):
    # 序列化，写到本地磁盘文件
    with open(filename,'wb') as f:
        pickle.dump(data, f)

def grab(filename):
    # 反序列化，从本地文件读出原有的对象
    with open(filename,'rb') as f:
        return pickle.load(f)

def Tree_to_eChartsJSON(tree):
    #Transform the whole tree into an eCharts_JSON.
    def to_dict(tree, nid):
        ntag = tree[nid].tag
        tree_dict = {'name': ntag, 'value': int(nid), "children": []}
        #if tree[nid].expanded:
        for elem in tree.children(nid):
            tree_dict["children"].append(to_dict(tree, elem.identifier))
        if len(tree_dict["children"]) == 0:
            tree_dict.pop('children', None)
        return tree_dict
    eChartsDict = {'data': [to_dict(tree, tree.root)]}
    return json.dumps(eChartsDict)
    pass

def write2db(SimTreeID, sTree, VMpool):
    JSONTree = Tree_to_eChartsJSON(sTree)
    opt_db.insert_into_simtree(SimTreeID, JSONTree)
    for item in VMpool:
        opt_db.insert_into_simvm(item["VMID"], json.dumps(item))
    print("已经将仿真树和其中的结点数据写入数据库.")
    pass

def SimTree():
    count = [0]
    SimTreeID = "10" + time.strftime("%y%m%d%H%M%S") + str(random.randint(1000, 9999))
    tree = Tree()
    VMpool = []
    init_data = {'probability': 1, 'status': [
        {'time': 0, 'shipid': '10086', 'lon': 123, 'lat': 30.99, 'speed': 7, 'heading': 75, 'interval': 100}, 
        {'time': 0, 'shipid': '10010', 'lon': 123.15, 'lat': 31.01, 'speed': 7, 'heading': 270, 'interval': 100},
        ]}
    data = {'probability': 1, 'status': [
        init_data['status'][0], 
        init_data['status'][1], 
        init_data['status'][0], 
        init_data['status'][1]
        ]}
    parent = None

    def CreatVMTree(tree, data, parent, count):
        count[0] += 1
        if count[0] > 365:
            return tree
        """ 
        data looks like: 
        GoHead:  {'probability': 0.818733374651966, 'status': [
            {'time': 400, 'VMid': '2003282016042971', 'shipid': '10086', 'lon': 123.04399241470725, 'lat': 35.001, 'speed': 10, 'heading': 90, 'interval': 100}, 
            {'time': 400, 'VMid': '2003282016042971', 'shipid': '10010', 'lon': 123.06920568604923, 'lat': 35.0, 'speed': 7, 'heading': 270, 'interval': 100}
            ]}
         """
        def GetInitData(data):
            data = copy.deepcopy(data)
            sta0 = data["status"][2]
            sta1 = data["status"][3]
            initStatus4DrawLines = [data["status"][0], data["status"][1]]
            shipData = {
                "ship0": {
                    "ShipID": sta0["shipid"],
                    "Tick": sta0["time"], 
                    "Lon": sta0["lon"],
                    "Lat": sta0["lat"],
                    "Speed": sta0["speed"],
                    "Heading": sta0["heading"]
                },
                "ship1": {"ShipID": sta1["shipid"], "Tick": sta1["time"], "Lon": sta1["lon"], "Lat": sta1["lat"], "Speed": sta1["speed"], "Heading": sta1["heading"]}
            }
            initData = copy.deepcopy(shipData)
            return initData, initStatus4DrawLines
            # return initData

        VMInitData, initStatus4DrawLines = GetInitData(data)
        # VMInitData = GetInitData(data)
        VM = SimVM.RunVM(VMInitData, initStatus4DrawLines, interval = 0, timeRatio = 200, runTimes = 32)
        # VM = SimVM.RunVM(VMInitData, interval = 0, timeRatio = 200, runTimes = 32)
        # Data = {"VMID": VM.id, "SimData": VM.GetSimData(), "NextStepData": VM.GetNextStepData(), "MET": VM.GetMetFlag()}
        Data = {"VMID": VM.id, "SimData": VM.GetSimData(), "NextStepData": VM.GetNextStepData(), "MET": VM.GetMetFlag(), "DeciResult": VM.DeciResult}

        tree.create_node(identifier=Data["VMID"], parent=parent)
        VMpool.append(Data)
        # tree.append({"identifier": Data["VMID"], "parent": parent, "VMIns": VM})
        # 采用方案1
        """
        方案1. tree.create_node(identifier=Data["VMID"], parent=parent)
        即 tree 的结点中只放仿真虚拟机的ID和父子关系，前端需要用到某的结点的Data时，再向后台请求，
        Data = SimVM.RunVM()结束后将结点的Data和对应的VMID存入数据库的一张表，仿真事件树另存在一张表.

        方案2. tree.create_node(identifier=Data["VMID"], data=Data, parent=parent)
        即 tree的结点中一次性将包括结点(仿真虚拟机)VMID,Data和父子关系全部存放，
        将一棵带有数据的完整的事件树作为一个整体存入一张表中.
        """
        # print("__SimShipRegistered: ", VM._SimVM__SimShipRegistered)
        # print("\n当前timer标识已经创建的节点数: {}\n".format(count))
        if Data["MET"] == 0:
            # 船还未相遇，仿真继续，分支
            for item in Data["NextStepData"]:
                # Recursion: 递归调用 生成新的结点
                tree = CreatVMTree(tree, Data["NextStepData"][item], parent=Data["VMID"], count=count)
        else:
            # 船已经相遇，仿真停止，不再分支
            pass
        return tree
    tree = CreatVMTree(tree, data, parent, count)
    return tree, SimTreeID, VMpool


def main():
    sTree, SimTreeID, VMpool = SimTree()
    print('SimTreeID: ', SimTreeID)
    # print(Tree_to_eChartsJSON(sTree))
    sTree.show()
    write2db(SimTreeID, sTree, VMpool)
    # for item in VMpool:
    #     print("VMID: ", item["VMID"])
    # print("pause.")

# TODO: 优化数据库操作：引入连接池
# TODO: 模型调参等。
if __name__ == '__main__':
    main()
