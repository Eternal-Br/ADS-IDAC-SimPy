# -*- coding: utf-8 -*-
"""
Created on Sun Dec 15 19:52:33 2019

@author: Jinfen Zhang
@edit by Bruce

"""
import sys, os
current_dir = os.path.dirname(__file__)
sys.path.append(current_dir)
sys.path.append("..")
import numpy as np
import GetVoPolygons as gvp
from matplotlib.patches import Polygon
from matplotlib.collections import PatchCollection
import matplotlib.pyplot as plt
import io, base64
import opt_db, TransBCD


def PolygonTransform(polygon):
    #把shapely.geometry中的Polygon格式转换成matplotlib格式的Polygon
    x, y = polygon.exterior.coords.xy
#    print(x)
    len_x = len(x)
    polygon_transform = []
    for i in np.arange(len_x):
        point_temp = [x[i],y[i]]
        polygon_transform.append(point_temp)
    polygon_transform = Polygon(polygon_transform, True)
    return polygon_transform


def GenVOImgB64(pos1, course1, speed1, pos2, course2, speed2, ImgID):
    """ 
    图片名称格式为 XXXX.png 其中XXXX为ImgID, 也即是虚拟机下某个船舶对应某次运行的ID.
    : return: base64编码的字节流 数据。

    注意 变更说明(Bruce 2020年4月11日):
    此处使用速度障碍法绘制VO图时，假定的场景位于直角坐标系内，
    两船的坐标的单位是 米 ，两船的速度单位也是米，角度单位为角度° ，
    然而在实际场景中，两船位于地理坐标系中，其坐标是经纬度，速度是米，角度是度°。
    在计算时，用到的是两船的相对位置。
    我们提出将两船在地理坐标系中的绝对位置转换为临时的直角坐标系的相对位置，
    如果以主船(ship1)作为临时参考系的原点，那么只需要转换客船相对于主船的坐标差值，其他参数无需转换，
    所以在这里引入 TransGCS2CCS函数 做上述转换, 而后续操作不需要做出任何改变。
    """
    pos1,course1,speed1,pos2,course2,speed2 = TransBCD.TransGCS2CCS(pos1,course1,speed1,pos2,course2,speed2)

    # 后面的操作不做任何改变即可
 
    fig, ax = plt.subplots()

    poly_vo,poly_front,poly_rear,poly_diverging = gvp.GetVoPolygons(pos1,course1,speed1,pos2,course2,speed2)

    patches = []
    colors = []
    if poly_vo:
        poly_vo = PolygonTransform(poly_vo)
        patches.append(poly_vo)
        colors.append(10)
        
    if poly_front:
        poly_front = PolygonTransform(poly_front)
        patches.append(poly_front)
        colors.append(30)

    if poly_rear:
        poly_rear = PolygonTransform(poly_rear)
        patches.append(poly_rear)
        colors.append(50)

    if poly_diverging:
        poly_diverging = PolygonTransform(poly_diverging)
        patches.append(poly_diverging)
        colors.append(70)
    # print(colors)
    #
    # fig, ax = plt.subplots()
    p = PatchCollection(patches, alpha=0.4)
    ax.add_collection(p)

    p.set_array(np.array(colors))
    ax.add_collection(p)

    #画速度向量
    vx = speed1 * 500 * np.sin(course1 * np.pi / 180)
    vy = speed1 * 500 * np.cos(course1 * np.pi / 180)
    ax.arrow(pos1[0], pos1[1], vx, vy, length_includes_head=True,\
            head_width=200, head_length=400, fc='r', ec='r')

    plt.xlim(pos1[0]-1000, pos1[0]+6000)
    plt.ylim(pos1[1]-3000, pos1[1]+6000)

    # plt.ion()
    # plt.plot()
    # plt.pause(1)
    # plt.cla()

    # 1. 下面一条语句用于生成png格式的图片并保存到某个路径下
    # 暂时不用这种方式
    # plt.savefig("./res/VOImg/{}.png".format(str(ImgID)))

    # 2. 下面的方式从fig中取出字节流，再进行base64压缩编码，并将结果返回
    buffer = io.BytesIO()
    fig.canvas.print_png(buffer)
    b64 = base64.b64encode(buffer.getvalue())
    plt.close(fig)

    # with open('./res/VOImg/testS2f01.png', 'wb') as f:
    #     f.write(data)
    # data = base64.b64encode(data)
    # opt_db.insert_into_voimg(1000010086312797, 2004071252277034, data)
    # print(data)

    # plt.show()
    # print('[DrawVoAreas]: Call DrawVoAreas succeed & VO Img {}.png saved.'.format(str(ImgID)))
    
    # 返回base64编码的字节流数据
    return b64


# 使用这里的数值测试，course就是ship的heading,即航艏向
# pos1 = [1000,-3134]
# course1 = 0
# speed1 = 5.144

# pos2 = [1950,1964]
# course2 = 180
# speed2 = 5.144

# 使用这里的坐标测试，course就是ship的heading,即航艏向
# pos1 = [123, 30.9900001]
# course1 = 75
# speed1 = 7

# pos2 = [123.15, 31.0100001]
# course2 = 270
# speed2 = 7

# def main():
#     GenVOImgB64(pos1, course1, speed1, pos2, course2, speed2, 1000010086312797)
#     pass


# if __name__ == '__main__':
#     main()
    