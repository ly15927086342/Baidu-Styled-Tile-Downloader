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
"visibility": "off"
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
"featureType": "manmade",
"elementType": "all",
"stylers": {
"color": "#000000ff"
}
}]

# 行政区划名称参考./ChinaAD.py
TARGET_AD = '北京市朝阳区'

# 根目录
ROOT_DIR = './example'

# 4-18，不同要素显示等级不同，参考README.md
TARGET_LEVEL = 14

# 目标突出要素，如果没有就填''
TARGET_OBJECT = '遥感'

# 个性地图0；遥感影像1
TARGET_TYPE = 1

# 是否绘制边界
B_isDraw = True

# 边界的样式
B_style = {
	'color': (0,255,0),# BGR顺序，即(blue, green, red)，颜色值0-255
	'thick': 2 #线宽
}