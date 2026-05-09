# Provisioning a Micro-Tier Cloud SQL Instance 

When deploying a Django project like **LevelUp** to Google Cloud Platform (GCP), it is crucial to manage costs, especially during development. GCP's default Cloud SQL creation screens often steer users toward high-performance, expensive "Enterprise Plus" tiers. 

This guide details how to bypass those prompts and configure an ultra-low-cost `db-f1-micro` PostgreSQL instance (approximately $0.01/hour) using the Cloud console UI, and how to securely connect it to your local environment for initial database setup.

---

## Step 1: Navigate to Cloud SQL
1. Log into the Google Cloud Console.
2. Ensure your target project is selected in the top navigation bar.
3. Open the left-hand **Navigation Menu** (hamburger icon).
4. Scroll down through the Products list and click on **Cloud SQL** (located between *Databases* and *Google Maps Platform*).

## Step 2: Bypass the Enterprise Plus Promo
When creating a new instance, Google often displays a large banner offering "30 days at no cost" for an Enterprise Plus edition (e.g., 8 vCPUs, 64GB RAM). Do not use this for a lightweight dev environment, as it will drain credits rapidly after the 30 days.

1. Scroll past the promotional banner.
2. Locate the card titled **Sandbox**.
3. Click the link inside the card that says **Create Sandbox instance**.

## Step 3: Enable Required APIs
If this is a brand new GCP project, you may hit an interim screen requiring you to enable underlying APIs.

1. Look for **Compute Engine API** showing as "Not enabled".
2. Click the **Enable** button at the bottom of the list.
3. Wait 30-60 seconds. The page will automatically refresh into the main configuration form once complete.

## Step 4: Basic Instance Info
1. **Database version:** Select the latest supported version (e.g., **PostgreSQL 18**).
2. **Instance ID:** Name your instance (e.g., `level-db-instance`). Use lowercase letters and hyphens.
3. **Password:** Click **Generate** or type a highly secure password for the default `postgres` user. **Save this password immediately**, as you will need it for your Django `.env` and `app.yaml` files!
4. **Region:** Choose a region close to you (e.g., `us-central1 (Iowa)`). Leave Zonal availability as **Single zone** to save costs.

## Step 5: The Micro-Tier Hardware Configuration
This is the most critical step for cost-saving.

1. Scroll down to **Choose a Cloud SQL edition**.
2. Ensure the radio button for **Cloud SQL Enterprise** is selected (NOT Enterprise Plus).
3. Scroll down and expand the **Customize your instance** (or **Machine configuration**) section.
4. Locate the **Machine type** or **Presets** dropdown.
5. Change the category from "Standard" to **Shared core**.
6. Select the **`db-f1-micro`** option (1 vCPU, 0.6 GB RAM).

## Step 6: Storage Optimization
To reduce costs further, downgrade the storage from SSD to standard spinning disks.

1. Expand the **Storage** section.
2. Change "Storage type" from SSD to **HDD (Standard)**.
3. Change "Storage capacity" to the minimum allowed (usually **10 GB**).
4. Uncheck **Enable automatic storage increases** to prevent unexpected scaling charges.

## Step 7: Finalize and Create
1. Review the "Pricing estimate" in the bottom corner. It should reflect the low hourly cost of the shared-core machine and HDD storage.
2. Click the blue **Create Instance** button at the bottom of the page.
3. Wait 5-10 minutes for the instance to provision and show a green checkmark indicating it is ready to accept connections.

## Step 8: Create the Database
The previous steps created the database *server* (the Instance). Now you need to create the actual database inside that server.

1. Once the instance has a green checkmark, click on its name (`level-db-instance`) to open the Overview page.
2. In the left-hand menu, click on the **Databases** tab.
3. Click the blue **Create database** button at the top.
4. Name your database (e.g., `levelup_db`).
5. Click **Create**.

## Step 9: Retrieve Your Connection Name
To connect your local Django application or App Engine environment to this cloud database, you need the instance's unique connection string.

1. Navigate back to the **Overview** page for your instance.
2. Scroll down to the **Connect to this instance** section.
3. Locate the **Connection name** (it will look like `YOUR_PROJECT_ID:us-central1:level-db-instance`).
4. Copy and save this string.

---

## Step 10: Local Connection via Cloud SQL Auth Proxy
To run production migrations from your local Mac/PC before deploying to App Engine, you must use the Cloud SQL Auth Proxy. This creates a secure, encrypted tunnel from your local machine directly to the Google data center.

1. Download the Cloud SQL Proxy binary for your OS (e.g., Apple Silicon ARM64) and place it in your project root folder.
2. Open a dedicated terminal tab and start the proxy using your connection string:

    ./cloud-sql-proxy YOUR_PROJECT_ID:us-central1:level-db-instance

3. Keep this terminal tab open. Wait until the terminal outputs: **"Ready for new connections"**.

## Step 11: Initializing the Production Database
A brand new Cloud SQL database is completely empty. It does not have the tables required to store user accounts or Django app data. If you attempt to create a superuser or boot the application now, you will encounter a `relation "auth_user" does not exist` error.

While the Cloud SQL proxy is running in the background, open a **new terminal tab**, activate your virtual environment, and push your schemas to the cloud:

1. **Apply Migrations:**

    python manage.py migrate
    
2. **Create the Production Admin:**
Once the migrations complete successfully, generate the administrator account for your live site:

    python manage.py createsuperuser

Your Cloud SQL database is now fully configured, populated with your Django tables, and ready for the App Engine deployment!