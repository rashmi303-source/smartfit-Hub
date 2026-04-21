from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [

    path('login/', views.LoginView.as_view(), name='login'),
    path('', views.LoginView.as_view(), name='home'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('dashboard/', views.DashboardView.as_view(), name='dashboard'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('diet/', views.DietView.as_view(), name='diet'),
    path('workout/', views.WorkoutView.as_view(), name='workout'),
    path('tracker/', views.TrackerView.as_view(), name='tracker'),
    path('api/profile/', views.profile_api, name='profile_api'),
    path('api/diet/', views.diet_api, name='diet_api'),
    path('api/workout/', views.workout_api, name='workout_api'),
    path('api/tracker/', views.tracker_api, name='tracker_api'),
    path('api/dashboard/', views.api_dashboard_public, name='api_dashboard'),
    path('api/workouts/', views.api_workouts_public, name='api_workouts'),
    path('api/profile-public/', views.api_profile_public, name='api_profile_public'),  # profile/ avoid conflict
]