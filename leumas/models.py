from django.db import models
from django.utils.text import slugify
from django.core.validators import MinValueValidator, MaxValueValidator


class Newsletter(models.Model):
    email = models.EmailField(unique=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.email

    class Meta:
        ordering = ['-subscribed_at']


class Tag(models.Model):
    """Tags for blog posts and portfolio projects"""
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['name']


class BlogPost(models.Model):
    """Blog posts model"""
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    category = models.CharField(max_length=50)
    author = models.CharField(max_length=100, default='Samuel Adomeh')
    published_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    featured_image = models.ImageField(upload_to='blog/', null=True, blank=True)
    excerpt = models.TextField()
    content = models.TextField()
    is_published = models.BooleanField(default=True)
    views_count = models.IntegerField(default=0)
    tags = models.ManyToManyField(Tag, blank=True)
    meta_description = models.CharField(max_length=160, blank=True, help_text="SEO meta description")
    meta_keywords = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return self.title

    def get_reading_time(self):
        """Calculate reading time in minutes"""
        words = len(self.content.split())
        return max(1, words // 200)

    def increment_views(self):
        """Increment view count"""
        self.views_count += 1
        self.save(update_fields=['views_count'])

    def get_related_posts(self, limit=3):
        """Get related posts by tags"""
        return BlogPost.objects.filter(
            tags__in=self.tags.all(),
            is_published=True
        ).exclude(id=self.id).distinct()[:limit]

    def get_absolute_url(self):
        return f'/blog/{self.id}/'

    class Meta:
        ordering = ['-published_date']
        indexes = [
            models.Index(fields=['-published_date']),
            models.Index(fields=['slug']),
            models.Index(fields=['is_published']),
        ]


class Portfolio(models.Model):
    """Portfolio projects model"""
    title = models.CharField(max_length=200)
    subtitle = models.CharField(max_length=200, blank=True)
    slug = models.SlugField(unique=True)
    category = models.CharField(max_length=50)
    image = models.ImageField(upload_to='portfolio/')
    description = models.TextField()
    challenge = models.TextField(blank=True)
    solution = models.TextField(blank=True)
    results = models.TextField(blank=True)
    tags = models.ManyToManyField(Tag, blank=True)
    is_featured = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True)
    meta_description = models.CharField(max_length=160, blank=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return f'/portfolio/{self.id}/'

    class Meta:
        ordering = ['-created_date']


class Service(models.Model):
    """Services offered"""
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    icon = models.CharField(max_length=50, help_text="FontAwesome icon class")
    order = models.IntegerField(default=0, validators=[MinValueValidator(0)])

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['order']


class Skill(models.Model):
    """Technical skills"""
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=100)  # e.g., "Cloud Platforms", "CI/CD"
    proficiency = models.IntegerField(
        default=80,
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )

    def __str__(self):
        return f"{self.name} ({self.category})"

    class Meta:
        ordering = ['category', '-proficiency']
        unique_together = ['name', 'category']


class Contact(models.Model):
    """Store contact form submissions"""
    name = models.CharField(max_length=120)
    email = models.EmailField()
    inquiry = models.CharField(max_length=70)
    message = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} - {self.inquiry}"

    class Meta:
        ordering = ['-submitted_at']
