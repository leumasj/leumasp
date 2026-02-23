from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from .models import BlogPost, Portfolio, Service, Skill, Newsletter
from .serializers import (
    BlogPostSerializer, BlogPostDetailSerializer,
    PortfolioSerializer, PortfolioDetailSerializer,
    ServiceSerializer, SkillSerializer, NewsletterSerializer
)


class BlogPostViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint for blog posts.
    
    List, retrieve, and search blog posts.
    """
    queryset = BlogPost.objects.filter(is_published=True)
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['category', 'tags', 'author']
    search_fields = ['title', 'content', 'excerpt']
    ordering_fields = ['published_date', 'views_count']
    ordering = ['-published_date']

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return BlogPostDetailSerializer
        return BlogPostSerializer

    @action(detail=True, methods=['post'])
    def increment_views(self, request, pk=None):
        """Increment view count for a blog post"""
        blog = self.get_object()
        blog.increment_views()
        return Response({'views_count': blog.views_count})

    @action(detail=True, methods=['get'])
    def related_posts(self, request, pk=None):
        """Get related posts for this blog"""
        blog = self.get_object()
        related = blog.get_related_posts()
        serializer = BlogPostSerializer(related, many=True)
        return Response(serializer.data)


class PortfolioViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint for portfolio projects.
    
    List and retrieve portfolio projects.
    """
    queryset = Portfolio.objects.all()
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['category', 'tags', 'is_featured']
    search_fields = ['title', 'description', 'challenge', 'solution']
    ordering_fields = ['created_date', 'is_featured']
    ordering = ['-is_featured', '-created_date']

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return PortfolioDetailSerializer
        return PortfolioSerializer

    @action(detail=False, methods=['get'])
    def featured(self, request):
        """Get featured portfolio projects"""
        featured = self.get_queryset().filter(is_featured=True)
        serializer = PortfolioSerializer(featured, many=True)
        return Response(serializer.data)


class ServiceViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint for services.
    
    List and retrieve services offered.
    """
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    ordering_fields = ['order']
    ordering = ['order']


class SkillViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint for technical skills.
    
    List and retrieve skills by category.
    """
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['category']
    ordering_fields = ['category', 'proficiency']
    ordering = ['category', '-proficiency']


class NewsletterViewSet(viewsets.ModelViewSet):
    """
    API endpoint for newsletter subscriptions.
    
    Create new newsletter subscriptions.
    """
    queryset = Newsletter.objects.all()
    serializer_class = NewsletterSerializer
    http_method_names = ['post']

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(
            {'detail': 'Successfully subscribed to the newsletter.'},
            status=status.HTTP_201_CREATED
        )

    def perform_create(self, serializer):
        serializer.save()
