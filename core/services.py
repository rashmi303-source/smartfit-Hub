from .models import User, DietPlan, WorkoutPlan
from django.utils import timezone
from datetime import timedelta


class DietService:
    INDIAN_FOODS = {
        'vegetarian': {
            'breakfast': ['Poha with curd', 'Vegetable Upma', 'Moong Dal Chilla', 'Besan Cheela'],
            'lunch': ['Dal Tadka Rice', 'Roti Sabzi', 'Rajma Chawal', 'Paneer Butter Masala'],
            'dinner': ['Khichdi', 'Roti Dal', 'Veg Biryani', 'Stuffed Capsicum'],
            'snacks': ['Mixed Sprouts', 'Fruit Salad', 'Roasted Chana', 'Greek Yogurt']
        },
        'non_veg': {
            'breakfast': ['Egg Bhurji', 'Chicken Omelette', 'Masala Egg', 'Chicken Sandwich'],
            'lunch': ['Chicken Curry Rice', 'Fish Fry Roti', 'Mutton Biryani', 'Egg Curry'],
            'dinner': ['Grilled Chicken', 'Tandoori Fish', 'Chicken Tikka', 'Egg Bharta'],
            'snacks': ['Boiled Eggs', 'Chicken Tikka', 'Fish Fingers', 'Grilled Paneer']
        },
        'vegan': {
            'breakfast': ['Oats with fruits', 'Vegan Pancakes', 'Smoothie Bowl'],
            'lunch': ['Dal Rice', 'Veg Curry Roti', 'Quinoa Khichdi'],
            'dinner': ['Veg Stir Fry', 'Lentil Soup', 'Stuffed Peppers'],
            'snacks': ['Fruits', 'Nuts', 'Roasted Seeds']
        }
    }

    @staticmethod
    def calculate_bmr(user):
        if user.gender == 'male':
            return 88.362 + (13.397 * user.weight) + (4.799 * user.height) - (5.677 * user.age)
        else:
            return 447.593 + (9.247 * user.weight) + (3.098 * user.height) - (4.330 * user.age)

    @staticmethod
    def get_daily_calories(user):
        bmr = DietService.calculate_bmr(user)
        multipliers = {'sedentary': 1.2, 'light': 1.375, 'moderate': 1.55, 'active': 1.725, 'very_active': 1.9}
        tdee = bmr * multipliers.get(user.activity_level, 1.2)
        adjustments = {'weight_loss': 0.85, 'maintenance': 1.0, 'muscle_gain': 1.15, 'weight_gain': 1.2}
        return int(tdee * adjustments.get(user.goal, 1.0))

    @staticmethod
    def generate_diet_plan(user):
        calories = DietService.get_daily_calories(user)
        macros = DietService.calculate_macros(calories)
        foods = DietService.INDIAN_FOODS.get(user.diet_type.lower(), DietService.INDIAN_FOODS['vegetarian'])

        meals = [
            {"name": "Breakfast",
             "items": [foods['breakfast'][0 % len(foods['breakfast'])], foods['snacks'][0 % len(foods['snacks'])]],
             "calories": int(calories * 0.25), "protein": macros['protein'] * 0.3, "carbs": macros['carbs'] * 0.25,
             "fats": macros['fats'] * 0.25},
            {"name": "Lunch", "items": [foods['lunch'][0 % len(foods['lunch'])]], "calories": int(calories * 0.35),
             "protein": macros['protein'] * 0.4, "carbs": macros['carbs'] * 0.4, "fats": macros['fats'] * 0.35},
            {"name": "Dinner", "items": [foods['dinner'][0 % len(foods['dinner'])]], "calories": int(calories * 0.3),
             "protein": macros['protein'] * 0.25, "carbs": macros['carbs'] * 0.3, "fats": macros['fats'] * 0.35},
            {"name": "Snacks", "items": [foods['snacks'][1 % len(foods['snacks'])]], "calories": int(calories * 0.1),
             "protein": macros['protein'] * 0.05, "carbs": macros['carbs'] * 0.05, "fats": macros['fats'] * 0.05}
        ]

        DietPlan.objects.create(
            user=user, date=timezone.now().date(),
            total_calories=calories, protein=macros['protein'],
            carbs=macros['carbs'], fats=macros['fats'], meals=meals
        )

    @staticmethod
    def calculate_macros(calories):
        protein = calories * 0.30 / 4
        carbs = calories * 0.50 / 4
        fats = calories * 0.20 / 9
        return {'protein': round(protein, 1), 'carbs': round(carbs, 1), 'fats': round(fats, 1)}


class WorkoutService:
    WORKOUTS = {
        'beginner': {
            'weight_loss': [
                {'name': 'Brisk Walking', 'sets': 1, 'reps': '30 mins', 'calories': 250},
                {'name': 'Bodyweight Squats', 'sets': 3, 'reps': 12},
                {'name': 'Pushups (Knee)', 'sets': 3, 'reps': 8}
            ],
            'muscle_gain': [
                {'name': 'Pushups', 'sets': 3, 'reps': 10},
                {'name': 'Squats', 'sets': 3, 'reps': 12},
                {'name': 'Plank', 'sets': 3, 'reps': '20 sec'}
            ],
            'weight_gain': [
                {'name': 'Pullups Assisted', 'sets': 3, 'reps': 8},
                {'name': 'Dumbbell Rows', 'sets': 3, 'reps': 10},
                {'name': 'Lunges', 'sets': 3, 'reps': 12}
            ]
        },
        'intermediate': {
            'weight_loss': [
                {'name': 'Running', 'sets': 1, 'reps': '40 mins'},
                {'name': 'Burpees', 'sets': 4, 'reps': 12},
                {'name': 'Mountain Climbers', 'sets': 3, 'reps': 20}
            ]
        }
    }

    @staticmethod
    def generate_workout_plan(user):
        level_map = {'sedentary': 'beginner', 'light': 'beginner', 'moderate': 'intermediate',
                     'active': 'intermediate', 'very_active': 'advanced'}
        level = level_map.get(user.activity_level, 'beginner')
        workouts = WorkoutService.WORKOUTS.get(level, {}).get(user.goal,
                                                              WorkoutService.WORKOUTS['beginner']['weight_loss'])
        duration = len(workouts) * 15

        WorkoutPlan.objects.create(
            user=user, title=f"{level.title()} {user.goal.replace('_', ' ').title()}",
            level=level, exercises=workouts, duration=duration, date=timezone.now().date()
        )