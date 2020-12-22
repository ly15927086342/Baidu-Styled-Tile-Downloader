#coding = 'utf-8'

from TileDownloader import *
from config import *

# 程序主函数
if __name__ == '__main__':

	TD = TileDownloader(
		type = TARGET_TYPE,
		style = MY_STYLE,
		adName = TARGET_NAME,
		adCode = TARGET_CODE,
		level = TARGET_LEVEL,
		dir_path = ROOT_DIR,
		target = TARGET_OBJECT,
		levelControl = AUTO_LEVEL,
		saveTile = SAVE_TILE,
		drawBoundary = B_ISDRAW,
		boundaryStyle = B_STYLE)

	TD.run()