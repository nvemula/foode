#from django
from django import forms
from django.utils.translation import ugettext_lazy as _

#from restaurants
from foode.apps.restaurants.models import Restaurant

class RestaurantForm(forms.ModelForm):
    """
    Restaurant Form: Used to add a new restaurant to the database
    """
    def __init__(self, *args, **kwargs):
        super(RestaurantForm, self).__init__(*args, **kwargs)
        self.is_update = False
    
    def clean(self):
        """ Do validation stuff. """
        # name is mandatory
        if 'name' not in self.cleaned_data:
            return
        # if a restaurant with that title already exists...
        if not self.is_update:
            if Restaurant.objects.filter(phone=self.cleaned_data['phone']).count() > 0:
                str="Different"
        return self.cleaned_data
    
    class Meta:
        model = Restaurant
        fields = ('name','address','phone','hours')

class RestaurantEditForm(forms.ModelForm):
    """
    Restaurant Form: Used to edit the basic info of an existing restaurant
    """
    
    def __init__(self, *args, **kwargs):
        super(RestaurantEditForm, self).__init__(*args, **kwargs)
        self.is_update = False
    
    def clean(self):
        """ Do validation stuff. """
        # name is mandatory
        if 'name' not in self.cleaned_data:
            return
        # if a restaurant with that title already exists...
        if not self.is_update:
            if Restaurant.objects.filter(phone=self.cleaned_data['phone']).count() > 0:
                raise forms.ValidationError(_("There is already this restaurant in the database"))
        return self.cleaned_data
    
    class Meta:
        model = Restaurant
        fields = ('name','address','phone','hours')

