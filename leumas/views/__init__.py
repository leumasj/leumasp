"""Views package for the Leumas portfolio application.

This package organizes views into logical modules:
- home.py: Homepage and about page views
- blog.py: Blog listing and detail views
- portfolio.py: Portfolio/works and project detail views
- services.py: Services listing and detail views
- contact.py: Contact form and newsletter subscription
- cv.py: CV download as PDF
- data.py: Shared data constants (PORTFOLIO_PROJECTS, SERVICES)
"""

from leumas.views.home import index, about
from leumas.views.blog import blog, blogs, blog_detail
from leumas.views.portfolio import portfolio_detail, works
from leumas.views.services import services, service_detail
from leumas.views.contact import ContactView, ContactSuccessView, subscribe_newsletter
from leumas.views.cv import download_cv

__all__ = [
    # Home views
    'index', 'about',
    # Blog views
    'blog', 'blogs', 'blog_detail',
    # Portfolio views
    'portfolio_detail', 'works',
    # Service views
    'services', 'service_detail',
    # Contact views
    'ContactView', 'ContactSuccessView', 'subscribe_newsletter',
    # CV view
    'download_cv',
]
