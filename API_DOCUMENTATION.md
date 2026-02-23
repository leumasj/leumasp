# API Documentation

This document describes the REST API endpoints available in the LeUmas portfolio application.

## Base URL
```
http://localhost:8000/api/
```

## Authentication
Current implementation uses Session Authentication. All endpoints are publicly accessible without authentication.

## Content Types
- Request: `application/json`
- Response: `application/json`

---

## Endpoints

### Blog Posts

#### List Blog Posts
**GET** `/api/blogs/`

Query Parameters:
- `search` - Search in title, content, excerpt
- `category` - Filter by category
- `tags` - Filter by tag IDs
- `author` - Filter by author
- `ordering` - Sort by field (`published_date`, `-published_date`, `views_count`, `-views_count`)
- `page` - Pagination (default 10 per page)

Response:
```json
{
  "count": 5,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "title": "Introduction to Django",
      "slug": "intro-django",
      "author": "Samuel",
      "category": "Web Development",
      "excerpt": "Learn Django basics",
      "featured_image": "/media/blog/...",
      "published_date": "2024-02-23T20:00:00Z",
      "updated_date": "2024-02-23T20:00:00Z",
      "views_count": 0,
      "tags": [{"id": 1, "name": "Django", "slug": "django"}],
      "reading_time": 5,
      "meta_description": "Learn Django basics"
    }
  ]
}
```

#### Get Blog Detail
**GET** `/api/blogs/{id}/`

Response includes full `content` and `related_posts`:
```json
{
  "id": 1,
  "title": "Introduction to Django",
  "content": "Full blog post content...",
  "reading_time": 5,
  "related_posts": [...]
}
```

#### Increment Blog View Count
**POST** `/api/blogs/{id}/increment_views/`

Response:
```json
{
  "views_count": 1
}
```

#### Get Related Posts
**GET** `/api/blogs/{id}/related_posts/`

Returns posts with shared tags.

---

### Portfolio

#### List Portfolio Projects
**GET** `/api/portfolio/`

Query Parameters:
- `search` - Search in title, description, challenge, solution
- `category` - Filter by category
- `tags` - Filter by tags
- `is_featured` - Filter featured projects (true/false)
- `ordering` - Sort by field (`created_date`, `-created_date`, `is_featured`)

#### Get Portfolio Detail
**GET** `/api/portfolio/{id}/`

Includes full `challenge`, `solution`, and `results`.

#### Get Featured Portfolio Projects
**GET** `/api/portfolio/featured/`

Returns only projects with `is_featured=true`.

---

### Services

#### List Services
**GET** `/api/services/`

Query Parameters:
- `ordering` - Sort by `order` (default ascending)

Response:
```json
[
  {
    "id": 1,
    "title": "Web Development",
    "slug": "web-dev",
    "description": "Full-stack web development",
    "icon": "fas fa-code",
    "order": 1
  }
]
```

---

### Skills

#### List Skills
**GET** `/api/skills/`

Query Parameters:
- `category` - Filter by skill category
- `ordering` - Sort by field (`category`, `-proficiency`)

Response:
```json
[
  {
    "id": 1,
    "name": "Python",
    "category": "Programming Languages",
    "proficiency": 95
  }
]
```

---

### Newsletter

#### Subscribe to Newsletter
**POST** `/api/newsletter/`

Request:
```json
{
  "email": "subscriber@example.com"
}
```

Response (201 Created):
```json
{
  "detail": "Successfully subscribed to the newsletter."
}
```

Errors:
- `400 Bad Request` - Invalid email or duplicate subscription
- `400 Bad Request` - Missing required `email` field

---

## Pagination

All list endpoints use page number pagination with 10 items per page.

Example:
```
GET /api/blogs/?page=2
```

Response:
```json
{
  "count": 50,
  "next": "http://localhost:8000/api/blogs/?page=3",
  "previous": "http://localhost:8000/api/blogs/?page=1",
  "results": [...]
}
```

---

## Error Handling

### Common Error Responses

**404 Not Found**
```json
{
  "detail": "Not found."
}
```

**400 Bad Request**
```json
{
  "field_name": ["This field is required."]
}
```

**400 Bad Request (Newsletter duplicate)**
```json
{
  "email": ["This email is already subscribed."]
}
```

---

## Testing

Run the test suite with:
```bash
python manage.py test leumas
```

View test coverage:
```bash
coverage run --source='.' manage.py test leumas
coverage report
coverage html  # Generate HTML coverage report
```

---

## Example Requests

### Using cURL

**Get all blog posts:**
```bash
curl http://localhost:8000/api/blogs/
```

**Search blog posts:**
```bash
curl "http://localhost:8000/api/blogs/?search=django"
```

**Get specific blog:**
```bash
curl http://localhost:8000/api/blogs/1/
```

**Increment blog views:**
```bash
curl -X POST http://localhost:8000/api/blogs/1/increment_views/
```

**Subscribe to newsletter:**
```bash
curl -X POST http://localhost:8000/api/newsletter/ \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com"}'
```

### Using Python Requests

```python
import requests

# Get all blogs
response = requests.get('http://localhost:8000/api/blogs/')
blogs = response.json()

# Get specific blog
blog = requests.get('http://localhost:8000/api/blogs/1/').json()

# Increment views
result = requests.post('http://localhost:8000/api/blogs/1/increment_views/').json()

# Subscribe to newsletter
data = {'email': 'test@example.com'}
response = requests.post('http://localhost:8000/api/newsletter/', json=data)
```

---

## Rate Limiting

Rate limiting is configured but not yet enabled. When enabled, it will limit API requests to prevent abuse.

---

## CORS Support

CORS is enabled for cross-origin requests. Configure allowed origins in:
```
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "https://yourdomain.com",
]
```
