# Deploying Django to Google App Engine (GAE)

This guide outlines the complete, production-ready process for taking a local Django application (**LevelUp**) and deploying it to the Google App Engine Standard Environment. 

It assumes you have already provisioned a Google Cloud SQL instance and created a database (see `README-CLOUD-SQL.md`).

---

## Step 1: Pre-Flight File Optimization (.gcloudignore)

By default, Google's deployment tool will attempt to upload every single file in your project folder, including your massive virtual environment and SDK tools. This will cause the deployment to hit file limits and fail.

Create a file named `.gcloudignore` in the root of your project and add the following to keep your upload lean (aiming for under 200 files):

    .gcloudignore
    .git/
    .gitignore
    
    # Virtual Environments & SDKs
    venv/
    env/
    .venv/
    google-cloud-sdk/
    
    # Python Cache & Local Configs
    __pycache__/
    *.pyc
    .env
    db.sqlite3

## Step 2: Install Production Server Packages

App Engine requires a production-grade web server to run Python, as well as a utility to serve Django's static files (like CSS and JavaScript) efficiently.

1. Ensure your local virtual environment is activated.
2. Install **Gunicorn** (the web server) and **Whitenoise** (the static file server):

    pip install gunicorn whitenoise

3. Freeze your dependencies so App Engine knows exactly what to install during deployment:

    pip freeze > requirements.txt

## Step 3: Configure `settings.py` for Production

Django needs to know how to behave when it wakes up inside a Google data center. Open `config/settings.py` and make the following changes:

**1. Allowed Hosts**
Allow traffic from Google's domains:

    ALLOWED_HOSTS = ['*']

**2. Static File Serving**
Add Whitenoise to your middleware, directly under `SecurityMiddleware`:

    MIDDLEWARE = [
        'django.middleware.security.SecurityMiddleware',
        'whitenoise.middleware.WhiteNoiseMiddleware', # ADD THIS
        'django.contrib.sessions.middleware.SessionMiddleware',
        # ...
    ]

Then, define the absolute path where Django should gather static files:

    STATIC_URL = 'static/'
    STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

**3. Environment-Aware Database Connection**
When running locally, connect via the `.env` file. When running on GAE, connect securely via Google's internal Unix Sockets:

    # env('GAE_APPLICATION') is automatically injected by Google App Engine
    if env('GAE_APPLICATION', default=None):
        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.postgresql',
                'NAME': env('DB_NAME'),
                'USER': env('DB_USER'),
                'PASSWORD': env('DB_PASS'),
                'HOST': f"/cloudsql/{env('CLOUD_SQL_CONNECTION_NAME')}",
            }
        }
    else:
        # Fallback to local .env configuration
        DATABASES = {
            'default': env.db(),
        }

## Step 4: The `app.yaml` Configuration File

App Engine relies on `app.yaml` to understand your infrastructure requirements. Create this file in your project root. 

*Crucial Note: You MUST include the `entrypoint` command. Without it, GAE will look for a `main.py` file, crash, and return a 502 Bad Gateway error.*

    runtime: python312
    
    # Point the Gunicorn server to your specific Django wsgi file
    entrypoint: gunicorn -b :$PORT config.wsgi:application
    
    env_variables:
      DB_NAME: "levelup_db"
      DB_USER: "postgres"
      DB_PASS: "YourDatabasePassword"
      CLOUD_SQL_CONNECTION_NAME: "YOUR_PROJECT_ID:us-central1:level-db-instance"
    
    handlers:
    # Route all web traffic to the Django application
    - url: /.*
      script: auto

## Step 5: Google Cloud Project Prep (APIs & IAM)

Brand new Google Cloud projects start with heavy security restrictions and disabled APIs to save resources. You must manually open the doors for the deployment robot (the default service account).

**1. Enable Required APIs**
Turn on the Artifact Registry (container storage) and Cloud Build (the compiler):

    gcloud services enable artifactregistry.googleapis.com cloudbuild.googleapis.com

**2. Grant IAM Permissions**
Give your App Engine service account the keys to write to the storage buckets and registries:

    gcloud projects add-iam-policy-binding YOUR_PROJECT_ID \
      --member="serviceAccount:YOUR_PROJECT_ID@appspot.gserviceaccount.com" \
      --role="roles/artifactregistry.admin"
      
    gcloud projects add-iam-policy-binding YOUR_PROJECT_ID \
      --member="serviceAccount:YOUR_PROJECT_ID@appspot.gserviceaccount.com" \
      --role="roles/storage.admin"

## Step 6: Collect Static Files

Instruct Django to gather all static files (including the admin panel styles) into a single folder so Whitenoise can serve them. Run locally:

    python manage.py collectstatic

*(Type `yes` when prompted to overwrite existing files).*

## Step 7: Deploy to Google Cloud

With the APIs awake and the files optimized, push the code to Google's servers:

    gcloud app deploy

* **Note on Locked Deployments:** If a previous deployment crashed, Google may place a "ghost lock" on your default service (Error: *operation is already in progress*). This lock cannot be bypassed manually; you must wait 10 to 15 minutes for the internal system timeout to clear it before attempting to deploy again.

## Step 8: Post-Deploy Database Migrations

Your code is now live, but your production database is entirely empty. You must build the tables before the app will function.

1. In a new terminal tab, start your Cloud SQL Auth Proxy to open a secure tunnel to your live database:

    ./cloud-sql-proxy YOUR_PROJECT_ID:us-central1:level-db-instance

2. Back in your main terminal, apply the migrations to the live database:

    python manage.py migrate

3. Create your production administrator account:

    python manage.py createsuperuser

## Step 9: Monitor and Launch

Your application is fully deployed and connected! 

To view real-time server logs (excellent for debugging 500 errors):

    gcloud app logs tail -s default
    
To open your live production application in the browser:

    gcloud app browse