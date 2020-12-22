#coding = 'utf-8'

from utils.CoordTransform import LngLatTransfer
# from pyproj import Transformer
import math

# wgs84坐标转百度地图瓦片编号xy
# 公式参考http://cntchen.github.io/2016/05/09/%E5%9B%BD%E5%86%85%E4%B8%BB%E8%A6%81%E5%9C%B0%E5%9B%BE%E7%93%A6%E7%89%87%E5%9D%90%E6%A0%87%E7%B3%BB%E5%AE%9A%E4%B9%89%E5%8F%8A%E8%AE%A1%E7%AE%97%E5%8E%9F%E7%90%86/

# transformer = Transformer.from_crs(4326, 3857)

def WGS84_to_TILE(lng, lat, level):
	[pointX,pointY] = LngLatTransfer().WGS84_to_WebMercator(lng,lat)
	# print(transformer.transform(lat,lng))
	# pointX,pointY = transformer.transform(lat,lng)
	# print(pointX,pointY)
	tileX = math.floor(pointX*(math.pow(2,level-18))/256)
	tileY = math.floor(pointY*(math.pow(2,level-18))/256)
	return [tileX,tileY]