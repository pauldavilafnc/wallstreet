/* Wolfin — modo offline.
   Estratégia: rede primeiro, sempre revalidando (nunca aparece arquivo velho quando há internet);
   se a rede falhar ou demorar demais, usa a última cópia guardada.
   Identificação dos caches: wallstreet::<escopo>::v<versão>  (ex.: wallstreet::/wallstreet/::v3).
   Este arquivo só cria, lê e apaga caches com essa identificação (e o nome antigo wallstreet-vN usado
   por versões anteriores deste app). Caches de outros projetos do mesmo domínio nunca são tocados.
   Não guarda dados financeiros (eles ficam no localStorage). */
const VERSAO = '3';
const ESCOPO = new URL(self.registration.scope).pathname;            // ex.: /wallstreet/
const PREFIXO = 'wallstreet::' + ESCOPO + '::';
const CACHE = PREFIXO + 'v' + VERSAO;
const LEGADO = /^wallstreet-v\d+$/;                                    // nome das versões antigas deste app
const meuCache = k => k.startsWith(PREFIXO) || LEGADO.test(k);
const ESSENCIAIS = ['index.html'];                                     // sem isso a instalação falha (e a versão atual continua valendo)
const OPCIONAIS = ['./', 'manifest.webmanifest', 'icon-192.png', 'icon-512.png', 'icon-maskable-512.png', 'apple-touch-icon.png', 'favicon-32.png', 'favicon-48.png'];
const ESPERA_REDE = 6000;                                              // rede lenta: depois disso usa a cópia guardada (e atualiza em segundo plano)
const meu = u => u.origin === location.origin && u.pathname.startsWith(ESCOPO);   // só arquivos deste app

self.addEventListener('install', e => {
  e.waitUntil((async () => {
    try {
      const c = await caches.open(CACHE);
      for (const u of ESSENCIAIS) await c.add(new Request(u, { cache: 'reload' }));
      await Promise.all(OPCIONAIS.map(u => c.add(new Request(u, { cache: 'reload' })).catch(() => {})));
    } catch (erro) {
      await caches.delete(CACHE).catch(() => {});                      // não deixa cache pela metade; a versão anterior segue funcionando
      throw erro;
    }
    await self.skipWaiting();
  })());
});

/* Remove as versões antigas DESTE app (e o nome antigo wallstreet-vN). Roda ao ativar e de novo na primeira requisição:
   assim, mesmo que o worker antigo ainda termine uma gravação em segundo plano e recrie um cache velho, ele é limpo. */
let limpou = false;
async function limparAntigos() {
  try {
    const c = await caches.open(CACHE);
    if (!(await c.match('index.html'))) return;                        // só limpa as versões antigas se a nova está íntegra
    for (const k of await caches.keys()) if (k !== CACHE && meuCache(k)) await caches.delete(k);
  } catch (_) { /* limpar é opcional: nunca impede o app de funcionar */ }
}

self.addEventListener('activate', e => {
  e.waitUntil((async () => {
    await limparAntigos();
    await self.clients.claim();
  })());
});

async function guardada(r) {
  try {
    const c = await caches.open(CACHE);                                // só o cache DESTE app
    return (await c.match(r, { ignoreSearch: true })) || (r.mode === 'navigate' ? await c.match('index.html') : undefined);
  } catch (_) { return undefined; }
}

async function responder(e, r) {
  const rede = fetch(r, { cache: 'no-cache' }).then(res => {
    if (res.ok && res.type === 'basic') {
      const copia = res.clone();
      e.waitUntil(caches.open(CACHE).then(c => c.put(r, copia)).catch(() => {}));
    }
    return res;
  });
  e.waitUntil(rede.catch(() => {}));
  try {
    return await Promise.race([rede, new Promise(ok => setTimeout(async () => { const x = await guardada(r); if (x) ok(x); }, ESPERA_REDE))]);
  } catch (_) {
    return (await guardada(r)) || new Response('Sem conexão e sem cópia guardada deste arquivo.', { status: 503, statusText: 'Offline', headers: { 'Content-Type': 'text/plain; charset=utf-8' } });
  }
}

/* Vídeo da intro (mp4/webm): o navegador pede trechos (Range). Baixa o arquivo inteiro uma vez, guarda no cache deste app e
   responde os trechos (206) a partir da cópia — assim a intro em vídeo também toca offline. Se não houver cópia nem rede, falha
   (a página então usa a intro em CSS). Nomes de arquivo mudam a cada nova versão do vídeo. */
const ehVideo = u => /\.(mp4|webm)$/i.test(u.pathname);
async function video(e, r) {
  const url = new URL(r.url).href;
  let c, cop;
  try { c = await caches.open(CACHE); cop = await c.match(url); } catch (_) { /* segue sem cache */ }
  if (!cop) {
    try {
      const res = await fetch(url, { cache: 'no-cache' });
      if (!res.ok || res.type !== 'basic') return res;
      cop = res;
      if (c) e.waitUntil(c.put(url, res.clone()).catch(() => {}));
    } catch (_) { return new Response('', { status: 503, statusText: 'Offline' }); }
  }
  const faixa = r.headers.get('range'), m = faixa && /^bytes=(\d*)-(\d*)$/.exec(faixa);
  if (!m) return cop;
  const buf = await cop.arrayBuffer(), total = buf.byteLength;
  let ini = m[1] === '' ? Math.max(0, total - Number(m[2])) : Number(m[1]);
  let fim = (m[1] === '' || m[2] === '') ? total - 1 : Math.min(Number(m[2]), total - 1);
  if (!(ini <= fim) || ini >= total) return new Response('', { status: 416, headers: { 'Content-Range': 'bytes */' + total } });
  return new Response(buf.slice(ini, fim + 1), { status: 206, headers: { 'Content-Type': cop.headers.get('Content-Type') || (/\.mp4$/i.test(url) ? 'video/mp4' : 'video/webm'), 'Content-Range': 'bytes ' + ini + '-' + fim + '/' + total, 'Content-Length': String(fim - ini + 1), 'Accept-Ranges': 'bytes' } });
}

self.addEventListener('fetch', e => {
  const r = e.request;
  if (r.method !== 'GET' || !meu(new URL(r.url))) return;
  if (!limpou) { limpou = true; e.waitUntil(limparAntigos()); }
  e.respondWith(ehVideo(new URL(r.url)) ? video(e, r) : responder(e, r));
});
