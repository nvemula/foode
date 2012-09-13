from django.contrib import admin
from foode.apps.restaurants.models import *

class RestaurantAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'added',)

admin.site.register(Restaurant, RestaurantAdmin)
admin.site.register(MenuList)
admin.site.register(MenuItem)

