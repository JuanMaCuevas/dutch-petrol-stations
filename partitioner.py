
def encode_params(area,type_gas):
	import urllib.parse
	position = {'left':area[0][1],'right':area[1][1],'bottom':area[0][0],'top':area[1][0],'type':type_gas }
	return urllib.parse.urlencode(position)

def list_stations_from_xml(text):
	from xml.etree import ElementTree
	xml=ElementTree.fromstring(text)
	return [marker.attrib for marker in xml.findall('marker')]

def request_list_stations_in_area(area,type_fuel):
	import requests
	url = f'https://www.brandstof-zoeker.nl/getxml.fcgi?{encode_params(area,type_fuel)}'
	headers =  {'Connection':'keep-alive','Accept':'application/xml, text/xml, */*; q=0.01','X-Requested-With':'XMLHttpRequest','Sec-Fetch-Mode':'cors','Sec-Fetch-Site':'same-origin',	'Referer':'https://www.brandstof-zoeker.nl/',}
	response = requests.get(url, headers=headers)
	return list_stations_from_xml(response.text)

def request_stations_online(area):
	return [request_list_stations_in_area(area,'Euro 95'),
			request_list_stations_in_area(area,'Diesel')]

def nine_points(area):
	# 0 1 2
	# 3 4 5
	# 6 7 8
	# (yb,xa)       (yb,xa+w)       (yb,xb)
	# (ya+h,xa)     (ya+h,xa+w)     (ya+h,xb)
	# (ya,xa)       (ya,xa+w)       (ya,xb)
	xa=area[0][1]
	xb=area[1][1]
	ya=area[1][0]
	yb=area[0][0]
	w=abs(xb-xa)/2
	h=abs(yb-ya)/2
	return [(yb,xa),(yb,xa+w),(yb,xb),(ya+h,xa),(ya+h,xa+w),(ya+h,xb),(ya,xa),(ya,xa+w),(ya,xb)] 

def is_portrait(area):
	return abs(area[1][1]-area[0][1])/2>abs(area[0][0]-area[1][0])/2

def divide_two(area):
	nine = nine_points(area)
	if is_portrait(area):
		return [[nine[0],nine[7]],[nine[1],nine[8]]]
	else:
		return [[nine[0],nine[5]],[nine[3],nine[8]]]
	
def areaSize(area):
	return abs(area[1][1]-area[0][1]) * abs(area[0][0]-area[1][0])

def save_data(data):
	import pickle
	# open a file, where you ant to store the data
	file = open('areas.dat', 'wb')
	# dump information to that file
	pickle.dump(data, file)
	# close the file
	file.close()


def process_area(init_area):
	process = [init_area]
	areas = []
	total = areaSize(process[0])
	sumSize = 0

	queriesNow = 0
	queriesLater = 0 

	while process:
		print(f'{sumSize*100/total}% {queriesNow} {queriesLater}')
		area = process.pop(0)
		items = query_points(area)
		count = max(len(items[0]),len(items[1]))
		print(f'counts {len(items[0])} {len(items[1])} ')
		queriesNow+=2
		queriesLater+=2
		if count==0:
			sumSize+=areaSize(area)
			queriesLater-=2
			continue
		if count<100:
			areas.append([area,count,items])
			save_data(areas)
			print(f'added {count} in {area}')
			sumSize+=areaSize(area)
			continue
		queriesLater-=2
		process=process+divide_two(area)

def calculate_min_list_areas(init_area):
	process = [init_area]
	areas = []
	queries = 0
	while process:
		area = process.pop(0)
		items = request_stations_online(area)
		count = max(len(items[0]),len(items[1]))
		queries+=2
		if count>=100:
			process=process+divide_two(area)
		elif count>0:
			areas.append([area,count])
		print(f'{queries} queries\t{len(process)} left')
	return areas #[[area,count],...]
		
def save_min_areas_csv(areas):
	import csv
	with open('partitions.csv', mode='w') as partitions_file:
		writer = csv.writer(partitions_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
		for area in areas:
			count = area[1]
			area=area[0]
			writer.writerow([area[0][0],area[0][1],area[1][0],area[1][1],count])

topLeft = [53.5005991,3.3571575]
bottomRight = [50.7501736,7.2313807]
init_area = [topLeft,bottomRight]
areas = calculate_min_list_areas(init_area)
save_min_areas_csv(areas)
# areas[
# [topleft,bottomright]
	#max(count)
	# [
	# items euro 95
	# items diesel
	# ]
# ]
