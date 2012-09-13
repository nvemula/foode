# python
import os
from os import path
from datetime import datetime

# django imports
from django.conf import settings
from django.db import models
from django.contrib.auth.models import User,AnonymousUser
from django.utils.translation import ugettext_lazy as _


#from djangoratings
from foode.apps.djangoratings.fields import RatingField


class Restaurant(models.Model):
    """
    Restaurant Model: name,address,phone,rating,adder,added,
    """  
    name = models.CharField(_('Name'), max_length=255,blank=False)
    address =  models.TextField(_('Address'),blank=False,null=False,max_length=1024)
    hours =  models.CharField(_('Working Hours'),blank=False,null=False,max_length=1024)
    phone = models.CharField(_('Phone'),max_length=20,null=False,blank=False)
    rating = RatingField(range=5,can_change_vote = True,allow_anonymous = True,use_cookies = True) # 5 possible rating values, 1-5
    added = models.DateTimeField(_('added_on'), default=datetime.now)

    def get_absolute_url(self):
        return ("describe_restaurant", [self.pk])
    get_absolute_url = models.permalink(get_absolute_url)
    
    def __unicode__(self):
        return self.name
    
    class Meta:
        ordering = ('-added', )

class MenuList(models.Model):
    """Food Category in a restaurant menu : Vegetarian,Non-veg,Soups,etc"""
    res = models.ForeignKey(Restaurant,verbose_name=_("resmenlist"))
    listname = models.CharField(_('listname'), max_length=1024,default="Category")    

class MenuItem(models.Model):
    """FoodItem added to a FoodCategory : Vada in Tiffins,Tomato Soup in Soups etc"""
    resname =  models.ForeignKey(Restaurant,verbose_name=_("resnamelist"))
    menulist = models.ForeignKey(MenuList,verbose_name=_("menulist"))
    menuitem = models.CharField(_('menuitem'), max_length=1024,default="Menu Item")    
    rating = RatingField(range=5,can_change_vote = True,allow_anonymous = True,use_cookies =True) # 5 possible rating values, 1-5


