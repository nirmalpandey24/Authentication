from django.urls import path
from .views import CustomUserDetail, CustomUserInfo,LoginView , UserView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path("customuser/", CustomUserDetail.as_view(), name="customuser-detail"),
    path("customuser/<int:id>/", CustomUserInfo.as_view(), name="customuser-info"),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('login',LoginView.as_view(),name='login'),
    path('User',UserView.as_view(),name='login')
    
]
