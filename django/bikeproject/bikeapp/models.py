from django.db import models
from django.utils import timezone
# Create your models here.
class BikeCollections(models.Model):
    image = models.ImageField(upload_to='pics')
    name = models.CharField(max_length=100,unique=True)
    price = models.CharField(max_length=50)
    description = models.TextField()
    anchor = models.CharField(max_length=50, default='Know More')
    anchor_link = models.CharField(max_length=150, default="#")

class Booking(models.Model):
    username = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    phoneno = models.CharField(max_length=15,unique=True)
    city = models.CharField(max_length=100)
    prefered_bike = models.CharField(max_length=100)
    

class Testride(models.Model):
    username = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    phoneno = models.CharField(max_length=15)
    city = models.CharField(max_length=100)
    prefered_bike = models.CharField(max_length=100)
    testride_datetime = models.DateTimeField(default=timezone.now)
   