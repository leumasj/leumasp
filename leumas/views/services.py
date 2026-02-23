from django.shortcuts import render
from leumas.views.data import SERVICES


def services(request):
    """Display services page"""
    context = {
        'all_services': SERVICES,
        'all_projects': {},  # Will be provided by index view if needed
        'scroll_to': 'service'
    }
    return render(request, 'leumas/services.html', context)


def service_detail(request, service_id):
    """Display details for a specific service"""
    service = SERVICES.get(service_id)
    if not service:
        services_list = list(SERVICES.values())
        service = services_list[0] if services_list else None
    
    context = {
        'service': service,
        'service_id': service_id,
        'all_services': SERVICES,
    }
    return render(request, 'leumas/service-details.html', context)
