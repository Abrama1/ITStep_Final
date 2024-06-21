from django.urls import path
from . import views

urlpatterns = [
    path('', views.game, name='game'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('history/', views.history, name='history'),
    path('leaderboard/', views.leaderboard, name='leaderboard'),
    path('save_game_result/', views.save_game_result, name='save_game_result'),
    path('profile/', views.profile, name='profile'),
]
