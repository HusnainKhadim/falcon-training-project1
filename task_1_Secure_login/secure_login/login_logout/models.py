from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

class Books(models.Model):

    euipment_name = models.CharField(max_length=150)
    euipment_type = models.CharField(max_length=150, null=True, blank=True)
    requested_or_not = models.BooleanField(default=False)
    booked_or_not = models.BooleanField(default=False)
    availabilty = models.BooleanField(default=True, null=True, blank=True)
    return_days = models.IntegerField(default=3, null=True, blank=True)
    requested_user_id = models.ForeignKey(User, on_delete=models.CASCADE, default=None, null=True, blank=True)

    class Meta:
        verbose_name = 'Book'


    def __str__(self):
        return self.euipment_name


class BookedEquipments(models.Model):

    equipment_id = models.ForeignKey(Books, on_delete=models.CASCADE)
    equipment_time = models.DateTimeField(default=datetime.now, blank=True)

    class Meta:
        verbose_name = 'BookedEquipment'

    def __str__(self):
        return self.equipment_id.euipment_name


class HistoricalBookings(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None, null=True, blank=True)
    booked_equipment = models.ForeignKey(Books, blank=True, null=True, on_delete=models.SET_NULL,db_constraint=False)

    class Meta:
        verbose_name = 'HistoricalBooking'

    def __str__(self):
        
        try:
            return self.booked_equipment.equipment_id.euipment_name
        except:
            return str(self.booked_equipment)

    

class PendingUsers(models.Model):

    username = models.CharField(max_length=150)
    password = models.CharField(max_length=150)

    class Meta:
        verbose_name = 'PendingUser'

    def __str__(self):
        return self.username
