from flask import Flask, render_template, jsonify, send_file
import random, json, base64, os
# import my_utils as utils
import opt_db


# 获取server.py当前路径，以及父路径、祖父路径
current_dir = os.path.dirname(__file__)
parent_dir = os.path.dirname(current_dir)  # 获得current_dir所在的目录,
grandparent_dir = os.path.dirname(parent_dir)
print("current_dir: ", current_dir)
# print("parent_dir: ", parent_dir)
# print("grandparent_dir: ", grandparent_dir)

app = Flask(
    __name__, 
    static_folder = parent_dir + "/client/static", 
    template_folder = parent_dir + "/client/templates"
    )

app.jinja_env.auto_reload = True
app.config['TEMPLATES_AUTO_RELOAD'] = True

data0 = [
    {'name': 'root', 'value': 10086,'children':[
        {'name': 'A', 'value': 1, 'children': [{'name': 'C', 'value': 3}, {'name': 'D', 'value': 4}]}, 
        {'name': 'B', 'value': 2, 'children': [{'name': 'E', 'value': 5}, {'name': 'F', 'value': 6}]}
        ]}]


# dataIndex = [data0, data1, data2, data3]
def get_data():
    # i = random.randint(0, 3)
    # return dataIndex[i]
    return data0

map_data0 = [{"lon": 122.226654,"lat": 31.210672}]
map_data1 = [{"lon": 122.226654,"lat": 31.210672}, {"lon": 122.226654,"lat": 31.410672}]
map_data2 = [{"lon": 122.226654,"lat": 31.210672}, {"lon": 122.226654,"lat": 31.410672}, {"lon": 122.426654,"lat": 31.210672}]
map_data = [map_data0, map_data1, map_data2]
def get_map_data():
    i = random.randint(0, 2)
    return map_data[i]


# 根路由，首页页面
@app.route("/")
def index():
    return render_template("view.html")


# 英语版本的首页页面
@app.route("/en_version")
def index_en():
    return render_template("view-en.html")

# 网站入口
@app.route("/index")
def site_index():
    return render_template("index.html")

@app.route("/demo")
def site_demo():
    return render_template("demonstrate.html")

# 初始加载的树数据，可删除之
@app.route("/tree")
def get_tree():
    return(jsonify({"data": get_data()}))


# 获取最新的仿真树data
@app.route("/tree/lastest")
def get_lastest_tree():
    data = opt_db.select_lastest_tree()
    return(jsonify({"TREEID": data[0], "TREEData": json.loads(data[1])}))
    # return opt_db.select_lastest_tree()[1]


# 从数据库中查询指定TREEID的data并返回
@app.route("/tree/<treeid>")
def get_tree_by_id(treeid):
    data = opt_db.select_from_simtree(treeid)[1] # 此时是JSON格式的字符串
    return data

@app.route("/map")
def get_map():
    return(jsonify({"data": get_map_data()}))


# 从数据库中查询指定VMID的data并返回
@app.route("/vm/<vmid>")
def get_vm_by_id(vmid):
    data = opt_db.select_from_simvm(vmid)[1] # 此时是JSON格式的字符串
    return data


@app.route("/img/<imageid>")
def img_index(imageid):
    # 方式1: 前端采用DOM操作img属性，采用http请求，后端从文件目录返回图片
    # filename = grandparent_dir + "/res/VOImg/{}.png".format(imageid)
    # return send_file(filename, mimetype='image/png')

    # 方式2: 前端采用Ajax方式时，后端返回base64编码的字符串

	# 1. 从本地加载一条数据
    # with open("C:/Users/Bruce Lee/Documents/workspace/ADS-IDAC-SimPy/res/VOImg/{}.png".format(imageid), 'rb') as f:
    #     b64 = base64.b64encode(f.read())
    # return b64
	
	# 2. 从数据库加载已经Base64编码的图片数据
    # select_from_voimg返回结果格式为: data = (imgID, VMID, data)
    return opt_db.select_from_voimg(imageid)[2]


@app.route("/sangji")
def sangji():
    return render_template("sangji.html")


if __name__ == "__main__":
    app.run(debug=True)