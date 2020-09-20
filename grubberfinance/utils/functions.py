import datetime
import os
import random
import string
import math

from django.db.models import Count, Sum, Avg
from django.utils import timezone
from django.utils.text import slugify

def random_integer_generator(size=12, chars=string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

def random_string_generator(size=10, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

def get_filename(path): #/abc/filename.mp4
    return os.path.basename(path)


def unique_account_number_generator(instance):
    """
    This is for a Django project with an account_number field
    """
    size = random.randint(9, 12)
    new_account_number = random_integer_generator(size=size)

    Klass = instance.__class__
    qs_exists = Klass.objects.filter(account_number=new_account_number).exists()
    if qs_exists:
        return unique_slug_generator(instance)
    return new_account_number


def unique_routing_number_generator(instance):
    """
    This is for a Django project with an routing_number field
    """
    size = random.randint(9, 12)
    new_routing_number = random_integer_generator(size=size)

    Klass = instance.__class__
    qs_exists = Klass.objects.filter(routing_number=new_routing_number).exists()
    if qs_exists:
        return unique_slug_generator(instance)
    return new_routing_number

def unique_online_pin_generator(instance):
    """
    This is for a Django project with an pin field
    """
    size = random.randint(4, 4)
    new_online_pin = random_integer_generator(size=size)

    Klass = instance.__class__
    qs_exists = Klass.objects.filter(pin=new_online_pin).exists()
    if qs_exists:
        return unique_slug_generator(instance)
    return new_online_pin


def unique_online_pin_generator(instance):
    """
    This is for a Django project with an pin field
    """
    size = random.randint(4, 4)
    new_online_pin = random_integer_generator(size=size)

    Klass = instance.__class__
    qs_exists = Klass.objects.filter(pin=new_online_pin).exists()
    if qs_exists:
        return unique_slug_generator(instance)
    return new_online_pin


def unique_slug_generator(instance, new_slug=None):
    """
    This is for a Django project and it assumes your instance
    has a model with a slug field and a title character (char) field.
    """
    if new_slug is not None:
        slug = new_slug
    else:
        slug = slugify(instance.title)

    Klass = instance.__class__
    qs_exists = Klass.objects.filter(slug=slug).exists()
    if qs_exists:
        new_slug = "{slug}-{randstr}".format(
                    slug=slug,
                    randstr=random_string_generator(size=4)
                )
        return unique_slug_generator(instance, new_slug=new_slug)
    return slug
