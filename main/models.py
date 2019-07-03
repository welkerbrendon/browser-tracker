from django.db import models
from django.contrib.auth.models import User

class ViewAccess(models.Model):
    id = models.AutoField(primary_key=True)
    viewing_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="viewing_user")
    sharing_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sharing_user")
    created_at = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

class ActivityType(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    type_name = models.CharField(max_length=50)
    universal = models.BooleanField(default=True)

class SiteType(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    type_name = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

class Site(models.Model):
    id = models.AutoField(primary_key=True)
    site_type = models.ForeignKey(SiteType, models.SET_NULL, null=True)
    url = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

class Activities(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    activity_type = models.ForeignKey(ActivityType, on_delete=models.SET_NULL, null=True)
    site = models.ForeignKey(Site, on_delete=models.SET_NULL, null=True)
    day = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    productive = models.BooleanField(null=True)
    notes = models.TextField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

class CombinedActivites(models.Model):
    id = models.AutoField(primary_key=True)
    first_activity = models.ForeignKey(Activities, on_delete=models.CASCADE, related_name="first_activity")
    second_activity = models.ForeignKey(Activities, on_delete=models.CASCADE, related_name="second_activity")
    created_at = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

class PageVisited(models.Model):
    id = models.AutoField(primary_key=True)
    activity = models.ForeignKey(Activities, on_delete=models.CASCADE)
    page_extension = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
