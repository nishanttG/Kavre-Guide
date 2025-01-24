from django.contrib import admin
from travello.models import Guide, Destination, Contact, Booking,Message,Availability

# Register your models here.

admin.site.register(Destination)
admin.site.register(Guide)
admin.site.register(Contact)
admin.site.register(Booking)
admin.site.register(Message)
admin.site.register(Availability)

