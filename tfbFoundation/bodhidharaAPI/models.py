from django.db import models

# bodhidhara news insert model
class BodhidharaNews(models.Model):
    title = models.CharField(max_length=300)
    category = models.CharField(max_length=100)
    fb_post_id = models.TextField(null=True, blank=True)
    fb_video_ids =  models.JSONField(null=True, blank=True)
    fb_photo_ids = models.JSONField(null=True, blank=True)
    fb_post_react = models.JSONField(null=True, blank=True)
    views = models.JSONField(default=list)
    created_at = models.DateTimeField(auto_now_add=True)


