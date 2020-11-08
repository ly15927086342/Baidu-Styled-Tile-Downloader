#coding = 'utf-8'

from ChinaAD import *
from CoordTransform import *
from TileXY import *
from getBounds import *
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
	def __init__(self, style = [], AD = '', dir_path = './', target = '' , level = 15, scale = 1):
		super( TileDownloader, self).__init__()
		self.style = style
		self.AD = AD
		self.dir = dir_path
		self.level = level
		self.scale = scale
		self.tile_list = []
		self.Task = Queue()
		self.thread_pool = []
		self.fail_list = []
		self.target_obj = target
		self.THREAD_MAX = 10

	def run(self):
		self.getTime()
		print('-----地图样式生成-----')
		self.generateStyle()
		print('-----样式生成完毕-----')


		print('-----开始获取行政区-----')
		url = ChinaAD().ADName_to_Url(self.AD)
		if(url == False):
			exit(0)
		self.region = json.loads(requests.get(url).text)
		self.bounds = getBounds(self.region)
		print('-----行政区获取完毕-----')


		print('-----检查文件夹路径-----')
		self.checkParms()
		print('-----路径检查完毕-----')
		

		print('-----经纬度转瓦片号-----')
		self.swTile = WGS84_to_TILE(self.bounds['southwest'][0],self.bounds['southwest'][1],self.level)
		self.neTile = WGS84_to_TILE(self.bounds['northeast'][0],self.bounds['northeast'][1],self.level)
		print('-----瓦片号获取完毕-----')


		print('-----多线程爬取瓦片-----')
		self.getTiles(self.swTile,self.neTile)
		for tilexy in self.tile_list:
			self.Task.put({
				'x':tilexy[0],
				'y':tilexy[1],
				'z':self.level,
				'udt':self.time,
				'scale':self.scale,
				'ak':'8d6c8b8f3749aed6b1aff3aad6f40e37',
				'styles':self.style_str
				})
		for i in range(0,self.THREAD_MAX):
			t = threading.Thread(target=self.spideTile)
			t.start()
			self.thread_pool.append(t)
		# 阻塞线程
		for thread in self.thread_pool:
			thread.join()
		self.thread_pool.clear()
		print('-----瓦片爬取完毕-----')


		print('-----图片开始合成-----')
		self.generatePic()
		print('-----图片合成完毕-----')


		print('-----打印日志-----')
		self.log()
		print('-----程序结束-----')

	# 记录失败链接、图片的范围等信息至dir/log.txt
	def log(self):
		t = time.localtime()
		with open(self.dir + 'log.txt', 'a', encoding='utf-8') as file:
			file.write(self.AD + '.jpg信息:\n')
			file.write('目标突出要素：' + self.target_obj + '\n')
			file.write('时间：' + '.'.join([str(t.tm_year),str(t.tm_mon),str(t.tm_mday)]) + ' ' + ':'.join([str(t.tm_hour),str(t.tm_min),str(t.tm_sec)]) + '\n')
			file.write('等级：' + str(self.level) + '\n')
			file.write('瓦片范围：' + str(self.swTile[0]) + '_' + str(self.swTile[1]) + '-' + str(self.neTile[0]) + '_' + str(self.neTile[1]) + '\n')
			file.write('瓦片数量：' + str(len(self.tile_list)) + '\n')
			file.write('经纬度范围：' + str(self.bounds['southwest'][0]) + '_' + str(self.bounds['southwest'][1]) + '-' + str(self.bounds['northeast'][0]) + '_' + str(self.bounds['northeast'][1]) + '\n')
			file.write('样式信息：' + str(self.style)+ '\n') 
			file.write('压缩样式信息：' + str(self.style_str)+ '\n') 
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

	# 检查文件夹路径
	def checkParms(self):
		if(not self.dir[-1:]=='/'):
			self.dir = self.dir + '/' + '_'.join([self.AD,self.target_obj]) + '/'
		if(not os.path.exists(self.dir)):
			try:
				os.makedirs(self.dir)
			except:
				raise Exception("文件夹路径格式错误或非文件夹")
		else:
			for fn in os.listdir(self.dir):
				if fn.endswith('.jpg'):
					raise Exception("目标文件夹下存在图片，请清空文件夹或删除文件夹再运行")
					exit(0)
		if(not os.path.exists(self.dir + 'tiles/')):
			try:
				os.makedirs(self.dir + 'tiles/')
			except:
				raise Exception("文件夹路径格式错误或非文件夹")

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
			url = self.Task.get()
			try:
				html = requests.get(url='http://api1.map.bdimg.com/customimage/tile',params=url)
				with open(self.dir + 'tiles/' + str(url['x']) + '_' + str(url['y']) +'.jpg', 'wb') as file:
					file.write(html.content)
					file.close()
				print(str(url['x']),str(url['y']),'finish')
			except:
				self.Task.put(url)
				self.fail_list.append(url)
			time.sleep(0.5 + random.random()*0.5)
		
	# 获取所有待爬瓦片号
	def getTiles(self,swTile,neTile):
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
