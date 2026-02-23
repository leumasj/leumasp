from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import SimpleRouter

from leumas import api
from leumas.views import (
    index, about, blog, blogs, blog_detail,
    portfolio_detail, works, services, service_detail,
    ContactView, ContactSuccessView, subscribe_newsletter,
    download_cv
)

# Register API viewsets
router = SimpleRouter()
router.register(r'api/blogs', api.BlogPostViewSet, basename='api-blogs')
router.register(r'api/portfolio', api.PortfolioViewSet, basename='api-portfolio')
router.register(r'api/services', api.ServiceViewSet, basename='api-services')
router.register(r'api/skills', api.SkillViewSet, basename='api-skills')
router.register(r'api/newsletter', api.NewsletterViewSet, basename='api-newsletter')

# Namespace for reversing URLs from this app
app_name = 'leumas'

urlpatterns = [
    # Traditional views
    path('', index, name='leumas-index'),
    path('about', about, name='leumas-about'),
    path('contact', ContactView.as_view(), name='leumas-contact'),
    path('services', services, name='leumas-services'),
    path('works', works, name='leumas-works'),
    path('blog', blog, name='leumas-blog'),
    path('blogs', blogs, name='leumas-blogs'),
    path('success/', ContactSuccessView.as_view(), name="success"),
    path('portfolio/<int:project_id>/', portfolio_detail, name='portfolio-detail'),
    path('service/<int:service_id>/', service_detail, name='service-detail'),
    path('blog/<int:blog_id>/', blog_detail, name='blog-detail'),
    path('subscribe-newsletter/', subscribe_newsletter, name='subscribe-newsletter'),
    path('download-cv/', download_cv, name='download-cv'),
    path('pj', index, name='leumas-pj'),

    # REST API endpoints
    *router.urls,

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)