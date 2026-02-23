from django.views.generic import FormView, TemplateView
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.utils.decorators import method_decorator
try:
    from ratelimit.decorators import ratelimit
except Exception:
    def ratelimit(*args, **kwargs):
        def _decorator(func):
            return func
        return _decorator
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives

from leumas.forms import ContactForm, NewsletterForm
from leumas.models import Newsletter


@method_decorator(ratelimit(key='ip', rate='5/m', block=True), name='dispatch')
class ContactView(FormView):
    """Handle contact form submission with rate limiting"""
    template_name = 'leumas/index.html'
    form_class = ContactForm
    success_url = reverse_lazy('leumas:success')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['scroll_to'] = 'contact'
        return context

    def form_valid(self, form):
        form.send()
        return super().form_valid(form)


class ContactSuccessView(TemplateView):
    """Display success message after contact form submission"""
    template_name = 'leumas/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['scroll_to'] = 'contact'
        return context


@require_POST
@ratelimit(key='ip', rate='10/m', block=True)
def subscribe_newsletter(request):
    """Handle newsletter subscription with rate limiting and confirmation email"""
    form = NewsletterForm(request.POST)

    if form.is_valid():
        newsletter = form.save()

        # Send confirmation email to subscriber
        context = {'email': newsletter.email}
        text_body = render_to_string('leumas/emails/newsletter_confirm.txt', context)
        html_body = render_to_string('leumas/emails/newsletter_confirm.html', context)

        msg = EmailMultiAlternatives(
            subject='Newsletter subscription confirmed',
            body=text_body,
            from_email=None,
            to=[newsletter.email]
        )
        msg.attach_alternative(html_body, 'text/html')
        try:
            msg.send(fail_silently=True)
        except Exception:
            pass

        return JsonResponse({
            'success': True,
            'message': 'Thank you for subscribing! Check your email for updates.'
        })
    else:
        return JsonResponse({
            'success': False,
            'message': 'Email already subscribed or invalid.',
            'errors': form.errors
        }, status=400)
