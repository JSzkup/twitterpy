import geocoder


g = geocoder.osm('Mountain View, CA') 
#print(g.latlng)
print(g.lat)
print(g.lng)
