from django.contrib import admin
from .models import Flight, Airport, Passenger

# Register your models here.
class FlightAdmin(admin.ModelAdmin):
    list_display = ("id", "origin", "destination", "duration")

class PassengerAdmin(admin.ModelAdmin):
    filter_horizontal = ("flights")
    
admin.site.register(Flight)
admin.site.register(Airport)
admin.site.register(Passenger)