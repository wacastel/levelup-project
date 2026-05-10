from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import Habit, DailyLog
from .forms import HabitForm, DailyLogForm

@login_required
def habit_list(request):
    # Retrieve only the habits belonging to the logged-in user [cite: 2]
    habits = Habit.objects.filter(user=request.user)
    
    if request.method == 'POST':
        form = HabitForm(request.POST)
        if form.is_valid():
            new_habit = form.save(commit=False)
            new_habit.user = request.user
            new_habit.save()
            messages.success(request, 'New habit created!')
            return redirect('habit_list')
    else:
        form = HabitForm()
        
    context = {
        'habits': habits,
        'form': form,
    }
    return render(request, 'tracker/habit_list.html', context)

@login_required
def complete_habit(request, habit_id):
    # Fetch the habit, ensuring it belongs to the logged-in user [cite: 81]
    habit = get_object_or_404(Habit, id=habit_id, user=request.user)
    
    if request.method == 'POST':
        form = DailyLogForm(request.POST)
        if form.is_valid():
            # Check the unique_together constraint before saving 
            today = timezone.now().date()
            if DailyLog.objects.filter(habit=habit, completed_date=today).exists():
                messages.warning(request, "You've already logged this habit today!")
                return redirect('habit_list')

            daily_log = form.save(commit=False)
            daily_log.habit = habit
            daily_log.save()
            
            # Reward the user with XP [cite: 81, 82]
            if hasattr(request.user, 'add_xp'):
                request.user.add_xp(habit.xp_reward)
                messages.success(request, f'+{habit.xp_reward} XP! Habit logged.')
            else:
                messages.success(request, 'Habit logged successfully!')
                
            return redirect('habit_list')
    else:
        form = DailyLogForm()
        
    context = {
        'habit': habit,
        'form': form,
    }
    return render(request, 'tracker/complete_habit.html', context)
