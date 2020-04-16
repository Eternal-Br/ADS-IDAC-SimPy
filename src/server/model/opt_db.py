"""
操作MySQL数据库工具集，目前插入操作为简单的分表单条插入，有待优化为通用插入
"""

import mysql.connector
# import mysql.connector.pooling
import json

# 测试数据
data0 = {"data": [{"name": "root", "value": 0}]}
data1 = {"data": [{"name": "root", "value": 1, "children":[{"name": "root-child1", "value": 2}, {"name": "root-child2", "value": 3}]}]}
data2 = {"data": [{"name": "root", "value": 1, "children":[{"name": "root-child1", "value": 2}, {"name": "root-child2", "value": 3, "children": [{"name": "root-child2-child1", "value": 4}, {"name": "root-child2-child2", "value": 5}]}]}]}
data3 = {"data": [{"name": "root", "value": 1, "children":[{"name": "root-child1", "value": 2}, {"name": "root-child2", "value": 3, "children": [{"name": "root-child2-child1", "value": 4, "children": [{"name": "root-child2-child1-child1", "value": 6}, {"name": "root-child2-child1-child3", "value": 7}]}, {"name": "root-child2-child2", "value": 5}]}]}]}
data4 = {"data": [{"name": "root", "value": 1, "children":[{"name": "root-child1", "value": 2}, {"name": "root-child2", "value": 3, "children": [{"name": "root-child2-child1", "value": 4, "children": [{"name": "root-child2-child1-child1", "value": 6}, {"name": "root-child2-child1-child3", "value": 7}]}, {"name": "root-child2-child2", "value": 5, "children": [{"name": "root-child2-child2-child1", "value": 8}, {"name": "root-child2-child2-child2", "value": 9}]}]}]}]}


def link_mysql(db="idac"):
    mydb = mysql.connector.connect(
    host='127.0.0.1',
    port = 3306,
    user='user1',      # 数据库IP、用户名和密码
    passwd='hello',
    database = db,
    charset = 'utf8'
    )
    return mydb
    pass


def insert_into_simtree(TREEID, data):
    """
    将 仿真树 数据插入表 sim_tree
    :TREEID : varchar string 数字序列,
    :data ： JSON格式的字符串
    """
    mydb = link_mysql()
    cursor = mydb.cursor()
    sql_insert = "INSERT INTO sim_tree (TREEID, data) VALUES (%s, %s)"
    # print(sql_insert)
    cursor.execute(sql_insert, (TREEID, data))
    mydb.commit() # 提交插入操作
    print("1 record inserted.")
    mydb.close()  # 关闭数据库连接
    pass

def insert_into_simvm(VMID, data):
    """ 
    将VM数据插入表sim_vm 
    :VMID : varchar string 数字序列,
    :data : JSON格式的字符串
    """
    mydb = link_mysql()
    cursor = mydb.cursor()
    sql_insert = "INSERT INTO sim_vm (VMID, data) VALUES (%s, %s)"
    # print(sql_insert)
    cursor.execute(sql_insert, (VMID, data))
    mydb.commit() # 提交插入操作
    print("1 record inserted.")
    mydb.close()  # 关闭数据库连接
    pass

# 将图片插入数据库的方式暂时不用
def insert_into_voimg(imgID, VMID, data):
    """ 
    将VM仿真过程中生成的voimg图片插入表 voimg 
    :imgID : varchar string 数字序列,
    :VMID : 所属VM ,varchar string 数字序列,
    :data : 二进制字节流
    """
    mydb = link_mysql()
    cursor = mydb.cursor()
    sql_insert = "INSERT INTO voimg (imgID, VMID, data) VALUES (%s, %s, %s)"
    # print(sql_insert)
    cursor.execute(sql_insert, (imgID, VMID, data))
    mydb.commit() # 提交插入操作
    print("1 record inserted.")
    mydb.close()  # 关闭数据库连接
    pass

def select_from_simtree(TREEID):
    """ 
    从表sim_tree中查询tree数据
    :TREEID : 查询的TREE,
    :return : data = (TREEID, data)
    """
    mydb = link_mysql()
    cursor = mydb.cursor()
    sql_select = "SELECT TREEID, data FROM sim_tree WHERE TREEID = {}".format(TREEID)
    cursor.execute(sql_select)
    # data = cursor.fetchall()
    data = cursor.fetchone() # TREEID是唯一的，两者结果是一致的
    mydb.close()
    return data


def select_lastest_tree():
    """
    从表sim_tree中查询最新的一条tree数据
    : return: (TREEID, data)
    """
    mydb = link_mysql()
    cursor = mydb.cursor()
    sql_select = "SELECT TREEID, DATA FROM sim_tree WHERE TREEID = (SELECT MAX(TREEID) FROM sim_tree)"
    cursor.execute(sql_select)
    data = cursor.fetchone() 
    mydb.close()
    return data

def select_from_simvm(VMID):
    """ 
    从表sim_vm中查询VM数据 
    :VMID : 查询的VM,
    :return : data = (VMID, data)
    """
    # print("进入数据库操作函数vm")
    mydb = link_mysql()
    cursor = mydb.cursor()
    sql_select = "SELECT VMID, data FROM sim_vm WHERE VMID = {}".format(VMID)
    cursor.execute(sql_select)
    # data = cursor.fetchall()
    data = cursor.fetchone() # VMID是唯一的，两者结果是一致的
    mydb.close()
    return data
    
# 从数据库中查询一张图片
def select_from_voimg(imgID):
    """ 
    从表voimg中查询标识为 imgID 的VM的imgs 
    :imageid : 查询img所属的ID,
    :return : data = (imgID, VMID, data)
    """
    mydb = link_mysql()
    cursor = mydb.cursor()
    sql_select = "SELECT imgID, VMID, data FROM voimg WHERE imgID = '{}'".format(imgID)
    cursor.execute(sql_select)
    data = cursor.fetchone() # 
    mydb.close()
    return data

# print('latest treeid: ', select_lastest_tree())

# ---------------------------------------------------------------
# Old method
# ---------------------------------------------------------------
# def insert_into_mysql(val, param="one"):
#     '''
#     :val : 待插入数据
#     :param : "one"表示插入一条数据,"many"表示插入多条数据.
#     '''
#     mydb = link_mysql()
#     cursor = mydb.cursor()
#     sql_insert = "INSERT INTO idac (VMID, data) VALUES (%s, %s)"
#     # print(sql_insert)
#     if param == "one":
#         cursor.execute(sql_insert, val)
#         mydb.commit() # 提交插入操作
#         print("1 record inserted.")
#         mydb.close()  # 关闭数据库连接
#         return
#     elif param == "many":
#         cursor.executemany(sql_insert, val)
#         mydb.commit() # 提交插入操作
#         print(cursor.rowcount, "records inserted.")
#         mydb.close()  # 关闭数据库连接
#         return       
#     else:
#         print("请输入正确的参数以确定要插入的行数.")
#         mydb.close()
#         return

# def select_all_from_mysql():
#     mydb = link_mysql()
#     cursor = mydb.cursor()
#     sql_select = "select * from idac"
#     cursor.execute(sql_select)
#     data = cursor.fetchall()
#     mydb.close()
#     return data

# def test_select_all():
#     mydata = select_all_from_mysql()
#     for item in mydata:
#         print(item, '\n')
#         item_data = json.loads(item[1])
#         print(item_data, '\n')
#         print(type(item_data))
    
# def test_insert_one(data):
#     data = json.dumps(data)
#     VMID = "1100"
#     val = (VMID, data)
#     insert_into_mysql(val, param="one")
#     pass

# ---------------------------------------------------------------
# Old method
# ---------------------------------------------------------------
