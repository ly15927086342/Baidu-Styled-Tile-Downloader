#coding = 'utf-8'

from utils.ChinaAD import *
from utils.CoordTransform import *
from utils.TileXY import *
from utils.getBounds import *
from utils.LngLatToPixel import RegionToPixels
from utils.drawBoundary import drawPoly
from queue import Queue
from PIL import Image
import time
import requests
import random
import json
import os
import threading

'''
核心类
'''
class  TileDownloader(object):
	# @param type [0:个性地图栅格瓦片；1:遥感影像栅格瓦片]
	# @param style [个性地图style json]
	# @param AD [行政区划完整名称，如果是某个区，需要带上市，具体命名见ChinaAD.py]
	# @param dir_path [输出文件的文件夹路径]
	# @param target [突出要素的名称，可不写，只和输出文件名有关]
	# @param level [地图的比例尺]
	# @param scale [图片放大倍数，1为正常大小（256*256）]
	def __init__(self, type = 0, style = [], adCode = None, adName = None, dir_path = './',\
		target = '' , level = 15, levelControl = False, scale = 1, drawBoundary = False, \
		boundaryStyle = {}, saveTile = True):
		super( TileDownloader, self).__init__()
		self.type = type
		self.style = style
		self.adCode = adCode
		self.adName = adName
		self.dir = dir_path
		self.level = level
		self.levelControl = levelControl
		self.scale = scale
		self.isDraw = drawBoundary
		self.b_style = boundaryStyle
		self.tile_list = []
		self.saveTile = saveTile
		self.Task = Queue()
		self.thread_pool = []
		self.target_obj = target
		self.THREAD_MAX = 2

	def run(self):

		self.getTime()

		print('-----开始获取行政区-----')
		[url, self.adName, self.adCode] = ChinaAD().adPropertyToUrl(name = self.adName, code = self.adCode)
		if(url == False):
			exit(0)
		print(self.adName + ':' + str(self.adCode))
		self.region = json.loads(requests.get(url).text)
		self.bounds = getBounds(self.region)
		print('-----行政区获取完毕-----')

		print('-----地图样式生成-----')
		self.generateStyle()
		print('-----样式生成完毕-----')


		print('-----经纬度转瓦片号-----')
		self.swTile = WGS84_to_TILE(self.bounds['southwest'][0],self.bounds['southwest'][1],self.level)
		self.neTile = WGS84_to_TILE(self.bounds['northeast'][0],self.bounds['northeast'][1],self.level)
		self.getTiles(self.swTile,self.neTile)
		# 遥感影像，且瓦片数量超过500，缩小level
		while self.levelControl and len(self.tile_list) > 500:
			self.level = self.level - 1
			self.swTile = WGS84_to_TILE(self.bounds['southwest'][0],self.bounds['southwest'][1],self.level)
			self.neTile = WGS84_to_TILE(self.bounds['northeast'][0],self.bounds['northeast'][1],self.level)
			self.getTiles(self.swTile,self.neTile)
		print('-----瓦片号获取完毕-----')


		print('-----检查文件夹路径-----')
		doDownload = self.checkParms()
		print('-----路径检查完毕-----')


		if doDownload:
			print('-----多线程爬取瓦片-----')
			self.openThread()
			print('-----瓦片爬取完毕-----')


		print('-----图片开始合成-----')
		self.generatePic()
		print('-----图片合成完毕-----')


		if self.isDraw:
			print('-----绘制行政边界-----')
			polys = RegionToPixels(self.region['features'][0]['geometry']['coordinates'],self.level,self.swTile,self.neTile)
			drawPoly(self.dir + 'result.jpg', polys, self.b_style)
			print('-----边界绘制完毕-----')


		print('-----打印日志-----')
		self.log()
		print('-----程序结束-----')

	def openThread(self):
		print('瓦片总量：' + str(len(self.tile_list)))
		for tilexy in self.tile_list:
			if self.type == 0:
				self.Task.put({
					'x':tilexy[0],
					'y':tilexy[1],
					'z':self.level,
					'udt':self.time,
					'scale':self.scale,
					'ak':'8d6c8b8f3749aed6b1aff3aad6f40e37',
					'styles':self.style_str
					})
			else:
				self.Task.put({
					'qt':'satepc',
					'u':'x=%s;y=%s;z=%s;v=009;type=sate'%(tilexy[0],tilexy[1],self.level),
					'udt':self.time,
					'app':'webearth2',
					'fm':46,
					'x':tilexy[0],
					'y':tilexy[1]
					})

		for i in range(0,self.THREAD_MAX):
			t = threading.Thread(target=self.spideTile)
			t.start()
			self.thread_pool.append(t)

		# 阻塞线程
		for thread in self.thread_pool:
			thread.join()
		self.thread_pool.clear()

	# 记录失败链接、图片的范围等信息至dir/log.txt
	def log(self):
		t = time.localtime()
		with open(self.dir + 'log.txt', 'a', encoding='utf-8') as file:
			file.write(self.adName + '.jpg信息:\n')
			file.write('目标突出要素：' + self.target_obj + '\n')
			file.write('时间：' + '.'.join([str(t.tm_year),str(t.tm_mon),str(t.tm_mday)]) + ' ' + ':'.join([str(t.tm_hour),str(t.tm_min),str(t.tm_sec)]) + '\n')
			file.write('等级：' + str(self.level) + '\n')
			file.write('瓦片范围：' + str(self.swTile[0]) + '_' + str(self.swTile[1]) + '-' + str(self.neTile[0]) + '_' + str(self.neTile[1]) + '\n')
			file.write('瓦片数量：' + str(len(self.tile_list)) + '\n')
			file.write('经纬度范围：' + str(self.bounds['southwest'][0]) + '_' + str(self.bounds['southwest'][1]) + '-' + str(self.bounds['northeast'][0]) + '_' + str(self.bounds['northeast'][1]) + '\n')
			file.write('样式信息：' + str(self.style)+ '\n') 
			file.write('压缩样式信息：' + str(self.style_str)+ '\n') 
			file.write('行政区json：' + json.dumps(self.region))
			file.write('\n')

	# 图片生成
	def generatePic(self):
		res = Image.new('RGB', (256*(self.neTile[0]-self.swTile[0]+1), 256*(self.neTile[1]-self.swTile[1]+1)))
		for fn in os.listdir(self.dir + 'tiles/'):
			if fn.endswith('.jpg'):
				try:
					im = Image.open(self.dir + 'tiles/' + fn)
					[x, y] = fn.split('.')[0].split('_')
					res.paste(im, box=((int(x)-self.swTile[0])*256,(self.neTile[1]-int(y))*256))
				except:
					pass
		# 保存图片
		res.save(self.dir + 'result.jpg')
		# 无需保留瓦片，则清空
		if not self.saveTile:
			ts = os.listdir(self.dir+'tiles/')
			for t in ts:
				os.remove(self.dir+'tiles/' + t)
			os.rmdir(self.dir+'tiles/')

	# 检查文件夹路径，返回True，需要下载瓦片，返回False，不需要下载瓦片
	def checkParms(self):
		if not self.type in [0,1]:
			print('type只能是0或1')
			exit(0)
		if self.level < 3 or self.level > 18:
			print('地图比例尺范围必须在3-18之间')
			exit(0)

		if(not self.dir[-1:]=='/'):
			self.dir = self.dir + '/' + '_'.join([self.adName,self.target_obj,str(self.level)]) + '/'

		if(not os.path.exists(self.dir)):
			try:
				os.makedirs(self.dir)
			except:
				raise Exception("文件夹路径格式错误或非文件夹")
		else:
			ts = os.listdir(self.dir+'tiles/')
			if len(ts) != len(self.tile_list):
				for t in ts:
					os.remove(self.dir+'tiles/' + t)
			else:# 瓦片已经下载过了，不用重新下
				return False
		if(not os.path.exists(self.dir + 'tiles/')):
			try:
				os.makedirs(self.dir + 'tiles/')
			except:
				raise Exception("文件夹路径格式错误或非文件夹")
		return True

	# 获取当前时间，格式 yyyymmdd
	def getTime(self):
		t = time.localtime(time.time())
		year = str(t.tm_year)
		mon = ('0'+str(t.tm_mon)) if t.tm_mon<10 else str(t.tm_mon)
		day = ('0'+str(t.tm_mday)) if t.tm_mday<10 else str(t.tm_mday)
		self.time = year + mon + day

	# 爬取瓦片
	def spideTile(self):
		while (not self.Task.empty()):
			params = self.Task.get()
			if self.type == 0:
				target_url = 'https://api.map.baidu.com/customimage/tile/'
			else:
				target_url = 'https://maponline'+str(random.choice([1,2,3]))+'.bdimg.com/starpic/'
			try:
				html = requests.get(url=target_url, params=params, timeout=5)
				with open(self.dir + 'tiles/' + str(params['x']) + '_' + str(params['y']) +'.jpg', 'wb') as file:
					file.write(html.content)
					file.close()
				print(str(params['x']),str(params['y']),'finish','剩余task:',str(self.Task.qsize()))
			except:
				self.Task.put(params)
		
	# 获取所有待爬瓦片号
	def getTiles(self,swTile,neTile):
		self.tile_list = []
		for lng in range(swTile[0],neTile[0]+1):
			for lat in range(swTile[1],neTile[1]+1):
				self.tile_list.append([lng,lat])

	# 生成压缩style样式字符串
	def generateStyle(self):
		res = ''
		for feature in self.style:
			f_list = []
			for key in feature.keys():
				if(type(feature[key])==dict):
					for inner_key in feature[key].keys():
						f_list.append(self.processLabel(inner_key) + ':' + self.processLabel(feature[key][inner_key]))
				else:
					f_list.append(self.processLabel(key) + ':' + self.processLabel(feature[key]))
			res = res + '|'.join(f_list) + ','
			f_list.clear()
		self.style_str = res

	# 压缩规则
	def processLabel(self,name):
		res = str(name)
		if(res=='featureType'):
			res = 't'
		elif(res=='elementType'):
			res = 'e'
		elif(res=='labels'):
			res = 'l'
		elif(res=='geometry'):
			res = 'g'
		elif(res=='visibility'):
			res = 'v'
		elif(res=='color'):
			res = 'c'
		elif(res=='hue'):
			res = 'h'
		elif(res=='weight'):
			res = 'w'
		elif(res=='lightness'):
			res = 'l'
		elif(res=='saturation'):
			res = 's'
		else:
			pass
		return res
