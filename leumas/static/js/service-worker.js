/* Phase 4.1: Service Worker for Offline Support & Caching */

const CACHE_NAME = 'leumas-v1';
const ASSETS_TO_CACHE = [
    '/',
    '/static/css/style.css',
    '/static/css/bootstrap.min.css',
    '/static/css/plugin.css',
    '/static/css/flaticon.css',
    '/static/js/jquery.js',
    '/static/js/bootstrap.min.js',
    '/static/js/main.js',
    '/static/js/performance-optimization.js',
    '/offline.html'
];

// Install event - cache assets
self.addEventListener('install', (event) => {
    console.log('[SW] Installing Service Worker...');
    event.waitUntil(
        caches.open(CACHE_NAME).then((cache) => {
            console.log('[SW] Caching app shell');
            return cache.addAll(ASSETS_TO_CACHE).catch(err => {
                console.log('[SW] Asset caching skipped (offline):', err);
            });
        })
    );
    self.skipWaiting();
});

// Activate event - cleanup old caches
self.addEventListener('activate', (event) => {
    console.log('[SW] Activating Service Worker...');
    event.waitUntil(
        caches.keys().then((cacheNames) => {
            return Promise.all(
                cacheNames.map((cacheName) => {
                    if (cacheName !== CACHE_NAME) {
                        console.log('[SW] Deleting old cache:', cacheName);
                        return caches.delete(cacheName);
                    }
                })
            );
        })
    );
    self.clients.claim();
});

// Fetch event - serve from cache, fallback to network
self.addEventListener('fetch', (event) => {
    const { request } = event;
    
    // Skip non-GET requests
    if (request.method !== 'GET') {
        return;
    }

    // Skip Chrome extensions and other non-http(s) requests
    if (!request.url.startsWith('http')) {
        return;
    }

    event.respondWith(
        caches.match(request).then((response) => {
            // Cache hit - return response
            if (response) {
                // Update cache in background
                updateCache(request);
                return response;
            }

            return fetch(request)
                .then((response) => {
                    // Don't cache non-successful responses
                    if (!response || response.status !== 200 || response.type === 'error') {
                        return response;
                    }

                    // Clone the response
                    const responseToCache = response.clone();

                    // Cache successful requests for images and API
                    if (request.destination === 'image' || request.url.includes('/api/')) {
                        caches.open(CACHE_NAME).then((cache) => {
                            cache.put(request, responseToCache);
                        });
                    }

                    return response;
                })
                .catch(() => {
                    // Offline - try cache
                    return caches.match(request).then((response) => {
                        if (response) {
                            return response;
                        }
                        // Return offline page for HTML requests
                        if (request.headers.get('accept').includes('text/html')) {
                            return caches.match('/offline.html');
                        }
                    });
                });
        })
    );
});

// Update cache in background
function updateCache(request) {
    return caches.open(CACHE_NAME).then((cache) => {
        return fetch(request)
            .then((response) => {
                if (response && response.status === 200) {
                    cache.put(request, response.clone());
                }
                return response;
            })
            .catch(err => {
                console.debug('[SW] Update failed:', err);
            });
    });
}

// Handle messages from clients
self.addEventListener('message', (event) => {
    if (event.data.type === 'SKIP_WAITING') {
        self.skipWaiting();
    }

    if (event.data.type === 'GET_CACHE_SIZE') {
        caches.open(CACHE_NAME).then((cache) => {
            cache.keys().then((requests) => {
                event.ports[0].postMessage({
                    type: 'CACHE_SIZE',
                    size: requests.length
                });
            });
        });
    }

    if (event.data.type === 'CLEAR_CACHE') {
        caches.delete(CACHE_NAME).then(() => {
            event.ports[0].postMessage({
                type: 'CACHE_CLEARED'
            });
        });
    }
});

console.log('[SW] Service Worker loaded');
