from django.shortcuts import render
from leumas.blog_helpers import get_blog_posts_with_dynamic_dates
from leumas.views.data import SERVICES, PORTFOLIO_PROJECTS


def index(request):
    """Display home page with featured content"""
    blog_posts = get_blog_posts_with_dynamic_dates()
    context = {
        'all_services': SERVICES,
        'all_projects': PORTFOLIO_PROJECTS,
        'preview_blogs': {1: blog_posts.get(1), 2: blog_posts.get(2), 3: blog_posts.get(3), 4: blog_posts.get(4)},
    }
    return render(request, 'leumas/index.html', context)


def about(request):
    """Display about page"""
    context = {
        'all_services': SERVICES,
        'all_projects': PORTFOLIO_PROJECTS,
        'scroll_to': 'about'
    }
    return render(request, 'leumas/index.html', context)
