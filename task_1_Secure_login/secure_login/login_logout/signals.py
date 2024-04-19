from django.db.models.signals import post_save
from .models import BookedEquipments, Books, HistoricalBookings
from django.dispatch import receiver
 
 
@receiver(post_save, sender=Books) 
def create_BookedEquipment(sender, instance, created, **kwargs):
    
    if instance.booked_or_not == True :

        BookedEquipments.objects.create(equipment_id=instance)
        HistoricalBookings.objects.create(user=instance.requested_user_id, booked_equipment=instance)