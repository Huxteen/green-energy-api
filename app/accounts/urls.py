
from django.urls import path
from accounts import views

app_name = 'users'

urlpatterns = [
     path('create/', views.CreateUserView.as_view(), name='create'),
     path('token/', views.CreateTokenView.as_view(), name='token'),
     path('update/', views.ManageUserView.as_view(), name='update'),
     path('create-admin/', views.CreateAdminUserView.as_view(),
          name='create-admin'),
     path('user/<int:pk>/', views.AdminManageUserDetail.as_view(),
          name="update-user-details"),
     path('user/list/', views.ListUserAPIView.as_view(), name='list-user'),
]
