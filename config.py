#coding = 'utf-8'

'''
配置文件
'''

# style规则参考./README.md
MY_STYLE = [
{
"featureType": "all",
"elementType": "labels",
"stylers": {
"visibility": "off"
}
},
{
"featureType": "road",
"elementType": "all",
"stylers": {
"visibility": "on"
}
},
{
"featureType": "background",
"elementType": "all",
"stylers": {
"color": "#ffffffff"
}
},
{
"featureType": "road",
"elementType": "all",
"stylers": {
"color": "#000000ff"
}
}]

# 行政区名
TARGET_NAME = None

# 行政区号
TARGET_CODE = None

# 根目录
ROOT_DIR = './res'

# 4-18，不同要素显示等级不同，参考README.md
TARGET_LEVEL = 17

# 是否保留瓦片
SAVE_TILE = False

# 爬遥感影像时level是否由系统决定
AUTO_LEVEL = False

# 目标突出要素，如果没有就填''
TARGET_OBJECT = 'RS'

# 个性地图0；遥感影像1
TARGET_TYPE = 1

# 是否绘制边界
B_ISDRAW = True

# 边界的样式
B_STYLE = {
	'color': (0,0,255),# BGR顺序，即(blue, green, red)，颜色值0-255
	'thick': 5 #线宽
}

# 矩形范围还是行政区,0：矩形，1：行政区
RECT_OR_DISTRICT = 0

# 矩形范围,西南和东北角经纬度WGS84坐标
RECT_BOX = \
[(114.343750484277,30.522583309109),
(114.378917150943,30.562583309109)]