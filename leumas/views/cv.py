from django.shortcuts import render
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.units import inch
from io import BytesIO

from leumas.views.data import SERVICES


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
