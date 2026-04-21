from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import User, DailyTracking, DietPlan, WorkoutPlan

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name',
                 'age', 'height', 'weight', 'gender', 'goal', 'diet_type', 'activity_level']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, attrs):
        user = authenticate(username=attrs['username'], password=attrs['password'])
        if not user:
            raise serializers.ValidationError('Invalid credentials')
        attrs['user'] = user
        return attrs

class ProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['age', 'height', 'weight', 'gender', 'goal', 'diet_type', 'activity_level']

class DailyTrackingSerializer(serializers.ModelSerializer):
    class Meta:
        model = DailyTracking
        fields = '__all__'
        read_only_fields = ['user']
        extra_kwargs = {
            'calories_consumed': {'required': False},
            'calories_burned': {'required': False},
            'water_intake': {'required': False},
            'weight': {'required': False},
        }

class DietPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = DietPlan
        fields = '__all__'
        read_only_fields = ['user']

class WorkoutPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkoutPlan
        fields = '__all__'
        read_only_fields = ['user']