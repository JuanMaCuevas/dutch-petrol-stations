import requests
import csv 
import math


def main():
	felipes=[52.392692,4.643914]
	julitas =[52.3784493,4.8054312]
	stations = load_stations(True)
	
	stations = sort_by_diesel_price(stations)
	
	stations = append_distance_to_point(stations,felipes)
	stations = sort_by_distance(stations)
	
	nearby = stations[:200]

	nearby = append_price_approx(nearby,10,60)
	nearby.sort(key = lambda s: s[-1])

	nearby=nearby[:10]
	low = min([x[-1] for x in nearby])
	high = max([x[-1] for x in nearby])
	for s in nearby:
		kms= s[-2]
		price = float(s[2])
		ratio = s[-1]
		print(f'{kms:.2f} {price:.2f} {ratio:.2f}',maps_url(s))
	




def key(k,lis):
	return lis[0].index(k)

def append_distance_to_point(stations,point):
	return [x+[distance_points(point,[float(i) for i in x[:2]])] for x in stations[1:]] 

def load_stations(onlineTrue):
	if onlineTrue:
		text = requests.get('http://fuel.juanma.nl/stations.csv').text.splitlines()
	else:
		text = open('data/stations.csv','r').readlines()
	stations = csv.reader(text, delimiter=',')
	return [x for x in stations][1:]

maps_url = lambda s: f'https://www.google.es/maps/@{s[0]},{s[1]},300m/data=!3m1!1e3?hl=es'
brand_url = lambda s:f'https://www.brandstof-zoeker.nl/station/{s[4]}'

def sort_by_distance(s):
	s.sort(key = lambda s: s[-1])
	return s

def sort_by_diesel_price(s):
	s=[x for x in s if x[2]!='']
	s.sort(key = lambda s: s[2])

	return s

def ratio(g):
	dist = g[-1]*2
	price = float(g[2])
	tank = 80
	liters100km = 10
	return (price*(tank+dist*liters100km/100))+g[-1]*0.5

def append_price_approx(s,liters_per100km,tank_size_liters):

	return [x+[ratio(x)] for x in s] 





def getSet(k,lis):
	s=set(x[key(k,lis)].lower() for x in lis[1:])
	s.remove('')
	return sorted(list(s))

def distance_points(a,b):
	# print(a,b)
	return haversine(a[0],a[1],b[0],b[1])

def haversine(lon1, lat1, lon2, lat2):
	"""
	Calculate the great circle distance between two points 
	on the earth (specified in decimal degrees)
	"""
	# convert decimal degrees to radians 
	lon1, lat1, lon2, lat2 = map(math.radians, [lon1, lat1, lon2, lat2])

	# haversine formula 
	dlon = lon2 - lon1 
	dlat = lat2 - lat1 
	a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
	c = 2 * math.asin(math.sqrt(a)) 
	r = 6371 # Radius of earth in kilometers. Use 3956 for miles
	return c * r  




def summary(stations):
	fields = ['price_diesel', 'price_euro95', 'chain', 'place', 'updated_diesel', 'updated_euro95']
	for f in fields:
		print(f)
		print(getSet(f,stations))
		print()


main()


# stations = [x for x in stations if x[9].lower()=='haarlem' and x[2]!='']
# stations.sort(key = lambda stations: stations[2]) 

# for s in stations:
#   print(f'https://www.google.es/maps/@{s[0]},{s[1]},300m/data=!3m1!1e3?hl=es https://www.brandstof-zoeker.nl/station/{s[4]} {s[2]}')
