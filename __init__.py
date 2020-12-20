#coding = 'utf-8'

from TileDownloader import *
from config import *

# 程序主函数
if __name__ == '__main__':

	TD = TileDownloader(
		type = TARGET_TYPE,
		style = MY_STYLE,
		AD = TARGET_AD,
		level = TARGET_LEVEL,
		dir_path = ROOT_DIR,
		target = TARGET_OBJECT,
		drawBoundary = B_isDraw,
		boundaryStyle = B_style)

	TD.run()