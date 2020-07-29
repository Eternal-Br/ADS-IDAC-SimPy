"""
Trans Between Coordinate and Distance 
提供经度差、纬度差转化为距离的函数
提供距离转化为经度差、纬度差的函数
"""
from math import cos, pi


def DeltaLat2DeltaMeter(DeltaLat):
    """ 
    将纬度差转换为距离差(单位:米), 1′纬度取平均值1852m.
    : DeltaLat: 纬度差,
    : return DeltaMeter.
    """
    DeltaMeter = DeltaLat * 111120 
    return DeltaMeter


def DeltaLon2DeltaMeter(DeltaLon, CurrentLat):
    """ 
    将经度差转换为距离差(单位:米), 1′纬度取平均值1852m.
    : DeltaLat: 纬度差,
    : CurrentLat: 当前实际纬度,
    : return DeltaMeter.
    """
    DeltaMeter = DeltaLon * 111 * cos(CurrentLat * pi / 180) * 1000
    return DeltaMeter


def DeltaMeter2DeltaLat(DeltaMeter):
    """ 
    将距离差转化为纬度差 
    """
    DeltaLat = DeltaMeter / 111120
    return DeltaLat


def DeltaMeter2DeltaLon(DeltaMeter, CurrentLat):
    """ 
    将距离差转化为经度差 
    """
    DeltaLon = DeltaMeter / (111 * cos(CurrentLat * pi / 180) * 1000)
    return DeltaLon


def TransGCS2CCS(pos1,course1,speed1,pos2,course2,speed2):
    """ 
    Transform Geographical Coordinate System to Cartesian Coordinate System
    以ship1的pos1为参考系原点, 将地理坐标系中的参数转化为笛卡尔(直角)坐标系中
    pos2 = [pos2[0]-pos1[0], pos2[1]-pos1[1]], 再将pos2进行TransBCD转换
    pos1 = [0,0]
    """
    pos2 = [
        DeltaLon2DeltaMeter(pos2[0]-pos1[0], pos2[1]),
        DeltaLat2DeltaMeter(pos2[1]-pos1[1])
    ]
    # print("pos2转化之后: ", pos2)
    pos1  = [0, 0]
    return pos1,course1,speed1,pos2,course2,speed2


# print(DeltaLon2DeltaMeter(1/60, 30))