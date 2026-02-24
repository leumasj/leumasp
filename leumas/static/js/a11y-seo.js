/* Phase 4.3: Accessibility & SEO Enhancements */

class AccessibilitySEO {
    constructor() {
        this.config = {
            enableAriaLabels: true,
            enableKeyboardNavigation: true,
            enableSkipLinks: true,
            enableFocusVisible: true,
            enableHeadingHierarchy: true
        };
    }

    /**
     * Add skip to main content link
     */
    addSkipLinks() {
        const skipLink = document.createElement('a');
        skipLink.href = '#main-content';
        skipLink.className = 'skip-link';
        skipLink.textContent = 'Skip to main content';
        skipLink.style.cssText = `
            position: absolute;
            top: -40px;
            left: 0;
            background: #000;
            color: #fff;
            padding: 8px;
            z-index: 100;
            text-decoration: none;
            border-radius: 0 0 4px 0;
        `;

        skipLink.addEventListener('focus', () => {
            skipLink.style.top = '0';
        });

        skipLink.addEventListener('blur', () => {
            skipLink.style.top = '-40px';
        });

        document.body.insertBefore(skipLink, document.body.firstChild);
    }

    /**
     * Enhance focus visibility
     */
    enableFocusVisible() {
        const style = document.createElement('style');
        style.textContent = `
            *:focus-visible {
                outline: 2px solid #4285f4;
                outline-offset: 2px;
                border-radius: 4px;
            }

            button:focus-visible,
            a:focus-visible,
            input:focus-visible,
            select:focus-visible,
            textarea:focus-visible {
                box-shadow: 0 0 0 3px rgba(66, 133, 244, 0.1);
            }

            .dark-mode *:focus-visible {
                outline-color: #667eea;
            }
        `;
        document.head.appendChild(style);
    }

    /**
     * Add ARIA labels to interactive elements
     */
    addAriaLabels() {
        // Add aria-label to icon buttons without text
        document.querySelectorAll('button:not([aria-label])').forEach(btn => {
            if (!btn.textContent.trim() && btn.querySelector('i, svg')) {
                const icon = btn.querySelector('i, svg');
                const iconClass = icon.classList ? Array.from(icon.classList).join(' ') : '';
                
                if (iconClass.includes('heart')) btn.setAttribute('aria-label', 'Toggle favorite');
                else if (iconClass.includes('search')) btn.setAttribute('aria-label', 'Search');
                else if (iconClass.includes('menu') || iconClass.includes('bars')) btn.setAttribute('aria-label', 'Toggle menu');
                else if (iconClass.includes('close') || iconClass.includes('times')) btn.setAttribute('aria-label', 'Close');
                else if (iconClass.includes('arrow')) btn.setAttribute('aria-label', 'Navigation');
            }
        });

        // Add aria-label to form inputs without labels
        document.querySelectorAll('input:not([aria-label]):not([aria-labelledby])').forEach(input => {
            const label = document.querySelector(`label[for="${input.id}"]`);
            if (!label) {
                const placeholder = input.placeholder;
                if (placeholder) {
                    input.setAttribute('aria-label', placeholder);
                }
            }
        });
    }

    /**
     * Validate heading hierarchy
     */
    validateHeadingHierarchy() {
        const headings = document.querySelectorAll('h1, h2, h3, h4, h5, h6');
        const headingLevels = Array.from(headings).map(h => parseInt(h.tagName[1]));
        
        const warnings = [];
        for (let i = 1; i < headingLevels.length; i++) {
            const diff = headingLevels[i] - headingLevels[i - 1];
            if (diff > 1) {
                warnings.push({
                    message: `Heading hierarchy jump from H${headingLevels[i - 1]} to H${headingLevels[i]}`,
                    element: headings[i],
                    severity: 'warning'
                });
            }
        }

        if (warnings.length > 0) {
            console.warn('❗ Accessibility: Heading hierarchy issues found:', warnings);
        }

        return warnings;
    }

    /**
     * Add keyboard navigation support
     */
    enableKeyboardNavigation() {
        document.addEventListener('keydown', (e) => {
            // Escape to close modals
            if (e.key === 'Escape') {
                const modal = document.querySelector('.modal.show');
                if (modal) {
                    modal.classList.remove('show');
                    modal.style.display = 'none';
                }
            }

            // Tab to navigate skip links
            if (e.key === 'Tab') {
                document.body.classList.add('keyboard-nav');
            }
        });

        document.addEventListener('mousedown', () => {
            document.body.classList.remove('keyboard-nav');
        });
    }

    /**
     * Add Schema.org JSON-LD for rich snippets
     */
    addSchema(type, data) {
        const script = document.createElement('script');
        script.type = 'application/ld+json';
        
        const schemaData = this.buildSchema(type, data);
        script.textContent = JSON.stringify(schemaData);
        
        document.head.appendChild(script);
    }

    /**
     * Build schema markup based on type
     */
    buildSchema(type, data) {
        const baseSchema = {
            '@context': 'https://schema.org'
        };

        switch (type) {
            case 'person':
                return {
                    ...baseSchema,
                    '@type': 'Person',
                    'name': data.name,
                    'url': data.url,
                    'image': data.image,
                    'jobTitle': data.jobTitle,
                    'worksFor': data.company,
                    'sameAs': data.socialProfiles || []
                };

            case 'organization':
                return {
                    ...baseSchema,
                    '@type': 'Organization',
                    'name': data.name,
                    'url': data.url,
                    'logo': data.logo,
                    'sameAs': data.socialProfiles || []
                };

            case 'article':
                return {
                    ...baseSchema,
                    '@type': 'BlogPosting',
                    'headline': data.title,
                    'description': data.description,
                    'image': data.image,
                    'datePublished': data.datePublished,
                    'dateModified': data.dateModified,
                    'author': {
                        '@type': 'Person',
                        'name': data.author
                    }
                };

            case 'product':
                return {
                    ...baseSchema,
                    '@type': 'Product',
                    'name': data.name,
                    'description': data.description,
                    'image': data.image,
                    'offers': {
                        '@type': 'Offer',
                        'price': data.price,
                        'priceCurrency': data.currency || 'USD'
                    }
                };

            case 'breadcrumb':
                return {
                    ...baseSchema,
                    '@type': 'BreadcrumbList',
                    'itemListElement': data.items.map((item, index) => ({
                        '@type': 'ListItem',
                        'position': index + 1,
                        'name': item.name,
                        'item': item.url
                    }))
                };

            default:
                return baseSchema;
        }
    }

    /**
     * Add Open Graph meta tags
     */
    addOpenGraphTags(data) {
        const metaTags = {
            'og:title': data.title,
            'og:description': data.description,
            'og:image': data.image,
            'og:url': data.url,
            'og:type': data.type || 'website',
            'og:site_name': data.siteName,
            'twitter:card': data.twitterCard || 'summary_large_image',
            'twitter:title': data.title,
            'twitter:description': data.description,
            'twitter:image': data.image
        };

        Object.entries(metaTags).forEach(([property, content]) => {
            if (content) {
                let meta = document.querySelector(`meta[property="${property}"]`) || 
                          document.querySelector(`meta[name="${property}"]`);
                
                if (!meta) {
                    meta = document.createElement('meta');
                    const isProperty = property.startsWith('og:');
                    meta.setAttribute(isProperty ? 'property' : 'name', property);
                    document.head.appendChild(meta);
                }
                
                meta.setAttribute('content', content);
            }
        });
    }

    /**
     * Optimize images for accessibility
     */
    optimizeImageAccessibility() {
        document.querySelectorAll('img:not([alt])').forEach(img => {
            const filename = img.src.split('/').pop() || 'Image';
            img.setAttribute('alt', filename.replace(/[-_./]/g, ' '));
        });

        document.querySelectorAll('img[alt=""]').forEach(img => {
            img.setAttribute('role', 'presentation');
        });
    }

    /**
     * Add color contrast checker
     */
    checkColorContrast() {
        const issues = [];

        document.querySelectorAll('*').forEach(el => {
            if (el.offsetParent === null) return; // Skip hidden elements

            const bgColor = window.getComputedStyle(el).backgroundColor;
            const fgColor = window.getComputedStyle(el).color;

            // Basic contrast ratio calculation
            const ratio = this.calculateContrastRatio(bgColor, fgColor);
            
            if (ratio < 4.5 && el.textContent.length > 0) {
                issues.push({
                    element: el,
                    contrastRatio: ratio.toFixed(2),
                    wcagLevel: ratio >= 4.5 ? 'AA' : ratio >= 3.0 ? 'AAA' : 'Failed'
                });
            }
        });

        if (issues.length > 0) {
            console.warn('⚠️ Accessibility: Color contrast issues found:', issues);
        }

        return issues;
    }

    /**
     * Calculate relative luminance
     */
    getLuminance(r, g, b) {
        const [rs, gs, bs] = [r, g, b].map(x => {
            x = x / 255;
            return x <= 0.03928 ? x / 12.92 : Math.pow((x + 0.055) / 1.055, 2.4);
        });
        return 0.2126 * rs + 0.7152 * gs + 0.0722 * bs;
    }

    /**
     * Calculate contrast ratio
     */
    calculateContrastRatio(bgColor, fgColor) {
        const getBgRGB = (color) => {
            if (color === 'rgba(0, 0, 0, 0)') return [255, 255, 255];
            const match = color.match(/\d+/g);
            return match ? [parseInt(match[0]), parseInt(match[1]), parseInt(match[2])] : [255, 255, 255];
        };

        const getFgRGB = (color) => {
            const match = color.match(/\d+/g);
            return match ? [parseInt(match[0]), parseInt(match[1]), parseInt(match[2])] : [0, 0, 0];
        };

        const [bgR, bgG, bgB] = getBgRGB(bgColor);
        const [fgR, fgG, fgB] = getFgRGB(fgColor);

        const bgLum = this.getLuminance(bgR, bgG, bgB);
        const fgLum = this.getLuminance(fgR, fgG, fgB);

        const lighter = Math.max(bgLum, fgLum);
        const darker = Math.min(bgLum, fgLum);

        return (lighter + 0.05) / (darker + 0.05);
    }

    /**
     * Initialize all accessibility features
     */
    init() {
        // Enable features based on config
        if (this.config.enableSkipLinks) this.addSkipLinks();
        if (this.config.enableFocusVisible) this.enableFocusVisible();
        if (this.config.enableAriaLabels) this.addAriaLabels();
        if (this.config.enableKeyboardNavigation) this.enableKeyboardNavigation();

        // Validation and optimization
        this.optimizeImageAccessibility();
        if (this.config.enableHeadingHierarchy) this.validateHeadingHierarchy();
        
        // Check contrast (but don't break on issues)
        try {
            this.checkColorContrast();
        } catch (e) {
            console.debug('Color contrast check skipped:', e);
        }

        console.log('✓ Accessibility & SEO enhancements initialized');
        window.a11y = this;
    }
}

// Initialize Accessibility & SEO when DOM ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
        const a11y = new AccessibilitySEO();
        a11y.init();
    });
} else {
    const a11y = new AccessibilitySEO();
    a11y.init();
}
