from .models import Activities, Site
from django.contrib.auth.models import User
import datetime

def check_already_exists(user_id, data):
    site = Site.objects.filter(id=get_site_id(data.get('url')))[0]
    user = User.objects.filter(id=user_id)[0]

    return Activities.objects.filter(user_id=user.id,
                                     site_id=site.id,
                                     start_time=data.get('start_time')).count() >= 1

def create_new_activity(user_id, data):
    site = Site.objects.filter(id=get_site_id(data.get('url')))[0]
    user = User.objects.filter(id=user_id)[0]

    Activities(user=user, site=site, start_time=data.get('start_time')).save()
    return Activities.objects.filter(user_id=user.id,
                                  site_id=site.id,
                                  start_time=data.get('start_time')).count() == 1

def get_site_id(url):
    result = Site.objects.filter(url=url)
    if result.count() == 1:
        return result[0].id
    elif result.count() == 0:
        Site(url=url).save()
        return Site.objects.filter(url=url)[0].id
    else:
        return -1