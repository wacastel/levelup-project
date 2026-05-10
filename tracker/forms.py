from django import forms
from .models import Habit, DailyLog

class HabitForm(forms.ModelForm):
    class Meta:
        model = Habit
        # We exclude 'user' and 'created_at' as they are handled in the background
        fields = ['title', 'description', 'xp_reward']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'E.g., 30 Min Walk'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'xp_reward': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
        }

class DailyLogForm(forms.ModelForm):
    class Meta:
        model = DailyLog
        # We only need the notes field; 'habit' and 'completed_date' are handled by the view/model [cite: 3, 4]
        fields = ['notes']
        widgets = {
            'notes': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Optional: How did it go?'}),
        }
