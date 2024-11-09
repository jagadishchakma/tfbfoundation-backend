from django.urls import path
from . import views


urlpatterns = [
    path('news/', views.NewsView.as_view(), name='news_view'),
    path('news/insert/', views.NewsInsertView.as_view(), name='news_insert'),
    path('news/views/count/', views.NewsViewCount.as_view(), name='news_view_count')
]
