import json
from shapely import wkt
from shapely.geometry import mapping

def wtkToJson(wktData) :
    # Convertir le WKT en un objet Shapely
    polygon_geom = wkt.loads(wktData)

    # Convertir l'objet Shapely en GeoJSON
    geojson = mapping(polygon_geom)
    #print(geojson)
    #exit()
    return geojson