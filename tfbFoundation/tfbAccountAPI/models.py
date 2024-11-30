from django.contrib.auth.models import User
from django.db import models

# Profile models
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    photo = models.CharField(max_length=300, default="https://images.tfbfoundation.org/default_profile.png/")
    profession = models.CharField(max_length=200)
    address = models.TextField()
    current_address = models.TextField()
    phone_no = models.CharField(max_length=12)
    district = models.CharField(max_length=200)
    sub_district = models.CharField(max_length=200)
    account_type = models.CharField(max_length=200)
    verification_code = models.CharField(null=True,blank=True, max_length=5)
    created_at  = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.phone_no

class NewsSaved(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='saved')
    news_id = models.CharField(max_length=250)
    created_at = models.DateTimeField(auto_now_add=True)