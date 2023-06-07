
from django.db import models

class TestClass(models.Model):
    Nitrogen = models.CharField(max_length=200)
    Phosphorus = models.CharField(max_length=200)
    Potassium = models.CharField(max_length=200)
    Temperature = models.CharField(max_length=200)
    Humidity = models.CharField(max_length=200)
    PH = models.CharField(max_length=200)
    Rainfall = models.CharField(max_length=200)



