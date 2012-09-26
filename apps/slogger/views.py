from apps.slogger.models import *
from django.contrib.contenttypes.models import ContentType
from foode.apps.restaurants.views import *
from django.shortcuts import render_to_response, get_object_or_404

def universal_slog_handler(request,slug):
    """ Takes a slug name and returns the respective page """
    static_urls = ['restaurants','directory','add']
    if slug =="add":
       return add_restaurant(request)
    if slug =="directory":
       return allrestaurants(request)
    if slug =="add":
       return add_restaurant(request)
    if slug =="restaurants":
       return restaurants(request)
    else:
        s = get_object_or_404(Slog,slugname=slug)
        ctype = s.content_type
        if ctype.model=="restaurant":
           return restaurant(request,restaurant_id=s.object_id)

@csrf_exempt
def save_slugofrest(request,restaurant_id):
    """The new slug name of the existing restaurant is saved """
    static_urls = ['restaurants','directory','add','admin']
    wrong_chars = [',','.','/','\\','@','&','%','?',':','*','#','!','|']
    wflag=0
    if request.method =="POST" and request.is_ajax:
       newslug= request.POST["slug"]
       ctype = ContentType.objects.get(app_label="restaurants", model="restaurant")
       s = Slog.objects.get(content_type=ctype,object_id=restaurant_id) 
       if newslug in static_urls: 
          msg = "Please choose a different name"
       else:
          prev=Slog.objects.filter(slugname=newslug)
          if prev:
             if prev[0]==s:
                if s.slugname==newslug:
                   msg="Saved"
                else:
                   s.slugname=newslug
                   s.save()
             else:         
                msg = "Please choose a different urlname"
          else:
               for i in wrong_chars:
                   if i in newslug:
                      msg="Wrong characters found"
                      return HttpResponse(msg)
                   else:
                      wflag=1
               if wflag==1:
                 s.slugname = newslug
                 s.save()
                 msg = "Successfully saved"  
    else:
        msg = "Failed to save"

    return HttpResponse(msg)


 

       

