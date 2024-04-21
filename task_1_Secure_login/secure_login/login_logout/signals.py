from django.db.models.signals import post_save
from .models import *
from django.dispatch import receiver
 
 
@receiver(post_save, sender=Books) 
def create_BookedEquipment(sender, instance, created, **kwargs):
    
    if instance.booked_or_not == True :

        BookedEquipments.objects.create(equipment_id=instance)
        HistoricalBookings.objects.create(user=instance.requested_user_id, booked_equipment=instance)


@receiver(post_save, sender=PendingUsers) 
def create_BookedEquipment(sender, instance, created, **kwargs):
    
    if instance.approved == True :

        user = User.objects.create_user(username=instance.username, password=instance.password)
        user.is_active
        user.save()

        instance.delete()