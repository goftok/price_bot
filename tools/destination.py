from geopy.distance import geodesic


NIJMEGEN = (51.8433, 5.8609)
LEUVEN = (50.8823, 4.7138)
HERENT = (50.9093, 4.6774)


def calculate_driving_distance(origin: tuple, destination: tuple):
    return geodesic(origin, destination).kilometers
