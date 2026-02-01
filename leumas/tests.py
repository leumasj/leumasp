from django.test import TestCase, override_settings
from django.core import mail
from .forms import ContactForm


class ContactFormTests(TestCase):

	def test_get_info_formats_subject_and_message(self):
		data = {
			'name': 'Alice',
			'email': 'alice@example.com',
			'inquiry': 'Hello',
			'message': 'This is a test message.'
		}
		form = ContactForm(data)
		self.assertTrue(form.is_valid())
		subject, msg = form.get_info()
		self.assertEqual(subject, 'Hello')
		self.assertIn('Alice with email alice@example.com said:', msg)

	@override_settings(EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend', RECIPIENT_ADDRESS='receiver@example.com', EMAIL_HOST_USER='sender@example.com')
	def test_send_uses_recipient_address(self):
		data = {
			'name': 'Bob',
			'email': 'bob@example.com',
			'inquiry': 'Question',
			'message': 'Please contact me.'
		}
		form = ContactForm(data)
		self.assertTrue(form.is_valid())
		# Clear outbox then send
		mail.outbox = []
		form.send()
		# One email should have been sent to RECIPIENT_ADDRESS
		self.assertEqual(len(mail.outbox), 1)
		sent = mail.outbox[0]
		self.assertEqual(sent.to, ['receiver@example.com'])
		self.assertEqual(sent.from_email, 'sender@example.com')
