from django.shortcuts import render
from django.views.generic import FormView, TemplateView
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from datetime import datetime, timedelta
from .forms import ContactForm, NewsletterForm
from .models import Newsletter


def get_dynamic_blog_dates():
    """Generate dynamic blog post dates within the last 2 weeks"""
    today = datetime.now()
    dates = []
    # Generate 7 dates going back 14 days, spaced out
    for i in range(7):
        date = today - timedelta(days=i*2)
        dates.append(date.strftime('%d %b, %Y'))
    return dates


# Get dynamic dates for blog posts
_blog_dates = get_dynamic_blog_dates()

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

# Blog posts data
BLOG_POSTS = {
    1: {
        'title': 'Kubernetes Security Best Practices: Protecting Your Containerized Applications',
        'date': _blog_dates[0],
        'author': 'Sam',
        'category': 'Kubernetes',
        'image': '/static/images/blog/img1.png',
        'excerpt': 'Comprehensive guide to implementing security best practices in Kubernetes environments.',
        'content': '''
        <h3>Introduction</h3>
        <p>Kubernetes has become the standard for container orchestration, but with great power comes great responsibility. Security in Kubernetes requires attention at multiple layers: cluster security, network policies, pod security, and secrets management.</p>
        
        <h3>Key Security Principles</h3>
        <p><strong>1. Principle of Least Privilege</strong><br/>
        Always run containers with minimal required permissions. Use Pod Security Policies and SecurityContexts to enforce constraints at the pod level. Avoid running containers as root whenever possible.</p>
        
        <p><strong>2. Network Isolation</strong><br/>
        Implement NetworkPolicies to control traffic between pods. Use service mesh solutions like Istio for advanced network security and traffic management. Encrypt communication between services using mTLS.</p>
        
        <p><strong>3. Image Security</strong><br/>
        Scan container images for vulnerabilities before deployment. Use private container registries and implement image signing. Regularly update base images and dependencies.</p>
        
        <h3>Implementing Pod Security Standards</h3>
        <p>Migrate from deprecated Pod Security Policies to Pod Security Standards. Define restricted, baseline, and unrestricted profiles for your workloads. Enforce these standards at the namespace level.</p>
        
        <h3>Secret Management</h3>
        <p>Never hardcode secrets in images or configuration files. Use dedicated secret management solutions like HashiCorp Vault, AWS Secrets Manager, or Azure Key Vault. Implement encryption for secrets at rest using etcd encryption.</p>
        
        <h3>RBAC Configuration</h3>
        <p>Implement Role-Based Access Control strictly. Create granular roles for different teams and services. Regularly audit role bindings and remove unnecessary permissions.</p>
        
        <h3>Monitoring and Auditing</h3>
        <p>Enable Kubernetes audit logging to track all API requests. Use security monitoring tools like Falco to detect suspicious container behavior. Implement real-time alerts for security events.</p>
        
        <h3>Conclusion</h3>
        <p>Kubernetes security is an ongoing process, not a one-time setup. Regularly update your security practices, stay informed about new vulnerabilities, and conduct security audits periodically. By following these best practices, you can significantly reduce your attack surface and protect your containerized applications.</p>
        ''',
        'technologies': ['Kubernetes', 'Security', 'Container', 'RBAC'],
    },
    2: {
        'title': 'GitOps vs Traditional CI/CD: Which Approach Wins in 2024?',
        'date': _blog_dates[1],
        'author': 'Sam',
        'category': 'CI/CD',
        'image': '/static/images/blog/img2.png',
        'excerpt': 'Comparing GitOps and traditional CI/CD pipelines to help you choose the right approach for your organization.',
        'content': '''
        <h3>Understanding the Paradigm Shift</h3>
        <p>GitOps represents a significant shift in how we think about deployment and infrastructure management. Instead of pushing changes to systems, GitOps pulls desired state from a Git repository, making Git the single source of truth.</p>
        
        <h3>Traditional CI/CD Pipeline Architecture</h3>
        <p><strong>Push-Based Model:</strong> Code commits trigger CI/CD pipelines that execute tests, build artifacts, and push changes to production. Deployment scripts execute directly on target systems.</p>
        
        <p><strong>Workflow:</strong> Developer commits → CI pipeline runs → Deployment triggered → Changes pushed to environment</p>
        
        <p><strong>Advantages:</strong></p>
        <ul>
        <li>Immediate feedback on failures</li>
        <li>Direct control over deployment process</li>
        <li>Well-established tooling (Jenkins, GitLab CI, GitHub Actions)</li>
        </ul>
        
        <h3>GitOps Approach</h3>
        <p><strong>Pull-Based Model:</strong> Declarative infrastructure and application definitions stored in Git. Controllers (like ArgoCD or Flux) continuously reconcile the actual state with desired state.</p>
        
        <p><strong>Workflow:</strong> Developer commits → Git repository updated → Controller detects drift → Automatic reconciliation</p>
        
        <p><strong>Advantages:</strong></p>
        <ul>
        <li>Git as single source of truth</li>
        <li>Automatic rollback via Git history</li>
        <li>Improved security (no direct access to production)</li>
        <li>Better audit trail and compliance</li>
        <li>Declarative, idempotent deployments</li>
        </ul>
        
        <h3>Key Differences</h3>
        <table>
        <tr>
        <th>Aspect</th>
        <th>Traditional CI/CD</th>
        <th>GitOps</th>
        </tr>
        <tr>
        <td>Deployment Model</td>
        <td>Push-based</td>
        <td>Pull-based</td>
        </tr>
        <tr>
        <td>Source of Truth</td>
        <td>Pipeline configuration</td>
        <td>Git repository</td>
        </tr>
        <tr>
        <td>Rollback</td>
        <td>Manual or scripted</td>
        <td>Git revert + auto-reconcile</td>
        </tr>
        <tr>
        <td>Security</td>
        <td>Requires deployment credentials</td>
        <td>No production credentials needed</td>
        </tr>
        </table>
        
        <h3>Real-World Scenarios</h3>
        <p><strong>Use Traditional CI/CD when:</strong></p>
        <ul>
        <li>Your infrastructure is not declaratively defined</li>
        <li>You need immediate feedback and tight feedback loops</li>
        <li>You have mixed on-premise and cloud environments</li>
        </ul>
        
        <p><strong>Use GitOps when:</strong></p>
        <ul>
        <li>You're running Kubernetes clusters</li>
        <li>You value security and audit trails</li>
        <li>You want predictable, reproducible deployments</li>
        <li>You need multi-environment deployments</li>
        </ul>
        
        <h3>Conclusion</h3>
        <p>The answer isn't either/or. Many organizations successfully use both: GitOps for Kubernetes and declarative infrastructure, combined with traditional CI/CD for build and test stages. The key is choosing the right tool for your specific use case.</p>
        ''',
        'technologies': ['GitOps', 'CI/CD', 'ArgoCD', 'Flux', 'Kubernetes'],
    },
    3: {
        'title': 'Observability at Scale: Implementing Distributed Tracing with Jaeger',
        'date': _blog_dates[2],
        'author': 'Sam',
        'category': 'Observability',
        'image': '/static/images/blog/img3.png',
        'excerpt': 'Master distributed tracing to understand microservices behavior and troubleshoot complex issues.',
        'content': '''
        <h3>Why Distributed Tracing Matters</h3>
        <p>In microservices architectures, a single user request can traverse dozens of services. Traditional logging and metrics fall short in understanding the complete flow. Distributed tracing provides end-to-end visibility into request journeys.</p>
        
        <h3>Understanding Jaeger Architecture</h3>
        <p>Jaeger is an open-source platform for distributed tracing, inspired by Google's Dapper paper. It helps track transactions across services and optimize backend performance.</p>
        
        <p><strong>Components:</strong></p>
        <ul>
        <li>Jaeger Client: Instrumentation libraries for different languages</li>
        <li>Jaeger Agent: UDP server receiving spans from clients</li>
        <li>Jaeger Collector: Processes and stores spans</li>
        <li>Query Service: Provides API for accessing traces</li>
        <li>Jaeger UI: Web interface for trace visualization</li>
        </ul>
        
        <h3>Core Concepts</h3>
        <p><strong>Traces:</strong> Record of a complete request journey</p>
        <p><strong>Spans:</strong> Individual operations within a trace (e.g., database query, HTTP call)</p>
        <p><strong>Baggage:</strong> Cross-process data propagation</p>
        
        <h3>Implementation Best Practices</h3>
        <p><strong>1. Instrumentation Strategy</strong><br/>
        Start with critical paths. Instrument entry points and external service calls first. Use automatic instrumentation where possible (OpenTelemetry collectors).</p>
        
        <p><strong>2. Sampling Strategies</strong><br/>
        Implement intelligent sampling to avoid overwhelming your system. Use probabilistic sampling (1% of requests), rate-limited sampling, or priority-based sampling.</p>
        
        <p><strong>3. Context Propagation</strong><br/>
        Use OpenTelemetry standards for context propagation across services. Ensure trace IDs are passed through HTTP headers, message queues, and async calls.</p>
        
        <h3>Advanced Features</h3>
        <p><strong>Service Dependencies:</strong> Jaeger can generate service dependency graphs from trace data, helping understand your microservices architecture.</p>
        
        <p><strong>Performance Analysis:</strong> Identify bottlenecks by analyzing span latencies and critical paths.</p>
        
        <p><strong>Error Analysis:</strong> Track errors across service boundaries and identify root causes.</p>
        
        <h3>Integration with Other Tools</h3>
        <p>Jaeger integrates seamlessly with Prometheus for metrics, ELK Stack for logs, and service meshes like Istio. This unified observability stack provides complete insight into your system behavior.</p>
        
        <h3>Conclusion</h3>
        <p>Distributed tracing is essential for operating microservices at scale. Jaeger provides the tools and architecture needed to implement tracing effectively. Start small, measure impact, and scale your observability infrastructure based on real needs.</p>
        ''',
        'technologies': ['Jaeger', 'Distributed Tracing', 'OpenTelemetry', 'Observability'],
    },
    4: {
        'title': 'Infrastructure as Code: Terraform Best Practices for Large Organizations',
        'date': _blog_dates[3],
        'author': 'Sam',
        'category': 'Infrastructure',
        'image': '/static/images/blog/img4.png',
        'excerpt': 'Learn enterprise-grade Terraform practices for managing complex infrastructure at scale.',
        'content': '''
        <h3>Introduction to Infrastructure as Code</h3>
        <p>Infrastructure as Code (IaC) treats infrastructure the same way we treat application code: versioned, reviewed, tested, and deployed through automated processes. Terraform is the leading declarative IaC tool.</p>
        
        <h3>Project Structure for Large Organizations</h3>
        <p><strong>Recommended Structure:</strong></p>
        <pre>
infrastructure/
├── modules/                 # Reusable components
│   ├── networking/
│   ├── compute/
│   ├── storage/
│   └── databases/
├── environments/            # Environment-specific
│   ├── dev/
│   ├── staging/
│   └── production/
├── global/                  # Shared resources
└── README.md
        </pre>
        
        <h3>Module Strategy</h3>
        <p><strong>Benefits of Modules:</strong></p>
        <ul>
        <li>Code reusability across projects</li>
        <li>Consistent resource management</li>
        <li>Easier maintenance and updates</li>
        <li>Clear separation of concerns</li>
        </ul>
        
        <p><strong>Module Best Practices:</strong></p>
        <ul>
        <li>One responsibility per module</li>
        <li>Well-documented inputs and outputs</li>
        <li>Version your modules</li>
        <li>Provide sensible defaults</li>
        </ul>
        
        <h3>State Management</h3>
        <p><strong>Remote State:</strong> Always use remote state in production. Store state in S3, Azure Blob Storage, or Terraform Cloud.</p>
        
        <p><strong>State Locking:</strong> Enable state locking to prevent concurrent modifications. Use DynamoDB with S3 or native locking in managed backends.</p>
        
        <p><strong>Sensitive Data:</strong> Use Terraform variables for secrets, encrypt in transit, and consider using Vault for secrets management.</p>
        
        <h3>Workflow and Collaboration</h3>
        <p><strong>Code Review Process:</strong></p>
        <ul>
        <li>Require PR reviews before merging</li>
        <li>Run terraform plan in CI pipeline</li>
        <li>Review plan output before approval</li>
        <li>Implement CODEOWNERS for critical paths</li>
        </ul>
        
        <h3>CI/CD Integration</h3>
        <p>Use tools like Terraform Cloud, GitLab CI, or GitHub Actions for automated planning and deployment. Implement approval gates before production changes.</p>
        
        <h3>Testing and Validation</h3>
        <p><strong>Tools:</strong></p>
        <ul>
        <li>terraform validate: Syntax checking</li>
        <li>terraform fmt: Code formatting</li>
        <li>Terratest: Go-based testing framework</li>
        <li>tflint: Linting for best practices</li>
        </ul>
        
        <h3>Multi-Environment Strategy</h3>
        <p>Use workspaces or separate stacks for different environments. Keep DRY principle by using modules and variables. Use tfvars files for environment-specific values.</p>
        
        <h3>Conclusion</h3>
        <p>Implementing these Terraform best practices will help your organization build scalable, maintainable, and secure infrastructure. Start with solid foundations and iterate based on team experience.</p>
        ''',
        'technologies': ['Terraform', 'Infrastructure as Code', 'AWS', 'Azure', 'GCP'],
    },
    5: {
        'title': 'Zero-Downtime Deployments: Strategies and Tools Every DevOps Engineer Should Know',
        'date': _blog_dates[4],
        'author': 'Sam',
        'category': 'Deployment',
        'image': '/static/images/blog/img5.png',
        'excerpt': 'Comprehensive guide to implementing zero-downtime deployment strategies in production environments.',
        'content': '''
        <h3>The Challenge of Zero-Downtime Deployments</h3>
        <p>In modern business, every minute of downtime costs money and damages customer trust. Zero-downtime deployments are no longer optional—they're a requirement. Let's explore the strategies and tools that make this possible.</p>
        
        <h3>Deployment Strategies</h3>
        <p><strong>1. Blue-Green Deployment</strong><br/>
        Maintain two identical production environments. Deploy new version to inactive environment, test, then switch traffic. Instant rollback available by switching back.</p>
        
        <p><strong>2. Canary Deployments</strong><br/>
        Gradually roll out new version to small percentage of users (e.g., 5%). Monitor metrics closely. If successful, increase percentage incrementally.</p>
        
        <p><strong>3. Rolling Deployments</strong><br/>
        Gradually replace old instances with new ones. Works particularly well with container orchestration like Kubernetes. Maintains service availability throughout.</p>
        
        <p><strong>4. Shadow Traffic</strong><br/>
        Route real production traffic to new version in parallel. Capture and compare responses for validation before switching traffic.</p>
        
        <h3>Kubernetes Native Approach</h3>
        <p><strong>Deployment Strategies in Kubernetes:</strong></p>
        <pre>
apiVersion: apps/v1
kind: Deployment
metadata:
  name: my-app
spec:
  replicas: 3
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1
      maxUnavailable: 0
  template:
    spec:
      containers:
      - name: app
        image: myapp:v2
        livenessProbe:
          httpGet:
            path: /health
            port: 8080
        readinessProbe:
          httpGet:
            path: /ready
            port: 8080
        </pre>
        
        <h3>Database Migrations</h3>
        <p><strong>Challenges:</strong> Database changes can cause conflicts during deployment.</p>
        
        <p><strong>Solutions:</strong></p>
        <ul>
        <li>Backward-compatible schema changes</li>
        <li>Feature flags for new columns/tables</li>
        <li>Separate deployment phases for schema and application code</li>
        <li>Use migration tools like Flyway or Liquibase</li>
        </ul>
        
        <h3>Health Checks and Readiness Probes</h3>
        <p>Proper health checks are critical for zero-downtime deployments.</p>
        
        <p><strong>Liveness Probe:</strong> Indicates if service is running. Kubernetes restarts unhealthy containers.</p>
        
        <p><strong>Readiness Probe:</strong> Indicates if service is ready for traffic. Kubernetes adds/removes from load balancer based on readiness.</p>
        
        <h3>Load Balancer Configuration</h3>
        <p>Configure connection draining/graceful shutdown timeouts. Ensure load balancer respects health checks. Implement gradual traffic switch during deployments.</p>
        
        <h3>Monitoring and Rollback</h3>
        <p>Monitor error rates, latency, and resource usage during deployment. Implement automatic rollback on critical metric degradation. Keep previous version available for quick rollback.</p>
        
        <h3>Tools for Zero-Downtime Deployments</h3>
        <ul>
        <li><strong>Kubernetes:</strong> Native rolling updates and readiness probes</li>
        <li><strong>ArgoCD:</strong> GitOps-based continuous deployment</li>
        <li><strong>Istio:</strong> Advanced traffic management and canary deployments</li>
        <li><strong>AWS CodeDeploy:</strong> AWS-native deployment service</li>
        <li><strong>Spinnaker:</strong> Open-source continuous deployment platform</li>
        </ul>
        
        <h3>Conclusion</h3>
        <p>Zero-downtime deployments require careful planning and the right tooling. Start with blue-green or rolling deployments, implement robust health checks, and progressively adopt more sophisticated strategies like canary deployments as you gain experience.</p>
        ''',
        'technologies': ['Deployment', 'Kubernetes', 'Zero-Downtime', 'CI/CD'],
    },
    6: {
        'title': 'Container Registry Management: Harbor vs Docker Registry vs Artifactory',
        'date': _blog_dates[5],
        'author': 'Sam',
        'category': 'Containers',
        'image': '/static/images/blog/img6.png',
        'excerpt': 'Comparing container registry solutions to help you choose the right one for your organization.',
        'content': '''
        <h3>Why Container Registry Matters</h3>
        <p>Container registries are the foundation of container-based deployments. They store, manage, and distribute container images across your infrastructure. Choosing the right registry impacts security, performance, and operational complexity.</p>
        
        <h3>Overview of Container Registries</h3>
        <p><strong>Docker Registry (open-source):</strong></p>
        <ul>
        <li>Basic, distribution-focused registry</li>
        <li>Minimal features</li>
        <li>Good for simple deployments</li>
        <li>No built-in UI or ACL system</li>
        </ul>
        
        <p><strong>Harbor (CNCF project):</strong></p>
        <ul>
        <li>Enterprise-grade registry with security focus</li>
        <li>Image scanning and vulnerability detection</li>
        <li>RBAC and fine-grained access control</li>
        <li>Replication across registries</li>
        <li>Built-in web UI</li>
        <li>Excellent for private enterprise deployments</li>
        </ul>
        
        <p><strong>JFrog Artifactory:</strong></p>
        <ul>
        <li>Universal artifact repository</li>
        <li>Supports Docker, Maven, npm, Helm, etc.</li>
        <li>Advanced security scanning</li>
        <li>High availability and disaster recovery</li>
        <li>Complex pricing for larger deployments</li>
        </ul>
        
        <h3>Feature Comparison</h3>
        <table>
        <tr>
        <th>Feature</th>
        <th>Docker Registry</th>
        <th>Harbor</th>
        <th>Artifactory</th>
        </tr>
        <tr>
        <td>Web UI</td>
        <td>No</td>
        <td>Yes</td>
        <td>Yes</td>
        </tr>
        <tr>
        <td>Security Scanning</td>
        <td>No</td>
        <td>Yes (Trivy)</td>
        <td>Yes</td>
        </tr>
        <tr>
        <td>RBAC</td>
        <td>Limited</td>
        <td>Excellent</td>
        <td>Excellent</td>
        </tr>
        <tr>
        <td>Replication</td>
        <td>No</td>
        <td>Yes</td>
        <td>Yes</td>
        </tr>
        <tr>
        <td>Multi-artifact Support</td>
        <td>No</td>
        <td>No</td>
        <td>Yes</td>
        </tr>
        <tr>
        <td>Cost</td>
        <td>Free</td>
        <td>Free (Open Source)</td>
        <td>Commercial</td>
        </tr>
        </table>
        
        <h3>Security Considerations</h3>
        <p><strong>Image Scanning:</strong> Detect vulnerabilities in images before deployment. Harbor includes Trivy scanner; Artifactory uses Xray.</p>
        
        <p><strong>Access Control:</strong> Implement role-based access control. Limit push access to CI/CD systems and pull access to deployment systems.</p>
        
        <p><strong>Image Signing:</strong> Use Docker Content Trust or Notary to sign images. Verify signatures during deployment.</p>
        
        <h3>Implementation Recommendations</h3>
        <p><strong>For Small Teams/Single Cloud:</strong> Start with Docker Registry or cloud provider's native registry (ECR, ACR, GCR).</p>
        
        <p><strong>For Enterprise with Multiple Teams:</strong> Harbor provides excellent security and multi-repository management. Open-source and free.</p>
        
        <p><strong>For Complex Artifact Ecosystems:</strong> Artifactory if you need to manage Docker, Maven, npm, Helm, and other artifact types centrally.</p>
        
        <h3>Best Practices</h3>
        <ul>
        <li>Always use private registries in production</li>
        <li>Implement image scanning in CI pipeline</li>
        <li>Use image pull policies (Always, IfNotPresent)</li>
        <li>Implement garbage collection for unused images</li>
        <li>Use image tagging strategy (semantic versioning)</li>
        <li>Replicate images across geographic regions</li>
        </ul>
        
        <h3>Conclusion</h3>
        <p>The right container registry depends on your organization's size, complexity, and requirements. Harbor is often the sweet spot for enterprise deployments, offering enterprise features without commercial licensing costs.</p>
        ''',
        'technologies': ['Container Registry', 'Harbor', 'Docker', 'Security'],
    },
    7: {
        'title': 'Disaster Recovery and Business Continuity: Building Resilient Cloud Infrastructure',
        'date': _blog_dates[6],
        'author': 'Sam',
        'category': 'Infrastructure',
        'image': '/static/images/blog/img5.png',
        'excerpt': 'Strategies and implementations for building resilient infrastructure with effective disaster recovery.',
        'content': '''
        <h3>Understanding Disaster Recovery and Business Continuity</h3>
        <p><strong>RTO (Recovery Time Objective):</strong> Maximum acceptable downtime. How quickly must services be restored?</p>
        
        <p><strong>RPO (Recovery Point Objective):</strong> Maximum acceptable data loss. How much recent data can you afford to lose?</p>
        
        <p>Effective disaster recovery balances cost, complexity, and recovery objectives.</p>
        
        <h3>DR Strategies and Costs</h3>
        
        <p><strong>1. Backup and Restore (High RPO, High RTO)</strong><br/>
        Most basic approach. Take regular backups, restore when needed.<br/>
        RTO: Hours, RPO: Hours<br/>
        Cost: Low</p>
        
        <p><strong>2. Pilot Light (Medium RPO, High RTO)</strong><br/>
        Core systems run in secondary region, but minimal resources.<br/>
        RTO: 30-60 minutes, RPO: 15-30 minutes<br/>
        Cost: Medium</p>
        
        <p><strong>3. Warm Standby (Low RPO, Medium RTO)</strong><br/>
        Scaled-down copy running continuously. Scale up when needed.<br/>
        RTO: 10 minutes, RPO: Few minutes<br/>
        Cost: Medium-High</p>
        
        <p><strong>4. Hot Standby / Multi-Region (Lowest RPO, Lowest RTO)</strong><br/>
        Full copy running with traffic split. Instant failover.<br/>
        RTO: Seconds, RPO: Seconds<br/>
        Cost: Highest</p>
        
        <h3>Database Backup Strategies</h3>
        
        <p><strong>Point-in-Time Recovery:</strong></p>
        <ul>
        <li>Full backups + transaction logs</li>
        <li>Enables recovery to any point in time</li>
        <li>Higher storage requirements</li>
        </ul>
        
        <p><strong>Replication:</strong></p>
        <ul>
        <li>Database replication to standby server(s)</li>
        <li>Synchronous for zero data loss, asynchronous for performance</li>
        <li>Automatic failover with proper setup</li>
        </ul>
        
        <h3>Application-Level Considerations</h3>
        
        <p><strong>Stateless Applications:</strong> Easiest to recover. Deploy new instances, point to recovered data.</p>
        
        <p><strong>Stateful Applications:</strong> More complex. Consider:</p>
        <ul>
        <li>Session persistence</li>
        <li>Cache invalidation</li>
        <li>Message queue durability</li>
        </ul>
        
        <h3>Implementing Multi-Region Architecture</h3>
        
        <p><strong>Key Components:</strong></p>
        <ul>
        <li>Active-Active: Both regions serve traffic (immediate failover)</li>
        <li>Global DNS with health checks</li>
        <li>Replicated data across regions</li>
        <li>Independent infrastructure in each region</li>
        </ul>
        
        <h3>Testing Your DR Plan</h3>
        
        <p><strong>Regular DR Drills:</strong></p>
        <ul>
        <li>Schedule quarterly DR tests</li>
        <li>Document recovery steps and timing</li>
        <li>Test actual failover processes</li>
        <li>Train team on disaster scenarios</li>
        </ul>
        
        <h3>Kubernetes-Specific DR</h3>
        
        <p><strong>Tools:</strong></p>
        <ul>
        <li>Velero: Kubernetes backup and restore</li>
        <li>Kasten K10: Enterprise Kubernetes data protection</li>
        <li>cluster-api: Multi-cluster management</li>
        </ul>
        
        <h3>Compliance and Documentation</h3>
        
        <ul>
        <li>Document RTO/RPO for each service</li>
        <li>Maintain recovery runbooks</li>
        <li>Track infrastructure dependencies</li>
        <li>Ensure compliance with regulatory requirements</li>
        </ul>
        
        <h3>Cost Optimization in DR</h3>
        
        <ul>
        <li>Use on-demand instances for warm standby</li>
        <li>Implement cost-effective backup storage</li>
        <li>Use spot instances for non-critical failover resources</li>
        <li>Automated scaling based on load</li>
        </ul>
        
        <h3>Conclusion</h3>
        <p>Disaster recovery is not a one-time implementation but an ongoing process. Start with clear RTO/RPO objectives, choose appropriate strategies, implement with infrastructure as code, and test regularly. The goal is business continuity—ensuring your services remain available even during adverse events.</p>
        ''',
        'technologies': ['Disaster Recovery', 'AWS', 'Kubernetes', 'Business Continuity'],
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
    return render(request, 'leumas/index.html')


def about(request):
    return render(request, 'leumas/index.html', {'scroll_to': 'about'})


def works(request):
    return render(request, 'leumas/index.html', {'scroll_to': 'project-gallery'})


def services(request):
    return render(request, 'leumas/index.html', {'scroll_to': 'service'})


def blog(request):
    context = {'all_blogs': BLOG_POSTS, 'scroll_to': 'blog'}
    return render(request, 'leumas/index.html', context)


def blogs(request):
    context = {'all_blogs': BLOG_POSTS, 'scroll_to': 'blog'}
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
    blog = BLOG_POSTS.get(blog_id)
    if not blog:
        blogs_list = list(BLOG_POSTS.values())
        blog = blogs_list[0] if blogs_list else None
    
    context = {
        'blog': blog,
        'blog_id': blog_id,
        'all_blogs': BLOG_POSTS,
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