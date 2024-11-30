from django.contrib import admin
from .models import BodhidharaNews,BodhidharaNewsComment,BodhidharaNewsCommentReply1,BodhidharaNewsCommentReply2

# Register your models here.
@admin.register(BodhidharaNews)
class BodhidharaNewsAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'category']

@admin.register(BodhidharaNewsComment)
class BodhidharaNewsCommentAdmin(admin.ModelAdmin):
    list_display = ['id', 'comment', 'created_at']


@admin.register(BodhidharaNewsCommentReply1)
class BodhidharaNewsCommentReply1Admin(admin.ModelAdmin):
    list_display = ['id', 'reply1', 'created_at']

@admin.register(BodhidharaNewsCommentReply2)
class BodhidharaNewsCommentReply2Admin(admin.ModelAdmin):
    list_display = ['id', 'reply2', 'created_at']