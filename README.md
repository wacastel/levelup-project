# LevelUp - Gamify Your Goals

**LevelUp** is a Django-based web application designed to help users track their habits and goals through a gamified experience. By completing daily tasks, users earn XP (Experience Points) and progress through levels, turning personal productivity into a role-playing game (RPG) journey.

---

## 🚀 Features

*   **User Authentication**: Secure sign-up and log-in system using Django's built-in authentication framework.
*   **Habit Tracking**: Define habits with custom XP rewards.
*   **Daily Logs**: Record habit completion with specific notes and daily constraints.
*   **Django Admin Integration**: A fully customized dashboard for administrative data management.
*   **Test-Driven Development (TDD)**: Comprehensive unit tests for Models, Views, and URL routing.

---

## 🛠️ Tech Stack

*   **Backend**: Python 3.13+ / Django 5.x
*   **Database**: SQLite (Local Dev) / PostgreSQL (Cloud SQL Production)
*   **Cloud Infrastructure**: Designed for Google App Engine (Standard Environment)
*   **Testing**: Django TestCase / Unit Testing

---

## ⚙️ Local Setup and Installation

Follow these steps to get the project running on your local machine:

1. **Clone the repository**:
   ```bash
   git clone [https://github.com/your-username/levelup-project.git](https://github.com/your-username/levelup-project.git)
   cd levelup-project
   
```

2. **Set up a virtual environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   
```

3. **Install dependencies**:
   ```bash
   pip install django
   ```

4. **Apply database migrations**:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Create a superuser** (for Admin access):
   ```bash
   python manage.py createsuperuser
   ```

6. **Launch the development server**:
   ```bash
   python manage.py runserver
   
```
   Visit `http://127.0.0.1:8000/` in your browser!

---

## 🧪 Running Tests

This project follows a strict TDD workflow. To run the full test suite for the `pages`, `tracker`, and `accounts` apps:

```bash
python manage.py test
```

---

## ☁️ Deployment Roadmap

This application is architected for deployment to **Google Cloud Platform (GCP)**:
- **Google App Engine**: Hosting the Django application layer.
- **Cloud SQL (PostgreSQL)**: Managed persistent storage.
- **Whitenoise**: Efficient static file serving for production environments.

---

## 📜 License

This project is open-source and available under the [MIT License](LICENSE).
