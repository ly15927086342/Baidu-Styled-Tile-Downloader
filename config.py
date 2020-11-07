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
"featureType": "water",
"elementType": "all",
"stylers": {
"color": "#0000ffff"
}
}]

# 行政区划名称参考./ChinaAD.py
TARGET_AD = '武汉市武昌区'

# 根目录
ROOT_DIR = './example'

# 4-18，不同要素显示等级不同，参考README.md
TARGET_LEVEL = 15

# 目标突出要素，如果没有就填''
TARGET_OBJECT = '水体'