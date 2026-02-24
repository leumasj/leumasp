/* Phase 4.1: Performance Optimization */

class PerformanceOptimizer {
    constructor() {
        this.lazyImages = [];
        this.observer = null;
        this.performanceMetrics = {
            startTime: performance.now(),
            images: {
                total: 0,
                loaded: 0
            },
            requests: {
                pending: 0,
                completed: 0
            }
        };
        this.moduleCache = new Map();
        this.cacheConfig = {
            imageCache: 'image-cache-v1',
            dataCache: 'data-cache-v1',
            ttl: 24 * 60 * 60 * 1000 // 24 hours
        };
    }

    /**
     * Initialize lazy loading system
     */
    initLazyLoading() {
        // Support for native lazy loading
        if ('loading' in HTMLImageElement.prototype) {
            document.querySelectorAll('img[data-lazy]').forEach(img => {
                img.src = img.dataset.src;
                img.removeAttribute('data-lazy');
                img.classList.add('loaded');
            });
        } else {
            // Fallback to Intersection Observer
            this.setupIntersectionObserver();
        }
    }

    /**
     * Setup Intersection Observer for lazy loading
     */
    setupIntersectionObserver() {
        const options = {
            root: null,
            rootMargin: '50px',
            threshold: 0.01
        };

        this.observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    this.loadImage(entry.target);
                }
            });
        }, options);

        document.querySelectorAll('img[data-lazy]').forEach(img => {
            this.observer.observe(img);
            this.performanceMetrics.images.total++;
        });

        // Lazy load other elements
        document.querySelectorAll('[data-lazy-load]').forEach(el => {
            this.observer.observe(el);
        });
    }

    /**
     * Load image and track metrics
     */
    loadImage(img) {
        if (!img.dataset.src) return;

        const src = img.dataset.src;
        
        // Add loading class
        img.classList.add('loading');
        img.style.opacity = '0';

        // Create new image to preload
        const newImg = new Image();
        newImg.onload = () => {
            img.src = src;
            img.classList.remove('loading');
            img.classList.add('loaded');
            img.style.opacity = '1';
            img.removeAttribute('data-lazy');
            
            this.performanceMetrics.images.loaded++;
            
            // Cache the image
            this.cacheImage(src);
            
            // Stop observing this image
            if (this.observer) {
                this.observer.unobserve(img);
            }
        };

        newImg.onerror = () => {
            img.classList.remove('loading');
            img.classList.add('error');
            console.warn(`Failed to load image: ${src}`);
        };

        newImg.src = src;
    }

    /**
     * Cache image in browser cache storage
     */
    cacheImage(url) {
        if (!('caches' in window)) return;

        caches.open(this.cacheConfig.imageCache).then(cache => {
            fetch(url, { method: 'HEAD' })
                .then(() => cache.add(url))
                .catch(err => console.debug('Image caching skipped:', err));
        });
    }

    /**
     * Dynamic module loading (Code Splitting)
     */
    async loadModule(modulePath, moduleName) {
        if (this.moduleCache.has(moduleName)) {
            return this.moduleCache.get(moduleName);
        }

        try {
            this.performanceMetrics.requests.pending++;
            const response = await fetch(modulePath);
            
            if (!response.ok) throw new Error(`HTTP ${response.status}`);
            
            const module = await response.json();
            this.moduleCache.set(moduleName, module);
            
            this.performanceMetrics.requests.completed++;
            this.performanceMetrics.requests.pending--;
            
            return module;
        } catch (error) {
            this.performanceMetrics.requests.pending--;
            console.error(`Failed to load module ${moduleName}:`, error);
            return null;
        }
    }

    /**
     * Prefetch resources
     */
    prefetchResources(urls) {
        urls.forEach(url => {
            const link = document.createElement('link');
            link.rel = 'prefetch';
            link.href = url;
            document.head.appendChild(link);
        });
    }

    /**
     * Preload critical resources
     */
    preloadResources(urls) {
        urls.forEach(url => {
            const link = document.createElement('link');
            link.rel = 'preload';
            link.href = url;
            
            // Determine resource type
            if (url.includes('.woff') || url.includes('.ttf')) {
                link.as = 'font';
                link.crossOrigin = 'anonymous';
            } else if (url.includes('.css')) {
                link.as = 'style';
            } else if (url.includes('.js')) {
                link.as = 'script';
            }
            
            document.head.appendChild(link);
        });
    }

    /**
     * Collect Core Web Vitals metrics
     */
    collectWebVitals() {
        const metrics = {
            fcp: null,      // First Contentful Paint
            lcp: null,      // Largest Contentful Paint
            fid: null,      // First Input Delay
            cls: null,      // Cumulative Layout Shift
            ttfb: null      // Time to First Byte
        };

        // Measure FCP & LCP
        if ('PerformanceObserver' in window) {
            try {
                const observer = new PerformanceObserver((list) => {
                    for (const entry of list.getEntries()) {
                        if (entry.name === 'first-contentful-paint') {
                            metrics.fcp = entry.startTime;
                        }
                        if (entry.entryType === 'largest-contentful-paint') {
                            metrics.lcp = entry.renderTime || entry.loadTime;
                        }
                    }
                });
                observer.observe({ entryTypes: ['paint', 'largest-contentful-paint'] });
            } catch (e) {
                console.debug('PerformanceObserver not fully supported');
            }
        }

        // Measure TTFB
        const navTiming = performance.getEntriesByType('navigation')[0];
        if (navTiming) {
            metrics.ttfb = navTiming.responseStart - navTiming.fetchStart;
        }

        return metrics;
    }

    /**
     * Display performance metrics
     */
    displayPerformanceMetrics() {
        const metrics = this.collectWebVitals();
        const loadTime = performance.now() - this.performanceMetrics.startTime;
        
        const summary = {
            pageLoadTime: loadTime.toFixed(2),
            imagesLoaded: `${this.performanceMetrics.images.loaded}/${this.performanceMetrics.images.total}`,
            requestsCompleted: this.performanceMetrics.requests.completed,
            webVitals: metrics
        };

        // Store in sessionStorage for debugging
        sessionStorage.setItem('perfMetrics', JSON.stringify(summary));

        // Log to console
        console.group('🚀 Performance Metrics');
        console.log(`Page Load Time: ${summary.pageLoadTime}ms`);
        console.log(`Images Loaded: ${summary.imagesLoaded}`);
        console.log(`Requests: ${summary.requestsCompleted}`);
        console.log('Web Vitals:', summary.webVitals);
        console.groupEnd();

        return summary;
    }

    /**
     * Display performance badge
     */
    showPerformanceBadge() {
        const metrics = this.collectWebVitals();
        const loadTime = performance.now() - this.performanceMetrics.startTime;

        let status = 'good';
        let message = `⚡ Fast (${loadTime.toFixed(0)}ms)`;

        if (loadTime > 3000) {
            status = 'critical';
            message = `⚠️ Slow (${loadTime.toFixed(0)}ms)`;
        } else if (loadTime > 2000) {
            status = 'warning';
            message = `⏱️ Fair (${loadTime.toFixed(0)}ms)`;
        }

        const badge = document.createElement('div');
        badge.className = `perf-badge ${status}`;
        badge.textContent = message;
        badge.title = 'Page performance indicator';
        
        document.body.appendChild(badge);

        // Auto-remove after 5 seconds
        setTimeout(() => badge.remove(), 5000);
    }

    /**
     * Optimize images with responsive srcset
     */
    optimizeResponsiveImages() {
        document.querySelectorAll('img[data-srcset]').forEach(img => {
            img.srcset = img.dataset.srcset;
            img.sizes = img.dataset.sizes || '(max-width: 768px) 100vw, 50vw';
        });
    }

    /**
     * Defer non-critical styles
     */
    deferNonCriticalStyles() {
        document.querySelectorAll('link[data-defer]').forEach(link => {
            if (link.rel === 'stylesheet') {
                link.media = 'print';
                link.onload = function() {
                    this.media = 'all';
                };
            }
        });
    }

    /**
     * Setup service worker for offline support
     */
    registerServiceWorker() {
        if ('serviceWorker' in navigator) {
            navigator.serviceWorker.register('/static/js/service-worker.js')
                .then(registration => {
                    console.log('✓ Service Worker registered:', registration.scope);
                })
                .catch(error => {
                    console.debug('Service Worker registration failed:', error);
                });
        }
    }

    /**
     * Monitor network activity
     */
    monitorNetworkActivity() {
        const observer = document.querySelector('.network-indicator');
        if (!observer) return;

        // Monitor fetch requests
        const originalFetch = window.fetch;
        window.fetch = function(...args) {
            observer.classList.add('active');
            return originalFetch.apply(this, args)
                .finally(() => {
                    setTimeout(() => {
                        observer.classList.remove('active');
                    }, 500);
                });
        };
    }

    /**
     * Initialize Intersection Observer for fade-in animations
     */
    observeFadeInElements() {
        const observerOptions = {
            threshold: 0.1,
            rootMargin: '0px 0px -50px 0px'
        };

        const fadeObserver = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('visible');
                    fadeObserver.unobserve(entry.target);
                }
            });
        }, observerOptions);

        // Observe all fade-in elements with stagger
        document.querySelectorAll('.fade-in-staggered').forEach((el, index) => {
            el.style.transitionDelay = `${index * 0.1}s`;
            fadeObserver.observe(el);
        });

        // Observe regular fade-in elements
        document.querySelectorAll('.fade-in-on-scroll').forEach(el => {
            fadeObserver.observe(el);
        });
    }

    /**
     * Batch DOM operations
     */
    async batchDOMUpdates(updates) {
        // Collect all updates and apply them together
        requestAnimationFrame(() => {
            updates.forEach(update => update());
        });
    }

    /**
     * Compress and optimize JavaScript
     */
    bundleize() {
        // Remove console logs in production
        if (window.location.hostname !== 'localhost') {
            console.log = function() {};
            console.warn = function() {};
        }
    }

    /**
     * Initialize all optimization features
     */
    init() {
        // Core optimizations
        this.initLazyLoading();
        this.optimizeResponsiveImages();
        this.deferNonCriticalStyles();
        this.observeFadeInElements();
        this.bundleize();

        // Performance monitoring
        window.addEventListener('load', () => {
            setTimeout(() => {
                this.displayPerformanceMetrics();
                this.showPerformanceBadge();
            }, 500);
        });

        // Network monitoring
        this.monitorNetworkActivity();

        // Attempt service worker registration
        this.registerServiceWorker();

        // Export for external access
        window.perfOptimizer = this;

        console.log('✓ Performance Optimizer initialized');
    }
}

// Initialize when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
        const optimizer = new PerformanceOptimizer();
        optimizer.init();
    });
} else {
    const optimizer = new PerformanceOptimizer();
    optimizer.init();
}
