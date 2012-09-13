"""Python datastructures to JSON objects """

from __future__ import division
from django.shortcuts import render_to_response, get_object_or_404,HttpResponse
from django.utils.simplejson import *
from django.contrib.contenttypes.models import ContentType
from django.conf import settings

#from djangoratings
from foode.apps.djangoratings.views import *
from foode.apps.djangoratings.models import *

from foode.apps.restaurants.models import *

def restaurants_to_jsonready(restaurants):
    """Takes a list of restaurant objects and returns a python dictionary """
    count = 0
    temp_restaurants = []
    for restaurant in restaurants:
           restaurant_data= {}
           restaurant_data["id"] = str(restaurant.id)
           restaurant_data["name"] = str(restaurant.name)
           restaurant_data["phone"] = str(restaurant.phone)
           restaurant_data["address"] = str(restaurant.address)
           temp_restaurants.insert(count,restaurant_data)
           count +=1
    return temp_restaurants 
              
def menulists_to_jsonready(menulists,request):
    """Takes a list of menulists/food categories and returns a python dictionary containing foodcategories,fooditems & their recent 50 ratings"""
    count = 0
    temp_lists = []
    ctype = ContentType.objects.get(app_label="restaurants", model="menuitem")
    for tmp in menulists:
        res_data = {}
        res_data["id"]=str(tmp.id)
        res_data["listname"]=str(tmp.listname)
        items = MenuItem.objects.filter(menulist=tmp)
        icount = 0
        temp_items = []
        for item in items:
            item_data = {}
            item_data["id"]=str(item.id)
            item_data["itemname"] = str(item.menuitem)
            rscore = Vote.objects.filter(content_type=ctype,object_id=item.id)[0:50]
            top50 = len(rscore)
            if rscore:
               sco = 0
               i=0
               while (i<top50):
                     sco += rscore[i].score
                     i+=1
               sco = sco/top50
            else: 
               sco =0 
            item_data["rrating"] = str(sco)
            """
            if request.user.is_authenticated():
               uscore = Vote.objects.filter(content_type=ctype,object_id=item.id,user=request.user)
            else:
               uscore = Vote.objects.filter(content_type=ctype,object_id=item.id,ip_address=request.META['REMOTE_ADDR'])
            if uscore:
               hasrated = True
               scor = uscore[0].score
            else: 
               scor = 0 
               hasrated = False
            item_data["urating"] = str(scor)
            item_data["hasrated"] = hasrated"""
            temp_items.insert(icount,item_data)
            icount +=1
        res_data["menuitems"] = temp_items
        temp_lists.insert(count,res_data)
        count +=1
    return temp_lists

def editmenulists_to_jsonready(menulists):
    """ Takes a list of foodcategories and returns a python dictionary containing food categories and its fooditems without ratings"""
    count = 0
    temp_lists = []
    for tmp in menulists:
        res_data = {}
        res_data["id"]=str(tmp.id)
        res_data["listname"]=str(tmp.listname)
        items = MenuItem.objects.filter(menulist=tmp)
        icount = 0
        temp_items = []
        for item in items:
            item_data = {}
            item_data["id"]=str(item.id)
            item_data["itemname"] = str(item.menuitem)
            temp_items.insert(icount,item_data)
            icount +=1
        res_data["menuitems"] = temp_items
        temp_lists.insert(count,res_data)
        count +=1
    return temp_lists

def JSONResponse(dictionary):
    """ Takes a python dictionary and sends a HttpResponse as a JSON object to the user"""
    diction = dumps(dictionary)
    return HttpResponse(diction,mimetype='application/json')
    


