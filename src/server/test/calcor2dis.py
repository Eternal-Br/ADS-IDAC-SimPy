import re
from numpy import cos, pi


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


with open('./content.txt', 'r') as f:
    content = f.read()
# print(content)

# 使用正表达式匹配出经纬度坐标
pattern_lon  = re.compile('.*?"lon": (.*?), "lat"', re.S)
pattern_lat  = re.compile('.*?"lat": (.*?), "speed"', re.S)
result_lon = re.findall(pattern_lon, content)
result_lat = re.findall(pattern_lat, content)
# print('result_lon: ', result_lon)
# print('result_lat: ', result_lat)


# 使用 map 函数做转换，将经纬度坐标的字符串转化为浮点型
def str2float(str_num):
    return float(str_num)

# 得到的是个可迭代的对象
lon_cor = list(map(str2float, result_lon))
lat_cor = list(map(str2float, result_lat))
# print(lon_cor)

lon_num = []
# lat_num = []

lat_num = list(map(DeltaLat2DeltaMeter, lat_cor))
# print(lat_num)

for idx, item in enumerate(lon_cor):
    # print(item, idx)
    bar = DeltaLon2DeltaMeter(item, lat_cor[idx])
    lon_num.append(bar)
# print(len(lon_num))
# lon_num
sorted_lon_num = sorted(lon_num)
# print(sorted_lon_num)

sorted_lat_num = sorted(lat_num)
# print(sorted_lat_num)



# with open('./case_cor2num.txt', 'a') as fs:
#     # fs.write('lon_cor: \n')
#     # fs.write(str(lon_cor) + '\n')
#     # fs.write('lat_cor: \n')
#     # fs.write(str(lat_cor) + '\n')
#     # fs.write('lon_num: \n')
#     # fs.write(str(lon_num) + '\n')
#     # fs.write('lat_num: \n')
#     # fs.write(str(lat_num) + '\n')
#     fs.write('sorted_lon_num: \n')
#     fs.write(str(sorted_lon_num) + '\n')
#     fs.write('sorted_lat_num: \n')
#     fs.write(str(sorted_lat_num) + '\n')
# print('write it.')

def work_line(input_x, input_y):
    min_x = 11705648
    min_y = 3444255
    x = (input_x - min_x) / 5.5
    y = (input_y - min_y) / 5.5
    # print(x, y)
    return x, y

ax_x = []
ax_y = []

for idx, item in enumerate(lon_num):
    sx, sy = work_line(item, lat_num[idx])
    ax_x.append(sx)
    ax_y.append(sy)
# print(len(ax_x))
# print(len(ax_y))

# from matplotlib import pyplot as plt

# plt.figure()
# plt.plot(ax_x, ax_y, 'r+')
# plt.show()


def TransGCS2SCS(gc_lon, gc_lat):
    # Trans Geographical Coordinate System to Screen Coordinate System according to  DF's needs.
    # Screen Coordinate System limits: x- 400, y- 1200
    # gc_lon: lon in Geographical Coordinate System like 123.12
    # gc_lat: lat in Geographical Coordinate System like 31.003

    # min_x and min_y are offsets/bias, and they only work well in this case.
    min_x = 11705648 
    min_y = 3444255
    # then Zoom out the offset coordinates 
    zoom_rate = 5.5
    lon = (DeltaLon2DeltaMeter(gc_lon, gc_lat) - min_x) / zoom_rate
    lat = (DeltaLat2DeltaMeter(gc_lat) - min_y) / zoom_rate
    # print(lon, lat)
    return lon, lat

# TransGCS2SCS(123.0715063832908, 31.005239585423563)
# TransGCS2SCS(123.09905697168907, 31.005239585423563)
# TransGCS2SCS(123.07195143492459, 31.01272693414327, )

