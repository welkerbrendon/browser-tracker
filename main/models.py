from django.db import models
from django.contrib.auth.models import User
import django_filters


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
    activity_type = models.ForeignKey(ActivityType, on_delete=models.CASCADE)
    day = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    productive = models.BooleanField()
    notes = models.TextField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    def get_total_time(self):
        end_time_seconds = (((self.end_time.hour * 60) + self.end_time.minute) * 60) + self.end_time.second
        start_time_seconds = (((self.start_time.hour * 60) + self.start_time.minute) * 60) + self.start_time.second
        return end_time_seconds - start_time_seconds

    def as_dict(self):
        return {
            "day": self.day,
            "start_time": self.start_time,
            "end_time": self.end_time,
            "productive": self.productive
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
    day = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    def as_dict(self):
        end_time_seconds = (((self.end_time.hour * 60) + self.end_time.minute) * 60) + self.end_time.second
        start_time_seconds = (((self.start_time.hour * 60) + self.start_time.minute) * 60) + self.start_time.second
        end_day = None
        visit_length_second_day = None
        visit_length_first_day = None
        if end_time_seconds < start_time_seconds:
            visit_length_first_day = (24 * 3600) - start_time_seconds
            visit_length_second_day = end_time_seconds
            end_time_seconds = end_time_seconds + (24 * 3600)
            end_day = (self.day.weekday() + 1) % 6

        return {
            "day": self.day,
            "end_day_of_week": end_day,
            "day_of_week": self.day.weekday(),
            "start_time": self.start_time,
            "end_time": self.end_time,
            "total_visit_length": end_time_seconds - start_time_seconds,
            "visit_length_first_day": visit_length_first_day,
            "visit_length_second_day": visit_length_second_day
        }

    class Meta:
        unique_together = (("user", "day", "start_time", "end_time", "site"),)


class Extension(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    site_visit = models.ForeignKey(SiteVisit, on_delete=models.CASCADE)
    page_extension = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)


class SiteVisitToActivity(models.Model):
    id = models.BigAutoField(primary_key=True)
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE)
    site_visit = models.ForeignKey(SiteVisit, on_delete=models.CASCADE)

    class Meta:
        unique_together = (("activity", "site_visit"),)