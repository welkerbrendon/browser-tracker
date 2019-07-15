from django.db import models
from django.contrib.auth.models import User
import django_filters
from datetime import datetime, date


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
    universal = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    def as_dict(self):
        return {
            "type_name": self.type_name,
            "universal": self.universal,
        }

    class Meta:
        unique_together = (("user", "type_name"),)


class Activity(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    activity_type = models.ForeignKey(ActivityType, on_delete=models.SET_NULL, null=True)
    day = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    productive = models.BooleanField()
    notes = models.TextField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    def as_dict(self):
        return {
            "day": self.day,
            "start_time": self.start_time,
            "end_time": self.end_time,
            "productive": self.productive,
        }

    class Meta:
        unique_together = (("user", "day", "start_time", "end_time"),)


class SiteType(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    type_name = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    def as_dict(self):
        return {
            "type_name": self.type_name,
            "created_at": self.created_at,
            "last_updated": self .last_updated
        }

    class Meta:
        unique_together = (("user", "type_name"),)


class Site(models.Model):
    id = models.AutoField(primary_key=True)
    site_type = models.ForeignKey(SiteType, models.SET_NULL, null=True)
    url = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)


class SiteVisit(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    site = models.ForeignKey(Site, on_delete=models.CASCADE)
    activity = models.ForeignKey(Activity, on_delete=models.SET_NULL, null=True)
    day = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    def as_dict(self):
        end_time_seconds = (((self.end_time.hour * 60) + self.end_time.minute) * 60) + self.end_time.seconds
        start_time_seconds = (((self.start_time.hour * 60) + self.start_time.minute) * 60) + self.start_time.seconds
        return {
            "day": self.day,
            "start_time": self.start_time,
            "end_time": self.end_time,
            "visit_length": end_time_seconds - start_time_seconds
        }

    class Meta:
        unique_together = (("user", "day", "start_time", "end_time", "site"),)


class F(django_filters.FilterSet):
    time = django_filters.TimeRangeFilter()

    class Meta:
        model = SiteVisit
        fields = ['start_time', 'end_time']


class Extension(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    site_visit = models.ForeignKey(SiteVisit, on_delete=models.CASCADE)
    page_extension = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)