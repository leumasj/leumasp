from django.shortcuts import render
from django.views.generic import FormView, TemplateView
from django.urls import reverse_lazy
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_POST
from datetime import datetime, timedelta
from .forms import ContactForm, NewsletterForm
from .models import Newsletter
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib.units import inch
from io import BytesIO


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
            'content': '''
            <h3>Understanding High Availability</h3>
            <p>High availability (HA) is a critical requirement for production Kubernetes clusters. In this guide, we explore the key components and best practices for building resilient Kubernetes infrastructure.</p>
            <h3>Key Components</h3>
            <ul>
                <li>Multiple control plane nodes with etcd clustering</li>
                <li>Load balancing for API server access</li>
                <li>Persistent volume management</li>
                <li>Network policies and segmentation</li>
            </ul>
            <h3>Implementation Best Practices</h3>
            <p>We cover deployment strategies, monitoring, and disaster recovery planning to ensure your clusters maintain 99.9% uptime SLA.</p>
            <h3>Monitoring and Observability</h3>
            <p>Proper monitoring is essential for maintaining cluster health. Learn how to implement comprehensive monitoring with Prometheus and Grafana.</p>
            '''
        },
        2: {
            'title': 'GitLab CI/CD Pipelines: From Zero to Hero',
            'category': 'CI/CD',
            'author': 'Samuel Adomeh',
            'date': dates[1],
            'image': '/static/images/blog/img2.png',
            'excerpt': 'Master GitLab CI/CD pipelines: creating efficient, scalable automation that enables rapid, reliable deployments.',
            'content': '''
            <h3>GitLab CI/CD Overview</h3>
            <p>GitLab provides powerful built-in CI/CD capabilities that integrate seamlessly with your repository. Learn how to leverage these tools effectively.</p>
            <h3>Pipeline Structure</h3>
            <p>We explore the anatomy of a CI/CD pipeline, including stages, jobs, and artifacts management.</p>
            <h3>Advanced Techniques</h3>
            <ul>
                <li>Parallel execution for faster builds</li>
                <li>Conditional pipelines and rules</li>
                <li>Caching strategies for performance</li>
                <li>Integration with Kubernetes for deployment</li>
            </ul>
            <h3>Security in CI/CD</h3>
            <p>Implement security scanning, secret management, and compliance checks within your pipeline.</p>
            '''
        },
        3: {
            'title': 'Terraform: Infrastructure as Code Best Practices',
            'category': 'Infrastructure',
            'author': 'Samuel Adomeh',
            'date': dates[2],
            'image': '/static/images/blog/img3.png',
            'excerpt': 'Learn Terraform best practices for managing cloud infrastructure as code with version control and team collaboration.',
            'content': '''
            <h3>Why Infrastructure as Code?</h3>
            <p>Infrastructure as Code (IaC) enables reproducible, version-controlled infrastructure deployments.</p>
            <h3>Terraform Fundamentals</h3>
            <p>We cover providers, resources, variables, and outputs - the building blocks of Terraform configurations.</p>
            <h3>Module Management</h3>
            <ul>
                <li>Creating reusable modules</li>
                <li>Module composition patterns</li>
                <li>Remote module registries</li>
                <li>Dependency management</li>
            </ul>
            <h3>State Management</h3>
            <p>Learn about Terraform state, remote backends, and best practices for team environments.</p>
            <h3>Advanced Topics</h3>
            <p>Explore workspaces, dynamic blocks, and other advanced Terraform features for complex infrastructure.</p>
            '''
        },
        4: {
            'title': 'Docker Container Optimization and Security',
            'category': 'Containers',
            'author': 'Samuel Adomeh',
            'date': dates[3],
            'image': '/static/images/blog/img4.png',
            'excerpt': 'Optimize Docker containers for performance, size reduction, and security hardening in production environments.',
            'content': '''
            <h3>Container Security Fundamentals</h3>
            <p>Security is paramount in containerized environments. Learn best practices for secure container deployment and management.</p>
            <h3>Image Optimization</h3>
            <ul>
                <li>Multi-stage builds for smaller images</li>
                <li>Layer caching optimization</li>
                <li>Base image selection</li>
                <li>Minimal container practices</li>
            </ul>
            <h3>Runtime Security</h3>
            <p>Implement resource limits, network policies, and security contexts to harden your containers.</p>
            <h3>Vulnerability Scanning</h3>
            <p>Integrate vulnerability scanning in your build pipeline using tools like Trivy and Anchore.</p>
            '''
        },
        5: {
            'title': 'Observability: Monitoring, Logging, and Tracing',
            'category': 'Observability',
            'author': 'Samuel Adomeh',
            'date': dates[4],
            'image': '/static/images/blog/img5.png',
            'excerpt': 'Implement comprehensive observability with Prometheus, ELK Stack, and distributed tracing for production systems.',
            'content': '''
            <h3>The Three Pillars of Observability</h3>
            <p>Metrics, logs, and traces provide comprehensive insight into application behavior and system health.</p>
            <h3>Metrics with Prometheus</h3>
            <ul>
                <li>Setting up Prometheus scrape configs</li>
                <li>Custom metrics instrumentation</li>
                <li>Alerting rules and evaluation</li>
                <li>Long-term metrics storage</li>
            </ul>
            <h3>Centralized Logging with ELK</h3>
            <p>Aggregate logs from multiple sources using Elasticsearch, Logstash, and Kibana.</p>
            <h3>Distributed Tracing</h3>
            <p>Implement distributed tracing with tools like Jaeger to understand request flows across microservices.</p>
            '''
        },
        6: {
            'title': 'AWS Networking: VPC, Subnets, and Security Groups',
            'category': 'Cloud',
            'author': 'Samuel Adomeh',
            'date': dates[5],
            'image': '/static/images/blog/img6.png',
            'excerpt': 'Deep dive into AWS networking fundamentals: VPCs, subnets, routing, and security group configurations.',
            'content': '''
            <h3>VPC Architecture</h3>
            <p>Design robust Virtual Private Cloud (VPC) architectures that support high availability and security.</p>
            <h3>Subnet Planning</h3>
            <ul>
                <li>Public vs private subnets</li>
                <li>Multi-AZ deployment strategies</li>
                <li>IP addressing and CIDR blocks</li>
                <li>Network ACLs and security groups</li>
            </ul>
            <h3>Connectivity Options</h3>
            <p>Learn about NAT gateways, VPN connections, and VPC peering for connecting networks.</p>
            <h3>Security Best Practices</h3>
            <p>Implement network segmentation, least privilege access, and monitoring for AWS networks.</p>
            '''
        },
        7: {
            'title': 'DevOps: Culture, Tools, and Practices',
            'category': 'DevOps',
            'author': 'Samuel Adomeh',
            'date': dates[6],
            'image': '/static/images/blog/img3.png',
            'excerpt': 'Explore DevOps culture, methodologies, and tools for building high-performing technology teams.',
            'content': '''
            <h3>DevOps Mindset</h3>
            <p>DevOps is more than tools - it\'s a culture of collaboration, automation, and continuous improvement.</p>
            <h3>Core DevOps Practices</h3>
            <ul>
                <li>Infrastructure as Code for reproducibility</li>
                <li>Continuous Integration and Deployment</li>
                <li>Automated testing and quality gates</li>
                <li>Monitoring and incident response</li>
            </ul>
            <h3>Team Structure</h3>
            <p>Explore cross-functional team models and communication strategies for DevOps success.</p>
            <h3>Metrics and Measurement</h3>
            <p>Track deployment frequency, lead time, and MTTR to measure DevOps effectiveness.</p>
            '''
        }
    }
    
    return blog_posts


# Get blog posts with dynamic dates  (call this function in views, not at module load)
# Note: BLOG_POSTS_TEMPLATE is generated dynamically on each request

# Portfolio projects data
PORTFOLIO_PROJECTS = {
    1: {
        'title': 'Kubernetes Multi-Cloud Orchestration',
        'subtitle': 'AWS, Azure & GCP K8s Cluster',
        'category': 'Infrastructure',
        'image': '/static/images/work/1.jpg',
        'description': 'Designed and implemented a comprehensive Kubernetes infrastructure spanning multiple cloud providers (AWS, Azure, GCP). This project involved setting up highly available K8s clusters with cross-cloud networking, automated scaling policies, and disaster recovery mechanisms.',
        'technologies': ['Kubernetes', 'Docker', 'AWS EKS', 'Azure AKS', 'Google GKE', 'Helm', 'Terraform'],
        'challenge': 'Managing consistent Kubernetes deployments and networking across three different cloud providers while maintaining security and cost optimization.',
        'solution': 'Implemented a unified Kubernetes management strategy using Helm charts and multi-cloud orchestration tools to ensure consistency and reduce operational overhead.',
        'results': 'Achieved 99.9% uptime, 40% cost reduction through optimization, and 60% faster deployment cycles.',
    },
    2: {
        'title': 'Advanced CI/CD Pipeline Architecture',
        'subtitle': 'GitLab CI + Docker + Kubernetes',
        'category': 'CI/CD',
        'image': '/static/images/work/2.jpg',
        'description': 'Built a complete DevOps infrastructure for continuous integration and continuous deployment using GitLab CI/CD. The pipeline automates code testing, building Docker images, security scanning, and deployment to Kubernetes clusters.',
        'technologies': ['GitLab CI', 'Docker', 'Kubernetes', 'Jenkins', 'SonarQube', 'Harbor', 'ArgoCD'],
        'challenge': 'Creating an automated pipeline that maintains code quality while enabling rapid deployments without manual interventions.',
        'solution': 'Implemented multi-stage pipelines with automated testing, container vulnerability scanning, and GitOps-based deployments.',
        'results': '95% test coverage, zero-downtime deployments, 10x faster release cycles.',
    },
    3: {
        'title': 'Infrastructure as Code (IaC)',
        'subtitle': 'Terraform + CloudFormation + Ansible',
        'category': 'Infrastructure',
        'image': '/static/images/work/3.jpg',
        'description': 'Developed comprehensive Infrastructure as Code implementations using Terraform and AWS CloudFormation to provision and manage cloud infrastructure programmatically. Automated provisioning, scaling, and configuration management.',
        'technologies': ['Terraform', 'CloudFormation', 'Ansible', 'AWS', 'Python', 'HCL'],
        'challenge': 'Managing complex infrastructure deployments across multiple environments with version control and repeatability.',
        'solution': 'Created modular Terraform modules and Ansible playbooks for consistent infrastructure deployment and management.',
        'results': 'Reduced infrastructure setup time from days to minutes, improved consistency across environments.',
    },
    4: {
        'title': 'PowerBI Analytics & Dashboards',
        'subtitle': 'Real-time Metrics & Reporting',
        'category': 'Analytics',
        'image': '/static/images/work/4.jpg',
        'description': 'Created interactive Power BI dashboards for real-time monitoring and business intelligence. Integrated data from multiple sources including databases, APIs, and cloud services for comprehensive analytics.',
        'technologies': ['Power BI', 'SQL', 'Azure Data Factory', 'DAX', 'Python', 'REST APIs'],
        'challenge': 'Consolidating data from disparate sources and creating meaningful visualizations for business decision-making.',
        'solution': 'Implemented data pipelines with Azure Data Factory and created interactive Power BI dashboards with drill-down capabilities.',
        'results': 'Enabled real-time business insights, reduced reporting time from 2 weeks to 1 day.',
    },
    5: {
        'title': 'Enterprise Monitoring Stack',
        'subtitle': 'Prometheus, ELK, Datadog Integration',
        'category': 'Infrastructure',
        'image': '/static/images/work/5.jpg',
        'description': 'Implemented enterprise-grade monitoring and logging infrastructure using Prometheus for metrics collection, ELK stack for log aggregation, and integrated with Datadog for centralized monitoring.',
        'technologies': ['Prometheus', 'Grafana', 'ELK Stack', 'Datadog', 'Alertmanager', 'Beats'],
        'challenge': 'Creating comprehensive observability across distributed systems with millions of events per minute.',
        'solution': 'Built scalable monitoring infrastructure with Prometheus and ELK, configured intelligent alerting rules.',
        'results': '99.9% uptime, reduced mean-time-to-detection (MTTD) from 30 minutes to 2 minutes.',
    },
    6: {
        'title': 'Google Apps Script Automation',
        'subtitle': 'Sheets, Forms & Business Integration',
        'category': 'Automation',
        'image': '/static/images/work/6.jpg',
        'description': 'Developed custom automation solutions using Google Apps Script to streamline business processes. Integrated Google Sheets, Forms, and Gmail with external APIs for end-to-end workflow automation.',
        'technologies': ['Google Apps Script', 'Google Sheets API', 'Python', 'REST APIs', 'Webhooks'],
        'challenge': 'Automating complex business workflows with legacy systems and multiple data sources.',
        'solution': 'Created custom scripts to synchronize data between Google Workspace and external systems automatically.',
        'results': '20 hours/week time savings, 100% data accuracy, seamless integration with existing tools.',
    },
    7: {
        'title': 'Enterprise AWS Migration',
        'subtitle': 'Zero-Downtime Cloud Transition',
        'category': 'Cloud',
        'image': '/static/images/work/7.jpg',
        'description': 'Led enterprise cloud migration from on-premise data centers to AWS with zero downtime. Managed database migration, application refactoring, and infrastructure transition for multiple business units.',
        'technologies': ['AWS', 'Database Migration Service', 'AWS DataSync', 'CloudFormation', 'Route53'],
        'challenge': 'Migrating critical business applications without service disruption while minimizing costs.',
        'solution': 'Implemented phased migration strategy with AWS DMS for database replication and CloudFormation for infrastructure provisioning.',
        'results': '30% infrastructure cost reduction, zero downtime migration, completed 3 months ahead of schedule.',
    },
    8: {
        'title': 'Jenkins Deployment Automation',
        'subtitle': 'Automated Testing & Deployment',
        'category': 'CI/CD',
        'image': '/static/images/work/8.jpg',
        'description': 'Built comprehensive Jenkins pipelines for automated testing, building, and deployment. Integrated static code analysis, security scanning, and automated testing frameworks.',
        'technologies': ['Jenkins', 'Groovy', 'Docker', 'SonarQube', 'JUnit', 'Selenium', 'Artifactory'],
        'challenge': 'Creating reliable automated deployments with comprehensive testing and security scanning.',
        'solution': 'Designed modular Jenkins pipelines with parallel execution, comprehensive artifact management, and deployment gates.',
        'results': '100% deployment automation, 50% faster release cycles, zero-downtime deployments.',
    },
    9: {
        'title': 'Microservices API Integration',
        'subtitle': 'REST, gRPC & Event-Driven Architecture',
        'category': 'Integration',
        'image': '/static/images/work/9.jpg',
        'description': 'Architected and implemented microservices-based API infrastructure using REST, gRPC, and event-driven patterns. Enabled scalable, loosely-coupled services with message queuing and event streaming.',
        'technologies': ['REST APIs', 'gRPC', 'Kafka', 'RabbitMQ', 'Python', 'Go', 'Docker', 'Kubernetes'],
        'challenge': 'Designing scalable microservices architecture with reliable inter-service communication.',
        'solution': 'Implemented API gateway, message queuing for asynchronous communication, and comprehensive monitoring.',
        'results': '99.95% availability, 10x throughput improvement, reduced latency by 60%.',
    },
}

# Services details data
SERVICES = {
    1: {
        'title': 'Cloud Infrastructure & DevOps',
        'icon': '/static/images/icon/024-server.png',
        'description': 'Enterprise-grade cloud infrastructure design, deployment, and management across AWS, Azure, and GCP.',
        'detailed_description': '''
        <h3>What's Included</h3>
        <ul>
            <li>Multi-cloud infrastructure design and architecture</li>
            <li>Kubernetes cluster setup and management (EKS, AKS, GKE)</li>
            <li>Containerization with Docker and container orchestration</li>
            <li>Infrastructure as Code (IaC) with Terraform and CloudFormation</li>
            <li>Auto-scaling and load balancing configuration</li>
            <li>Disaster recovery and backup strategies</li>
            <li>Security hardening and compliance management</li>
        </ul>
        <h3>Technologies Used</h3>
        <p>AWS (EC2, S3, RDS, Lambda, EKS, VPC), Azure (VMs, AKS, App Service, Cosmos DB), Google Cloud (Compute Engine, GKE, Cloud Storage), Kubernetes, Docker, Terraform, CloudFormation, Ansible, Helm</p>
        <h3>Timeline & Pricing</h3>
        <ul>
            <li>Hourly Consulting: $75-100/hour</li>
            <li>Small Project (Setup): 2-4 weeks | $5,000-15,000</li>
            <li>Enterprise Implementation: 8-12 weeks | $25,000-75,000+</li>
            <li>Ongoing Support: $2,000-5,000/month</li>
        </ul>
        <h3>Expected Outcomes</h3>
        <ul>
            <li>99.9% system uptime and availability</li>
            <li>30-50% reduction in infrastructure costs</li>
            <li>60-80% faster deployment cycles</li>
            <li>Automated scaling and resource optimization</li>
            <li>Enterprise-grade security and compliance</li>
        </ul>
        ''',
        'process': [
            'Infrastructure Assessment',
            'Cloud Strategy Planning',
            'Architecture Design',
            'Setup & Configuration',
            'Testing & Optimization',
            'Deployment & Monitoring',
            'Ongoing Support'
        ],
        'technologies': ['AWS', 'Azure', 'GCP', 'Kubernetes', 'Docker', 'Terraform', 'CloudFormation', 'Helm']
    },
    2: {
        'title': 'Web Development',
        'icon': '/static/images/icon/062-code-1.png',
        'description': 'Full-stack web development with modern frameworks and responsive design.',
        'detailed_description': '''
        <h3>What's Included</h3>
        <ul>
            <li>Full-stack web application development</li>
            <li>Frontend development (React, Vue.js, Angular)</li>
            <li>Backend development (Django, Node.js, Python)</li>
            <li>Responsive and mobile-first design</li>
            <li>Progressive Web Apps (PWA)</li>
            <li>API development and integration</li>
            <li>Database design and optimization</li>
            <li>Performance optimization and SEO</li>
        </ul>
        <h3>Technologies Used</h3>
        <p>React, Vue.js, Angular, Django, Node.js, Express.js, Python, JavaScript, HTML5, CSS3, PostgreSQL, MongoDB, Redis, Webpack, Docker</p>
        <h3>Timeline & Pricing</h3>
        <ul>
            <li>Simple Website: 2-3 weeks | $3,000-7,000</li>
            <li>E-commerce Platform: 4-8 weeks | $10,000-25,000</li>
            <li>Complex Web App: 8-16 weeks | $25,000-75,000+</li>
            <li>Hourly Rate: $60-85/hour</li>
        </ul>
        <h3>Expected Outcomes</h3>
        <ul>
            <li>Fast-loading, responsive web applications</li>
            <li>SEO-optimized pages with excellent performance scores</li>
            <li>Scalable architecture for future growth</li>
            <li>Secure and maintainable codebase</li>
            <li>Mobile-friendly user experience</li>
        </ul>
        ''',
        'process': [
            'Requirements Analysis',
            'UI/UX Design',
            'Frontend Development',
            'Backend Development',
            'Database Setup',
            'Integration Testing',
            'Deployment & Launch'
        ],
        'technologies': ['React', 'Vue.js', 'Django', 'Node.js', 'Python', 'PostgreSQL', 'MongoDB']
    },
    3: {
        'title': 'CI/CD Pipeline Automation',
        'icon': '/static/images/icon/043-analytics.png',
        'description': 'Automated testing, building, and deployment pipelines for rapid software releases.',
        'detailed_description': '''
        <h3>What's Included</h3>
        <ul>
            <li>CI/CD pipeline design and implementation</li>
            <li>Automated code testing and quality checks</li>
            <li>Container image building and registry management</li>
            <li>Automated security scanning (SAST, DAST)</li>
            <li>Blue-green and canary deployments</li>
            <li>Zero-downtime release strategies</li>
            <li>Automated rollback mechanisms</li>
            <li>Build artifact management and versioning</li>
        </ul>
        <h3>Technologies Used</h3>
        <p>GitLab CI/CD, GitHub Actions, Jenkins, Jenkins X, ArgoCD, SonarQube, Docker, Kubernetes, Artifactory, Nexus, AWS CodePipeline, Azure Pipelines</p>
        <h3>Timeline & Pricing</h3>
        <ul>
            <li>Basic Setup: 1-2 weeks | $3,000-6,000</li>
            <li>Full Pipeline Implementation: 2-4 weeks | $8,000-20,000</li>
            <li>Enterprise Pipeline: 4-8 weeks | $20,000-50,000+</li>
            <li>Monthly Maintenance: $1,500-3,000</li>
        </ul>
        <h3>Expected Outcomes</h3>
        <ul>
            <li>95%+ automated test coverage</li>
            <li>10x faster deployment cycles</li>
            <li>Zero-downtime deployments</li>
            <li>Reduced deployment failures by 90%</li>
            <li>Consistent build and release process</li>
        </ul>
        ''',
        'process': [
            'Pipeline Requirements Gathering',
            'Tool Selection & Setup',
            'Pipeline Design',
            'Implementation',
            'Testing & Validation',
            'Integration Testing',
            'Optimization & Documentation'
        ],
        'technologies': ['GitLab CI', 'GitHub Actions', 'Jenkins', 'Docker', 'Kubernetes', 'ArgoCD', 'SonarQube']
    },
    4: {
        'title': 'Performance & Security Optimization',
        'icon': '/static/images/icon/033-rocket.png',
        'description': 'Infrastructure security hardening and application performance tuning.',
        'detailed_description': '''
        <h3>What's Included</h3>
        <ul>
            <li>Security vulnerability assessment and penetration testing</li>
            <li>SSL/TLS certificate implementation and management</li>
            <li>WAF (Web Application Firewall) configuration</li>
            <li>DDoS protection setup</li>
            <li>Application performance profiling</li>
            <li>Database query optimization</li>
            <li>CDN and caching strategies</li>
            <li>Load balancing and auto-scaling optimization</li>
            <li>Compliance audit (HIPAA, GDPR, PCI-DSS, SOC2)</li>
        </ul>
        <h3>Technologies Used</h3>
        <p>SSL/TLS, nginx, Apache, HAProxy, CloudFlare, AWS CloudFront, New Relic, DataDog, Prometheus, Grafana, OpenVAS, Burp Suite</p>
        <h3>Timeline & Pricing</h3>
        <ul>
            <li>Security Audit: 1-2 weeks | $3,000-8,000</li>
            <li>Performance Optimization: 2-3 weeks | $5,000-12,000</li>
            <li>Full Security & Performance: 4-6 weeks | $15,000-35,000</li>
            <li>Ongoing Monitoring: $2,000-5,000/month</li>
        </ul>
        <h3>Expected Outcomes</h3>
        <ul>
            <li>99.9% uptime SLA compliance</li>
            <li>30-50% improvement in page load times</li>
            <li>Zero critical security vulnerabilities</li>
            <li>PCI-DSS/HIPAA/GDPR compliance achieved</li>
            <li>Reduced infrastructure costs through optimization</li>
        </ul>
        ''',
        'process': [
            'Security Assessment',
            'Vulnerability Analysis',
            'Performance Baseline Testing',
            'Optimization Implementation',
            'Security Hardening',
            'Compliance Verification',
            'Monitoring Setup'
        ],
        'technologies': ['SSL/TLS', 'WAF', 'CloudFlare', 'DataDog', 'New Relic', 'nginx', 'Prometheus']
    },
    5: {
        'title': 'Mobile App Development',
        'icon': '/static/images/icon/064-vector.png',
        'description': 'Native and cross-platform mobile applications for iOS and Android.',
        'detailed_description': '''
        <h3>What's Included</h3>
        <ul>
            <li>Native iOS development (Swift)</li>
            <li>Native Android development (Kotlin)</li>
            <li>Cross-platform development (React Native, Flutter)</li>
            <li>UI/UX design and prototyping</li>
            <li>Backend API integration</li>
            <li>Local and cloud data storage</li>
            <li>Push notifications and messaging</li>
            <li>App Store and Google Play deployment</li>
            <li>Performance optimization</li>
        </ul>
        <h3>Technologies Used</h3>
        <p>React Native, Flutter, Swift, Kotlin, Firebase, AWS Mobile Services, GraphQL, REST APIs, SQLite, CoreData, Realm Database</p>
        <h3>Timeline & Pricing</h3>
        <ul>
            <li>Simple App (Single Platform): 4-6 weeks | $8,000-15,000</li>
            <li>Cross-platform App: 6-10 weeks | $15,000-30,000</li>
            <li>Complex App (Native): 8-14 weeks | $25,000-60,000+</li>
            <li>Hourly Rate: $65-90/hour</li>
        </ul>
        <h3>Expected Outcomes</h3>
        <ul>
            <li>Fully functional iOS and Android applications</li>
            <li>Published on App Store and Google Play</li>
            <li>Seamless user experience across devices</li>
            <li>Offline functionality and data sync</li>
            <li>Scalable backend integration</li>
        </ul>
        ''',
        'process': [
            'App Concept & Requirements',
            'UI/UX Design',
            'Backend API Development',
            'Mobile App Development',
            'Testing & QA',
            'App Store Submission',
            'Post-Launch Support'
        ],
        'technologies': ['React Native', 'Flutter', 'Swift', 'Kotlin', 'Firebase', 'GraphQL']
    },
    6: {
        'title': 'System Architecture & Consulting',
        'icon': '/static/images/icon/054-puzzle.png',
        'description': 'Enterprise-grade system design and technical consulting for scaling operations.',
        'detailed_description': '''
        <h3>What's Included</h3>
        <ul>
            <li>System architecture design and planning</li>
            <li>Technology stack recommendations</li>
            <li>Microservices architecture design</li>
            <li>Distributed systems design</li>
            <li>Scalability assessment and planning</li>
            <li>Cost optimization analysis</li>
            <li>Security architecture review</li>
            <li>Legacy system modernization planning</li>
            <li>Team technical guidance and mentoring</li>
        </ul>
        <h3>Technologies & Patterns</h3>
        <p>Microservices, Event-Driven Architecture, CQRS, API Gateway, Load Balancing, Distributed Caching, Message Queuing, Database Sharding, Search Engines</p>
        <h3>Timeline & Pricing</h3>
        <ul>
            <li>1-hour Consultation: $150-200</li>
            <li>1-week Engagement: $3,000-5,000</li>
            <li>1-month Engagement: $10,000-20,000</li>
            <li>Full Consulting Project: 8-12 weeks | $30,000-100,000+</li>
        </ul>
        <h3>Expected Outcomes</h3>
        <ul>
            <li>Clear technical roadmap for next 12-24 months</li>
            <li>30-40% cost reduction through optimization</li>
            <li>Scalable architecture for 10x growth</li>
            <li>Improved team technical capabilities</li>
            <li>Risk mitigation and best practices implementation</li>
        </ul>
        ''',
        'process': [
            'Initial Discovery Call',
            'Current State Assessment',
            'Industry Best Practices Review',
            'Architecture Design',
            'Recommendations & Planning',
            'Implementation Roadmap',
            'Team Training & Handoff'
        ],
        'technologies': ['Microservices', 'Distributed Systems', 'Cloud Architecture', 'DevOps', 'Kubernetes', 'Docker']
    },
}


class ContactView(FormView):
    template_name = 'leumas/index.html'
    form_class = ContactForm
    # Use the app namespace defined in `leumas/urls.py`
    success_url = reverse_lazy('leumas:success')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['scroll_to'] = 'contact'
        return context

    def form_valid(self, form):
        # Calls the custom send method defined on the form
        form.send()
        return super().form_valid(form)


class ContactSuccessView(TemplateView):
    template_name = 'leumas/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['scroll_to'] = 'contact'
        return context


def index(request):
    blog_posts = get_blog_posts_with_dynamic_dates()
    context = {
        'all_services': SERVICES,
        'all_projects': PORTFOLIO_PROJECTS,
        'preview_blogs': {1: blog_posts.get(1), 2: blog_posts.get(2), 3: blog_posts.get(3), 4: blog_posts.get(4)},
    }
    return render(request, 'leumas/index.html', context)


def about(request):
    context = {
        'all_services': SERVICES,
        'all_projects': PORTFOLIO_PROJECTS,
        'scroll_to': 'about'
    }
    return render(request, 'leumas/index.html', context)


def works(request):
    context = {
        'all_services': SERVICES,
        'all_projects': PORTFOLIO_PROJECTS,
        'scroll_to': 'project-gallery'
    }
    return render(request, 'leumas/index.html', context)


def services(request):
    context = {
        'all_services': SERVICES,
        'all_projects': PORTFOLIO_PROJECTS,
        'scroll_to': 'service'
    }
    return render(request, 'leumas/index.html', context)


def blog(request):
    blog_posts = get_blog_posts_with_dynamic_dates()
    context = {'all_blogs': blog_posts, 'scroll_to': 'blog'}
    return render(request, 'leumas/index.html', context)


def blogs(request):
    blog_posts = get_blog_posts_with_dynamic_dates()
    context = {'all_blogs': blog_posts, 'scroll_to': 'blog'}
    return render(request, 'leumas/index.html', context)


def portfolio_detail(request, project_id):
    """Display details for a specific portfolio project"""
    project = PORTFOLIO_PROJECTS.get(project_id)
    if not project:
        projects = list(PORTFOLIO_PROJECTS.values())
        project = projects[0] if projects else None
    
    context = {
        'project': project,
        'project_id': project_id,
        'all_projects': PORTFOLIO_PROJECTS,
    }
    return render(request, 'leumas/portfolio-details.html', context)


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


@require_POST
def subscribe_newsletter(request):
    """Handle newsletter subscription"""
    form = NewsletterForm(request.POST)
    
    if form.is_valid():
        form.save()
        return JsonResponse({
            'success': True,
            'message': 'Thank you for subscribing! Check your email for updates.'
        })
    else:
        errors = form.errors.as_json()
        return JsonResponse({
            'success': False,
            'message': 'Email already subscribed or invalid.',
            'errors': form.errors
        }, status=400)


def service_detail(request, service_id):
    """Display details for a specific service"""
    service = SERVICES.get(service_id)
    if not service:
        services_list = list(SERVICES.values())
        service = services_list[0] if services_list else None
    
    context = {
        'service': service,
        'service_id': service_id,
        'all_services': SERVICES,
    }
    return render(request, 'leumas/service-details.html', context)


def download_cv(request):
    """Generate and download CV as PDF"""
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, topMargin=0.5*inch, bottomMargin=0.5*inch)
    story = []
    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#333333'),
        spaceAfter=6,
        alignment=1  # Center
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=14,
        textColor=colors.HexColor('#667eea'),
        spaceAfter=12,
        spaceBefore=12,
        borderColor=colors.HexColor('#667eea'),
        borderWidth=0.5,
        borderPadding=6,
    )
    
    normal_style = ParagraphStyle(
        'CustomNormal',
        parent=styles['Normal'],
        fontSize=10,
        leading=14,
    )
    
    small_style = ParagraphStyle(
        'Small',
        parent=styles['Normal'],
        fontSize=9,
        leading=11,
    )
    
    # Header with name and contact
    story.append(Paragraph("SAMUEL ADOMEH", title_style))
    story.append(Paragraph("Senior DevOps Engineer", styles['Normal']))
    story.append(Spacer(1, 0.1*inch))
    
    contact_text = "Wroclaw, Poland | +48 661 910 134 | <a href='mailto:hemodasam@gmail.com'>hemodasam@gmail.com</a> | <a href='https://www.linkedin.com/in/samuel-adomeh'>LinkedIn</a> | <a href='https://github.com/leumasp'>GitHub</a>"
    story.append(Paragraph(contact_text, small_style))
    story.append(Spacer(1, 0.15*inch))
    
    # Professional Summary
    story.append(Paragraph("PROFESSIONAL SUMMARY", heading_style))
    summary = """With over a decade of experience as a Senior DevOps Engineer, I specialize in transforming complex development workflows into streamlined, automated processes. Expert in cloud infrastructure, containerization, CI/CD pipelines, and enterprise-level system architecture. Proven track record of delivering 99.9% uptime solutions, reducing deployment cycles by 60%, and optimizing infrastructure costs."""
    story.append(Paragraph(summary, normal_style))
    story.append(Spacer(1, 0.1*inch))
    
    # Services/Core Competencies
    story.append(Paragraph("SERVICES & EXPERTISE", heading_style))
    
    services_data = []
    for sid, service in SERVICES.items():
        services_data.append([
            Paragraph(f"<b>{service['title']}</b>", small_style),
            Paragraph(service['description'], small_style)
        ])
    
    services_table = Table(services_data, colWidths=[1.5*inch, 4.5*inch])
    services_table.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.lightgrey),
    ]))
    story.append(services_table)
    story.append(Spacer(1, 0.15*inch))
    
    # Education
    story.append(Paragraph("EDUCATION", heading_style))
    education_data = [
        ['2006-2008', 'MSC in Computer Engineer', 'Envato University'],
        ['2003-2005', 'BSC in Computer Engineer', 'Envato University'],
        ['2000-2002', 'HSC in Computer Engineer', 'Envato University'],
    ]
    edu_table = Table(education_data, colWidths=[1*inch, 2*inch, 2.5*inch])
    edu_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f0f0f0')),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.lightgrey),
    ]))
    story.append(edu_table)
    story.append(Spacer(1, 0.15*inch))
    
    # Experience
    story.append(Paragraph("EXPERIENCE", heading_style))
    experience_data = [
        ['2014-2018', 'Full Stack Web Developer', 'Envato Company'],
        ['2011-2014', 'Web Developer', 'Envato Company'],
        ['2009-2011', 'Web Designer', 'Envato Company'],
    ]
    exp_table = Table(experience_data, colWidths=[1*inch, 2*inch, 2.5*inch])
    exp_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f0f0f0')),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.lightgrey),
    ]))
    story.append(exp_table)
    story.append(Spacer(1, 0.15*inch))
    
    # Technical Skills
    story.append(Paragraph("TECHNICAL SKILLS", heading_style))
    
    skills_data = [
        ['Cloud Platforms', 'AWS, Azure, Google Cloud Platform (GCP)'],
        ['Containerization', 'Docker, Kubernetes, Docker Compose, Helm'],
        ['CI/CD Tools', 'GitLab CI/CD, GitHub Actions, Jenkins, ArgoCD'],
        ['Infrastructure as Code', 'Terraform, CloudFormation, Ansible'],
        ['Monitoring & Logging', 'Prometheus, ELK Stack, Datadog, New Relic'],
        ['Scripting Languages', 'Bash/Shell, Python, PowerShell, Groovy'],
        ['Programming Languages', 'Python, Go, Node.js, Java'],
        ['Databases', 'PostgreSQL, MySQL, MongoDB, Redis'],
        ['Networking & Security', 'SSL/TLS, WAF, DDoS Protection, IAM, VPC Configuration'],
        ['Tools & Platforms', 'Git, Docker Registry, Artifactory, Jenkins, SonarQube'],
    ]
    
    skills_table = Table(skills_data, colWidths=[1.5*inch, 4.5*inch])
    skills_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f0f0f0')),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (0, -1), 'LEFT'),
        ('ALIGN', (1, 0), (1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.lightgrey),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ]))
    story.append(skills_table)
    story.append(Spacer(1, 0.15*inch))
    
    # Languages
    story.append(Paragraph("LANGUAGES", heading_style))
    story.append(Paragraph("English - Fluent | Polish - Professional Working Proficiency", normal_style))
    story.append(Spacer(1, 0.1*inch))
    
    # Certifications/Highlights
    story.append(Paragraph("KEY HIGHLIGHTS", heading_style))
    highlights = [
        "✓ Achieved 99.9% uptime SLA compliance across multiple deployments",
        "✓ Reduced deployment cycles by 60% through CI/CD automation",
        "✓ Designed and implemented multi-cloud infrastructure (AWS, Azure, GCP)",
        "✓ Led teams of 5+ engineers in DevOps transformation initiatives",
        "✓ Successfully migrated 15+ legacy applications to cloud-native architecture",
        "✓ Implemented monitoring solutions covering 1000+ metrics across enterprise infrastructure",
    ]
    for highlight in highlights:
        story.append(Paragraph(highlight, small_style))
    
    # Build PDF
    doc.build(story)
    buffer.seek(0)
    
    response = HttpResponse(buffer.getvalue(), content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="Samuel_Adomeh_CV.pdf"'
    return response