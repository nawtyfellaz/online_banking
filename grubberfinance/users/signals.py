from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver, Signal
from django.db.models import Max, Sum

from grubberfinance.utils.functions import (
    unique_routing_number_generator,
    unique_account_number_generator,
    unique_slug_generator,
    unique_online_pin_generator
)

from grubberfinance.users.models import User

def pre_save_account_details(sender, instance, *args, **kwargs):
    if not instance.account_number:
        instance.account_number = unique_account_number_generator(instance)

    if not instance.routing_number:
        instance.routing_number = unique_routing_number_generator(instance)

    if not instance.slug:
        instance.slug = unique_slug_generator(instance)

    if not instance.pin:
        instance.pin = unique_online_pin_generator(instance)

pre_save.connect(pre_save_account_details, sender=User)
