#coding = 'utf-8'

from CoordTransform import LngLatTransfer
from TileXY import WGS84_to_TILE
# from pyproj import Transformer
import numpy as np
import math

# transformer = Transformer.from_crs(4326, 3857)

def WGS84_to_Pixel(lng, lat, level):
	[pointX,pointY] = LngLatTransfer().WGS84_to_WebMercator(lng,lat)
	pixelX = math.floor(pointX*math.pow(2,level-18)-math.floor(pointX*math.pow(2,level-18)/256)*256)
	pixelY = math.floor(pointY*math.pow(2,level-18)-math.floor(pointY*math.pow(2,level-18)/256)*256)
	return [pixelX,pixelY]

def lineString(arr,level,sw,ne):
	res = []
	for p in arr:
		[px,py] = WGS84_to_Pixel(p[0], p[1], level)
		[tx,ty] = WGS84_to_TILE(p[0], p[1], level)
		res.append([px+256*(tx-sw[0]),256*(ne[1]-sw[1]+1)-(py+256*(ty-sw[1]))])
	return res

# multipolygon的wgs84坐标转pixel坐标
# 公式参考http://cntchen.github.io/2016/05/09/%E5%9B%BD%E5%86%85%E4%B8%BB%E8%A6%81%E5%9C%B0%E5%9B%BE%E7%93%A6%E7%89%87%E5%9D%90%E6%A0%87%E7%B3%BB%E5%AE%9A%E4%B9%89%E5%8F%8A%E8%AE%A1%E7%AE%97%E5%8E%9F%E7%90%86/
def RegionToPixels(multiPoly,level,sw,ne):
	polys = []
	for poly in multiPoly:
		for singlePoly in poly:
			polys.append(lineString(singlePoly,level,sw,ne))
	return polys