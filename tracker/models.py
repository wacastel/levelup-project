from django.db import models
from django.contrib.auth.models import User

# Corrected: subclass models.Model instead of models.fields.Model
class Habit(models.Model):
    # Tie each habit to a specific user
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='habits')
    
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    
    # How much XP this habit is worth when completed
    xp_reward = models.PositiveIntegerField(default=10) 
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

# Corrected: subclass models.Model instead of models.fields.Model
class DailyLog(models.Model):
    # A record of when a habit was completed
    habit = models.ForeignKey(Habit, on_delete=models.CASCADE, related_name='logs')
    completed_date = models.DateField(auto_now_add=True)
    
    # Optional: Allow notes on how the completion went
    notes = models.CharField(max_length=255, blank=True)

    class Meta:
        # Prevent logging the same habit multiple times on the same day
        unique_together = ['habit', 'completed_date']

    def __str__(self):
        return f"{self.habit.title} completed on {self.completed_date}"
