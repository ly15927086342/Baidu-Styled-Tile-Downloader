# coding='utf-8'

from TileDownloader import *
from config import *
import requests

def runIter(p):
	

# 程序主函数
if __name__ == '__main__':

	# a = requests.get('https://geo.datav.aliyun.com/areas_v2/bound/632801_full.json')
	# print(a.status_code)
	# exit()
	Enter = 'https://geo.datav.aliyun.com/areas_v2/bound/{0}_full.json'
	res = requests.get(Enter.format(100000)).json()
	Province = []
	for item in res['features']:
		Province.append({
			'id':item['properties']['adcode'],
			'name':item['properties']['name']
			})
	Province.pop()
	for pro in Province:
		url = Enter.format(pro['id'])
		print(url)
		


	# TD = TileDownloader(
	# 	type = TARGET_TYPE,
	# 	style = MY_STYLE,
	# 	AD = TARGET_AD,
	# 	level = TARGET_LEVEL,
	# 	dir_path = ROOT_DIR,
	# 	target = TARGET_OBJECT,
	# 	drawBoundary = B_isDraw,
	# 	boundaryStyle = B_style)

	# TD.run()