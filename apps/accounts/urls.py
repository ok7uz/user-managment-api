from django.urls import path

from apps.accounts.views import (
    LoginAPIView,
    RegisterAPIView,
    SocialAuthAPIView,
    ProfileAPIView
)


urlpatterns = [
    path('login/', LoginAPIView.as_view(), name='login'),
    path('register/', RegisterAPIView.as_view(), name='register'),
    path('social-auth/', SocialAuthAPIView.as_view(), name='social-auth'),

    path('profile/', ProfileAPIView.as_view(), name='profile'),
]
