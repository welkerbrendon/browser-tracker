from django.contrib import admin
from .models import *


# Register your models here.
admin.site.register(ViewAccess)
admin.site.register(ActivityType)
admin.site.register(SiteType)
admin.site.register(Site)
admin.site.register(PageVisited)
admin.site.register(Activities)
