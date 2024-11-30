from . import views
from django.urls import path


urlpatterns = [
    path('create/', views.AccountCreateView.as_view(), name="create"),
    path('verify/', views.AccountVerifyView.as_view(), name="verify"),
    path('resend/', views.ResendVerificationCodeView.as_view(), name="resend"),
    path('login/', views.AccountLoginView.as_view(), name="login"),
    path('logout/', views.AccountLogoutView.as_view(), name="logout"),
    path('get/<str:id>/', views.AccountGetView.as_view(), name="account_get"),
    path('news/saved/', views.UserNewsSavedView.as_view(), name="news_saved")
]
