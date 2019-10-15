
def load_areas_csv():
	import csv
	with open('partitions.csv') as csv_file:
		csv_reader = csv.reader(csv_file, delimiter=',')
		line_count = 0
		areas=[]
		for row in csv_reader:
			areas.append(row)	
			line_count += 1
		print(f'partitions.csv has {line_count} areas.')
		return areas

def plot_areas(data):
	import folium
	nlMap = folium.Map(location=[52.228175,5.3473425], tiles='Stamen Toner', zoom_start=6)
	points = []
	for area in data:
		points.append(area[0][0])
		points.append(area[0][1])
		col='white'
		if area[1]>66:
			col='red'
		elif area[1]>33:
			col = "yellow"
		else:
			col = "green"
		folium.Rectangle(points,color=col,opacity=1,fill=True).add_to(nlMap)
		points=[]
	nlMap.save('laPointMap.html')


def plot_areas_map(areas):
	import folium	
	nlMap = folium.Map(location=[52.228175,5.3473425], tiles='Stamen Toner', zoom_start=6)
	points = []
	for area in areas:
		area = [float(x) for x in area]
		p=[[area[0],area[1]],[area[2],area[3]]]
		points.append(p[0])
		points.append(p[1])
		col='white'	
		if area[-1]>66:
			col='red'
		elif area[-1]>33:
			col = "yellow"
		else:
			col = "green"
		folium.Rectangle(points,color=col,opacity=1,fill=True).add_to(nlMap)
		points=[]

	nlMap.save('map.html')
	print('open map.html')


areas = load_areas_csv()
plot_areas_map(areas)