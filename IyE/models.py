__author__ = 'cristian'

from django.contrib.auth.models import User
from django.db import models as m


class Products(m.Model):
    """ Model used to store the basic information about a product
    We use two tables because when we want to present a lot of products in a
    compact way we only need this basic information, so we only want to fetch
    the required info
    """
    name = m.CharField(max_length=60)
    short_description = m.CharField(max_length=60)
    new = m.BooleanField(default=True)
    popular = m.BooleanField(default=False)
    price = m.FloatField(default=1.0)
    image_path = m.TextField(max_length=100)


class ProductDetail(m.Model):
    """ Model used to store additional information about a product
    """
    product = m.ForeignKey(Products)
    description = m.TextField()
    brand = m.CharField(max_length=60)
    times_purchased = m.IntegerField(default=0)


class UserDetail(m.Model):
    """ Model used to store the user's personal information
    Right now we don't want to store the credit card information until we
    have a better security implementation
    """
    user = m.ForeignKey(User)
    fullname = m.CharField(max_length=100, blank=True)
    number_exterior = m.CharField(max_length=10, blank=True)
    number_interior = m.CharField(max_length=10, blank=True)
    street = m.CharField(max_length=40, blank=True)
    colony = m.CharField(max_length=40, blank=True)
    cp = m.IntegerField(default=0)
    city = m.CharField(max_length=40, blank=True)
    state = m.CharField(max_length=40, blank=True)
    country = m.CharField(max_length=40, blank=True)