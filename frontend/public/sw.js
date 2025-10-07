self.addEventListener('install', (event) => {
  event.waitUntil((async () => {
    const cache = await caches.open('kenyapos-static-v1')
    await cache.addAll([
      '/',
      '/index.html',
      '/vite.svg',
    ])
  })())
})

self.addEventListener('fetch', (event) => {
  const { request } = event
  if (request.method !== 'GET') return
  event.respondWith((async () => {
    const cache = await caches.open('kenyapos-static-v1')
    const cached = await cache.match(request)
    if (cached) return cached
    try {
      const resp = await fetch(request)
      if (resp && resp.status === 200 && request.url.startsWith(self.location.origin)) {
        cache.put(request, resp.clone())
      }
      return resp
    } catch (err) {
      return cached || Response.error()
    }
  })())
})
