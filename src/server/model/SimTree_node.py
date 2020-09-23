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
import MyNode, MyNode_2ships
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
    print('已写入sim tree.')
    for item in VMpool:
        opt_db.insert_into_simvm(item["VMID"], json.dumps(item))
    print("已经将仿真树和其中的结点数据写入数据库.")
    pass

def write2dynTree(sTree):
    opt_db.del_dynTree()
    allNodes = sTree.all_nodes()
    for node in allNodes:
        rootId = node.tag
        children = sTree.children(rootId)
        if (children is not None) and len(children) > 0:
            childrenArr = []
            for node in children:
                leafDic = {'name': node.tag, 'value': int(node.tag)}
                childrenArr.append(leafDic)
            childDic = {'data':[{'name': rootId, 'value': int(rootId), "children": childrenArr}]}
            # print(childDic)
            opt_db.insert_into_dynTree(rootId,json.dumps(childDic))
    pass

def SimTree():

    SimTreeID = "10" + time.strftime("%y%m%d%H%M%S") + str(random.randint(1000, 9999))
    tree = Tree()
    VMpool = []
    GenVMID = time.strftime("%y%m%d%H%M%S") + str(random.randint(1000, 9999))
    # 在多船避碰中，如果要加步长控制，用VM = MyNode_2ships.SimVM(GenVMID, timeratio=10)
    VM = MyNode.SimVM(GenVMID, timeratio=10)   #没加步长控制的树
    # VM = MyNode_2ships.SimVM(GenVMID, timeratio=10)    #加上步长控制的树，需要几艘船，就留几艘
    VM.addShip(ShipID='1', VM=VM, Tick=0, Lon=123, Lat=30.916667, Speed=18, Heading=0)
    VM.addShip(ShipID='2', VM=VM, Tick=0, Lon=123.074551, Lat=31.0535, Speed=18, Heading=230)
    VM.addShip(ShipID='3', VM=VM, Tick=0, Lon=123.074940, Lat=30.963, Speed=16, Heading=300)
    VM.addShip(ShipID='4', VM=VM, Tick=0, Lon=122.950364, Lat=31.0425, Speed=13, Heading=135)
    parent = None

    def CreatVMTree(tree, vm, parent):
        will_branch, simdata, gotten_VM = vm.Run(32)

        # Data = {"VMID": my_self.id, "SimData": VM.GetSimData(), "NextStepData":gotten_VM}
        Data = {"VMID": vm.id, "VM_prob": vm.VM_prob, "SimData": simdata}
        tree.create_node(identifier=Data["VMID"], parent=parent)
        VMpool.append(Data)

        if will_branch: 
            for item in gotten_VM:
                # Recursion: 递归调用 生成新的结点
                tree = CreatVMTree(tree, item, parent=Data["VMID"])
        return tree

    tree = CreatVMTree(tree, VM, parent)
    return tree, SimTreeID, VMpool


def main():
    sTree, SimTreeID, VMpool = SimTree()
    print('SimTreeID: ', SimTreeID)
    # print(Tree_to_eChartsJSON(sTree))
    sTree.show()
    write2dynTree(sTree)
    write2db(SimTreeID, sTree, VMpool)
    # for item in VMpool:
    #     print("VMID: ", item["VMID"])
    # print("pause.")


if __name__ == '__main__':
    main()
