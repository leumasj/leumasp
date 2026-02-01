from django.shortcuts import render
from django.views.generic import FormView, TemplateView
from django.urls import reverse_lazy
from .forms import ContactForm


class ContactView(FormView):
    template_name = 'leumas/index.html'
    form_class = ContactForm
    # Use the app namespace defined in `leumas/urls.py`
    success_url = reverse_lazy('leumas:success')

    def form_valid(self, form):
        # Calls the custom send method defined on the form
        form.send()
        return super().form_valid(form)


class ContactSuccessView(TemplateView):
    template_name = 'leumas/index.html'


def index(request):
    return render(request, 'leumas/index.html')


def about(request):
    return render(request, 'leumas/index.html')


def contact(request):
    return render(request, 'leumas/index.html')


def works(request):
    return render(request, 'leumas/portfolios.html')


def services(request):
    return render(request, 'leumas/service-details.html')


def blog(request):
    return render(request, 'leumas/blogs.html')


def blogs(request):
    return render(request, 'leumas/blogs.html')


def pj(request):
    return render(request, 'leumas/portfolio-details.html')