#from django
from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template

# from restaurants
from foode.apps.restaurants.models import Restaurant

urlpatterns = patterns('foode.apps.restaurants.views',
         url(r"^$", direct_to_template, {
        "template": "home.html",
     }, name="home"),#home page or landing page
        url(r'^restaurants/$', 'restaurants', name="restaurants"),#search results page
        url(r'^directory/$', 'allrestaurants', name="allrestaurants"),#shows all restaurants
        url(r'^(\d+)/menulist/$', 'menulist', name="menulist"),#creates a new menulist/food category
        url(r'^(\d+)/editmenulist/$', 'editmenulist', name="editmenulist"),#saves a menulist name
        url(r'^(\d+)/menuitem/$', 'menuitem', name="menuitem"),#creates a  new fooditem
        url(r'^(\d+)/editmenuitem/$', 'editmenuitem', name="editmenuitem"),#saves the name of menuitem
        url(r'^(\d+)/removemenuitem/$', 'removemenuitem', name="removemenuitem"),   #removes a menuitem from the menu
        url(r'^ratemenuitem/(?P<menuitem_id>\w+)/(?P<rating>\w+)/$', 'ratemenuitem', name="ratemenuitem"),#user's rating is stored 
        url(r'^(\d+)/removemenulist/$', 'removemenulist', name="removemenulist"),  #a menulist is removed 
        url(r'^editmenulistview/(?P<restaurant_id>\w+)/$', 'editmenulistview', name="editmenulistview"),#menu book for editing
        url(r'^menulistview/(?P<restaurant_id>\w+)/$', 'menulistview', name="menulistview"),#menubook,used also for preview


    
        #Add,Describe,Edit,Delete Restaurant urls
        url(r'^add/$', 'add_restaurant', name="add_restaurant"),#add a new restaurant
        url(r'^(\d+)/$', 'restaurant', name="describe_restaurant"),#restaurant details page
        url(r'^(\d+)/edit/$', 'edit_restaurant', name="edit_restaurant"),#edit a restaurant
        url(r'^(\d+)/delete/$', 'delete_restaurant', name="delete_restaurant"),#delete a restaurant
        url(r'^restaurantshuffle/$', 'restaurantshuffle', name="restaurantshuffle"),#shuffle

)

