# Deploying leumas to PythonAnywhere

## Step 1: Create GitHub Repository

First, push your code to GitHub:

```bash
cd /Users/leumas/Portfolio/leumas/leumasp
git init
git add .
git commit -m "Initial commit: leumas portfolio"
git remote add origin https://github.com/yourusername/leumasp.git
git branch -M main
git push -u origin main
```

## Step 2: Create PythonAnywhere Account

1. Go to https://www.pythonanywhere.com/
2. Click **"Create account"**
3. Choose a username (e.g., `yourusername`)
4. Your free web app will be at: `yourusername.pythonanywhere.com`
5. Verify your email

## Step 3: Create Web App

1. Log in to PythonAnywhere
2. Click **"Web"** in the top menu
3. Click **"Add a new web app"**
4. Choose **"Manual configuration"** (not a template)
5. Select **Python 3.10**
6. Click through to finish

## Step 4: Clone Your Repository

In PythonAnywhere terminal:

```bash
cd /home/yourusername
git clone https://github.com/yourusername/leumasp.git
cd leumasp
mkvirtualenv --python=/usr/bin/python3.10 leumasp-env
workon leumasp-env
pip install -r requirements.txt
python manage.py collectstatic --noinput
```

## Step 5: Configure Web App

### 5a. WSGI Configuration

1. Go to **Web** → **yourusername.pythonanywhere.com** (click on it)
2. Scroll to **"Code"** section
3. Find **"WSGI configuration file"**
4. Click the link to edit it
5. Replace the content with:

```python
import os
import sys

path = '/home/yourusername/leumasp'
if path not in sys.path:
    sys.path.append(path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'leumasp.settings'

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

**Save** the file.

### 5b. Python Version

In the same **Web** page:
- Scroll to **"Python version"** section
- Click the version (should be 3.10)

### 5c. Virtual Environment

- Scroll to **"Virtualenv"**
- Click the text field
- Enter: `/home/yourusername/.virtualenvs/leumasp-env`
- Click the checkmark

### 5d. Static Files

1. Scroll to **"Static files"** section
2. Click **"Enter URL"** and type: `/static/`
3. Click **"Enter path"** and browse to: `/home/yourusername/leumasp/staticfiles`
4. Click the checkmark

If using default admin, also add:
- URL: `/admin/static/`
- Path: `/home/yourusername/.virtualenvs/leumasp-env/lib/python3.10/site-packages/django/contrib/admin/static`

## Step 6: Set Environment Variables

1. Go to **Web** → your app
2. Scroll down to **"Environment variables"** section
3. Click **"Add a new variable"**
4. Add each variable from `.env.example`:

```
SECRET_KEY = (generate a random 50-char string or keep the one from settings)
DEBUG = False
ALLOWED_HOSTS = yourusername.pythonanywhere.com,www.yourusername.pythonanywhere.com
EMAIL_HOST = smtp.gmail.com
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = your-email@gmail.com
EMAIL_HOST_PASSWORD = your-app-password
RECIPIENT_ADDRESS = your-email@gmail.com
```

### Getting Gmail App Password:
1. Enable 2-Factor Authentication on Gmail
2. Go to https://myaccount.google.com/apppasswords
3. Generate an app password for "Mail" on "Windows PC" (or your device)
4. Copy the 16-character password
5. Paste into `EMAIL_HOST_PASSWORD`

## Step 7: Run Migrations

In PythonAnywhere terminal:

```bash
cd /home/yourusername/leumasp
source /home/yourusername/.virtualenvs/leumasp-env/bin/activate
python manage.py migrate
python manage.py createsuperuser  # Optional: create admin user
```

## Step 8: Reload Web App

1. Go to **Web** → **yourusername.pythonanywhere.com**
2. Click **"Reload yourusername.pythonanywhere.com"** button (green at top)
3. Wait 20 seconds

## Step 9: Test Your Site

Visit: `https://yourusername.pythonanywhere.com`

### Troubleshooting:

If you see an error:
1. Go to **Web** → your app
2. Scroll to **"Log files"** section
3. Click **"error.log"** to see what went wrong
4. Common issues:
   - `ModuleNotFoundError`: Virtual environment path is wrong
   - `No such file or directory`: Static files path is wrong
   - `ALLOWED_HOSTS` error: Add domain to `ALLOWED_HOSTS` env var
   - `Email sending failed`: Check `EMAIL_HOST_PASSWORD` is correct

## Step 10 (Optional): Set Custom Domain

1. Go to **Account** → **"Domains"** (if you own a domain)
2. Click **"Add a domain"**
3. Enter your domain (e.g., `yourdomain.com`)
4. Update your domain registrar's DNS to point to PythonAnywhere's IP
5. PythonAnywhere will provide instructions

## Step 11: Update GitHub

Whenever you make changes locally:

```bash
git add .
git commit -m "Update portfolio"
git push origin main
```

Then on PythonAnywhere terminal:

```bash
cd /home/yourusername/leumasp
git pull origin main
python manage.py collectstatic --noinput
```

Go to **Web** and click **"Reload"** button.

## Deployment Checklist

- [ ] GitHub repository created and code pushed
- [ ] PythonAnywhere account created
- [ ] Web app configured
- [ ] Repository cloned on PythonAnywhere
- [ ] Virtual environment created
- [ ] Requirements installed
- [ ] WSGI file updated
- [ ] Static files path configured
- [ ] Environment variables set
- [ ] Migrations run
- [ ] Site tested at `yourusername.pythonanywhere.com`
- [ ] Custom domain set (optional)

## Security Notes

- ✅ `DEBUG = False` in production (env var)
- ✅ `SECRET_KEY` should be random and kept secret (env var)
- ✅ HTTPS is enabled by default
- ✅ CSRF protection enabled
- ✅ Email credentials stored as env vars (not in code)
- ✅ Static files served efficiently with WhiteNoise

## Updates & Maintenance

- Monitor `error.log` regularly for issues
- Keep Django and dependencies updated with: `pip install --upgrade -r requirements.txt`
- Check PythonAnywhere notifications for server updates
- Backup your database regularly (download from `/home/yourusername/leumasp/db.sqlite3`)
