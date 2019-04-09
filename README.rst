===============================
weathersimulator
===============================


.. image:: https://img.shields.io/travis/jadhavsheetal/WeatherSimulator.svg
        :target: https://travis-ci.org/jadhavsheetal/WeatherSimulator
.. image:: https://circleci.com/gh/jadhavsheetal/WeatherSimulator.svg?style=svg
    :target: https://circleci.com/gh/jadhavsheetal/WeatherSimulator
.. image:: https://codecov.io/gh/jadhavsheetal/WeatherSimulator/branch/master/graph/badge.svg
   :target: https://codecov.io/gh/jadhavsheetal/WeatherSimulator


Generate Fake Weather Data primarily of US/Canadian cities


Features
--------

Add a list of features.


Example
-------

Add a short example

::

    show some example code here


Documentation
-------------

The project serves as a simple implementation to generate fake weather data i.e. temperature,pressure, humidity, weather summary
for a given city and datetime

There are two main steps in the fake data generation
	1. Generate numerical data for temperature, pressure and humidity from the dataset available as a csv file "weather_train.csv"
	2. Using ML algorithm predict the correct weather summary such as Sunny, Rain or Snow based on the numerical data (temperature, pressure and humidity)
	

	Approach for Step 1:
	This is a simplistic implementation for generating fake weather data using the past data available in the csv file. 
	Using the past data for the feature e.g. humidity for the same city and same day and hour, we first
	1. Calculate the mean for that range 
	2. Since for a normal distribution, majority data lies between 1 standard deviation of the mean, 
		we can create a fake value using a random number between +1 and -1 of the std of the mean for that range

	Assumptions :
	1. For simplicity's sake, we assume the weather remains within the normal range and we are not generating data for severe weather conditions
	2. Also another major assumption, we are assuming the weather can be predicted based on latitude, longitude
		Weather in general has many influencing factors 
		1. Elevation 
		2. Proximity to ocean massess (ocean currents)
		3. latitude - longitude : how far it is from the equator as that indicates the location of sun 
		4. Topographical features such as vegetation etc
		
		I have made an assumption that the latitude/longitude serves as a proxy for the above features. Assuming that there are no major events/changes to the earth's surface. 
		The above feaures will remain the same across time. Again i'm oversimplifying by discounting phenomena such as climate change or changes due to shifting continents etc
		So latitude and longitude serves a broad indicator for the above factors
	

Approach for Step 2: 
	Based on temperature, humidity and pressure, we can create a basic classification model to predict whether the weather would be Rainy, Sunny or Snowy

Tests
-----

A suite of tests were built using `pytest <http://pytest.org/latest/>`_.

To run the test suite, from the command line in the project's root directory::

    $ py.test tests/



Requirements
------------

Add requirements and code dependencies.


Installation
------------

To install weathersimulator from source:

1. Check that you have Python_ installed::

    $ python --version

If you do not have Python_ installed, please download the latest version from `Python's download page`_

2. Download weathersimulator from the repository and extract to a directory of your choice.

   Or, if you have git_ installed you can clone the project::

    $ git clone <remote url to weathersimulator>

3. Navigate to the project's root directory where the setup script called `setup.py` is located::

    $ cd weathersimulator/

| The `setup.py` is a Python file that contains information regarding the installation of a Python module/package, and
| usually specifies that the module/package has been packaged and distributed with the standard Python distribution
| package called Distutils_.

4. Run `setup.py` with the `install` command::

    $ python setup.py install

weathersimulator will now be installed to the standard location for third-party Python modules on your
computer platform.

For more information regarding installing third-party Python modules, please see `Installing Python Modules`_
For a description of how installation works including where the module will be installed on your computer platform,
please see `How Installation Works`_.


Author
------

Sheetal Jadhav <jadhavsheetal@gmail.com>

