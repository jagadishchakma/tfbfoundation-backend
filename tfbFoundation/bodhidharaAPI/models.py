from django.db import models
from django.contrib.auth.models import User

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

# bodhidhara news comment model
class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    news = models.ForeignKey(BodhidharaNews, on_delete=models.CASCADE, related_name='comments')
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

# bodhidhdara news reply1 model
class Reply1(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='replies1')
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='replies1')
    reply1 = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

# bodhidhara news reply2
class Reply2(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='replies2')
    reply1 = models.ForeignKey(Reply1, on_delete=models.CASCADE, related_name='replies2')
    reply2 = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)




