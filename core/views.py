from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.views import View
from django.db import models
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from datetime import date

User = get_user_model()

from .models import DailyTracking, DietPlan, WorkoutPlan
from .serializers import UserSerializer, ProfileUpdateSerializer, DailyTrackingSerializer, DietPlanSerializer, \
    WorkoutPlanSerializer, LoginSerializer
from .services import DietService, WorkoutService

# ========================================
# Authentication Views (PERFECT)
# ========================================

class LoginView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('core:dashboard')
        return render(request, 'core/auth/login.html')

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            messages.success(request, f'Welcome back, {user.first_name or user.username}!')
            return redirect('core:dashboard')

        messages.error(request, 'Invalid username or password.')
        return render(request, 'core/auth/login.html')

class RegisterView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('dashboard')
        return render(request, 'core/auth/register.html')

    def post(self, request):
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')
            return render(request, 'core/auth/register.html')

        try:
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name=request.POST.get('first_name', ''),
                last_name=request.POST.get('last_name', '')
            )
            login(request, user)
            messages.success(request, 'Registration successful!')
            return redirect('dashboard')
        except Exception as e:
            messages.error(request, 'Registration failed.')
            return render(request, 'core/auth/register.html')

class LogoutView(View):
    def get(self, request):
        logout(request)
        messages.success(request, 'Logged out successfully.')
        return redirect('/login/')


# ========================================
# Template Views (All Fixed)
# ========================================

class DashboardView(View):
    def get(self, request):
        if not request.user.is_authenticated:
            return redirect('login')
        context = {
            'diet_plans': DietPlan.objects.filter(user=request.user)[:5],
            'workouts': WorkoutPlan.objects.filter(user=request.user).order_by('-date')[:5],
            'tracking': DailyTracking.objects.filter(user=request.user).order_by('-date')[:5]
        }
        return render(request, 'core/dashboard.html', context)


class ProfileView(View):
    def get(self, request):
        if not request.user.is_authenticated:
            return redirect('login')
        context = {'user': request.user}
        return render(request, 'core/profile.html', context)

    def post(self, request):
        print("POST DATA:", dict(request.POST))  # Debug

        try:
            # Basic info
            request.user.first_name = request.POST.get('first_name', '').strip()
            request.user.last_name = request.POST.get('last_name', '').strip()
            request.user.email = request.POST.get('email', '').strip()

            # Safe numeric fields
            for field in ['age']:
                value = request.POST.get(field, '').strip()
                if value:
                    request.user.age = int(value)

            for field in ['height', 'weight']:
                value = request.POST.get(field, '').strip()
                if value:
                    request.user.__setattr__(field, float(value))

            # Choice fields
            request.user.gender = request.POST.get('gender', '')
            request.user.goal = request.POST.get('goal', '')

            # Optional
            request.user.allergies = request.POST.get('allergies', '')

            request.user.save()
            print("SUCCESS: Profile saved!")
            messages.success(request, '✅ Profile updated successfully!')

        except ValueError as e:
            print("ERROR:", e)
            messages.error(request, '❌ Enter valid numbers for age/height/weight')
        except Exception as e:
            print("ERROR:", e)
            messages.error(request, '❌ Update failed')

        # Reload page with updated data
        context = {'user': request.user}
        return render(request, 'core/profile.html', context)

class DietView(View):
    def get(self, request):
        if not request.user.is_authenticated:
            return redirect('login')
        context = {'diet_plans': DietPlan.objects.filter(user=request.user).order_by('-date')}
        return render(request, 'core/diet.html', context)

class WorkoutView(View):
    def get(self, request):
        if not request.user.is_authenticated:
            return redirect('login')
        context = {'workouts': WorkoutPlan.objects.filter(user=request.user).order_by('-date')}
        return render(request, 'core/workout.html', context)

class TrackerView(View):
    def get(self, request):
        if not request.user.is_authenticated:
            return redirect('login')
        context = {'tracking': DailyTracking.objects.filter(user=request.user).order_by('-date')}
        return render(request, 'core/tracker.html', context)


# ========================================
# API Views (Simplified)
# ========================================

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def profile_api(request):
    return Response(UserSerializer(request.user).data)

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def diet_api(request):
    if request.method == 'GET':
        diets = DietPlan.objects.filter(user=request.user)[:10]
        return Response(DietPlanSerializer(diets, many=True).data)
    try:
        DietService.generate_diet_plan(request.user)
        return Response({'message': 'Diet generated!'})
    except:
        return Response({'error': 'Failed'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def workout_api(request):
    if request.method == 'GET':
        workouts = WorkoutPlan.objects.filter(user=request.user)[:10]
        return Response(WorkoutPlanSerializer(workouts, many=True).data)
    try:
        WorkoutService.generate_workout_plan(request.user)
        return Response({'message': 'Workout generated!'})
    except:
        return Response({'error': 'Failed'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def tracker_api(request):
    if request.method == 'GET':
        tracking = DailyTracking.objects.filter(user=request.user)
        return Response(DailyTrackingSerializer(tracking, many=True).data)

    if request.method == 'POST':
        serializer = DailyTrackingSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(user=request.user)
            print("SAVED ✅")
            return Response({'message': 'Saved successfully'})
        else:
            print("ERROR ❌:", serializer.errors)
            return Response(serializer.errors, status=400)

# ========================================
# REACT FRONTEND PUBLIC APIs (No Auth Required)
# ========================================

@api_view(['GET'])
@permission_classes([AllowAny])  # ← Public access
def api_dashboard_public(request):
    """Public dashboard data for React frontend"""
    data = {
        "workouts": 25,
        "calories": 2800,
        "weight": 72.5,
        "bmi": 23.7,
        "goal": "Muscle Gain",
        "streak": 7,
        "message": "Welcome to SmartFit Hub!"
    }
    return Response(data)

@api_view(['GET'])
@permission_classes([AllowAny])  # ← Public access
def api_workouts_public(request):
    """Sample workouts for React demo"""
    return Response([
        {"id":1, "name":"Chest Workout", "duration":"45min", "calories":350, "date":"2024-04-10"},
        {"id":2, "name":"Cardio Run", "duration":"30min", "calories":420, "date":"2024-04-12"},
        {"id":3, "name":"Leg Day", "duration":"60min", "calories":520, "date":"2024-04-14"},
        {"id":4, "name":"Full Body", "duration":"60min", "calories":600, "date":"2024-04-15"}
    ])

@api_view(['GET'])
@permission_classes([AllowAny])  # ← Public access
def api_profile_public(request):
    """Sample profile for React demo"""
    return Response({
        "name": "Demo User",
        "age": 28,
        "height": "175cm",
        "current_weight": "72.5kg",
        "target_weight": "68kg",
        "joined": "2024-01-15",
        "level": "Intermediate"
    })