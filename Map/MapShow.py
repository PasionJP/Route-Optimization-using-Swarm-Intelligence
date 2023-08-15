# import folium library
import folium
from pyproj import Geod
from geopy.geocoders import Nominatim

def geocodeAddress(Latitude, Longitude):
    geolocator = Nominatim(user_agent="geoapiExercises")
    
    location = geolocator.reverse(Latitude+","+Longitude)
    address = location.raw['address']

    return address

def mapShow(all_route_details, outputName):
    reverseGeocode = []
    lst = all_route_details
    # print("LST", lst)
    point = [lst[0][0][0], lst[0][0][1]]

    pathColors = ['red', 'blue', 'green', 'purple', 'orange', 'darkred', 'lightred', 'beige', 'darkblue', 'darkgreen', 'cadetblue', 'darkpurple', 'white', 'pink', 'lightblue', 'lightgreen']
    # create a map object
    mapObj = folium.Map(location=point, zoom_start=12)
    folium.TileLayer('openstreetmap').add_to(mapObj)
    for r in range(len(lst)):
        pointTag1 = lst[r][0][0]
        pointTag2 = lst[r][0][1]
        getGeocodeAddress = geocodeAddress(pointTag1, pointTag2)
        addr1 = getGeocodeAddress[list(getGeocodeAddress.keys())[0]]
        geocodeAddr = addr1 + ", " + getGeocodeAddress.get('city', '') + ", " + getGeocodeAddress.get('region', '')
        reverseGeocode.append(geocodeAddr)
        geocodeComplete = ', '.join(f'{value}' for key, value in getGeocodeAddress.items())
        folium.Marker([pointTag1, pointTag2]).add_child(folium.Popup(geocodeComplete)).add_to(mapObj)

    for i in range(len(lst)):
        res = []
        for j in range(len(lst[i][1])):
            res.append(tuple(lst[i][1][j]))

        # poly = folium.PolyLine(res)
        # poly.add_to(mapObj)
        # decoration = PolyLineDecorator(poly, offset='25%', end_offset = '25%', repeat=10, pixelSize=10, polygon=False, stroke=True, color='red')
        # decoration.add_to(mapObj)
        # create a polyline with the coordinates
        folium.PolyLine(res, color="blue", weight=2).add_to(mapObj)


        # format coordinates and draw line
        # loc = [[j for j in reversed(i)] for i in res]
        # folium.PolyLine(loc, color="red").add_to(mapObj)
        
        # get pieces of the line
        pairs = [(res[idx], res[idx-1]) for idx, val in enumerate(res) if idx != 0]

        pairs = [(((res[idx][0] + res[idx-1][0])/2, (res[idx][1] + res[idx-1][1])/2), res[idx-1]) for idx, val in enumerate(res) if idx != 0] 
        # get rotations from forward azimuth of the line pieces and add an offset of 90°
        geodesic = Geod(ellps='WGS84')
        rotations = [geodesic.inv(pair[0][1], pair[0][0], pair[1][1], pair[1][0])[0]+90 for pair in pairs]
        # create your arrow
        for pair, rot in zip(pairs, rotations):
            folium.RegularPolygonMarker(location=pair[0], color=pathColors[i], fill=True, fill_color=pathColors[i], fill_opacity=1,
                                            number_of_sides=3, rotation=rot).add_to(mapObj)


    # save the map object as a html
    mapObj.save(outputName)
    return reverseGeocode
    # psoVal = pso.ExecutePSO.runPSO()
    # for i in range(len(lst)):
    #     print(lst[i][0])