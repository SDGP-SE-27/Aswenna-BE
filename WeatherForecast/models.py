from django.db import models

class WeatherData(models.Model):
    location = models.CharField(max_length=100)
    temp = models.FloatField()
    wind = models.FloatField()
    humidity = models.FloatField()
    weather = models.CharField(max_length=50)

class ForecastData(models.Model):
    location = models.CharField(max_length=100)
    date = models.DateField()
    temp = models.FloatField()
    weather = models.CharField(max_length=50)

