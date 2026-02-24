# 🚀 Comprehensive Deployment Guide - Leumas Portfolio

This guide covers deploying the Leumas Portfolio to production on PythonAnywhere with complete step-by-step instructions.

---

## 📋 Table of Contents

1. [Pre-Deployment Checklist](#pre-deployment-checklist)
2. [Environment Setup](#environment-setup)
3. [PythonAnywhere Deployment](#pythonanywhere-deployment)
4. [Database Migration](#database-migration)
5. [Static Files](#static-files)
6. [SSL/HTTPS Configuration](#sslhttps-configuration)
7. [Email Configuration](#email-configuration)
8. [Error Tracking (Sentry)](#error-tracking-sentry)
9. [Monitoring & Health Checks](#monitoring--health-checks)
10. [Troubleshooting](#troubleshooting)
11. [Rollback Procedure](#rollback-procedure)
12. [After Deployment](#after-deployment)

---

## ✅ Pre-Deployment Checklist

### Code Quality
- [ ] All tests passing: `python manage.py test leumas`
- [ ] No security vulnerabilities: `bandit -r leumas`
- [ ] Code coverage above 80%: `coverage run --source='leumas' manage.py test`
- [ ] Linting checks pass: `flake8 leumas`
- [ ] No uncommitted changes: `git status`

### Configuration
- [ ] `.env.production` created with all secrets
- [ ] `DEBUG=False` in production settings
- [ ] `ALLOWED_HOSTS` includes production domain
- [ ] `SECRET_KEY` is strong and random
- [ ] Database credentials are secure

### Documentation
- [ ] Deployment steps documented
- [ ] Rollback procedure prepared
- [ ] Known issues documented
- [ ] Support contacts listed

---

## 🔧 Environment Setup

### 1. Create Production Environment File

```bash
cp .env.production.example .env.production
```

Fill in all required variables from `.env.production` template.

### 2. Generate Secret Key

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

Save this to `SECRET_KEY` in `.env.production`.

### 3. Verify Environment Variables

```bash
python -m dotenv -f .env.production list
```

---

## 🌐 PythonAnywhere Deployment

### Step 1: Create PythonAnywhere Account

1. Go to [PythonAnywhere.com](https://www.pythonanywhere.com)
2. Sign up with email
3. Choose account tier (free or premium)
4. Save your username

### Step 2: Set Up Web App

1. **Dashboard** → **Web** tab
2. Click **Add a new web app**
3. Select **Manual configuration**
4. Choose **Python 3.12** (or latest)
5. Note the WSGI file path

### Step 3: Clone Repository

In **Bash Console**:

```bash
cd ~
git clone https://github.com/leumasp/leumasp-main.git mysite
cd mysite
```

### Step 4: Create Virtual Environment

```bash
mkvirtualenv --python=/usr/bin/python3.12 mysite
pip install -r requirements.txt
```

### Step 5: Configure WSGI File

Edit the WSGI configuration file in PythonAnywhere:

```python
import os
import sys
from pathlib import Path

path = '/home/leumas/mysite'
if path not in sys.path:
    sys.path.append(path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'leumasp.settings'

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

### Step 6: Update Web App Settings

In **PythonAnywhere Web** tab:
- **Source code**: `/home/leumas/mysite`
- **Working directory**: `/home/leumas/mysite`
- **Virtualenv**: `/home/leumas/.virtualenvs/mysite`
- **Python version**: 3.12

---

## 🗄️ Database Migration

### Step 1: Run Migrations

```bash
cd ~/mysite
workon mysite
python manage.py migrate
```

### Step 2: Create Superuser

```bash
python manage.py createsuperuser
# Follow prompts
```

### Step 3: Verify Database

```bash
python manage.py shell
>>> from leumas.models import BlogPost
>>> BlogPost.objects.count()
```

---

## 📦 Static Files

### Step 1: Collect Static Files

```bash
python manage.py collectstatic --noinput
```

### Step 2: Configure in Web App

In **PythonAnywhere Web** tab, set Static files:
- **URL**: `/static/`
- **Directory**: `/home/leumas/mysite/staticfiles`

Reload the web app after configuration.

---

## 🔐 SSL/HTTPS Configuration

### Step 1: Enable HTTPS

In **PythonAnywhere Web** tab:
1. Enable **Force HTTPS**
2. Apply free SSL certificate

### Step 2: Update Django Settings

```python
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = 31536000
```

---

## 📧 Email Configuration

For Gmail SMTP in `.env.production`:

```env
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-16-char-app-password
```

Generate [App Password](https://myaccount.google.com/apppasswords) in Google Account.

### Test Email

```bash
python manage.py shell
>>> from django.core.mail import send_mail
>>> send_mail('Test', 'Message', 'from@example.com', ['to@example.com'])
1
```

---

## 🔍 Error Tracking (Sentry)

### Step 1: Create Sentry Project

1. Go to [Sentry.io](https://sentry.io)
2. Create new Django project
3. Copy DSN

### Step 2: Update Environment

```env
SENTRY_DSN=https://your-key@sentry.io/projectid
SENTRY_ENVIRONMENT=production
```

### Step 3: Configure Django

In `leumasp/settings.py`:

```python
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

sentry_sdk.init(
    dsn=os.environ.get('SENTRY_DSN'),
    integrations=[DjangoIntegration()],
    traces_sample_rate=0.1,
)
```

---

## 📊 Monitoring & Health Checks

### Step 1: Add Health Check Endpoint

Create view in `leumas/views.py`:

```python
from django.http import JsonResponse
from django.db import connection

def health_check(request):
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
        
        return JsonResponse({'status': 'healthy'})
    except Exception as e:
        return JsonResponse({'status': 'unhealthy', 'error': str(e)}, status=503)
```

Add to `leumasp/urls.py`:

```python
path('api/health/', views.health_check, name='health'),
```

### Step 2: Set Up Monitoring

Use [UptimeRobot.com](https://uptimerobot.com):

1. Create account
2. Add monitor for health endpoint
3. Get notifications on downtime

---

## 🚨 Troubleshooting

### ModuleNotFoundError

```bash
workon mysite
pip install -r requirements.txt
```

### 500 Error

1. Check **Web** → **Error log**
2. Check **Server log**
3. Set `DEBUG=True` temporarily

### Static Files Not Loading

```bash
python manage.py collectstatic --clear --noinput
# Reload web app
```

### Slow Page Load

1. Enable caching in settings
2. Optimize database queries
3. Check PythonAnywhere CPU usage

### Email Not Sending

```bash
python manage.py shell
>>> from django.core.mail import send_mail
>>> send_mail('Test', 'Test', 'from@email.com', ['to@email.com'])
```

---

## 🔄 Rollback Procedure

If deployment fails:

```bash
git reset --hard HEAD~1
git push origin main -f
# Reload web app in PythonAnywhere
```

Verify health:

```bash
curl https://leumas.pythonanywhere.com/api/health/
```

---

## ✨ After Deployment

### Verification Checklist

- [ ] Homepage loads
- [ ] All pages accessible
- [ ] Dark mode works
- [ ] Search/filtering works
- [ ] Contact form works
- [ ] Static files load
- [ ] Database connected
- [ ] Error tracking active
- [ ] Email sending works
- [ ] Health check responds

### Continuous Monitoring

- Monitor error logs daily
- Review Sentry errors weekly
- Check performance metrics
- Update dependencies monthly
- Backup database regularly

---

## 📞 Support

- **PythonAnywhere Docs**: https://help.pythonanywhere.com/
- **Django Docs**: https://docs.djangoproject.com/
- **GitHub Issues**: Report bugs
- **Email Support**: From deployed app

---

**Last Updated**: February 2026
**Version**: 4.0 (Complete with Phase 4 enhancements)
