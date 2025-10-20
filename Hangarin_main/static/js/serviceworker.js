const CACHE_NAME = 'hangarin-v1';
const URLS_TO_CACHE = [
  '/',
  '/static/manifest.json',   // correct path if it’s inside /static/
  '/offline/',
  '/static/css/styles.css',  // match your actual filename
  '/static/js/app.min.js',
];

// ✅ INSTALL: Cache essential assets
self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(async cache => {
        const results = await Promise.allSettled(
          URLS_TO_CACHE.map(async url => {
            try {
              const resp = await fetch(url);
              if (resp.ok) await cache.put(url, resp.clone());
            } catch (e) {
              console.warn(`Skipped caching ${url}:`, e);
            }
          })
        );
        console.log('Cache results:', results);
      })
      .then(() => self.skipWaiting())
  );
});

// ✅ ACTIVATE: Clean old caches + control all clients immediately
self.addEventListener('activate', event => {
  event.waitUntil(
    caches.keys().then(keys =>
      Promise.all(keys.map(k => k !== CACHE_NAME && caches.delete(k)))
    ).then(() => self.clients.claim()) // <-- Important!
  );
});

// ✅ FETCH: Network first for HTML, cache fallback for others
self.addEventListener('fetch', event => {
  const req = event.request;
  const url = new URL(req.url);

  // Network-first for HTML (keeps dashboard/login fresh)
  if (req.mode === 'navigate') {
    event.respondWith(
      fetch(req)
        .then(resp => {
          const copy = resp.clone();
          caches.open(CACHE_NAME).then(c => c.put(req, copy));
          return resp;
        })
        .catch(() => caches.match('/offline/'))
    );
    return;
  }

  // Cache-first for static assets
  event.respondWith(
    caches.match(req).then(resp => resp || fetch(req))
  );
});
