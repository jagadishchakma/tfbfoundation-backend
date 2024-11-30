from django.urls import path
from . import views


urlpatterns = [
    path('news/', views.NewsView.as_view(), name='news_view'),
    path('news/insert/', views.NewsInsertView.as_view(), name='news_insert'),
    path('news/<str:id>/', views.NewsSingleView.as_view(), name="news_single"),
    path('news/views/count/', views.NewsViewCount.as_view(), name='news_view_count'),

    path('news/comment/<str:id>/', views.NewsCommentView.as_view(), name='news_comment'), #post new comments
    path('news/comments/<str:id>/', views.NewsCommentsView.as_view(), name='news_comments'), #retrieve all news comments

    path('news/comment/reply1/<str:comment_id>/', views.NewsCommentReply1View.as_view(), name='comment_reply1'), #comment reply1
    path('news/comment/replies1/<str:comment_id>/', views.NewsCommentReplies1View.as_view(), name='comment_replies1'), #comment replies1

    path('news/comment/reply2/<str:reply1_id>/', views.NewsReply1Reply2View.as_view(), name='reply1_reply2'), # reply1 reply2
    path('news/comment/replies2/<str:reply1_id>/', views.NewsReply1Replies2View.as_view(), name='reply1_replies2') # reply1 reply2
]
