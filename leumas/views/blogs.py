from datetime import datetime, timedelta

def get_dynamic_blog_dates():
    """Generate dynamic blog post dates within the last 2 weeks"""
    today = datetime.now()
    dates = []
    # Generate 7 dates going back 14 days, spaced out
    for i in range(7):
        date = today - timedelta(days=i*2)
        dates.append(date.strftime('%d %b, %Y'))
    return dates


def get_blog_posts_with_dynamic_dates():
    """Get blog posts with fresh dynamic dates on each call"""
    dates = get_dynamic_blog_dates()
    
    blog_posts = {
        1: {
            'title': 'Setting Up Kubernetes High Availability Clusters',
            'category': 'Kubernetes',
            'author': 'Samuel Adomeh',
            'date': dates[0],
            'image': '/static/images/blog/img1.png',
            'excerpt': 'A comprehensive guide to setting up and maintaining highly available Kubernetes clusters across multiple availability zones.',
            'content': '...'
        },
        2: {
            'title': 'GitLab CI/CD Pipelines: From Zero to Hero',
            'category': 'CI/CD',
            'author': 'Samuel Adomeh',
            'date': dates[1],
            'image': '/static/images/blog/img2.png',
            'excerpt': 'Master GitLab CI/CD pipelines: creating efficient, scalable automation that enables rapid, reliable deployments.',
            'content': '...'
        },
        3: {
            'title': 'Terraform: Infrastructure as Code Best Practices',
            'category': 'Infrastructure',
            'author': 'Samuel Adomeh',
            'date': dates[2],
            'image': '/static/images/blog/img3.png',
            'excerpt': 'Learn Terraform best practices for managing cloud infrastructure as code with version control and team collaboration.',
            'content': '...'
        },
        4: {
            'title': 'Docker Container Optimization and Security',
            'category': 'Containers',
            'author': 'Samuel Adomeh',
            'date': dates[3],
            'image': '/static/images/blog/img4.png',
            'excerpt': 'Optimize Docker containers for performance, size reduction, and security hardening in production environments.',
            'content': '...'
        },
        5: {
            'title': 'Observability: Monitoring, Logging, and Tracing',
            'category': 'Observability',
            'author': 'Samuel Adomeh',
            'date': dates[4],
            'image': '/static/images/blog/img5.png',
            'excerpt': 'Implement comprehensive observability with Prometheus, ELK Stack, and distributed tracing for production systems.',
            'content': '...'
        },
        6: {
            'title': 'AWS Networking: VPC, Subnets, and Security Groups',
            'category': 'Cloud',
            'author': 'Samuel Adomeh',
            'date': dates[5],
            'image': '/static/images/blog/img6.png',
            'excerpt': 'Deep dive into AWS networking fundamentals: VPCs, subnets, routing, and security group configurations.',
            'content': '...'
        },
        7: {
            'title': 'DevOps: Culture, Tools, and Practices',
            'category': 'DevOps',
            'author': 'Samuel Adomeh',
            'date': dates[6],
            'image': '/static/images/blog/img3.png',
            'excerpt': 'Explore DevOps culture, methodologies, and tools for building high-performing technology teams.',
            'content': '...'
        }
    }
    
    return blog_posts
