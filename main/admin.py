from django.contrib import admin
from .models import *


# Register your models here.
admin.site.register(ViewAccess)
admin.site.register(ActivityType)
admin.site.register(Activity)
admin.site.register(SiteType)
admin.site.register(Site)
admin.site.register(SiteVisit)
admin.site.register(Extension)
admin.site.register(SiteVisitToActivity)