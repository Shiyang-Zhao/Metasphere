from django.contrib.auth import views as auth_views
from django.urls import path
from users import views as user_views

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('register/', user_views.register, name='register'),
    path('profile/<str:username>/', user_views.profile, name='profile'),
    path('logout/', auth_views.LogoutView.as_view(template_name='logout.html'), name='logout'),
    path('manage_friend/<str:username>',
         user_views.manage_friend, name='manage_friend')
]
