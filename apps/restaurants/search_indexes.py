import datetime
from haystack import indexes
from apps.restaurants.models import *

"""class RestaurantIndex(indexes.SearchIndex,indexes.Indexable):
    text = indexes.CharField(use_template=True,document=True)
    name = indexes.CharField(model_attr='name')
    address = indexes.CharField(model_attr='address')
    phone = indexes.CharField(model_attr='phone')
    content_auto = indexes.EdgeNgramField(model_attr='name')

   
    def get_model(self):
        return Restaurant
    def index_queryset(self):
        "Used when the entire index for model is updated."
        return self.get_model().objects.filter(added__lte=datetime.now())"""

class MenuItemIndex(indexes.SearchIndex,indexes.Indexable):
    text = indexes.CharField(document=True)
    name = indexes.CharField(model_attr='menuitem')
    #restaurant = indexes.CharField(model_attr='resname__id')
    content_auto = indexes.EdgeNgramField(model_attr='menuitem')
   
    def get_model(self):
        return MenuItem
    def index_queryset(self):
        "Used when the entire index for model is updated."
        return self.get_model().objects.all()




