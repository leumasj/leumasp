from django.shortcuts import render
from leumas.views.data import PORTFOLIO_PROJECTS


def portfolio_detail(request, project_id):
    """Display details for a specific portfolio project"""
    project = PORTFOLIO_PROJECTS.get(project_id)
    if not project:
        projects = list(PORTFOLIO_PROJECTS.values())
        project = projects[0] if projects else None
    
    context = {
        'project': project,
        'project_id': project_id,
        'all_projects': PORTFOLIO_PROJECTS,
    }
    return render(request, 'leumas/portfolio-details.html', context)


def works(request):
    """Display portfolio/works page"""
    context = {
        'all_services': {},  # Will be provided by index view if needed
        'all_projects': PORTFOLIO_PROJECTS,
        'scroll_to': 'project-gallery'
    }
    return render(request, 'leumas/portfolios.html', context)
