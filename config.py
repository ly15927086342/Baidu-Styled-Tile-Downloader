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
TARGET_NAME = '北京市朝阳区'

# 行政区号
TARGET_CODE = None

# 根目录
ROOT_DIR = './example'

# 4-18，不同要素显示等级不同，参考README.md
TARGET_LEVEL = 13

# 是否保留瓦片
SAVE_TILE = False

# 爬遥感影像时level是否由系统决定
AUTO_LEVEL = True

# 目标突出要素，如果没有就填''
TARGET_OBJECT = '道路'

# 个性地图0；遥感影像1
TARGET_TYPE = 1

# 是否绘制边界
B_ISDRAW = True

# 边界的样式
B_STYLE = {
	'color': (0,0,255),# BGR顺序，即(blue, green, red)，颜色值0-255
	'thick': 5 #线宽
}