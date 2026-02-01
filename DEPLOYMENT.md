# Deploying leumas to GitHub Pages

## Option 1: Static HTML Export (Recommended for GitHub Pages)

GitHub Pages only serves static files. To deploy the Django `leumasp` project, you have two choices:

### Option A: Export as Static HTML
```bash
# Collect static files
python manage.py collectstatic --noinput

# Generate static HTML from views (use a tool like Frozen-Flask or wget)
# Then push the static folder to GitHub Pages
```

### Option B: Deploy to a Python Hosting Service (Recommended)

Since `leumasp` has a contact form and database, deploy to a service that supports Python:

#### **Heroku (Free tier deprecated, but still available)**
```bash
# Install Heroku CLI: https://devcenter.heroku.com/articles/heroku-cli
heroku login
heroku create your-app-name
git push heroku main
```

#### **PythonAnywhere (Free tier available)**
- Sign up at https://www.pythonanywhere.com/
- Upload your code
- Configure web app to point to `leumasp/wsgi.py`
- Set custom domain to `username.pythonanywhere.com` or your own

#### **Railway.app (Free credits)**
```bash
# Install Railway CLI
npm install -g @railway/cli
railway login
railway init
railway up
```

#### **Render (Free tier)**
- https://render.com/
- Connect GitHub repo
- Create Web Service from `leumasp/wsgi.py`

#### **Vercel (Supports Python)**
- https://vercel.com/
- Create project from GitHub
- Add `vercel.json` config

## Option 2: GitHub Pages + Separate Frontend

Create a static HTML version hosted on GitHub Pages that links to your Django backend:

1. Create separate repo: `username.github.io`
2. Push `leumasp` backend to a hosting service
3. Configure static HTML to call backend API

## Recommended Setup for leumas

**Best Option**: PythonAnywhere or Railway
- **PythonAnywhere**: Easy setup, free tier with custom domain
- **Railway**: Modern, simple deployment from GitHub

### Steps for PythonAnywhere:
1. Go to https://www.pythonanywhere.com/
2. Create account
3. Upload code or connect GitHub
4. Create web app pointing to `/path/to/leumasp/leumasp/wsgi.py`
5. Configure environment variables (SECRET_KEY, DEBUG=False, ALLOWED_HOSTS)
6. Set custom domain

### Steps for Railway:
1. Push to GitHub: `git push origin main`
2. Go to https://railway.app/
3. Click "New Project" → "Deploy from GitHub"
4. Select your repo
5. Set build/start commands
6. Railway auto-deploys on push

## Pre-Deployment Checklist

- [ ] Set `DEBUG = False` in settings
- [ ] Set `ALLOWED_HOSTS` to your domain
- [ ] Generate a secure `SECRET_KEY`
- [ ] Configure database (PostgreSQL recommended)
- [ ] Test with `python manage.py check --deploy`

## Production Settings Update

Update `leumasp/settings.py` for production:

```python
import os

DEBUG = False
ALLOWED_HOSTS = ['yourdomain.com', 'www.yourdomain.com']
SECRET_KEY = os.environ.get('SECRET_KEY', 'fallback-key')

# Database
if os.environ.get('DATABASE_URL'):
    import dj_database_url
    DATABASES = {'default': dj_database_url.config()}

# Security
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
```

## Push to GitHub

```bash
cd /Users/leumas/Portfolio/leumas/leumasp
git init
git add .
git commit -m "Initial commit: leumas portfolio app"
git remote add origin https://github.com/yourusername/leumas.git
git branch -M main
git push -u origin main
```

Then connect to your chosen hosting service.
