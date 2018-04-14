from geopy.distance import geodesic

def get_bbox(lat, long):
    return (lat - 0.7, long - 0.7, lat + 0.7, long + 0.7)

# Distance in miles
def get_distance(lat1, lon1, lat2, lon2):
    return geodesic((lat1, lon1), (lat2, lon2)).miles
