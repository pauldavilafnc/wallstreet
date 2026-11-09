/* WALL STREET — modo offline. Estratégia: rede primeiro (sempre a versão mais nova quando há internet);
   se a rede falhar, usa a última cópia guardada. Não guarda dados financeiros (eles ficam no localStorage). */
const CACHE = 'wallstreet-v2';
const BASICOS = ['./', 'index.html', 'manifest.webmanifest', 'icon-192.png', 'icon-512.png', 'icon-maskable-512.png', 'apple-touch-icon.png', 'favicon-32.png', 'favicon-48.png'];
self.addEventListener('install', e => {
  e.waitUntil(caches.open(CACHE).then(c => c.addAll(BASICOS)).then(() => self.skipWaiting()));
});
self.addEventListener('activate', e => {
  e.waitUntil(caches.keys().then(ks => Promise.all(ks.filter(k => k !== CACHE).map(k => caches.delete(k)))).then(() => self.clients.claim()));
});
self.addEventListener('fetch', e => {
  const r = e.request, u = new URL(r.url);
  if (r.method !== 'GET' || u.origin !== location.origin) return;   // só arquivos do próprio site
  e.respondWith(
    fetch(r).then(res => {
      if (res.ok) { const copia = res.clone(); caches.open(CACHE).then(c => c.put(r, copia)); }
      return res;
    }).catch(() => caches.match(r).then(x => x || (r.mode === 'navigate' ? caches.match('index.html') : undefined)))
  );
});
