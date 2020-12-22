#coding = 'utf-8'

# 中国行政区及对应编码

import requests

AD = requests.get('https://geo.datav.aliyun.com/areas_v2/bound/all.json').json()

class ChinaAD:

	def __init__(self):
		if len(AD) <= 0:
			raise Exception("无法获取行政区划列表，请检查网络或接口")
		self.urlTemplate = 'https://geo.datav.aliyun.com/areas_v2/bound/{0}.json'

	def checkPath(self, list, id, code):
		if id >= len(list):
			return True
		else:
			for item in AD:
				if code == item['adcode']:
					parent = item['name']
					pcode = item['parent']
			if list[id] in parent:
				return self.checkPath(list, id+1, pcode)
			return False

	def adPropertyToUrl(self, code=None, name=None):
		if code:
			for item in AD:
				if code == item['adcode']:
					return [self.urlTemplate.format(code), item['name'], code]
			else:
				print('行政区号不完整或不存在')
				return [False,name,code]
		elif name:
			ind = 0
			li = []
			for i in range(0,len(name)):
				if name[i] in '省市区县':
					li.append(name[ind:i+1])
					ind = i+1
			li.reverse()
			if len(li) == 0:
				li.append(name)
			code = []
			for item in AD:
				if li[0] in item['name']:
					if self.checkPath(li,1,item['parent']):
						code.append([self.urlTemplate.format(item['adcode']), name, item['adcode']])
			if len(code) == 0:
				print('行政区名不完整或不存在')
				return [False,name,code]
			elif len(code) == 1:
				return code[0]
			else:
				print(name+'对应多个区划，请选择一个重新运算')
				print('|'.join([str(item[2]) for item in code]))
				return [False,name,code]
		print('缺少行政区划名或区号')
		return [False,name,code]
			
