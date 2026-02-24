/* Phase 4.4: Sentry Error Tracking Integration */

class SentryErrorTracker {
    constructor(dsn, options = {}) {
        this.dsn = dsn;
        this.options = {
            environment: options.environment || (window.location.hostname === 'localhost' ? 'development' : 'production'),
            tracesSampleRate: options.tracesSampleRate || 0.1,
            maxBreadcrumbs: options.maxBreadcrumbs || 100,
            attachStacktrace: options.attachStacktrace !== false,
            beforeSend: options.beforeSend || this.defaultBeforeSend.bind(this),
            ignoreErrors: options.ignoreErrors || []
        };
        
        this.initialized = false;
        this.breadcrumbs = [];
    }

    /**
     * Initialize Sentry tracking
     */
    async init() {
        if (!this.dsn) {
            console.debug('Sentry DSN not provided - error tracking disabled');
            return;
        }

        try {
            // Load Sentry SDK dynamically
            await this.loadSentrySDK();
            this.setupGlobalErrorHandlers();
            this.setupPerformanceMonitoring();
            this.setupBreadcrumbs();
            
            this.initialized = true;
            console.log('✓ Sentry error tracking initialized');
        } catch (error) {
            console.error('Failed to initialize Sentry:', error);
        }
    }

    /**
     * Load Sentry SDK from CDN
     */
    loadSentrySDK() {
        return new Promise((resolve, reject) => {
            // Load Sentry SDK
            const script = document.createElement('script');
            script.src = 'https://cdn.jsdelivr.net/npm/@sentry/tracing@latest/dist/bundle.min.js';
            script.onload = () => {
                // Initialize Sentry after SDK loads
                if (window.Sentry) {
                    window.Sentry.init({
                        dsn: this.dsn,
                        environment: this.options.environment,
                        tracesSampleRate: this.options.tracesSampleRate,
                        maxBreadcrumbs: this.options.maxBreadcrumbs,
                        attachStacktrace: this.options.attachStacktrace,
                        beforeSend: this.options.beforeSend,
                        integrations: [
                            new window.Sentry.Replay({
                                maskAllText: true,
                                blockAllMedia: true
                            })
                        ],
                        replaysSessionSampleRate: 0.1,
                        replaysOnErrorSampleRate: 1.0
                    });
                    resolve();
                } else {
                    reject(new Error('Sentry SDK failed to load'));
                }
            };
            script.onerror = () => reject(new Error('Failed to load Sentry SDK'));
            document.head.appendChild(script);
        });
    }

    /**
     * Setup global error handlers
     */
    setupGlobalErrorHandlers() {
        if (!window.Sentry) return;

        // Caught exceptions
        window.addEventListener('error', (event) => {
            window.Sentry.captureException(event.error || new Error(event.message), {
                contexts: {
                    error: {
                        filename: event.filename,
                        lineno: event.lineno,
                        colno: event.colno
                    }
                }
            });
        });

        // Unhandled promise rejections
        window.addEventListener('unhandledrejection', (event) => {
            window.Sentry.captureException(event.reason, {
                contexts: {
                    promise: {
                        type: 'unhandledRejection'
                    }
                }
            });
        });
    }

    /**
     * Setup performance monitoring
     */
    setupPerformanceMonitoring() {
        if (!window.Sentry || !('PerformanceObserver' in window)) return;

        try {
            // Track navigation timing
            window.addEventListener('load', () => {
                const navTiming = performance.getEntriesByType('navigation')[0];
                if (navTiming) {
                    window.Sentry.captureMessage('Page performance metrics', 'info', {
                        measurements: {
                            'ttfb': {
                                value: navTiming.responseStart - navTiming.fetchStart,
                                unit: 'millisecond'
                            },
                            'fcp': {
                                value: this.getFirstContentfulPaint(),
                                unit: 'millisecond'
                            },
                            'lcp': {
                                value: this.getLargestContentfulPaint(),
                                unit: 'millisecond'
                            }
                        }
                    });
                }
            });

            // First Contentful Paint
            const paintObserver = new PerformanceObserver((list) => {
                for (const entry of list.getEntries()) {
                    if (entry.name === 'first-contentful-paint') {
                        window.Sentry.captureMessage('FCP recorded', 'debug', {
                            measurements: {
                                'fcp': {
                                    value: entry.startTime,
                                    unit: 'millisecond'
                                }
                            }
                        });
                    }
                }
            });
            paintObserver.observe({ entryTypes: ['paint'] });
        } catch (error) {
            console.debug('Performance monitoring setup skipped:', error);
        }
    }

    /**
     * Setup breadcrumb tracking
     */
    setupBreadcrumbs() {
        if (!window.Sentry) return;

        // Track console messages
        const originalLog = console.log;
        const originalWarn = console.warn;
        const originalError = console.error;

        console.log = (...args) => {
            window.Sentry.addBreadcrumb({
                message: args.join(' '),
                level: 'info',
                category: 'console'
            });
            return originalLog.apply(console, args);
        };

        console.warn = (...args) => {
            window.Sentry.addBreadcrumb({
                message: args.join(' '),
                level: 'warning',
                category: 'console'
            });
            return originalWarn.apply(console, args);
        };

        console.error = (...args) => {
            window.Sentry.addBreadcrumb({
                message: args.join(' '),
                level: 'error',
                category: 'console'
            });
            return originalError.apply(console, args);
        };

        // Track user interactions
        document.addEventListener('click', (event) => {
            const target = event.target;
            let label = target.textContent?.slice(0, 100) || target.id || target.className;
            
            window.Sentry.addBreadcrumb({
                message: `Clicked: ${label}`,
                category: 'user-action',
                level: 'info',
                data: {
                    elementType: target.tagName,
                    elementId: target.id,
                    elementClass: target.className
                }
            });
        }, true);

        // Track page navigation
        window.addEventListener('popstate', () => {
            window.Sentry.addBreadcrumb({
                message: `Navigated to: ${window.location.pathname}`,
                category: 'navigation',
                level: 'info',
                data: {
                    url: window.location.href
                }
            });
        });

        // Track fetch requests
        const originalFetch = window.fetch;
        window.fetch = function(...args) {
            const [resource] = args;
            const url = typeof resource === 'string' ? resource : resource.url;
            
            const startTime = Date.now();

            return originalFetch.apply(this, args)
                .then((response) => {
                    const duration = Date.now() - startTime;

                    window.Sentry.addBreadcrumb({
                        message: `${response.status} ${url}`,
                        category: 'fetch',
                        level: response.status >= 400 ? 'warning' : 'info',
                        data: {
                            method: args[1]?.method || 'GET',
                            statusCode: response.status,
                            duration
                        }
                    });

                    return response;
                })
                .catch((error) => {
                    const duration = Date.now() - startTime;

                    window.Sentry.addBreadcrumb({
                        message: `Failed: ${url}`,
                        category: 'fetch',
                        level: 'error',
                        data: {
                            error: error.message,
                            duration
                        }
                    });

                    throw error;
                });
        };
    }

    /**
     * Get first contentful paint
     */
    getFirstContentfulPaint() {
        const metricEntries = performance.getEntriesByType('paint');
        const fcp = metricEntries.find(entry => entry.name === 'first-contentful-paint');
        return fcp ? fcp.startTime : 0;
    }

    /**
     * Get largest contentful paint
     */
    getLargestContentfulPaint() {
        try {
            const observer = new PerformanceObserver((list) => {
                const entries = list.getEntries();
                return entries[entries.length - 1]?.renderTime || entries[entries.length - 1]?.loadTime || 0;
            });
            observer.observe({ entryTypes: ['largest-contentful-paint'] });
            return 0;
        } catch (e) {
            return 0;
        }
    }

    /**
     * Capture exception
     */
    captureException(error, context = {}) {
        if (!window.Sentry) return;

        window.Sentry.captureException(error, {
            contexts: context
        });
    }

    /**
     * Capture message
     */
    captureMessage(message, level = 'info', context = {}) {
        if (!window.Sentry) return;

        window.Sentry.captureMessage(message, level, {
            contexts: context
        });
    }

    /**
     * Set user context
     */
    setUser(userId, email = null, username = null) {
        if (!window.Sentry) return;

        window.Sentry.setUser({
            id: userId,
            email: email,
            username: username
        });
    }

    /**
     * Set custom context
     */
    setContext(name, data) {
        if (!window.Sentry) return;

        window.Sentry.setContext(name, data);
    }

    /**
     * Set tags
     */
    setTag(name, value) {
        if (!window.Sentry) return;

        window.Sentry.setTag(name, value);
    }

    /**
     * Default beforeSend filter
     */
    defaultBeforeSend(event, hint) {
        // Ignore certain error types
        if (event.exception) {
            const error = hint.originalException;
            
            // Ignore network errors in production
            if (error?.message?.includes('Failed to fetch')) {
                return null;
            }

            // Ignore script errors from browser extensions
            if (event.stacktrace?.frames?.some(f => 
                f.filename?.includes('chrome-extension') || 
                f.filename?.includes('moz-extension')
            )) {
                return null;
            }
        }

        return event;
    }

    /**
     * Start a transaction for performance monitoring
     */
    startTransaction(name, op = 'http.request') {
        if (!window.Sentry) return null;

        return window.Sentry.startTransaction({
            name: name,
            op: op
        });
    }
}

// Initialize Sentry when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
        // Get Sentry DSN from data attribute or meta tag
        const sentryDSN = document.querySelector('[data-sentry-dsn]')?.dataset.sentryDsn || 
                         document.querySelector('meta[name="sentry-dsn"]')?.content;

        if (sentryDSN) {
            const tracker = new SentryErrorTracker(sentryDSN, {
                environment: document.querySelector('[data-environment]')?.dataset.environment || 'production',
                tracesSampleRate: 0.1
            });

            tracker.init().then(() => {
                window.sentryTracker = tracker;
            });
        }
    });
} else {
    // Get Sentry DSN from data attribute or meta tag
    const sentryDSN = document.querySelector('[data-sentry-dsn]')?.dataset.sentryDsn || 
                     document.querySelector('meta[name="sentry-dsn"]')?.content;

    if (sentryDSN) {
        const tracker = new SentryErrorTracker(sentryDSN);
        tracker.init().then(() => {
            window.sentryTracker = tracker;
        });
    }
}
