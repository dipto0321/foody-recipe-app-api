from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from user import views

app_name = 'user'
urlpatterns = [
    path('create/', views.CreateUserView.as_view(), name='create'),
    path('token/', views.TokenObtainPairView.as_view(), name='token'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('me/', views.ManageUserView.as_view(), name='me'),
]
