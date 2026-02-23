from django.contrib import admin
from .models import Newsletter, BlogPost, Portfolio, Service, Skill, Tag, Contact


@admin.register(Newsletter)
class NewsletterAdmin(admin.ModelAdmin):
    list_display = ('email', 'subscribed_at', 'is_active')
    list_filter = ('is_active', 'subscribed_at')
    search_fields = ('email',)
    readonly_fields = ('subscribed_at',)
    fieldsets = (
        ('Subscription Information', {
            'fields': ('email', 'is_active', 'subscribed_at')
        }),
    )


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'category', 'is_published', 'published_date', 'views_count')
    list_filter = ('is_published', 'category', 'published_date', 'tags')
    search_fields = ('title', 'content', 'author')
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ('views_count', 'published_date', 'updated_date')
    filter_horizontal = ('tags',)
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'slug', 'author')
        }),
        ('Content', {
            'fields': ('excerpt', 'content', 'featured_image')
        }),
        ('Metadata', {
            'fields': ('category', 'tags', 'meta_description', 'meta_keywords', 'is_published')
        }),
        ('Statistics', {
            'fields': ('views_count', 'published_date', 'updated_date'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Portfolio)
class PortfolioAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'is_featured', 'created_date')
    list_filter = ('category', 'is_featured', 'created_date', 'tags')
    search_fields = ('title', 'description', 'challenge', 'solution')
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ('created_date',)
    filter_horizontal = ('tags',)
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'subtitle', 'slug', 'category', 'image', 'is_featured')
        }),
        ('Content', {
            'fields': ('description', 'challenge', 'solution', 'results')
        }),
        ('Metadata', {
            'fields': ('tags', 'meta_description'),
        }),
        ('Metadata', {
            'fields': ('created_date',),
            'classes': ('collapse',)
        }),
    )


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('title', 'order')
    list_editable = ('order',)
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ('title', 'description')


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'proficiency')
    list_filter = ('category',)
    search_fields = ('name', 'category')
    list_editable = ('proficiency',)


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'inquiry', 'submitted_at', 'is_read')
    list_filter = ('is_read', 'submitted_at')
    search_fields = ('name', 'email', 'message')
    readonly_fields = ('name', 'email', 'inquiry', 'message', 'submitted_at')
    
    fieldsets = (
        ('Contact Information', {
            'fields': ('name', 'email', 'inquiry')
        }),
        ('Message', {
            'fields': ('message',)
        }),
        ('Status', {
            'fields': ('is_read', 'submitted_at')
        }),
    )
