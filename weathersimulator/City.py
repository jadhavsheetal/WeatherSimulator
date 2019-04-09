# City Object that holds the city name, latitude and longitude
class City :
        
    def __init__(self, name, latitude=float('NaN'), longitude=float('NaN')):
        self.name = name
        self.latitude = latitude
        self.longitude = longitude