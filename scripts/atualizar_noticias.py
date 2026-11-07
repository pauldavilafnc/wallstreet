#!/usr/bin/env python3
"""Atualiza o arquivo noticias.json a partir de feeds RSS/Atom públicos.

- Só usa a biblioteca padrão do Python (nada para instalar).
- Não faz scraping: lê apenas os feeds que as próprias fontes publicam.
- Nunca inventa nada: título, resumo, data e link vêm do feed.
- Se um feed falhar, ele é ignorado; se TUDO falhar, o arquivo atual é mantido.
"""
import html, json, re, sys, urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta, timezone
from email.utils import parsedate_to_datetime
from pathlib import Path

BR = timezone(timedelta(hours=-3))           # horário de Brasília
SAIDA = Path(__file__).resolve().parent.parent / "noticias.json"
DIAS_MAX, POR_CATEGORIA, POR_FONTE = 7, 8, 3

# (categoria, nome exibido, URL do feed, filtrar por palavras de economia?)
# br = Brasil, mu = Mundo. Ajuste/acrescente feeds aqui. Se um endereço mudar,
# o script apenas ignora esse feed e avisa no log da execução.
FEEDS = [
    ("br", "Agência Brasil", "https://agenciabrasil.ebc.com.br/rss/economia/feed.xml", False),
    ("br", "G1 Economia", "https://g1.globo.com/rss/g1/economia/", False),
    ("br", "InfoMoney", "https://www.infomoney.com.br/economia/feed/", False),
    ("br", "InfoMoney", "https://www.infomoney.com.br/feed/", True),
    ("br", "Banco Central do Brasil", "https://www.bcb.gov.br/api/feed/sitebcb/sitefeeds/noticias", False),
    ("mu", "BBC News Brasil", "https://feeds.bbci.co.uk/portuguese/rss.xml", True),
    ("mu", "G1 Mundo", "https://g1.globo.com/rss/g1/mundo/", True),
]
ECONOMIA = re.compile(
    r"econom|infla|juros|selic|banco central|bolsa|d[oó]lar|euro\b|mercado|\bfed\b|\bbce\b|\bpib\b|"
    r"invest|fiscal|emprego|petr[oó]leo|a[cç][õo]es|crise|tarifa|com[eé]rcio|fmi|moeda|d[ií]vida", re.I)

# Classificação Brasil x Mundo: pontua o título (peso 3) e o resumo (peso 1) e compara.
# A categoria padrão vem da fonte; só troca se o outro lado pontuar MAIS (empate = mantém).
EXTERIOR = re.compile(
    r"\b(EUA|Estados Unidos|americano|americana|Jap[ãa]o|japon[êe]s|China|chin[êe]s|Coreia|Europa|europeu|europeia|zona do euro|"
    r"Fed|Nasdaq|Dow Jones|Wall Street|T[óo]quio|Londres|Alemanha|Fran[çc]a|Reino Unido|Trump|Warsh|BCE|Opep|[ÍI]ndia|"
    r"R[úu]ssia|Ucr[âa]nia|Oriente M[ée]dio|Israel|Ir[ãa]|Nikkei|S&P|Argentina|M[ée]xico|Canad[áa]|Austr[áa]lia|Hong Kong|"
    r"Seul|Paraguai|Uruguai|Bol[íi]via|Chile|Peru|Col[ôo]mbia|Venezuela|global|internacional|internacionais|mundial|exterior)\b")
BRASIL = re.compile(
    r"Brasil|brasileir[oa]s?|Ibovespa|\bB3\b|Selic|Copom|IBGE|IPCA|Petrobras|Lula|Haddad|Tesouro Nacional|INSS|Receita Federal|"
    r"Congresso|Senado|C[âa]mara dos Deputados|STF|BNDES|\bPix\b|\breal\b|R\$|Ita[úu]|Bradesco|Nubank|\bVale\b|governo federal|Planalto")
def pontos(rx, t, s):
    return 3 * len(rx.findall(t)) + len(rx.findall(s))

def classificar(cat, titulo, resumo_):
    """Brasil/Mundo pelo conteúdo. Ex.: 'Bolsa do Japão cai...' do G1 Economia -> Mundo."""
    e, b = pontos(EXTERIOR, titulo, resumo_), pontos(BRASIL, titulo, resumo_)
    if cat == "br" and e > b:
        return "mu"
    if cat == "mu" and b > e:
        return "br"
    return cat

# Legendas de foto (muito comuns nos resumos do G1): "... Fulano/AP texto da matéria"
CREDITO = re.compile(
    r"\S+(?:\s\S+){0,3}\s?/\s?(?:AP|Reuters|AFP|EPA|Getty Images|Bloomberg|Divulga[çc][ãa]o|Pool|Reprodu[çc][ãa]o|"
    r"TV Globo|Ag[êe]ncia Brasil|Ag[êe]ncia O Globo)\b(?:\s?/\s?[A-Z][\wÀ-ÿ]+)?")
LEGENDA = re.compile(r"^\s*(Foto|Imagem|Legenda|Ilustra[çc][ãa]o)\s*:", re.I)

def local(tag):
    return tag.rsplit("}", 1)[-1]

def limpar(txt, limite=230):
    txt = html.unescape(re.sub(r"<[^>]+>", " ", txt or ""))
    txt = re.sub(r"\s+", " ", txt).strip()
    if len(txt) > limite:
        txt = txt[:limite].rsplit(" ", 1)[0].rstrip(" ,;:.-") + "…"
    return txt

def resumo(raw, limite=230):
    """Resumo do feed sem legendas de foto. Se sobrar quase nada, devolve vazio (nunca inventa)."""
    raw = re.sub(r"<figure.*?</figure>|<figcaption.*?</figcaption>|<img[^>]*>", " ", raw or "", flags=re.S | re.I)
    txt = limpar(raw, 10_000)
    if LEGENDA.match(txt):
        return ""
    m = CREDITO.search(txt)
    if m:                                   # tudo até o crédito é legenda da foto
        txt = txt[m.end():].strip()
    txt = limpar(txt, limite)
    return txt if len(txt) >= 25 else ""

def data(txt):
    txt = (txt or "").strip()
    try:
        d = parsedate_to_datetime(txt)
    except Exception:
        try:
            d = datetime.fromisoformat(txt.replace("Z", "+00:00"))
        except Exception:
            return None
    if d.tzinfo is None:
        d = d.replace(tzinfo=timezone.utc)
    return d.astimezone(BR)

def ler_feed(xml_bytes, stats=None):
    """Devolve lista de dicts {t, s, u, d} a partir de RSS ou Atom."""
    raiz = ET.fromstring(xml_bytes)
    itens = []
    st = stats if stats is not None else {}
    for k in ("total", "sem_titulo", "sem_https", "sem_data"):
        st.setdefault(k, 0)
    for el in raiz.iter():
        if local(el.tag) not in ("item", "entry"):
            continue
        st["total"] += 1
        t = s = u = p = ""
        for ch in el:
            n = local(ch.tag)
            if n == "title":
                t = limpar("".join(ch.itertext()), 200)
            elif n == "link":
                href = ch.get("href")
                if href and ch.get("rel", "alternate") == "alternate":
                    u = u or href.strip()
                elif not href and (ch.text or "").strip():
                    u = u or ch.text.strip()
            elif n in ("description", "summary") and not s:
                s = resumo(ch.text or "".join(ET.tostring(x, encoding="unicode") for x in ch)) if len(ch) else resumo(ch.text or "")
            elif n in ("pubDate", "published", "updated", "date") and not p:
                p = ch.text or ""
        d = data(p)
        if st["total"] == 1:
            st["amostra"] = f"campos={[local(c.tag) for c in el]} link={u!r} data={p!r}"
        if not t:
            st["sem_titulo"] += 1
        elif not u.startswith("https://"):
            st["sem_https"] += 1
        elif not d:
            st["sem_data"] += 1
        else:
            itens.append({"t": t, "s": s, "u": u, "d": d})
    return itens

def baixar(url):
    req = urllib.request.Request(url, headers={"User-Agent": "WallStreetNoticias/1.0 (+uso pessoal)"})
    with urllib.request.urlopen(req, timeout=25) as r:
        return r.read(3_000_000)

def montar(coletado, agora):
    """coletado: lista de (categoria, fonte, filtrar, itens). Devolve lista final de notícias."""
    vistos, pool = set(), []
    for cat0, fonte, filtrar, itens in coletado:
        for i in itens:
            cat = classificar(cat0, i["t"], i["s"])
            if i["d"] > agora + timedelta(hours=1) or agora - i["d"] > timedelta(days=DIAS_MAX):
                continue
            if filtrar and not ECONOMIA.search(i["t"] + " " + i["s"]):
                continue
            chave = re.sub(r"\W+", "", i["t"].lower())
            if i["u"] in vistos or chave in vistos:
                continue
            vistos.update((i["u"], chave))
            pool.append((cat, fonte, i))
    pool.sort(key=lambda x: x[2]["d"], reverse=True)
    saida, cont_cat, cont_fonte = [], {}, {}
    for cat, fonte, i in pool:
        if cont_cat.get(cat, 0) >= POR_CATEGORIA or cont_fonte.get((cat, fonte), 0) >= POR_FONTE:
            continue
        cont_cat[cat] = cont_cat.get(cat, 0) + 1
        cont_fonte[(cat, fonte)] = cont_fonte.get((cat, fonte), 0) + 1
        item = {"c": cat, "t": i["t"], "f": fonte, "d": i["d"].strftime("%Y-%m-%d"),
                "h": i["d"].strftime("%H:%M"), "u": i["u"]}
        if i["s"]:
            item["s"] = i["s"]
        saida.append(item)
    return saida

def main():
    agora = datetime.now(BR)
    coletado = []
    for cat, fonte, url, filtrar in FEEDS:
        try:
            st = {}
            itens = ler_feed(baixar(url), st)
            coletado.append((cat, fonte, filtrar, itens))
            print(f"ok     {fonte}: {len(itens)} aceitos de {st['total']} entradas "
                  f"(sem título {st['sem_titulo']}, sem https {st['sem_https']}, sem data {st['sem_data']})")
            if st["total"] and not itens:
                print(f"       amostra da 1ª entrada: {st.get('amostra')}", file=sys.stderr)
        except Exception as e:                      # um feed fora do ar não derruba os outros
            print(f"FALHOU {fonte} ({url}): {e}", file=sys.stderr)
    novos = montar(coletado, agora)
    if not novos:        # nada novo: NÃO mexe no arquivo (senão pareceria atualizado sem estar)
        print("Nenhuma notícia nova obtida; noticias.json mantido.", file=sys.stderr)
        return 1
    antigos = []
    if SAIDA.exists():
        try:
            antigos = json.loads(SAIDA.read_text(encoding="utf-8")).get("items", [])
        except Exception:
            pass
    for cat in ("br", "mu"):                          # categoria vazia: mantém a anterior
        if not any(n["c"] == cat for n in novos):
            novos += [n for n in antigos if n["c"] == cat]
    SAIDA.write_text(json.dumps({"at": agora.isoformat(timespec="minutes"), "items": novos},
                                ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(f"noticias.json atualizado: {len(novos)} notícias.")
    return 0

if __name__ == "__main__":
    sys.exit(main())
