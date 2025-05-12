from rest_framework import viewsets, permissions
from .models import Category, Food, FoodLog, Routine
from .serializers import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from django.db.models import Sum, F,Count
from collections import defaultdict, OrderedDict
from datetime import datetime,timedelta
from rest_framework import status, filters


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated]

class FoodViewSet(viewsets.ModelViewSet):
    queryset = Food.objects.all()
    serializer_class = FoodSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name'] 
    @action(detail=False, methods=['post'], serializer_class=FoodCalculationSerializer)
    def calculate_nutrition(self, request):
        """
        Calculate the nutrition details based on food name and quantity.
        """
        serializer = FoodCalculationSerializer(data=request.data)
        if serializer.is_valid():
            food_name = serializer.validated_data['food_name']
            quantity = serializer.validated_data['quantity']

            try:
                food = Food.objects.get(name__iexact=food_name)
            except Food.DoesNotExist:
                return Response({'error': 'Food not found'}, status=status.HTTP_404_NOT_FOUND)

            # Calculate the nutrition based on quantity
            result = {
                "food": food.name,
                "quantity": quantity,
                "calories": round(food.calories * quantity, 2),
                "protein": round((food.protein or 0) * quantity, 2),
                "carbs": round((food.carbs or 0) * quantity, 2),
                "fats": round((food.fats or 0) * quantity, 2)
            }

            return Response(result, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class FoodLogViewSet(viewsets.ModelViewSet):
    queryset = FoodLog.objects.all()
    serializer_class = FoodLogSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [filters.SearchFilter]
    search_fields = ['food__name']  

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    @action(detail=False, methods=['get'])
    def total_summary(self, request):
        date = request.query_params.get('date')
        if not date:
            date = datetime.today().date()

        logs = FoodLog.objects.filter(user=request.user, date=date)
        summary = logs.aggregate(
            total_calories=Sum(F('quantity') * F('food__calories')),
            total_protein=Sum(F('quantity') * F('food__protein')),
            total_carbs=Sum(F('quantity') * F('food__carbs')),
            total_fats=Sum(F('quantity') * F('food__fats')),
        )
        return Response({key: value or 0 for key, value in summary.items()})

    @action(detail=False, methods=['get'])
    def today_meal_summary(self, request):
        """Summary of today's meals with food details, ordered (breakfast, lunch, snacks, dinner)"""
        today = datetime.today().date()
        logs = FoodLog.objects.filter(user=request.user, date=today).select_related('food')

        meal_order = ['breakfast', 'lunch', 'snacks', 'dinner']
        
        meal_summary = defaultdict(lambda: {
            'foods': [],
            'total_calories': 0,
            'total_protein': 0,
            'total_carbs': 0,
            'total_fats': 0
        })

        overall_total = {
            'total_calories': 0,
            'total_protein': 0,
            'total_carbs': 0,
            'total_fats': 0
        }

        for log in logs:
            meal_type = log.meal_type.lower()

            calories = (log.food.calories or 0) * log.quantity
            protein = (log.food.protein or 0) * log.quantity
            carbs = (log.food.carbs or 0) * log.quantity
            fats = (log.food.fats or 0) * log.quantity

            meal_summary[meal_type]['foods'].append({
                'food_name': log.food.name,
                'quantity': log.quantity,
                'calories': calories,
                'protein': protein,
                'carbs': carbs,
                'fats': fats,
            })

            meal_summary[meal_type]['total_calories'] += calories
            meal_summary[meal_type]['total_protein'] += protein
            meal_summary[meal_type]['total_carbs'] += carbs
            meal_summary[meal_type]['total_fats'] += fats

            # Add to overall
            overall_total['total_calories'] += calories
            overall_total['total_protein'] += protein
            overall_total['total_carbs'] += carbs
            overall_total['total_fats'] += fats

        # Ensure order and fill missing meals as None
        ordered_meals = OrderedDict()
        for meal in meal_order:
            ordered_meals[meal] = meal_summary.get(meal) or None

        return Response({
            'meals': ordered_meals,
            'total': overall_total
        })

    @action(detail=False, methods=['get'])
    def history(self, request):
        """Show user previous food logs grouped by date"""
        logs = FoodLog.objects.filter(user=request.user).order_by('-date')
        history = defaultdict(list)

        for log in logs:
            history[str(log.date)].append({
                'food_name': log.food.name,
                'quantity': log.quantity,
                'meal_type': log.meal_type,
                'calories': log.food.calories * log.quantity,
                'protein': (log.food.protein or 0) * log.quantity,
                'carbs': (log.food.carbs or 0) * log.quantity,
                'fats': (log.food.fats or 0) * log.quantity,
            })

        return Response(history)
    @action(detail=False, methods=['get'])
    def weekly_summary(self, request):
        """Show last 7 days food summary"""
        today = datetime.today().date()
        last_week = today - timedelta(days=6)  # 6 days back + today = 7 days

        logs = FoodLog.objects.filter(user=request.user, date__range=[last_week, today])

        summary_per_day = defaultdict(lambda: {
            'total_calories': 0,
            'total_protein': 0,
            'total_carbs': 0,
            'total_fats': 0
        })

        for log in logs:
            date_str = str(log.date)
            summary_per_day[date_str]['total_calories'] += (log.food.calories * log.quantity)
            summary_per_day[date_str]['total_protein'] += ((log.food.protein or 0) * log.quantity)
            summary_per_day[date_str]['total_carbs'] += ((log.food.carbs or 0) * log.quantity)
            summary_per_day[date_str]['total_fats'] += ((log.food.fats or 0) * log.quantity)

        return Response(summary_per_day)
    @action(detail=False, methods=['get'])
    def top_foods(self, request):
        """Show top eaten foods by user"""
        foods = FoodLog.objects.filter(user=request.user)\
            .values('food__name')\
            .annotate(times_eaten=Count('id'))\
            .order_by('-times_eaten')[:5]  # Top 5 foods

        return Response(foods)



    
    # @action(detail=False, methods=['get'])
    # def goal_progress(self, request):
    #     """Calories goal vs achieved today"""
    #     today = datetime.today().date()
    #     logs = FoodLog.objects.filter(user=request.user, date=today)

    #     total_calories = logs.aggregate(
    #         total=Sum(F('quantity') * F('food__calories'))
    #     )['total'] or 0

    #     user_details = request.user  # assuming OneToOne with UserDetails
    #     daily_goal = user_details.daily_calorie_limit

    #     percentage = (total_calories / daily_goal) * 100 if daily_goal else 0

    #     return Response({
    #         'goal': daily_goal,
    #         'achieved': total_calories,
    #         'percentage': round(percentage, 2)
    #     })



class RoutineViewSet(viewsets.ModelViewSet):
    queryset = Routine.objects.all()
    serializer_class = RoutineSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)


class FoodBulkUploadAPIView(APIView):
    permission_classes = [permissions.IsAdminUser]

    def post(self, request):
        serializer = FoodBulkUploadSerializer(data=request.data.get("foods", []), many=True)
        if serializer.is_valid():
            created = []
            for item in serializer.validated_data:
                category_name = item["category"]
                category, _ = Category.objects.get_or_create(
                    name=category_name, 
                    defaults={"slug": category_name.lower().replace(" ", "-")}
                )

                food = Food.objects.create(
                    name=item["name"],
                    category=category,
                    calories=item["calories"],
                    protein=item.get("protein", 0),
                    carbs=item.get("carbs", 0),
                    fats=item.get("fats", 0)
                )
                created.append(food.name)
            return Response({"message": "Foods uploaded", "created": created}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

