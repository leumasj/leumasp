/* Phase 4.2: Advanced Dev Tools & Debugging */

class DevTools {
    constructor() {
        this.isDevelopment = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1';
        this.errorLog = [];
        this.performanceLog = [];
        this.networkLog = [];
        this.isEnabled = this.isDevelopment;
    }

    /**
     * Enhanced console logging with levels
     */
    log(level, message, data = null) {
        const timestamp = new Date().toLocaleTimeString();
        const logEntry = { timestamp, level, message, data };

        switch (level) {
            case 'error':
                console.error(`[ERROR] ${message}`, data);
                this.errorLog.push(logEntry);
                this.captureErrorTrace();
                break;
            case 'warn':
                console.warn(`[WARN] ${message}`, data);
                break;
            case 'info':
                console.info(`[INFO] ${message}`, data);
                break;
            case 'debug':
                if (this.isDevelopment) {
                    console.debug(`[DEBUG] ${message}`, data);
                }
                break;
            case 'perf':
                console.log(`[PERF] ${message}`, data);
                this.performanceLog.push(logEntry);
                break;
        }
    }

    /**
     * Capture error traces
     */
    captureErrorTrace() {
        const stack = new Error().stack;
        if (stack) {
            console.log('Stack Trace:', stack);
        }
    }

    /**
     * Monitor error events globally
     */
    setupErrorMonitoring() {
        window.addEventListener('error', (event) => {
            this.log('error', 'Uncaught Error', {
                message: event.message,
                filename: event.filename,
                lineno: event.lineno,
                colno: event.colno,
                error: event.error
            });
        });

        window.addEventListener('unhandledrejection', (event) => {
            this.log('error', 'Unhandled Promise Rejection', {
                reason: event.reason
            });
        });
    }

    /**
     * Performance profiling
     */
    profileFunction(functionName, func) {
        return (...args) => {
            const start = performance.now();
            const result = func(...args);
            const end = performance.now();
            
            this.log('perf', `${functionName} took ${(end - start).toFixed(2)}ms`, {
                function: functionName,
                duration: (end - start).toFixed(2),
                args: args.length
            });

            return result;
        };
    }

    /**
     * Profile async function
     */
    profileAsyncFunction(functionName, asyncFunc) {
        return async (...args) => {
            const start = performance.now();
            const result = await asyncFunc(...args);
            const end = performance.now();
            
            this.log('perf', `${functionName} (async) took ${(end - start).toFixed(2)}ms`, {
                function: functionName,
                duration: (end - start).toFixed(2),
                args: args.length
            });

            return result;
        };
    }

    /**
     * Monitor fetch requests
     */
    logFetchRequest(url, options = {}) {
        const start = performance.now();
        
        return fetch(url, options)
            .then(response => {
                const end = performance.now();
                const duration = (end - start).toFixed(2);

                this.networkLog.push({
                    timestamp: new Date().toLocaleTimeString(),
                    method: options.method || 'GET',
                    url,
                    status: response.status,
                    duration
                });

                this.log('debug', `FETCH ${response.status}`, {
                    method: options.method || 'GET',
                    url,
                    duration: `${duration}ms`
                });

                return response;
            })
            .catch(error => {
                const end = performance.now();
                this.log('error', 'FETCH Error', {
                    url,
                    duration: `${(end - start).toFixed(2)}ms`,
                    error: error.message
                });
                throw error;
            });
    }

    /**
     * Memory usage monitor
     */
    getMemoryUsage() {
        if (!performance.memory) {
            return { available: 'Not available' };
        }

        return {
            usedJSHeapSize: `${(performance.memory.usedJSHeapSize / 1048576).toFixed(2)} MB`,
            totalJSHeapSize: `${(performance.memory.totalJSHeapSize / 1048576).toFixed(2)} MB`,
            jsHeapSizeLimit: `${(performance.memory.jsHeapSizeLimit / 1048576).toFixed(2)} MB`
        };
    }

    /**
     * Display debug panel
     */
    showDebugPanel() {
        const panel = document.createElement('div');
        panel.id = 'dev-debug-panel';
        panel.style.cssText = `
            position: fixed;
            bottom: 80px;
            right: 20px;
            width: 350px;
            max-height: 500px;
            background: rgba(0, 0, 0, 0.95);
            color: #00ff00;
            border: 2px solid #00ff00;
            border-radius: 8px;
            padding: 15px;
            font-family: 'Courier New', monospace;
            font-size: 12px;
            overflow-y: auto;
            z-index: 10001;
            box-shadow: 0 0 20px rgba(0, 255, 0, 0.3);
        `;

        const header = document.createElement('div');
        header.style.cssText = 'margin-bottom: 10px; font-weight: bold; border-bottom: 1px solid #00ff00; padding-bottom: 5px;';
        header.textContent = '⚙️ DEBUG PANEL (DEV ONLY)';

        const content = document.createElement('div');
        content.style.cssText = 'max-height: 400px; overflow-y: auto; font-size: 11px; line-height: 1.4;';

        // Memory info
        const memory = this.getMemoryUsage();
        content.innerHTML += `
            <div style="margin-bottom: 10px; color: #ffff00;">
                💾 Memory:<br>
                ${Object.entries(memory).map(([k, v]) => `${k}: ${v}`).join('<br>')}
            </div>
        `;

        // Error log
        if (this.errorLog.length > 0) {
            content.innerHTML += `
                <div style="margin-bottom: 10px; color: #ff6b6b;">
                    ❌ Errors (${this.errorLog.length}):<br>
                    ${this.errorLog.slice(-3).map(e => `[${e.timestamp}] ${e.message}`).join('<br>')}
                </div>
            `;
        }

        // Network log
        if (this.networkLog.length > 0) {
            content.innerHTML += `
                <div style="margin-bottom: 10px; color: #4dabf7;">
                    🌐 Network (${this.networkLog.length}):<br>
                    ${this.networkLog.slice(-3).map(n => `${n.method} ${n.status} ${n.duration}ms`).join('<br>')}
                </div>
            `;
        }

        // Performance log
        if (this.performanceLog.length > 0) {
            content.innerHTML += `
                <div style="margin-bottom: 10px; color: #a78bfa;">
                    ⚡ Performance:<br>
                    ${this.performanceLog.slice(-3).map(p => `${p.data.duration}ms - ${p.message}`).join('<br>')}
                </div>
            `;
        }

        const closeBtn = document.createElement('button');
        closeBtn.textContent = '✕ Close';
        closeBtn.style.cssText = `
            margin-top: 10px;
            background: #00ff00;
            color: #000;
            border: none;
            padding: 5px 10px;
            border-radius: 4px;
            cursor: pointer;
            font-family: monospace;
            width: 100%;
        `;
        closeBtn.onclick = () => panel.remove();

        panel.appendChild(header);
        panel.appendChild(content);
        panel.appendChild(closeBtn);
        document.body.appendChild(panel);
    }

    /**
     * Toggle debug panel with keyboard shortcut
     */
    enableDebugMode() {
        let debugKeyCount = 0;
        const debugSequence = 'debug';
        let inputSequence = '';

        document.addEventListener('keypress', (e) => {
            inputSequence += e.key;
            if (inputSequence.length > debugSequence.length) {
                inputSequence = inputSequence.slice(-debugSequence.length);
            }

            if (inputSequence === debugSequence) {
                const existing = document.getElementById('dev-debug-panel');
                if (existing) {
                    existing.remove();
                } else {
                    this.showDebugPanel();
                }
                inputSequence = '';
            }
        });

        console.log('%c🛠️ Dev Tools Enabled', 'color: #00ff00; font-size: 14px; font-weight: bold;');
        console.log('%cType "debug" to toggle debug panel', 'color: #ffff00; font-size: 12px;');
    }

    /**
     * Export logs
     */
    exportLogs() {
        const logs = {
            errors: this.errorLog,
            performance: this.performanceLog,
            network: this.networkLog,
            timestamp: new Date().toISOString()
        };

        const dataStr = JSON.stringify(logs, null, 2);
        const dataBlob = new Blob([dataStr], { type: 'application/json' });
        const url = URL.createObjectURL(dataBlob);
        const link = document.createElement('a');
        link.href = url;
        link.download = `debug-logs-${Date.now()}.json`;
        link.click();
        URL.revokeObjectURL(url);

        this.log('info', 'Logs exported', { filename: link.download });
    }

    /**
     * Get debug summary
     */
    getSummary() {
        return {
            environment: this.isDevelopment ? 'development' : 'production',
            errorCount: this.errorLog.length,
            networkRequests: this.networkLog.length,
            performanceMetrics: this.performanceLog.length,
            memory: this.getMemoryUsage()
        };
    }

    /**
     * Initialize dev tools
     */
    init() {
        if (!this.isEnabled) return;

        this.setupErrorMonitoring();
        this.enableDebugMode();

        // Expose to window for console access
        window.devTools = this;

        this.log('info', 'Dev Tools initialized', {
            environment: 'development',
            hostname: window.location.hostname
        });

        // Print startup info
        console.log('%c📊 Dev Tools Ready', 'color: #4dabf7; font-size: 14px; font-weight: bold;');
        console.table(this.getSummary());
    }
}

// Initialize Dev Tools in development
if (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1') {
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', () => {
            const devTools = new DevTools();
            devTools.init();
        });
    } else {
        const devTools = new DevTools();
        devTools.init();
    }
}
