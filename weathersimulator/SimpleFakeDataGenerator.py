import pandas as pd
import random
import math
import FileUtil

# A simple implementation for generating Fake Weather Data 
# Approach :
#	1. Generate numerical data for temperature, humidity, pressure
#		- Simple implementation, that looks at the past data for the city for same day and hour in past years
#		- Calculate the mean for each feature such as temperature etc
#		- new value = mean + (standard deviation * random float between -1 and 1)
#		- the new value will be in a plausible range (-1, 1) of std of the older values
#		
#	2. A Naive Bayes Classifier that predicts the weather summary - Rain or Sunny or Snow
#		- Once we've calculated temp, humidity, pressure, you can use as an input for predicting the weather outlook 

class SimpleFakeDataGenerator :   
	
	#  Constructor
	#	cities - Cities Dataframe which contains city name, country, latitude, longitude
	#	trainDF - Weather data split for training, includes city name, datetime (hourly) , temperature, pressure, humidity, summary
	#	testDF - Used for both creating classifier and used in testing
	#	classifierPath - Path where the classifier used for predicting summary is saved
    def __init__(self, cities, trainDF, testDF, model) :
        self.citiesDF = cities
        self.trainDF = trainDF
        self.testDF = testDF
        self.num = 5
        self.model = model

	# Get city closest to the input city. This is used when no exact match is found for the city in the training/reference dataset
	# city - City object 
	# num - no of closest cities to look for 
    def getClosestCities(self, city, num):
        newdf = self.citiesDF.copy()
        newdf['latDiff'] = abs(newdf["Latitude"] - city.latitude)
        newdf['lonDiff'] = abs(newdf["Longitude"] - city.longitude)
        newdf = newdf.sort_values(['latDiff','lonDiff']).head(num)  
        return newdf

	# Helper function to format floats to 1 decimal point
    def formatFloat(self, input) :
        if not math.isnan(input) :
            input = "{:.1f}".format(input)
        return input
	
	# Calculate a fake value using mean and standard deviation
	# InputDF - is the input data train 
	# key - temperature, pressure, humidity 
	# Returns a value between 1 std from mean
    def getFakeValue(self, inputDF, key ) :
        m = inputDF[key].mean()
        sd = inputDF[key].std()  
        value = m + random.uniform(-1, 1) * sd
        return value
	
	#Generate fake data output as dictionary
	# Pseudo-code :
	#	Looks for the city and past years data for same day and hour.
	#	If data not available, looks for closests cities with data available 
	# 	The fake values are then generated using mean of those values and 
	# 	adding an offset of  value between +1 or -1 std 
	
    def getFakeWeatherData(self, inputDate, city) :
        res = {}
        fdate1 = inputDate.strftime('-%m-%d %H:00:00')
        fds1 = self.trainDF[(self.trainDF.datetime.str.contains(fdate1)) & (self.trainDF.city==city.name)]
        if len(fds1.index) == 0 :
           closestCitiesDF = self.getClosestCities(city, self.num)
           cityNames = closestCitiesDF['City'].tolist()
           fds1 = self.trainDF[(self.trainDF.datetime.str.contains(fdate1)) & (self.trainDF.city.isin(cityNames))]
        res['temperature'] = self.formatFloat(self.getFakeValue(fds1, "temperature"))
        res['pressure'] = self.formatFloat(self.getFakeValue(fds1, "pressure"))
        res['humidity'] = self.formatFloat(self.getFakeValue(fds1, "humidity"))
      
        prediction = self.model.classify(res)
        res["summary"]=prediction
        return res
	
	# Is used to get data from the test set 
	# used for comparing with the fake data generated
	# The fake data generated must be between the max and mean values for that city and datetime
    def getActualWeatherData(self, inputDate, city) :
        res = {}
        fdate1 = inputDate.strftime('%Y-%m-%d %H:00:00')
        fds1 = self.testDF[(self.testDF.datetime == fdate1) & (self.testDF.city==city)]   
		
        res['temperature'] = self.formatFloat(fds1["temperature"].mean())
        res['pressure'] = self.formatFloat(fds1["pressure"].mean())
        res['humidity'] = self.formatFloat(fds1["humidity"].mean())
        res['summary'] = fds1["summary"].mode()[0]   
        return res