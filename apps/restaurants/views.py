from operator import itemgetter


#from django
from random import choice
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect,HttpResponse,HttpRequest
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User,AnonymousUser
from django.db.models import Q
from django.contrib.contenttypes.models import ContentType
from django.core.context_processors import csrf
from django.views.decorators.csrf import csrf_protect,csrf_exempt

#from restaurants
from foode.apps.restaurants.models import *
from foode.apps.restaurants.forms import *

#from djangoratings
from foode.apps.djangoratings.views import *
from foode.apps.djangoratings.models import *

#from python dict to json parsing py2js.py file
from foode.apps.restaurants.pyds2json import *

def allrestaurants(request):
    """ Returns the all restaurants list, ordered by added date. Called directory in urls.py"""
    restaurants = Restaurant.objects.all().order_by("-added")
    return render_to_response("restaurants/all.html", {
        "restaurants": restaurants,
    }, context_instance=RequestContext(request))
    

def restaurants(request):
    """ Returns the restaurants with the fooditems ordered by taste in descending order """
    if request.method == "GET":
       count = 0
       ecount = 0
       mcount = 0
       restaurants = []
       exactitems = []
       matcheditems = []
       menuitem = request.GET['fooditem']
       if menuitem:
          menuitems = MenuItem.objects.filter(menuitem__contains=menuitem)
          if menuitems:
             ctype = ContentType.objects.get(app_label="restaurants", model="menuitem")
             for mitem in menuitems:
                 res_data = {}
                 rscore = Vote.objects.filter(content_type=ctype,object_id=mitem.id)[0:50]
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
                 res_data["restaurant"] = mitem.resname
                 res_data[sco] =mitem.menuitem
                 if menuitem.lower() == mitem.menuitem.lower():
                    exactitems.insert(ecount,res_data)
                    ecount += 1
                 else:
                    matcheditems.insert(mcount,res_data)
                    mcount +=1
             exactitems = sorted(exactitems,reverse=True) 
             matcheditems = sorted(matcheditems,reverse=True) 
             restaurants = exactitems + matcheditems
             return render_to_response("restaurants/restaurants.html", {
                  "restaurants":restaurants,
                  "menuitem":menuitem,
                  }, context_instance=RequestContext(request))
          else:   
             return render_to_response("restaurants/restaurants.html", {
               "restaurants":restaurants,
               "menuitem":menuitem,
                }, context_instance=RequestContext(request))
       else:
          return HttpResponseRedirect(reverse("home"))

def restaurant(request, restaurant_id):
    """ Returns a restaurant page with its details by taking restaurant_id as parameter """
    restaurant = Restaurant.objects.get(id=restaurant_id)
    return render_to_response("restaurants/restaurant.html", {
        "restaurant": restaurant,
       }, context_instance=RequestContext(request))   

def add_restaurant(request): 
    """ Adds a new restaurant to the database.Also,returns the form  """
    # POST request
    if request.method == "POST":
       restaurant_form = RestaurantForm(request.POST, request.FILES)
       if restaurant_form.is_valid():
        # from ipdb import set_trace; set_trace()
          new_restaurant = restaurant_form.save(commit=False)
          new_restaurant.save(csrf(request))
          return HttpResponseRedirect(reverse("allrestaurants"))
    else:
           restaurant_form = RestaurantForm()
           return render_to_response("restaurants/add.html", {
               "restaurant_form": restaurant_form,
               }, context_instance=RequestContext(request))
    # generic case
    return render_to_response("restaurants/add.html", {
       "restaurant_form": restaurant_form,
       }, context_instance=RequestContext(request)) 
    
@csrf_exempt
def edit_restaurant(request, restaurant_id):
    """ Returns the edit page for a restaurant by taking restaurant_id as parameter """
    restaurant = Restaurant.objects.get(id=restaurant_id)          
    if request.method == "POST":
       restaurant_form = RestaurantEditForm(request.POST, request.FILES, instance=restaurant)
       restaurant_form.is_update = True
       #from ipdb import set_trace; set_trace()
       if restaurant_form.is_valid():
          restaurant_form.save()
          return HttpResponseRedirect(reverse("allrestaurants"))             
       else:
          restaurant_form = RestaurantEditForm(instance=restaurant)
          return render_to_response("restaurants/edit.html", {
            "restaurant_form": restaurant_form,
            "restaurant": restaurant,
            }, context_instance=RequestContext(request)) 
    else:
           restaurant_form = RestaurantEditForm(instance=restaurant)
           return render_to_response("restaurants/edit.html", {
            "restaurant_form": restaurant_form,
            "restaurant": restaurant,
            }, context_instance=RequestContext(request))   
          
def delete_restaurant(request, restaurant_id):
    """ Deletes a restaurant,menu from the database by taking restaurant id as a parameter """
    restaurant = get_object_or_404(Restaurant, id=restaurant_id)
    ctype = ContentType.objects.get(app_label="restaurants", model="menuitem")
    menulists = MenuList.objects.filter(res=restaurant)
    for mlist in menulists:
       items = MenuItem.objects.filter(menulist=mlist)
       for item in items:
           uscore = Vote.objects.filter(content_type=ctype,object_id=item.id)
           if uscore:
              for usc in uscore:
                  usc.delete()
           rscore = Score.objects.filter(content_type=ctype,object_id=item.id)
           if rscore:
              for rsc in rscore:
                  rsc.delete()
           item.delete()
       mlist.delete()
    restaurant.delete()
    return HttpResponseRedirect(reverse("allrestaurants"))

@csrf_exempt
def menulist(request,restaurant_id):
    """Creates a new menulist/foodcategory by taking the restaurant id as a parameter"""
    if request.method =="POST" and request.is_ajax:
       restaurant = Restaurant.objects.get(id=restaurant_id)   
       datatmp = request.POST
       data = datatmp.values()
       for temp in data:
           menul = MenuList(res=restaurant,listname=temp)
           menul.save()
       msg = "Successfully added to the menu."          
       

    else:
        msg = "Failed to add to the menu.Try again"

    return HttpResponse(msg)    

@csrf_exempt
def editmenulist(request,restaurant_id):
    """The new name of the existing menulist/food category is saved """
    if request.method =="POST" and request.is_ajax:
       restaurant = Restaurant.objects.get(id=restaurant_id)   
       datatmp = request.POST
       data = datatmp.keys()
       for temp in data:
           menul = MenuList.objects.get(res=restaurant,id=temp)
           menul.listname=datatmp[temp]
           menul.save()
       msg = "Successfully updated the menu."          
       

    else:
        msg = "Failed to save the menu"

    return HttpResponse(msg)   

def removemenulist(request,menulist_id):
    """Removes a menulist & all its menuitems and their userratings from the db"""
    if request.is_ajax:
       ctype = ContentType.objects.get(app_label="restaurants", model="menuitem")
       menul = MenuList.objects.get(id=menulist_id)
       items = MenuItem.objects.filter(menulist=menul)
       for item in items:
           uscore = Vote.objects.filter(content_type=ctype,object_id=item.id)
           if uscore:
              for usc in uscore:
                  usc.delete()
           rscore = Score.objects.filter(content_type=ctype,object_id=item.id)
           if rscore:
              for rsc in rscore:
                  rsc.delete()
           item.delete()
       menul.delete()
       msg = "Successfully removed from the menu."          
    else:
        msg = "Failed to remove from the menu"

    return HttpResponse(msg)   

def menulistview(request,restaurant_id):
    """" Returns a JSON object containing the menulists and their menuitems(with ratings) by taking the restaurant id"""
    if request.is_ajax and request.method=="GET":
       restaurant = Restaurant.objects.get(id=restaurant_id)
       menulists = MenuList.objects.filter(res=restaurant)
       tmplists = menulists_to_jsonready(menulists,request)
       res_data={}
       res_data["menulists"]=tmplists
       return JSONResponse(res_data)
    elif not request.is_ajax:
       return HttpResponse("Invalid call")
    

def editmenulistview(request,restaurant_id):
    """" Returns a JSON object containing the menulists and their menuitems(without ratings) by taking the restaurant id"""
    restaurant = Restaurant.objects.get(id=restaurant_id)
    menulists = MenuList.objects.filter(res=restaurant)
    tmplists = editmenulists_to_jsonready(menulists)
    res_data={}
    res_data["menulists"]=tmplists
    return JSONResponse(res_data)

@csrf_exempt
def menuitem(request,restaurant_id):
    """The new fooditems are added to their respective foodcategories """
    if request.method =="POST" and request.is_ajax:
       restaurant = Restaurant.objects.get(id=restaurant_id)   
       datatmp = request.POST
       keys = datatmp.keys()
       for key in keys:
           tt = datatmp[key]
           b = key.rpartition('z')[0][11:]
           listmenu = MenuList.objects.get(id=b)
           menuitem = MenuItem(resname=restaurant,menulist=listmenu,menuitem=tt)
           menuitem.save()
       msg = "Successfully added to the menu."          
    else:
        msg = "Failed to add to the menu.Try again"

    return HttpResponse(str(msg))        

@csrf_exempt
def editmenuitem(request,restaurant_id):
    """The new name of the fooditem is saved"""
    if request.method =="POST" and request.is_ajax:
       restaurant = Restaurant.objects.get(id=restaurant_id)   
       datatmp = request.POST
       data = datatmp.keys()
       for temp in data:
           menui = MenuItem.objects.get(resname=restaurant,id=temp)
           menui.menuitem=datatmp[temp]
           menui.save()
       msg = "Successfully updated the menu."          
       

    else:
        msg = "Failed to save the menu"

    return HttpResponse(msg)   

def removemenuitem(request,menuitem_id):
    """ Removes a menuitem/fooditem & its ratings from a menulist """
    if request.is_ajax:
           ctype = ContentType.objects.get(app_label="restaurants", model="menuitem")
           menuitem = MenuItem.objects.get(id=menuitem_id)
           uscore = Vote.objects.filter(content_type=ctype,object_id=menuitem_id)
           if uscore:
              for usc in uscore:
                  usc.delete()
           rscore = Score.objects.filter(content_type=ctype,object_id=menuitem_id)
           if rscore:
              for rsc in rscore:
                  rsc.delete()
           menuitem.delete()
           msg = "Successfully deleted from the list and menu."          
    else:
        msg = "Failed to remove from the menu"

    return HttpResponse(str(msg))        

def ratemenuitem(request,menuitem_id,rating):
    """The user rating for a particular food item is stored"""
    if request.is_ajax:
         ctype = ContentType.objects.get(app_label="restaurants", model="menuitem")
         itemid = menuitem_id[5:] 
         menuitem = MenuItem.objects.get(id=itemid)
         if request.user.is_authenticated():
            uscore = Vote.objects.filter(content_type=ctype,object_id=menuitem.id,user=request.user)
            if uscore:
              for usc in uscore:
                  usc.delete()
            menuitem.rating.add(score=rating,user=request.user,ip_address=request.META['REMOTE_ADDR'])
            msg="Succesfully rated"
         else:   
            uscore = Vote.objects.filter(content_type=ctype,object_id=menuitem.id,ip_address=request.META['REMOTE_ADDR'])
            if uscore:
              for usc in uscore:
                  usc.delete()
            menuitem.rating.add(score=rating,user=request.user,ip_address=request.META['REMOTE_ADDR'])
            msg = "Successfully rated the menuitem"          
    else:
         msg = "Failed to rate the menuitem"

    return HttpResponse(str(msg))        

def restaurantshuffle(request):
    """ Returns a random restaurant in an area when a foodie cant decide where to go.Work in Progress """
    res = Restaurant.objects.all()
    rest = choice(res)
    rid = rest.id
    return HttpResponseRedirect(reverse('describe_restaurant',args=[rid]))


 

