#coding = 'utf-8'

# coordinates只剩一层list
def flatten(arr):
	res = []
	for item in arr:
		if(type(item)==list and type(item[0])==list):
			res = res + flatten(item)
		else:
			res.append(item)
	return res

# region是geojson格式
def getBounds(region):
	a = region['features'][0]['geometry']['coordinates']
	flat_region = flatten(a)
	max_lng = flat_region[0][0]
	max_lat = flat_region[0][1]
	min_lng = flat_region[0][0]
	min_lat = flat_region[0][1]
	for loc in flat_region:
		max_lng = max(max_lng,loc[0])
		max_lat = max(max_lat,loc[1])
		min_lng = min(min_lng,loc[0])
		min_lat = min(min_lat,loc[1])
	return {
	'southwest':[min_lng,min_lat],
	'northeast':[max_lng,max_lat]
	}