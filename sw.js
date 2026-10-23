/* 醸造ボード service worker
 * 画面ファイルだけを保存し、電波がないときも画面が開くようにする。
 * データ（Apps Script への通信）は保存しない。画面はネット優先なので、更新は次に開いたときに反映される。 */
const CACHE = 'brewboard-v2';
const SHELL = ['./', 'index.html', 'manifest.webmanifest', 'icons/icon-192.png', 'icons/icon-512.png', 'icons/apple-touch-icon.png', 'icons/favicon-64.png'];
self.addEventListener('install', e => {
  e.waitUntil(caches.open(CACHE).then(c => c.addAll(SHELL)).then(() => self.skipWaiting()));
});
self.addEventListener('activate', e => {
  e.waitUntil(caches.keys().then(ks => Promise.all(ks.filter(k => k !== CACHE).map(k => caches.delete(k)))).then(() => self.clients.claim()));
});
self.addEventListener('fetch', e => {
  const req = e.request;
  if (req.method !== 'GET') return;
  const url = new URL(req.url);
  if (url.origin !== self.location.origin) return; // Apps Script・フォントは触らない
  if (url.pathname.endsWith('/version.json')) return; // 版の確認は常にネットから
  e.respondWith(
    fetch(req, { cache: 'no-cache' }).then(res => {  // HTTP キャッシュを使わず毎回確認（更新をすぐ反映）
      if (res.ok) { const copy = res.clone(); caches.open(CACHE).then(c => c.put(req, copy)); }
      return res;
    }).catch(() => caches.match(req).then(r => r || caches.match('index.html')))
  );
});
