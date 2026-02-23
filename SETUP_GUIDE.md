# LeUmas Portfolio - Setup & Development Guide

## 📋 Table of Contents

1. [Project Overview](#project-overview)
2. [environment Setup](#environment-setup)
3. [Database Configuration](#database-configuration)
4. [Running Locally](#running-locally)
5. [REST API](#rest-api)
6. [Admin Interface](#admin-interface)
7. [Testing](#testing)
8. [Deployment](#deployment)
9. [Troubleshooting](#troubleshooting)

---

## Project Overview

This is a modern Django portfolio website with:
- **Blog System**: Full-featured blog with reading time calculation, related posts, and view tracking
- **Portfolio Showcase**: Project management with challenge/solution/results framework
- **REST API**: Fully functional REST API built with Django REST Framework
- **Admin Interface**: Comprehensive Django admin for managing all content
- **Email Subscriptions**: Newsletter subscription system
- **Error Tracking**: Sentry integration for production monitoring
- **Caching**: In-memory caching for performance optimization

### Tech Stack
- **Django 4.2.8**: Web framework
- **Django REST Framework 3.14.0**: REST API
- **Pillow 10.1.0**: Image processing
- **PostgreSQL** (recommended for production)
- **Redis** (recommended for production caching)

---

## Environment Setup

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/leumasp.git
cd leumasp-main
```

### 2. Create Virtual Environment

```bash
# Create virtual environment
python3 -m venv .venv

# Activate virtual environment
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

```bash
# Copy example environment file
cp .env.example .env

# Edit .env with your settings
nano .env  # or use your preferred editor
```

#### Essential .env Settings:
```env
DEBUG=True  # Set to False in production
SECRET_KEY=your-secret-key-here  # Generate with: python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
ALLOWED_HOSTS=localhost,127.0.0.1
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
RECIPIENT_ADDRESS=your-email@gmail.com
CORS_ALLOWED_ORIGINS=http://localhost:3000
```

---

## Database Configuration

### SQLite (Development - Default)

SQLite is configured by default and works out of the box:

```bash
# Create tables
python manage.py migrate

# Create superuser
python manage.py createsuperuser
```

### PostgreSQL (Recommended for Production)

1. **Install PostgreSQL**

```bash
# macOS
brew install postgresql@15

# Ubuntu
sudo apt-get install postgresql postgresql-contrib

# Windows - Download from https://www.postgresql.org/download/windows/
```

2. **Create Database**

```bash
createdb leumasp_db
```

3. **Update .env**

```env
DATABASE_URL=postgresql://username:password@localhost:5432/leumasp_db
```

4. **Install psycopg2**

```bash
pip install psycopg2-binary
```

5. **Migrate Database**

```bash
python manage.py migrate
```

---

## Running Locally

### Start Development Server

```bash
python manage.py runserver
```

Visit `http://localhost:8000` in your browser.

### Run Migrations

```bash
# Check for pending migrations
python manage.py showmigrations

# Apply migrations
python manage.py migrate

# Create new migrations after model changes
python manage.py makemigrations
```

### Create Superuser (Admin Access)

```bash
python manage.py createsuperuser
```

Then visit `http://localhost:8000/admin` to log in.

---

## REST API

### Available Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/blogs/` | GET | List all blog posts |
| `/api/blogs/{id}/` | GET | Get blog detail |
| `/api/blogs/{id}/increment_views/` | POST | Increment view count |
| `/api/portfolio/` | GET | List portfolio projects |
| `/api/portfolio/{id}/` | GET | Get project detail |
| `/api/portfolio/featured/` | GET | Get featured projects |
| `/api/services/` | GET | List services |
| `/api/skills/` | GET | List skills by category |
| `/api/newsletter/` | POST | Subscribe to newsletter |

### Example API Requests

**List blog posts:**
```bash
curl http://localhost:8000/api/blogs/
```

**Search blogs:**
```bash
curl "http://localhost:8000/api/blogs/?search=django&category=web"
```

**Get blog detail:**
```bash
curl http://localhost:8000/api/blogs/1/
```

**Get related posts:**
```bash
curl http://localhost:8000/api/blogs/1/related_posts/
```

**Subscribe to newsletter:**
```bash
curl -X POST http://localhost:8000/api/newsletter/ \
  -H "Content-Type: application/json" \
  -d '{"email":"user@example.com"}'
```

### Using Python Requests Library

```python
import requests

# Get all blogs
response = requests.get('http://localhost:8000/api/blogs/')
print(response.json())

# Search blogs
response = requests.get('http://localhost:8000/api/blogs/', params={
    'search': 'django',
    'page': 1
})
print(response.json())

# Subscribe to newsletter
data = {'email': 'user@example.com'}
response = requests.post('http://localhost:8000/api/newsletter/', json=data)
print(response.json())
```

For more details, see [API_DOCUMENTATION.md](API_DOCUMENTATION.md).

---

## Admin Interface

### Accessing Admin

Visit `http://localhost:8000/admin` and log in with your superuser credentials.

### Available Admin Sections

1. **Blog Posts**
   - List all blog posts
   - Filter by category, tags, published status
   - Search by title or content
   - Auto-generate slug
   - View count tracking

2. **Portfolio Projects**
   - Manage portfolio projects
   - Mark as featured
   - Add challenge/solution/results
   - Assign tags

3. **Services**
   - Manage service offerings
   - Reorder services by drag-and-drop

4. **Skills**
   - Add technical skills
   - Organize by category
   - Set proficiency level (0-100)

5. **Tags**
   - Create and manage tags
   - Auto-slug generation

6. **Newsletter**
   - View email subscriptions
   - Activate/deactivate subscriptions

7. **Contact Messages**
   - View contact form submissions
   - Track read status

---

## Testing

### Run All Tests

```bash
python manage.py test leumas
```

### Run Specific Test Class

```bash
python manage.py test leumas.tests.BlogPostModelTest
```

### Run Specific Test Method

```bash
python manage.py test leumas.tests.BlogPostModelTest.test_blog_creation
```

### Run with Verbose Output

```bash
python manage.py test leumas --verbosity=2
```

### Generate Coverage Report

```bash
# Run tests with coverage
coverage run --source='.' manage.py test leumas

# View coverage report
coverage report

# Generate HTML coverage report
coverage html
# Open htmlcov/index.html in browser
```

### Test Categories

**Model Tests**
- BlogPost creation, slugs, reading time, related posts
- Portfolio project management
- Service and Skill models
- Tag functionality
- Newsletter subscriptions
- Contact messages

**API Tests**
- Blog list/detail endpoints
- Search and filtering
- View counting
- Portfolio endpoints
- Service/Skill endpoints
- Newsletter subscription
- Error handling

---

## Production Deployment

### 1. Environment Preparation

```bash
# Generate secure secret key
python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
```

Update `.env` for production:
```env
DEBUG=False
SECRET_KEY=your-generated-key
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
SECURE_SSL_REDIRECT=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
SENTRY_DSN=your-sentry-dsn-if-configured
```

### 2. Run Migrations

```bash
python manage.py migrate
```

### 3. Collect Static Files

```bash
python manage.py collectstatic --no-input
```

### 4. Create Superuser (if not exists)

```bash
python manage.py createsuperuser
```

### 5. Use Production Server (not Django development)

Use [Gunicorn](https://gunicorn.org/):

```bash
pip install gunicorn
gunicorn leumasp.wsgi:application --bind 0.0.0.0:8000
```

Or [uWSGI](https://uwsgi-docs.readthedocs.io/):

```bash
pip install uwsgi
uwsgi --http :8000 --wsgi-file leumasp/wsgi.py --master --processes 4 --threads 2
```

### 6. Use Nginx as Reverse Proxy

See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed Nginx configuration.

### 7. Exit Strategies Test

Before deploying, test everything locally:

```bash
# Test with production settings
DEBUG=False python manage.py check --deploy

# Test static files
python manage.py collectstatic --dry-run
```

---

## Troubleshooting

### Common Issues

#### 1. "ModuleNotFoundError: No module named..."

**Solution:**
```bash
# Make sure virtual environment is activated
source .venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt
```

#### 2. "No directory at: .../staticfiles"

**Solution:**
```bash
# Collect static files
python manage.py collectstatic
```

#### 3. "Error connecting to database"

**Solution:**
```bash
# Check database URL in .env
# Verify database server is running
# For SQLite: remove db.sqlite3 and run migrations again
python manage.py migrate
```

#### 4. "Port 8000 already in use"

**Solution:**
```bash
# Use different port
python manage.py runserver 8001

# Or find and kill process using port 8000
lsof -i :8000
kill -9 <PID>
```

#### 5. Migrations not detected

**Solution:**
```bash
# Check migration files
python manage.py showmigrations

# Create migrations
python manage.py makemigrations leumas

# Apply migrations
python manage.py migrate
```

#### 6. Admin panel not loading styles

**Solution:**
```bash
# Run static file collection
python manage.py collectstatic --clear --no-input

# Clear browser cache (Ctrl+Shift+Delete)
```

#### 7. Logging to file fails

**Solution:**
```bash
# Create logs directory
mkdir -p logs

# Ensure directory is writable
chmod 755 logs
```

### Debug Mode

Enable detailed error pages (development only):

```env
DEBUG=True
```

Check Django system checks:
```bash
python manage.py check
```

### Log Files

View application logs:
```bash
tail -f logs/django.log
```

---

## File Structure

```
leumasp-main/
├── leumas/                    # Main app
│   ├── migrations/           # Database migrations
│   ├── static/              # Static files (CSS, JS, images)
│   ├── templates/           # HTML templates
│   ├── admin.py             # Admin configuration
│   ├── models.py            # Database models
│   ├── serializers.py       # REST API serializers
│   ├── api.py               # REST API viewsets
│   ├── urls.py              # URL routing
│   ├── views.py             # View functions
│   ├── forms.py             # Form classes
│   └── tests.py             # Unit tests
├── leumasp/                  # Project settings
│   ├── settings.py          # Django settings
│   ├── urls.py              # Global URL routing
│   ├── wsgi.py              # WSGI application
│   └── asgi.py              # ASGI application
├── logs/                     # Application logs
├── media/                    # Uploaded files
├── staticfiles/              # Collected static files
├── manage.py                # Django management script
├── requirements.txt          # Python dependencies
├── .env.example             # Environment variables template
├── API_DOCUMENTATION.md      # API reference
└── README.md                 # Project README
```

---

## Next Steps

1. **Add Sample Content**: Use admin panel to add blog posts, portfolio projects, and skills
2. **Configure Email**: Set up SMTP for contact form and newsletters
3. **Deploy to Production**: Follow deployment guide to go live
4. **Monitor Errors**: Set up Sentry for production error tracking
5. **Optimize Performance**: Set up Redis caching for production
6. **Add DNS**: Configure custom domain pointing to your server

---

## Support & Resources

- [Django Documentation](https://docs.djangoproject.com/)
- [Django REST Framework](https://www.django-rest-framework.org/)
- [Sentry Docs](https://docs.sentry.io/)
- [Gunicorn Deployment](https://gunicorn.org/)
- [PostgreSQL Docs](https://www.postgresql.org/docs/)

---

## License

[Add your license information here]

---

## Author

Samuel Adomeh
[Your contact information]
