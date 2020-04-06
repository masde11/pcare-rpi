# pcare-rpi
Python scripts to automate a watering system for a garden

The code is very basic at the moment and is running in a Raspberry Pi Zero W.
It checks for soil moisture and weather data at given times and activates a water valve if soil moisture is below a threshold.
Every time data is retrieved it is uploaded to a website, and user can click a button from the website in order to activate the water valve if desired.
