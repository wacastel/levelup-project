from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Habit, DailyLog

@admin.register(Habit)
class HabitAdmin(admin.ModelAdmin):
    # Determines which columns appear in the main list view
    list_display = ('title', 'user', 'xp_reward', 'created_at')
    
    # Adds a filter sidebar
    list_filter = ('created_at', 'user')
    
    # Adds a search bar that searches these specific fields
    search_fields = ('title', 'description', 'user__username')

@admin.register(DailyLog)
class DailyLogAdmin(admin.ModelAdmin):
    list_display = ('habit', 'get_user', 'completed_date')
    list_filter = ('completed_date', 'habit__user')
    
    # Custom method to display the user in the DailyLog list view
    # since 'user' is tied to the Habit, not directly to the DailyLog
    def get_user(self, obj):
        return obj.habit.user
    get_user.short_description = 'User'  # Names the column in the admin panel
    get_user.admin_order_field = 'habit__user' # Allows sorting by this column
