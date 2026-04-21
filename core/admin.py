from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, DailyTracking, DietPlan, WorkoutPlan

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ['username', 'email', 'user_type', 'age', 'weight', 'goal', 'created_at']
    list_filter = ['user_type', 'goal', 'diet_type', 'activity_level']
    search_fields = ['username', 'email', 'first_name']
    fieldsets = UserAdmin.fieldsets + (
        ('Fitness Info', {
            'fields': ('age', 'height', 'weight', 'gender', 'goal', 'diet_type', 'activity_level')
        }),
    )

@admin.register(DailyTracking)
class DailyTrackingAdmin(admin.ModelAdmin):
    list_display = ['date', 'user', 'calories_consumed', 'water_intake', 'weight', 'is_workout_completed']
    list_filter = ['date', 'is_workout_completed']
    date_hierarchy = 'date'

@admin.register(DietPlan)
class DietPlanAdmin(admin.ModelAdmin):
    list_display = ['date', 'user', 'total_calories', 'is_consumed']
    list_filter = ['date', 'is_consumed']
    readonly_fields = ['meals']

@admin.register(WorkoutPlan)
class WorkoutPlanAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'level', 'duration', 'is_completed']
    list_filter = ['level', 'is_completed']
    readonly_fields = ['exercises']