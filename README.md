# LevelUp - Gamify Your Goals

**LevelUp** is a Django-based web application designed to help users track their habits and goals through a gamified experience. By completing daily tasks, users earn XP (Experience Points) and progress through levels, turning personal productivity into a role-playing game (RPG) journey.

---

## 🚀 Features

* **User Authentication**: Secure sign-up and log-in system using Django's built-in authentication framework.
* **Habit Tracking**: Define habits with custom XP rewards.
* **Daily Logs**: Record habit completion with specific notes and daily constraints.
* **Django Admin Integration**: A fully customized dashboard for administrative data management.
* **Production-Ready Server**: WSGI configuration running via Gunicorn for high-concurrency request handling.
* **Test-Driven Development (TDD)**: Comprehensive unit tests for Models, Views, and URL routing.

---

## 🛠️ Tech Stack

* **Backend**: Python 3.12+ / Django 5.x
* **Web Server (WSGI)**: Gunicorn
* **Database**: SQLite (Local Dev) / PostgreSQL (Cloud SQL Production)
* **Cloud Infrastructure**: Google App Engine (Standard Environment)
* **Container Registry**: Google Artifact Registry
* **Static Files**: Whitenoise for efficient static file serving in production environments.

---

## ⚙️ Local Setup and Installation

Follow these steps to get the project running on your local machine:

1. **Clone the repository**:
    git clone https://github.com/your-username/levelup-project.git
    cd levelup-project

2. **Set up a virtual environment**:
    python3 -m venv venv
    source venv/bin/activate

3. **Install dependencies**:
    pip install -r requirements.txt

4. **Apply local database migrations**:
    python manage.py makemigrations
    python manage.py migrate

5. **Create a local superuser** (for Admin access):
    python manage.py createsuperuser

6. **Launch the development server**:
    python manage.py runserver

Visit `http://127.0.0.1:8000/` in your browser!

---

## ☁️ Google Cloud Deployment Guide

This application is fully architected for production deployment on **Google Cloud Platform (GCP)**. 

### 1. Prerequisites & GCP Setup
Ensure you have the Google Cloud SDK installed globally on your system (not inside the project directory) and initialize your project:

    gcloud init
    gcloud services enable artifactregistry.googleapis.com cloudbuild.googleapis.com

### 2. IAM Permissions
The App Engine default service account requires specific permissions to successfully build containers and write to storage buckets. Apply the following roles to your `[PROJECT_ID]@appspot.gserviceaccount.com` service account:

    gcloud projects add-iam-policy-binding [PROJECT_ID] \
      --member="serviceAccount:[PROJECT_ID]@appspot.gserviceaccount.com" \
      --role="roles/artifactregistry.admin"

    gcloud projects add-iam-policy-binding [PROJECT_ID] \
      --member="serviceAccount:[PROJECT_ID]@appspot.gserviceaccount.com" \
      --role="roles/storage.admin"

### 3. File Optimization (.gcloudignore)
To ensure fast, lean deployments without file-limit errors, ensure a `.gcloudignore` file is present in the root directory. This prevents uploading virtual environments and SDKs:

    .gcloudignore
    .git/
    .gitignore
    venv/
    env/
    .venv/
    google-cloud-sdk/
    __pycache__/
    *.pyc
    .env

### 4. Application Configuration (app.yaml)
App Engine requires an `app.yaml` file to define the runtime and database connections. Crucially, the `entrypoint` must be defined so Google's Nginx server knows how to boot the Django WSGI application via Gunicorn:

    runtime: python312
    entrypoint: gunicorn -b :$PORT config.wsgi:application

    env_variables:
      # Add environment variables here

### 5. Deployment
Deploy the application to App Engine:

    gcloud app deploy

### 6. Production Database Migrations (Cloud SQL Proxy)
App Engine handles the application code, but the Cloud SQL PostgreSQL database must be migrated separately using the Cloud SQL Auth Proxy.

In a separate terminal tab, start the proxy:

    ./cloud-sql-proxy [CONNECTION_NAME]

While the proxy is running, apply the migrations and create the production administrator account from your main terminal:

    python manage.py migrate
    python manage.py createsuperuser

---

## 🧪 Running Tests

This project follows a strict TDD workflow. To run the full test suite for the `pages`, `tracker`, and `accounts` apps:

    python manage.py test

---

## 📜 License

This project is open-source and available under the MIT License.