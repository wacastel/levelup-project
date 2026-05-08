from django.test import TestCase
from django.contrib.auth.models import User
from django.db.utils import IntegrityError
from .models import Habit, DailyLog

class HabitModelTests(TestCase):
    def setUp(self):
        # setUp runs before every single test. We need a user to tie habits to.
        self.user = User.objects.create_user(username="testuser", password="password123")

    def test_habit_creation_and_defaults(self):
        # Test that a habit is created correctly and defaults to 10 XP
        habit = Habit.objects.create(
            user=self.user,
            title="Drink Water",
            description="Drink 8 glasses of water today"
        )
        self.assertEqual(habit.title, "Drink Water")
        self.assertEqual(habit.xp_reward, 10) # Testing the default value
        self.assertEqual(str(habit), "Drink Water") # Testing the __str__ method

class DailyLogModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password123")
        self.habit = Habit.objects.create(user=self.user, title="Read 10 Pages")

    def test_daily_log_creation(self):
        # Test that a user can log a habit
        log = DailyLog.objects.create(habit=self.habit, notes="Read chapter 1")
        self.assertEqual(log.habit, self.habit)
        self.assertTrue(log.completed_date) # Date should be auto-populated
        
    def test_cannot_log_same_habit_twice_in_one_day(self):
        # Create the first log
        DailyLog.objects.create(habit=self.habit, notes="Morning session")
        
        # Attempting to create a second log for the exact same habit on the same day 
        # should raise an IntegrityError because of our 'unique_together' constraint.
        with self.assertRaises(IntegrityError):
            DailyLog.objects.create(habit=self.habit, notes="Evening session")
