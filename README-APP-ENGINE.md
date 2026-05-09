# Deploying Django to Google App Engine (GAE)

This guide outlines the process for taking a local Django application (**LevelUp**) and deploying it to the Google App Engine Standard Environment. 

It assumes you have already provisioned a Google Cloud SQL instance and created a database (see `README-CLOUD-SQL.md`).

---

## Step 1: Install Production Server Packages

App Engine requires a production-grade web server to run Python, as well as a utility to serve Django's static files (like CSS and JavaScript) efficiently.

1. Ensure your local virtual environment is activated.
2. Install **Gunicorn** (the web server) and **Whitenoise** (the static file server):
   ```bash
   pip install gunicorn whitenoise
   ```
3. Freeze your dependencies so App Engine knows exactly what to install during deployment:
   ```bash
   pip freeze > requirements.txt
   ```

## Step 2: Configure `settings.py` for Production

Django needs to know how to behave when it wakes up inside a Google data center instead of on your local machine. Open `config/settings.py` and make the following changes:

**1. Allowed Hosts**
Allow traffic from Google's domains (you can lock this down to your specific URL later):
```python
ALLOWED_HOSTS = ['*']
```

**2. Static File Serving**
Add Whitenoise to your middleware, directly under `SecurityMiddleware`:
```python
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware', # ADD THIS
    'django.contrib.sessions.middleware.SessionMiddleware',
    # ...
]
```
Then, define the absolute path where Django should gather static files:
```python
STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
```

**3. Environment-Aware Database Connection**
When running locally, connect via the `.env` file and Auth Proxy. When running on GAE, connect securely via Google's internal Unix Sockets. Replace your `DATABASES` dictionary with this logic:

```python
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
```

## Step 3: Create the `app.yaml` Configuration File

App Engine relies on an `app.yaml` file in the root of your project to understand your infrastructure requirements. Create this file and add the following blueprint:

```yaml
# Specify the Python version (3.12 is currently the latest supported by standard GAE)
runtime: python312

env_variables:
  # Database Credentials
  DB_NAME: "levelup_db"
  DB_USER: "postgres"
  DB_PASS: "Plot5150!"
  # The exact connection string from your Cloud SQL instance overview
  CLOUD_SQL_CONNECTION_NAME: "YOUR_PROJECT_ID:us-central1:level-db-instance"

handlers:
# Route all web traffic to the Django application
- url: /.*
  script: auto
```

## Step 4: Collect Static Files

Before deploying, you must instruct Django to gather all static files (including the built-in admin panel styles) into a single folder so Whitenoise can serve them.

Run this command locally:
```bash
python manage.py collectstatic
```
*(Type `yes` when prompted to overwrite existing files).*

## Step 5: Deploy to Google Cloud

With the configuration complete, you are ready to push the code to Google's servers.

1. Run the deployment command:
   ```bash
   gcloud app deploy
   ```
2. If prompted, select a region for your App Engine app. Choose the **same region** as your Cloud SQL database (e.g., `us-central`) to minimize latency.
3. Review the summary provided in the terminal and type `Y` to confirm.
4. Wait for the build and deployment process to finish (typically 2-5 minutes).

Once complete, the CLI will output your live production URL (e.g., `https://your-project-id.uc.r.appspot.com`). You can quickly open it from the terminal by running:
```bash
gcloud app browse
```