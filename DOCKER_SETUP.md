# Docker Setup Guide

This project includes Docker configuration for both local development and production deployment.

## Prerequisites

- Docker 20.10+
- Docker Compose 1.29+

## Quick Start with Docker

### 1. Clone the Repository

```bash
git clone https://github.com/leumasp/leumasp-main.git
cd leumasp-main
```

### 2. Create `.env` File

Copy the example environment file and update with your values:

```bash
cp .env.example .env
```

Edit `.env` with your configuration:

```env
# Django settings
DEBUG=False
ALLOWED_HOSTS=localhost,127.0.0.1,yourdomain.com
SECRET_KEY=your-secret-key-here-change-in-production

# Database
DB_NAME=leumasp_db
DB_USER=postgres
DB_PASSWORD=secure-password-here

# Email
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
RECIPIENT_ADDRESS=contact@yoursite.com

# Sentry (optional)
SENTRY_DSN=https://your-sentry-dsn@sentry.io/xxxx
```

### 3. Start Services

```bash
# Start all services in the background
docker-compose up -d

# Or start with logs in foreground
docker-compose up

# For development with hot reload
RELOAD=true docker-compose up
```

This will:
- Create a PostgreSQL database container
- Build and start the Django web application
- Start Redis for caching (optional)
- Apply migrations automatically
- Collect static files

### 4. Access the Application

- **Web Application:** http://localhost:8000
- **Database:** localhost:5432
- **Redis:** localhost:6379

### 5. Initial Setup (First Run)

```bash
# Create a superuser for admin panel
docker-compose exec web python manage.py createsuperuser

# Access admin at http://localhost:8000/admin
```

## Common Docker Commands

### View Logs

```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f web
docker-compose logs -f db

# Last 100 lines
docker-compose logs --tail=100
```

### Execute Commands

```bash
# Run Django management commands
docker-compose exec web python manage.py shell
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser

# Run Python interactive shell
docker-compose exec web python

# Run shell in container
docker-compose exec web bash
```

### Database Management

```bash
# Create database backup
docker-compose exec db pg_dump -U postgres leumasp_db > backup.sql

# Restore from backup
docker-compose exec -T db psql -U postgres leumasp_db < backup.sql

# Access database directly
docker-compose exec db psql -U postgres -d leumasp_db
```

### Stop and Clean Up

```bash
# Stop running containers
docker-compose stop

# Stop and remove containers
docker-compose down

# Remove everything including volumes (be careful!)
docker-compose down -v

# Remove and rebuild images
docker-compose down -v --rmi all
```

## Production Deployment

### Building the Production Image

```bash
# Build using the Dockerfile (multi-stage build)
docker build -t leumasp:latest .

# Tag for registry
docker tag leumasp:latest your-registry/leumasp:latest

# Push to registry
docker push your-registry/leumasp:latest
```

### Environment Variables for Production

```env
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
SECRET_KEY=long-random-string-from-secrets-manager
DATABASE_URL=postgresql://user:pass@db-host:5432/dbname
SENTRY_DSN=your-sentry-dsn
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=your-smtp-server
EMAIL_HOST_USER=your-email
EMAIL_HOST_PASSWORD=your-password
RECIPIENT_ADDRESS=contact@yourdomain.com
```

### Running with Production Settings

```bash
docker run \
  --name leumasp \
  -e DEBUG=False \
  -e ALLOWED_HOSTS=yourdomain.com \
  -e DATABASE_URL=postgresql://user:pass@db-host/dbname \
  -e SECRET_KEY=your-secret-key \
  -p 8000:8000 \
  leumasp:latest
```

## Docker Security Best Practices

1. **Use non-root user:** The Dockerfile runs the application as `appuser` (UID 1000)
2. **Minimize image size:** Multi-stage build excludes unnecessary files
3. **Use Alpine images:** Python 3.14-slim reduces attack surface
4. **Secrets management:** Use environment variables, never hardcode secrets
5. **Health checks:** Services include health checks for orchestration
6. **Volume mounts:** Production data persists in named volumes

## Kubernetes Deployment

For Kubernetes deployment, create a deployment manifest:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: leumasp
spec:
  replicas: 3
  selector:
    matchLabels:
      app: leumasp
  template:
    metadata:
      labels:
        app: leumasp
    spec:
      containers:
      - name: leumasp
        image: your-registry/leumasp:latest
        ports:
        - containerPort: 8000
        env:
        - name: DEBUG
          value: "False"
        - name: ALLOWED_HOSTS
          value: "yourdomain.com"
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: leumasp-secrets
              key: database-url
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "512Mi"
            cpu: "500m"
        livenessProbe:
          httpGet:
            path: /
            port: 8000
          initialDelaySeconds: 30
          periodSeconds: 10
```

## Troubleshooting

### Database Connection Issues

```bash
# Check database service is healthy
docker-compose ps

# Verify database connectivity
docker-compose exec web python manage.py dbshell
```

### Static Files Not Loading

```bash
# Rebuild and collect static files
docker-compose down -v
docker-compose up -d --build
docker-compose exec web python manage.py collectstatic --noinput
```

### Port Already in Use

```bash
# Kill process on port 8000
lsof -i :8000 | grep LISTEN | awk '{print $2}' | xargs kill -9

# Or change port in docker-compose.yml
# Change "8000:8000" to "8001:8000"
```

### Container Crashes

```bash
# Check logs
docker-compose logs web --tail=50

# Rebuild and restart
docker-compose down
docker-compose up -d --build
```

## Performance Tuning

### For Development

```yml
# In docker-compose.yml
web:
  command: >
    sh -c "python manage.py runserver 0.0.0.0:8000"
```

### For Production

- Increase gunicorn workers: `--workers 8` (based on CPU cores)
- Use production database: PostgreSQL with replication
- Enable caching: Configure Redis properly
- Use CDN for static files
- Enable database connection pooling: pgBouncer

## Additional Resources

- [Docker Documentation](https://docs.docker.com/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [Django Deployment Checklist](https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/)
- [Gunicorn Documentation](https://gunicorn.org/)
