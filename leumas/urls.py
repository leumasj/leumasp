from django.contrib import admin
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView

from .views import ContactView, ContactSuccessView


# Namespace for reversing URLs from this app
app_name = 'leumas'

urlpatterns = [
    path('', views.index, name='leumas-index'),
    path('about', views.about, name='leumas-about'),
    path('contact', ContactView.as_view(), name='leumas-contact'),
    path('services', views.services, name='leumas-services'),
    path('works', views.works, name='leumas-works'),
    path('blog', views.blog, name='leumas-blog'),
    path('blogs', views.blogs, name='leumas-blogs'),
    path('success/', ContactSuccessView.as_view(), name="success"),
    path('portfolio/<int:project_id>/', views.portfolio_detail, name='portfolio-detail'),
    path('service/<int:service_id>/', views.service_detail, name='service-detail'),
    path('blog/<int:blog_id>/', views.blog_detail, name='blog-detail'),
    path('subscribe-newsletter/', views.subscribe_newsletter, name='subscribe-newsletter'),
    path('pj', views.index, name='leumas-pj'),


] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)