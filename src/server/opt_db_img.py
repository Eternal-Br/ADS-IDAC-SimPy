import mysql.connector
import mysql.connector.pooling
import json




def link_mysql():
    mydb = mysql.connector.connect(
    host='127.0.0.1',
    port = 3306,
    user='root',      # 数据库IP、用户名和密码
    passwd='root',
    database = 'test',
    charset = 'utf8'
    )
    return mydb
    pass



# 使用 execute()  方法执行 SQL 查询
# cursor.execute("show databases;")
# cursor.execute("select * from idac")
# cursor.execute("use database_name;")
# cursor.execute("show tables;")

# for item in cursor:
#     print(item)

# 使用 fetchone() 方法获取单条数据;使用 fetchall() 方法获取所有数据
# data = cursor.fetchall()

# for item in data:
#     print(item)

# 向数据库中插入数据
# data1 = json.dumps(data)
# val = ("103", data1)
# insert_one_into_mysql(cursor, val)
# mydb.commit()



def insert_into_mysql(val, param="one"):
    '''
    :val : 待插入数据
    :param : "one"表示插入一条数据,"many"表示插入多条数据.
    '''
    mydb = link_mysql()
    cursor = mydb.cursor()
    # 这里有表的名称
    sql_insert = "INSERT INTO voimg (imgID, imgData) VALUES (%s, %s)"
    # print(sql_insert)
    if param == "one":
        cursor.execute(sql_insert, val)
        mydb.commit() # 提交插入操作
        print("1 record inserted.")
        mydb.close()  # 关闭数据库连接
        return
    if param == "many":
        cursor.executemany(sql_insert, val)
        mydb.commit() # 提交插入操作
        print(cursor.rowcount, "records inserted.")
        mydb.close()  # 关闭数据库连接
        return       
    else:
        print("请输入正确的参数以确定要插入的行数.")
        mydb.close()
        return


def select_all_from_mysql():
    mydb = link_mysql()
    cursor = mydb.cursor()
    sql_select = "select * from voimg"
    cursor.execute(sql_select)
    data = cursor.fetchall()
    mydb.close()
    return data


def test_select_all():
    mydata = select_all_from_mysql()
    for item in mydata:
        print(item, '\n')
        item_data = json.loads(item[1])
        print(item_data, '\n')
        print(type(item_data))

    
def test_insert_one(imgID, data):
    # imgID = "1101"    
    val = (imgID, data)
    insert_into_mysql(val, param="one")
    pass

def test_insert_many():
    
    pass

import base64, os
current_dir = os.path.dirname(__file__)
parent_dir = os.path.dirname(current_dir)  # 获得current_dir所在的目录,
grandparent_dir = os.path.dirname(parent_dir)
print("current_dir: ", current_dir)
# print("parent_dir: ", parent_dir)
# print("grandparent_dir: ", grandparent_dir)

def EncodeImg2B64Stream(path2img, imgID):
    """ 
    读取图片文件，并将其编码为b64字节流.
    : path2img : looks like grandparent_dir +'/res/VOImg/',
    : imgID 
    : return : b64ImgStream
    """
    imgName = '{}.png'.format(imgID)
    imgPath = path2img + imgName
    with open(imgPath, 'rb') as f:
        # f.read()
        # print(f.read())
        b64ImgStream = base64.b64encode(f.read())
        # print(type(b64))
    return b64ImgStream

thispath = grandparent_dir + '/res/VOImg/'
b64img = EncodeImg2B64Stream(thispath, 10086)
print(b64img)

# test_select_all()
# import base64
# with open('./static/res/ship0.png', 'rb') as f:
#     # f.read()
#     # print(f.read())
#     b64 = base64.b64encode(f.read())
#     # print(type(b64))
# test_insert_one("1000", b64)


