from geopy.distance import geodesic

SIZE = 0.6

def get_bbox(lat, long):
    return (lat - SIZE, long - SIZE, lat + SIZE, long + SIZE)

# Distance in miles
def get_distance(lat1, lon1, lat2, lon2):
    return geodesic((lat1, lon1), (lat2, lon2)).miles
