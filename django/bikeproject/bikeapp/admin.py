from django.contrib import admin
from . models import BikeCollections,Booking,Testride
# Register your models here.
admin.site.register(BikeCollections)
admin.site.register(Booking)
admin.site.register(Testride)