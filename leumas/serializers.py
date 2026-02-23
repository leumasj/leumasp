from rest_framework import serializers
from .models import BlogPost, Portfolio, Service, Skill, Tag, Newsletter


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name', 'slug']


class BlogPostSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, read_only=True)
    reading_time = serializers.SerializerMethodField()

    class Meta:
        model = BlogPost
        fields = [
            'id', 'title', 'slug', 'author', 'category', 'excerpt',
            'featured_image', 'published_date', 'updated_date', 'views_count',
            'tags', 'reading_time', 'meta_description'
        ]
        read_only_fields = ['id', 'slug', 'published_date', 'updated_date', 'views_count']

    def get_reading_time(self, obj):
        return obj.get_reading_time()


class BlogPostDetailSerializer(BlogPostSerializer):
    related_posts = serializers.SerializerMethodField()

    class Meta(BlogPostSerializer.Meta):
        fields = BlogPostSerializer.Meta.fields + ['content', 'related_posts']

    def get_related_posts(self, obj):
        related = obj.get_related_posts()
        return BlogPostSerializer(related, many=True).data


class PortfolioSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, read_only=True)

    class Meta:
        model = Portfolio
        fields = [
            'id', 'title', 'subtitle', 'slug', 'category', 'image',
            'description', 'tags', 'is_featured', 'created_date', 'meta_description'
        ]
        read_only_fields = ['id', 'slug', 'created_date']


class PortfolioDetailSerializer(PortfolioSerializer):
    class Meta(PortfolioSerializer.Meta):
        fields = PortfolioSerializer.Meta.fields + ['challenge', 'solution', 'results']


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ['id', 'title', 'slug', 'description', 'icon', 'order']
        read_only_fields = ['id', 'slug']


class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = ['id', 'name', 'category', 'proficiency']
        read_only_fields = ['id']


class NewsletterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Newsletter
        fields = ['email']
        extra_kwargs = {
            'email': {'required': True}
        }

    def validate_email(self, value):
        if Newsletter.objects.filter(email=value, is_active=True).exists():
            raise serializers.ValidationError('This email is already subscribed.')
        return value
