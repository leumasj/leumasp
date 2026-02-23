from django.test import TestCase, override_settings
from django.core import mail
from .forms import ContactForm
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from .models import BlogPost, Portfolio, Service, Skill, Tag, Newsletter, Contact


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
		# Two emails should have been sent: owner notification + sender confirmation
		self.assertEqual(len(mail.outbox), 2)
		# First email sent to owner (RECIPIENT_ADDRESS)
		owner_email = mail.outbox[0]
		self.assertEqual(owner_email.to, ['receiver@example.com'])
		self.assertEqual(owner_email.from_email, 'sender@example.com')
		# Second email sent to sender (confirmation)
		confirm_email = mail.outbox[1]
		self.assertEqual(confirm_email.to, ['bob@example.com'])
		self.assertEqual(confirm_email.from_email, 'sender@example.com')


class BlogPostModelTest(TestCase):
	"""Test cases for BlogPost model"""

	def setUp(self):
		"""Create test data"""
		self.tag1 = Tag.objects.create(name="Django", slug="django")
		self.tag2 = Tag.objects.create(name="Python", slug="python")
		
		self.blog1 = BlogPost.objects.create(
			title="Introduction to Django",
			slug="intro-django",
			category="Web Development",
			author="Samuel",
			excerpt="Learn Django basics",
			content="Django is a web framework. " * 100  # ~800 words for reading time calculation
		)
		self.blog1.tags.add(self.tag1)
		
		self.blog2 = BlogPost.objects.create(
			title="Python Tips and Tricks",
			slug="python-tips",
			category="Programming",
			author="Samuel",
			excerpt="Learn useful Python tips",
			content="Python is awesome. " * 100
		)
		self.blog2.tags.add(self.tag2, self.tag1)

	def test_blog_creation(self):
		"""Test creating a blog post"""
		self.assertEqual(self.blog1.title, "Introduction to Django")
		self.assertTrue(self.blog1.is_published)
		self.assertEqual(self.blog1.views_count, 0)

	def test_reading_time_calculation(self):
		"""Test reading time calculation"""
		reading_time = self.blog1.get_reading_time()
		self.assertGreater(reading_time, 0)
		# "Django is a web framework. " * 100 = 500 words
		# 500 / 200 = 2.5 → 2 minutes
		self.assertEqual(reading_time, 2)

	def test_increment_views(self):
		"""Test view count increment"""
		initial_views = self.blog1.views_count
		self.blog1.increment_views()
		self.blog1.refresh_from_db()
		self.assertEqual(self.blog1.views_count, initial_views + 1)

	def test_get_related_posts(self):
		"""Test getting related posts by tags"""
		related = self.blog1.get_related_posts()
		self.assertIn(self.blog2, related)

	def test_blog_slug_unique(self):
		"""Test that slugs are unique"""
		with self.assertRaises(Exception):
			BlogPost.objects.create(
				title="Duplicate",
				slug="intro-django",  # Same slug as blog1
				category="Test",
				excerpt="Test",
				content="Test content"
			)

	def test_blog_str_representation(self):
		"""Test string representation"""
		self.assertEqual(str(self.blog1), "Introduction to Django")


class PortfolioModelTest(TestCase):
	"""Test cases for Portfolio model"""

	def setUp(self):
		"""Create test portfolio project"""
		self.portfolio = Portfolio.objects.create(
			title="E-commerce Platform",
			slug="ecommerce-platform",
			category="Web Development",
			image="portfolio/ecommerce.jpg",
			description="Full-stack e-commerce solution",
			challenge="Scale for 10k daily users",
			solution="Used caching and optimization",
			results="Reduced load time by 60%"
		)

	def test_portfolio_creation(self):
		"""Test creating a portfolio project"""
		self.assertEqual(self.portfolio.title, "E-commerce Platform")
		self.assertFalse(self.portfolio.is_featured)

	def test_portfolio_str_representation(self):
		"""Test string representation"""
		self.assertEqual(str(self.portfolio), "E-commerce Platform")


class ServiceModelTest(TestCase):
	"""Test cases for Service model"""

	def setUp(self):
		"""Create test services"""
		self.service1 = Service.objects.create(
			title="Web Development",
			slug="web-dev",
			description="Full-stack web development",
			icon="fas fa-code",
			order=1
		)
		self.service2 = Service.objects.create(
			title="Consulting",
			slug="consulting",
			description="Tech consulting services",
			icon="fas fa-chart-line",
			order=2
		)

	def test_service_ordering(self):
		"""Test services are ordered correctly"""
		services = Service.objects.all()
		self.assertEqual(services[0].order, 1)
		self.assertEqual(services[1].order, 2)


class SkillModelTest(TestCase):
	"""Test cases for Skill model"""

	def setUp(self):
		"""Create test skills"""
		self.skill = Skill.objects.create(
			name="Python",
			category="Programming Languages",
			proficiency=95
		)

	def test_skill_creation(self):
		"""Test creating a skill"""
		self.assertEqual(self.skill.name, "Python")
		self.assertEqual(self.skill.proficiency, 95)

	def test_skill_proficiency_validation(self):
		"""Test proficiency validator"""
		from django.core.exceptions import ValidationError
		
		skill = Skill(
			name="Invalid",
			category="Test",
			proficiency=150  # > 100, should fail
		)
		with self.assertRaises(ValidationError):
			skill.full_clean()


class TagModelTest(TestCase):
	"""Test cases for Tag model"""

	def test_tag_slug_auto_generation(self):
		"""Test that slug is auto-generated from name"""
		tag = Tag.objects.create(name="Django Advanced")
		self.assertEqual(tag.slug, "django-advanced")

	def test_tag_unique_constraint(self):
		"""Test that tag names are unique"""
		Tag.objects.create(name="Python", slug="python")
		with self.assertRaises(Exception):
			Tag.objects.create(name="Python", slug="python-2")


class NewsletterModelTest(TestCase):
	"""Test cases for Newsletter model"""

	def test_newsletter_subscription(self):
		"""Test newsletter subscription creation"""
		newsletter = Newsletter.objects.create(email="test@example.com")
		self.assertTrue(newsletter.is_active)
		self.assertIsNotNone(newsletter.subscribed_at)

	def test_newsletter_email_unique(self):
		"""Test that email addresses are unique"""
		Newsletter.objects.create(email="unique@example.com")
		with self.assertRaises(Exception):
			Newsletter.objects.create(email="unique@example.com")


class BlogPostAPITest(APITestCase):
	"""Test cases for BlogPost REST API"""

	def setUp(self):
		"""Create test data"""
		self.client = APIClient()
		self.tag = Tag.objects.create(name="Django", slug="django")
		
		self.blog = BlogPost.objects.create(
			title="API Testing",
			slug="api-testing",
			category="Testing",
			excerpt="Learn API testing",
			content="API testing content. " * 50
		)
		self.blog.tags.add(self.tag)

	def test_blog_list_api(self):
		"""Test blog list endpoint"""
		response = self.client.get('/api/blogs/')
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertGreater(len(response.data['results']), 0)

	def test_blog_detail_api(self):
		"""Test blog detail endpoint"""
		response = self.client.get(f'/api/blogs/{self.blog.id}/')
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertEqual(response.data['title'], "API Testing")

	def test_blog_search_api(self):
		"""Test blog search functionality"""
		response = self.client.get('/api/blogs/?search=API')
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertGreater(len(response.data['results']), 0)

	def test_blog_filter_by_category(self):
		"""Test filtering blogs by category"""
		response = self.client.get('/api/blogs/?category=Testing')
		self.assertEqual(response.status_code, status.HTTP_200_OK)

	def test_increment_views_action(self):
		"""Test the increment_views custom action"""
		response = self.client.post(f'/api/blogs/{self.blog.id}/increment_views/')
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.blog.refresh_from_db()
		self.assertEqual(self.blog.views_count, 1)


class PortfolioAPITest(APITestCase):
	"""Test cases for Portfolio REST API"""

	def setUp(self):
		"""Create test data"""
		self.client = APIClient()
		self.portfolio = Portfolio.objects.create(
			title="Test Project",
			slug="test-project",
			category="Web",
			image="portfolio/test.jpg",
			description="Test project",
			is_featured=True
		)

	def test_portfolio_list_api(self):
		"""Test portfolio list endpoint"""
		response = self.client.get('/api/portfolio/')
		self.assertEqual(response.status_code, status.HTTP_200_OK)

	def test_portfolio_detail_api(self):
		"""Test portfolio detail endpoint"""
		response = self.client.get(f'/api/portfolio/{self.portfolio.id}/')
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertEqual(response.data['title'], "Test Project")

	def test_featured_portfolio_action(self):
		"""Test the featured custom action"""
		response = self.client.get('/api/portfolio/featured/')
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertGreater(len(response.data), 0)


class ServiceAPITest(APITestCase):
	"""Test cases for Service REST API"""

	def setUp(self):
		"""Create test data"""
		self.client = APIClient()
		self.service = Service.objects.create(
			title="Web Dev",
			slug="web-dev",
			description="Web development",
			icon="fas fa-code",
			order=1
		)

	def test_service_list_api(self):
		"""Test service list endpoint"""
		response = self.client.get('/api/services/')
		self.assertEqual(response.status_code, status.HTTP_200_OK)


class SkillAPITest(APITestCase):
	"""Test cases for Skill REST API"""

	def setUp(self):
		"""Create test data"""
		self.client = APIClient()
		self.skill = Skill.objects.create(
			name="Python",
			category="Languages",
			proficiency=90
		)

	def test_skill_list_api(self):
		"""Test skill list endpoint"""
		response = self.client.get('/api/skills/')
		self.assertEqual(response.status_code, status.HTTP_200_OK)

	def test_skill_filter_by_category(self):
		"""Test filtering skills by category"""
		response = self.client.get('/api/skills/?category=Languages')
		self.assertEqual(response.status_code, status.HTTP_200_OK)


class NewsletterAPITest(APITestCase):
	"""Test cases for Newsletter REST API"""

	def setUp(self):
		"""Setup test client"""
		self.client = APIClient()

	def test_newsletter_subscription_create(self):
		"""Test creating a newsletter subscription"""
		data = {'email': 'subscriber@example.com'}
		response = self.client.post('/api/newsletter/', data)
		self.assertEqual(response.status_code, status.HTTP_201_CREATED)
		self.assertTrue(Newsletter.objects.filter(email='subscriber@example.com').exists())

	def test_newsletter_duplicate_email(self):
		"""Test that duplicate emails are rejected"""
		email = 'subscriber@example.com'
		Newsletter.objects.create(email=email)
		
		data = {'email': email}
		response = self.client.post('/api/newsletter/', data)
		self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

	def test_newsletter_invalid_email(self):
		"""Test that invalid emails are rejected"""
		data = {'email': 'not-an-email'}
		response = self.client.post('/api/newsletter/', data)
		self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
