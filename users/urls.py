from django.urls import path
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)

from users.apps import UsersConfig
from users.views import (UserDestroyAPIView, UserPasswordResetAPIView,
                         UserPasswordResetConfirmAPIView,
                         UserRegistrationAPIView, UserRetrieveAPIView,
                         UserUpdateAPIView)

app_name = UsersConfig.name
urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('create/', UserRegistrationAPIView.as_view(), name='user_create'),
    path('update/<int:pk>/', UserUpdateAPIView.as_view(), name='user_update'),
    path('detail/<int:pk>/', UserRetrieveAPIView.as_view(), name='user_detail'),
    path('delete/<int:pk>/', UserDestroyAPIView.as_view(), name='user_delete'),
    path('reset_password/', UserPasswordResetAPIView.as_view(), name='password_reset'),
    path('reset_password_confirm/<str:uid>/<str:token>/', UserPasswordResetConfirmAPIView.as_view(),
         name='password_reset_confirm'),
]
