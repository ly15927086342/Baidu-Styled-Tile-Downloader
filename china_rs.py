# coding='utf-8'

from TileDownloader import *
from config import *
import requests
import os

Enter = 'https://geo.datav.aliyun.com/areas_v2/bound/{0}_full.json'

# 迭代爬取各省市的遥感影像
def runIter(p, father, dir):
	url = Enter.format(p['id'])
	res = requests.get(url)
	if res.status_code == 404:
		TD = TileDownloader(
		type = TARGET_TYPE,
		style = MY_STYLE,
		adCode = p['id'],
		level = TARGET_LEVEL,
		dir_path = dir+p['name']+'/',
		target = TARGET_OBJECT,
		levelControl = AUTO_LEVEL,
		saveTile = SAVE_TILE,
		drawBoundary = B_isDraw,
		boundaryStyle = B_style)
		TD.run()
	else:
		Province = []
		if(not os.path.exists(dir+p['name']+'/')):
			try:
				os.makedirs(dir+p['name']+'/')
			except:
				print(dir+p['name']+'/'+'创建失败')
		res = json.loads(res.text)
		for item in res['features']:
			Province.append({
				'id':item['properties']['adcode'],
				'name':item['properties']['name']
				})
		for pro in Province:
			runIter(pro, p, dir+p['name']+'/')
	

# 程序主函数
if __name__ == '__main__':
	china = {
	'id':100000,
	'name':'中华人民共和国'
	}
	runIter(china, {'name':''}, './personal/')