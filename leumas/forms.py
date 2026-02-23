from django import forms
from django.conf import settings
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string
from .models import Newsletter


class ContactForm(forms.Form):

    name = forms.CharField(max_length=120)
    email = forms.EmailField()
    inquiry = forms.CharField(max_length=70)
    message = forms.CharField(widget=forms.Textarea)

    def get_info(self):
        """
        Method that returns formatted information
        :return: subject, msg
        """
        # Cleaned data
        cl_data = super().clean()

        name = cl_data.get('name').strip()
        from_email = cl_data.get('email')
        subject = cl_data.get('inquiry')

        msg = f'{name} with email {from_email} said:'
        msg += f'\n"{subject}"\n\n'
        msg += cl_data.get('message')

        return subject, msg

    def send(self):

        subject, msg = self.get_info()
        # Owner notification (plain text)
        owner_subject = f"Contact form: {subject}"
        context = {
            'name': self.cleaned_data.get('name').strip(),
            'email': self.cleaned_data.get('email'),
            'subject': subject,
            'message': self.cleaned_data.get('message')
        }

        text_body = render_to_string('leumas/emails/contact_received.txt', context)
        html_body = render_to_string('leumas/emails/contact_received.html', context)

        owner_email = EmailMultiAlternatives(
            subject=owner_subject,
            body=text_body,
            from_email=settings.EMAIL_HOST_USER,
            to=[settings.RECIPIENT_ADDRESS]
        )
        owner_email.attach_alternative(html_body, "text/html")
        owner_email.send(fail_silently=True)

        # Confirmation email to the sender
        confirm_subject = "Thanks for contacting Samuel Adomeh"
        confirm_text = render_to_string('leumas/emails/contact_confirm.txt', context)
        confirm_html = render_to_string('leumas/emails/contact_confirm.html', context)

        confirm_email = EmailMultiAlternatives(
            subject=confirm_subject,
            body=confirm_text,
            from_email=settings.EMAIL_HOST_USER,
            to=[self.cleaned_data.get('email')]
        )
        confirm_email.attach_alternative(confirm_html, "text/html")
        confirm_email.send(fail_silently=True)


class NewsletterForm(forms.ModelForm):
    class Meta:
        model = Newsletter
        fields = ['email']
        widgets = {
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your email...',
                'required': True,
            })
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if Newsletter.objects.filter(email=email, is_active=True).exists():
            raise forms.ValidationError('This email is already subscribed to our newsletter.')
        return email
