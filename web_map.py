'''
This is a program for making an interactive map for showing locations of Serbian cities.
'''

import pandas
import folium

cities = pandas.read_csv("RS_Cities.txt")
lat = list(cities['lat'])
lon = list(cities['lng'])
pop = list(cities['population'])

def color_produces(population):
    if population < 50000:
        return 'green'
    elif 50000 <= population < 500000:
        return 'orange'
    elif 500000 <= population:
        return 'red'
    else:
        return 'blue'

def radius_produces(population):
    if population < 50000:
        return 4
    elif 50000 <= population < 500000:
        return 5
    elif 500000 <= population:
        return 6
    else:
        return 3


map = folium.Map(location=[44.0128, 20.9114], zoom_start=7)
fgv = folium.FeatureGroup(name='Serbian cities')
for lt, ln, po in zip(lat, lon, pop):
    fgv.add_child(folium.CircleMarker(location=[lt, ln], popup=folium.Popup(str(po) + 'm', parse_html=True),fill = True,
                                     fill_color=color_produces(po), fill_opacity = 0.7, radius = radius_produces(po), color = 'gray',
                                     weight = 1.0))
map.add_child(fgv)
fgp = folium.FeatureGroup(name='Country borders')
fgp.add_child(folium.GeoJson(data=open("world.json", 'r', encoding='utf-8-sig').read(), style_function=lambda
    x:{'fillColor':'green' if x['properties']['POP2005']<10000000 else
'orange' if 10000000 <=x['properties']['POP2005']<20000000 else 'red'}))
map.add_child(fgp)
map.add_child(folium.map.LayerControl(position='topright', collapsed=True, autoZIndex=True))
map.save("Map.html")