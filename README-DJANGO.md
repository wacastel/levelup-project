# LevelUp: Django Architecture & Implementation Guide

This document serves as a deep dive into the architectural patterns of Django and how they are explicitly implemented to power the **LevelUp** gamified habit-tracking platform.

It is designed as a technical reference guide to explain *how* Django works under the hood, and *why* the application is structured the way it is.

---

## 1. The Core Philosophy: MVT Architecture

Django follows a design pattern known as **MVT (Model-View-Template)**. While similar to the traditional MVC (Model-View-Controller) pattern used by other frameworks, Django handles the "Controller" part itself.

Here is how the responsibilities are divided in LevelUp:

* **Model (The Data):** The single, definitive source of truth about your data. It contains the essential fields and behaviors of the data you are storing. Django translates these Python classes into complex PostgreSQL database tables automatically.
* **View (The Logic):** The "brain" of the application. It receives an HTTP request from a user, retrieves the necessary data from the Models, applies business logic (like calculating XP or level-ups), and passes that data to a Template.
* **Template (The Presentation):** The HTML/CSS structure that determines how the data is visually presented to the user. Django's templating engine allows us to inject dynamic Python variables directly into HTML.

---

## 2. Project vs. App Structure

Django strictly separates the global configuration from the actual features of the application.

* **The Project (`config/` or `levelup/`):** This is the management layer. It contains global settings (`settings.py`), the master routing map (`urls.py`), and the WSGI configuration (`wsgi.py`) used by Gunicorn and Google App Engine to boot the server.
* **The Apps (`accounts/`, `tracker/`, `pages/`):** Django is modular. An "app" is a self-contained module that does one specific thing.
* `accounts`: Handles user registration, login, and profile management.
* `tracker`: The core engine of LevelUp (habits, daily logs, XP calculation).
* `pages`: Handles static content like the landing page or about page.



---

## 3. LevelUp Models: The Database Blueprint

In Django, you do not write raw SQL to create database tables. Instead, you write Python classes in `models.py`. Django's ORM (Object-Relational Mapper) translates these classes into your Cloud SQL database.

### The Custom User Model

By default, Django comes with a built-in User model. For LevelUp, we extend this to include RPG mechanics:

```
from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    xp = models.IntegerField(default=0)
    level = models.IntegerField(default=1)

    def add_xp(self, amount):
        self.xp += amount
        # Logic to calculate if XP exceeds the threshold for the next level
        if self.xp >= self.calculate_next_level_threshold():
            self.level += 1
        self.save()

```

### The Tracker Models

The `tracker` app defines what users are interacting with daily.

```
class Habit(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    xp_reward = models.IntegerField(default=10)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class DailyLog(models.Model):
    habit = models.ForeignKey(Habit, on_delete=models.CASCADE)
    completed_date = models.DateField(auto_now_add=True)
    notes = models.TextField(blank=True, null=True)

```

* **Foreign Keys:** The `user = models.ForeignKey(...)` creates a one-to-many relationship. A user can have many habits. If the user is deleted (`on_delete=models.CASCADE`), all their habits are cleanly deleted from the PostgreSQL database as well.

---

## 4. Views & URLs: The Brains and the Map

When a user interacts with LevelUp, Django uses `urls.py` to route their request to the correct function in `views.py`.

### The URL Router (`urls.py`)

This is the switchboard. When a user navigates to `levelup.com/habits/`, Django reads this file to figure out what Python code to execute.

```
from django.urls import path
from . import views

urlpatterns = [
    path('habits/', views.habit_list, name='habit_list'),
    path('habits/<int:habit_id>/complete/', views.complete_habit, name='complete_habit'),
]

```

### The Business Logic (`views.py`)

The view processes the request. For LevelUp, this is where the gamification magic happens.

```
from django.shortcuts import render, redirect, get_object_or_404
from .models import Habit, DailyLog

def complete_habit(request, habit_id):
    # 1. Fetch the habit, ensuring it belongs to the logged-in user
    habit = get_object_or_404(Habit, id=habit_id, user=request.user)
    
    if request.method == "POST":
        # 2. Create a log entry for today
        DailyLog.objects.create(habit=habit, notes=request.POST.get('notes'))
        
        # 3. Reward the user with XP
        request.user.add_xp(habit.xp_reward)
        
        # 4. Redirect them back to their dashboard
        return redirect('habit_list')
        
    # If not a POST request, just show the confirmation page
    return render(request, 'tracker/complete_habit.html', {'habit': habit})

```

---

## 5. The Request/Response Cycle

To fully understand Django, here is the exact lifecycle of a single interaction in LevelUp (e.g., clicking the "Complete Habit" button):

1. **The Request:** The user's browser sends an HTTP POST request to `https://levelup.appspot.com/habits/5/complete/`.
2. **The Server:** Google App Engine routes the traffic to Gunicorn.
3. **The Router:** Gunicorn passes the request to Django's root `urls.py`. Django strips away the domain name, looks at `/habits/5/complete/`, and matches it to a URL pattern.
4. **The View:** Django calls the `complete_habit` function, passing in the `request` object and the number `5` as the `habit_id`.
5. **The ORM (Database):** The view asks the ORM for Habit #5. The ORM translates this into a highly optimized SQL `SELECT` query, securely runs it against your Cloud SQL PostgreSQL instance via the Unix socket, and returns the data as a Python object.
6. **The Logic:** The view creates a new DailyLog, updates the user's XP, and saves both to the database.
7. **The Response:** The view instructs Django to return an HTTP 302 Redirect back to the dashboard. The browser receives this and loads the updated page, showing the user their shiny new XP total.

---

## 6. The Django Admin: Free CRUD

One of Django's most powerful features is the built-in Admin panel. By registering your models in `admin.py`, Django instantly generates a secure, production-ready GUI for managing your database.

```
from django.contrib import admin
from .models import Habit, DailyLog

# Registering the models makes them manageable at /admin/
admin.site.register(Habit)
admin.site.register(DailyLog)

```

In LevelUp, this allows administrators to manually adjust a user's XP, correct habit streaks, or moderate data without writing a single line of SQL or building custom internal tools.