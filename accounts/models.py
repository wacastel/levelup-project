from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    # Gamification fields
    xp = models.PositiveIntegerField(default=0)
    level = models.PositiveIntegerField(default=1)

    def calculate_next_level_threshold(self):
        """
        Calculates how much total XP is needed to reach the NEXT level.
        Base formula: 100 XP per current level. 
        (e.g., Level 1 needs 100 XP to hit Level 2. Level 2 needs 200 XP to hit Level 3)
        """
        return self.level * 100

    def add_xp(self, amount):
        """
        Adds XP to the user and checks for level ups.
        """
        self.xp += amount
        
        # Loop in case they earn a massive amount of XP and level up multiple times at once
        while self.xp >= self.calculate_next_level_threshold():
            # Deduct the threshold amount (or keep it cumulative, depending on your preference)
            # For this example, we'll use cumulative XP, so we just increment the level
            self.level += 1
            
        self.save()

    def __str__(self):
        return f"{self.username} (Level {self.level})"
