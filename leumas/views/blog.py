from django.shortcuts import render
from leumas.blog_helpers import get_blog_posts_with_dynamic_dates


def blog(request):
    """Display blog listings page"""
    blog_posts = get_blog_posts_with_dynamic_dates()
    context = {'all_blogs': blog_posts, 'scroll_to': 'blog'}
    return render(request, 'leumas/blogs.html', context)


def blogs(request):
    """Alias for blog view"""
    blog_posts = get_blog_posts_with_dynamic_dates()
    context = {'all_blogs': blog_posts, 'scroll_to': 'blog'}
    return render(request, 'leumas/blogs.html', context)


def blog_detail(request, blog_id):
    """Display details for a specific blog post"""
    blog_posts = get_blog_posts_with_dynamic_dates()
    blog = blog_posts.get(blog_id)
    if not blog:
        blogs_list = list(blog_posts.values())
        blog = blogs_list[0] if blogs_list else None
    
    context = {
        'blog': blog,
        'blog_id': blog_id,
        'all_blogs': blog_posts,
    }
    return render(request, 'leumas/blog-details.html', context)
