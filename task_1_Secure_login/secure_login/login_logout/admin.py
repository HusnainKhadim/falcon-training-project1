from django.contrib import admin
from .models import *

admin.site.register(Books)
admin.site.register(BookedEquipments)
admin.site.register(PendingUsers)
admin.site.register(HistoricalBookings)