import os
import argparse
import pandas as pd
import FileUtil
from datetime import datetime, date, time, timedelta
from City import City
from SimpleFakeDataGenerator import SimpleFakeDataGenerator

class GenerateWeather :
	# Constructor 
	# initializes training data files, data frames and classifier for summary
	def __init__(self) :
		self.cityDFPath = "weathersimulator/historical-hourly-weather-data/city_attributes.csv"
		self.trainDF = "weathersimulator/historical-hourly-weather-data/weather_train.csv"
		self.testDF = "weathersimulator/historical-hourly-weather-data/weather_test.csv"
		self.classifierPath = "weathersimulator/classifier/summary.dat"
		self.cities = None
		self.model = None
		self.train = None 
		self.test = None
		self.initializeData()
		
		return
		
	
	# Checks whether data file exists and initializes the dataframes and classifier
	def initializeData(self) :
		
		if not os.path.exists(self.cityDFPath) :
			raise ValueError("Please make sure {} is available", self.cityDFPath);
		if not os.path.exists(self.trainDF) :
			raise ValueError("Please make sure {} is available", self.trainDF);
		if not os.path.exists(self.testDF) :
			raise ValueError("Please make sure {} is available", self.testDF);
		if not os.path.exists(self.classifierPath) :
			raise ValueError("Please make sure {} is available", self.classifierPath);
		
		self.model = FileUtil.getObjectFromPath(self.classifierPath)
		self.cities = pd.read_csv(self.cityDFPath)
		self.train = pd.read_csv(self.trainDF)
		self.test = pd.read_csv(self.testDF)
		
	
	#Generates weather data for next 10 hours for input city starting at inputDate
	def getFakeData(self, city, inputDate, n = 10) :
		results = ""
		if city is None :
			raise ValueError("Please provide city name and/or latitude-longitude")
		
		gen = SimpleFakeDataGenerator(self.cities, self.train, self.test, self.model)
		
		# Increment dates by an hour for n times and generate data
		for i in range(n) :
			date1 = inputDate + timedelta(hours=i) 
			res = gen.getFakeWeatherData(date1, city)	
			res["date"] = date1
			out = self.formatWeatherData(city, res)
			if i < n -1 :
				out += '\n'
			results += out
			
		return results
	
	#Format resulting weather data as per prescribed format	
	def formatWeatherData(self, city, res) :
		out = ""
		out += "{}|{},{}".format(city.name, city.latitude, city.longitude) + "|"
		out += res["date"].isoformat() + "|"
		out += res["summary"] + "|"
		out += res["temperature"] + "|"
		out += res["pressure"] + "|"
		out += res["humidity"] 
		return out

# Parses input arguments and passes them to generate weather data	
# Inputs : (All are mandatory)
# cityName - Name of an US/Canadian city
# latitude - Latitude of the city
# longitude - Longitude of the city
# inputDate - Starting time for the 10 hours for which results will be generated
#
# Output : Prints the fake weather data 
def main(): 
	parser = argparse.ArgumentParser()
	
	parser.add_argument("cityName", type=str, help="Name of the city.")
	parser.add_argument("latitude", type=str, help="Latitude") 
	parser.add_argument("longitude", type=str, help="Longitude") 
	parser.add_argument("inputDate", type=str, help="Input Date {Y-M-d H-m-s}") 
	
	args = parser.parse_args()
	cityName = args.cityName
	latitude = args.latitude
	longitude = args.longitude
	inputDateStr = args.inputDate
	
	if inputDateStr is not None :
		inputDate = datetime.strptime(inputDateStr, '%Y-%m-%d %H:%M:%S')
	else :
		inputDate = now().strftime('%Y-%m-%d %H:00:00')
	
	city = City(cityName, latitude, longitude)
	gen = GenerateWeather()
	results = gen.getFakeData(city, inputDate)
	
	print(results)
	
	return
		
if __name__== "__main__":
	main()