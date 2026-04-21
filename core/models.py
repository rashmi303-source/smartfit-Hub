from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from django.db import models

class User(AbstractUser):
    USER_TYPE_CHOICES = [
        ('user', 'User'),
        ('trainer', 'Trainer'),
        ('admin', 'Admin'),
    ]

    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES, default='user')
    age = models.IntegerField(null=True, blank=True)
    height = models.FloatField(null=True, blank=True)  # cm
    weight = models.FloatField(null=True, blank=True)  # kg
    gender = models.CharField(max_length=10, choices=[('male', 'Male'), ('female', 'Female')], null=True, blank=True)
    goal = models.CharField(max_length=20, choices=[
        ('weight_loss', 'Weight Loss'),
        ('weight_gain', 'Weight Gain'),
        ('muscle_gain', 'Muscle Gain'),
        ('maintenance', 'Maintenance')
    ], null=True, blank=True)
    diet_type = models.CharField(max_length=20, choices=[
        ('vegetarian', 'Vegetarian'),
        ('non_veg', 'Non-Veg'),
        ('vegan', 'Vegan')
    ], null=True, blank=True)
    activity_level = models.CharField(max_length=20, choices=[
        ('sedentary', 'Sedentary'),
        ('light', 'Light'),
        ('moderate', 'Moderate'),
        ('active', 'Active'),
        ('very_active', 'Very Active')
    ], null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username


class DailyTracking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='daily_tracking')
    date = models.DateField(default=timezone.now)
    calories_consumed = models.IntegerField(default=0)
    calories_burned = models.IntegerField(default=0)
    water_intake = models.FloatField(default=0)  # liters
    weight = models.FloatField(null=True, blank=True)
    is_workout_completed = models.BooleanField(default=False)


class DietPlan(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='diet_plans')
    date = models.DateField()
    total_calories = models.IntegerField()
    protein = models.FloatField()
    carbs = models.FloatField()
    fats = models.FloatField()
    meals = models.JSONField()
    is_consumed = models.BooleanField(default=False)


class WorkoutPlan(models.Model):
    LEVEL_CHOICES = [
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='workout_plans')
    title = models.CharField(max_length=200)
    level = models.CharField(max_length=20, choices=LEVEL_CHOICES)
    exercises = models.JSONField()
    duration = models.IntegerField()  # minutes
    date = models.DateField()
    is_completed = models.BooleanField(default=False)
