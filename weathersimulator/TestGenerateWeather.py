import unittest
import math
import random
import pandas as pd
from GenerateWeather import GenerateWeather
from City import City
from datetime import datetime, date, time, timedelta

class TestGenerateWeather(unittest.TestCase) :
	
	def setUp(self) :
		self.gen = GenerateWeather()
		
		return
	
	# Base case with all input supplied correctly	
	# the data should be in the correct range for that city
	def testBaseCase(self) :
		latitude = 41.850029
		longitude = -87.650047
		city = City("Chicago", latitude, longitude)
		date1 = datetime.today()
		date1 = date1.replace(year=2017)
		date1 = date1.replace(month=11)
		date1 = date1.replace(day=23)
		date1 = date1.replace(hour=11)
		
		res = self.gen.getFakeData(city, date1 , 1)
		print()
		print(res)
		
		
		testData = self.gen.test[(self.gen.test.city == 'Chicago') & (self.gen.test.datetime.str.contains('2017-11-23'))]
		trainData = self.gen.train[(self.gen.train.city == city.name) & (self.gen.train.datetime.str.contains('-11-23 11:00:00'))]
		testData = pd.concat([trainData, testData])
		tMin = testData['temperature'].min() - testData['temperature'].std()
		tMax = testData['temperature'].max() + testData['temperature'].std()
		
		pMin = testData['pressure'].min() - testData['pressure'].std()
		pMax = testData['pressure'].max() + testData['pressure'].std()
		
		hMin = testData['humidity'].min() - testData['humidity'].std()
		hMax = testData['humidity'].max() + testData['humidity'].std()
		
		print("Temperature({}, {})".format(tMin, tMax))
		print("Pressure({}, {})".format(pMin, pMax))
		print("Humidity({}, {})".format(hMin, hMax))
		
		[rTemp, rPressure, rHum] = self.getNumericalWeatherData(res)
		
		self.assertTrue(rTemp <= tMax and rTemp >= tMin )
		self.assertTrue(rPressure <= pMax and rPressure >= pMin )
		self.assertTrue(rHum <= hMax and rHum >= hMin )
		
	# Test with correct city name thats available in training dataset but provide incorrect latitude longitude	
	# the data should be in the correct range for that city
	def testExistingCityWrongLocation(self) :
		latitude = 41.00
		longitude = -87.00
		city = City("Chicago", latitude, longitude)
		
		date1 = datetime.today()
		date1 = date1.replace(year=2017)
		date1 = date1.replace(month=11)
		date1 = date1.replace(day=23)
		date1 = date1.replace(hour=11)
		res = self.gen.getFakeData(city, date1, 1)
		print()
		print(res)
		
		testData = self.gen.test[(self.gen.test.city == city.name) & (self.gen.test.datetime.str.contains('2017-11-23 11:00:00'))]
		trainData = self.gen.train[(self.gen.train.city == city.name) & (self.gen.train.datetime.str.contains('-11-23 11:00:00'))]
		testData = pd.concat([trainData, testData])
		tMin = testData['temperature'].min() - testData['temperature'].std()
		tMax = testData['temperature'].max() + testData['temperature'].std()
		
		pMin = testData['pressure'].min() - testData['pressure'].std()
		pMax = testData['pressure'].max() + testData['pressure'].std()
		
		hMin = testData['humidity'].min() - testData['humidity'].std()
		hMax = testData['humidity'].max() + testData['humidity'].std()
		
		print("Temperature({}, {})".format(tMin, tMax))
		print("Pressure({}, {})".format(pMin, pMax))
		print("Humidity({}, {})".format(hMin, hMax))
		
		[rTemp, rPressure, rHum] = self.getNumericalWeatherData(res)
		
		self.assertTrue(rTemp <= tMax and rTemp >= tMin )
		self.assertTrue(rPressure <= pMax and rPressure >= pMin )
		self.assertTrue(rHum <= hMax and rHum >= hMin )
		

	def getNumericalWeatherData(self, res) :
		
		rTemp = res.split("|")[4]
		rTemp = float(rTemp)
		
		rPressure= res.split("|")[5]
		rPressure = float(rPressure)
		
		rHum = res.split("|")[6]
		rHum = float(rHum)
		
		return [rTemp, rPressure, rHum]
	
	
	#Tests a city that doesn't exists in the training dataset
	# The generated values are considered valid if they are in range for that day for any city
	def testNewCity(self) :
		latitude = 41.7408652
		longitude = -87.8603343
		city = City("Willow Springs", latitude, longitude)
		
		date1 = datetime.today()
		date1 = date1.replace(year=2017)
		date1 = date1.replace(month=11)
		date1 = date1.replace(day=23)
		date1 = date1.replace(hour=11)
		res = self.gen.getFakeData(city, date1, 1)
		print()
		print(res)
		
		testData = self.gen.test[(self.gen.test.datetime.str.startswith('2017-11-23'))]
		tMin = testData['temperature'].min() - testData['temperature'].std()
		tMax = testData['temperature'].max() + testData['temperature'].std()
		
		pMin = testData['pressure'].min() - testData['pressure'].std()
		pMax = testData['pressure'].max() + testData['pressure'].std()
		
		hMin = testData['humidity'].min() - testData['humidity'].std()
		hMax = testData['humidity'].max() + testData['humidity'].std()
		
		print("Temperature({}, {})".format(tMin, tMax))
		print("Pressure({}, {})".format(pMin, pMax))
		print("Humidity({}, {})".format(hMin, hMax))
		
		[rTemp, rPressure, rHum] = self.getNumericalWeatherData(res)
		
		self.assertTrue(rTemp <= tMax and rTemp >= tMin )
		self.assertTrue(rPressure <= pMax and rPressure >= pMin )
		self.assertTrue(rHum <= hMax and rHum >= hMin )
		
	def testRandomCities(self) :
		cities = self.gen.cities.iloc[random.sample(self.gen.cities.index.tolist(), 5)]
		
		
		date1 = datetime.today()
		date1 = date1.replace(year=2017)
		date1 = date1.replace(month=11)
		date1 = date1.replace(day=23)
		date1 = date1.replace(hour=11)
		
		for i, row in cities.iterrows() :
			print()
			city = City(row['City'], row['Latitude'], row['Longitude'])
			res = self.gen.getFakeData(city, date1, 1)
			print(res)
			
			testData = self.gen.test[(self.gen.test.city == city.name) & (self.gen.test.datetime.str.startswith('2017-11-23'))]
			trainData = self.gen.train[(self.gen.train.city == city.name) & (self.gen.train.datetime.str.contains('-11-23 '))]
			testData = pd.concat([trainData, testData])
			
			tMin = testData['temperature'].min() - testData['temperature'].std()
			tMax = testData['temperature'].max() + testData['temperature'].std()
			
			pMin = testData['pressure'].min() - testData['pressure'].std()
			pMax = testData['pressure'].max() + testData['pressure'].std()
			
			hMin = testData['humidity'].min() - testData['humidity'].std()
			hMax = testData['humidity'].max() + testData['humidity'].std()
			
			print("Temperature({}, {})".format(tMin, tMax))
			print("Pressure({}, {})".format(pMin, pMax))
			print("Humidity({}, {})".format(hMin, hMax))
			
			[rTemp, rPressure, rHum] = self.getNumericalWeatherData(res)
			
			self.assertTrue(math.isnan(tMax) or rTemp <= tMax)
			self.assertTrue(math.isnan(tMin) or rTemp >= tMin )
			self.assertTrue(math.isnan(pMax) or rPressure <= pMax)
			self.assertTrue(math.isnan(pMin) or rPressure >= pMin )
			self.assertTrue(math.isnan(hMax) or rHum <= hMax)
			self.assertTrue(math.isnan(hMin) or  rHum >= hMin )
	
if __name__ == '__main__':
	unittest.main()
		
	
