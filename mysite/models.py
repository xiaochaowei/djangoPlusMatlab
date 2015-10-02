from django.db import models
class Sample(models.Model):
	name = models.CharField(max_length=200)
	origin = models.CharField(max_length=200)
	industryType = models.CharField(max_length=200)
	water = models.FloatField()
	volatiles = models.FloatField() 
	carbon = models.FloatField()
	ash = models.FloatField()
	elementType = models.CharField(max_length=200)
	industryElementContent = models.CharField(max_length=200)
	industryScaleContent = models.CharField(max_length=200)
	hotType = models.CharField(max_length=200)
	highValue = models.FloatField()
	lowValue = models.FloatField()
	gravityType = models.CharField(max_length = 200)
	reactor = models.CharField(max_length=200)
	temperatureSpeed = models.FloatField()
	gas = models.CharField(max_length=200)
	gravityData = models.CharField(max_length=200)

class Compound(models.Model):
	name = models.CharField(max_length=200)
	content = models.CharField(max_length=200)
	scale = models.CharField(max_length=200)