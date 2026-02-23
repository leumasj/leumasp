# Data constants for portfolio and services
# These are separated for easier maintenance and potential database migration

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
