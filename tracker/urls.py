from django.urls import path
from . import views

urlpatterns = [
    # The main dashboard to list and add habits
    path('habits/', views.habit_list, name='habit_list'),
    
    # The endpoint to handle logging a completion
    path('habits/<int:habit_id>/complete/', views.complete_habit, name='complete_habit'),
]
