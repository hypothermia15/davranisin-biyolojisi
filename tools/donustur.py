#!/usr/bin/env python3
"""Davranışın Biyolojisi öğrenme notlarını (Markdown, 3. sürüm) etkileşimli web rehberine çevirir.

    python3 tools/donustur.py <ogrenme-notlari-v3.md> <rehber klasörü>

- Çıktı: <rehber klasörü>/index.html. Şekiller <rehber klasörü>/sekiller/sekil-NN.png olarak beklenir.
- "Ders 01 [00:25:35]" ve "2024/23 [1:04]" biçimindeki zaman damgaları YouTube'daki ders kaydına bağlanır.
- Metindeki atıflar kaynakçadaki künyeye, "Şekil N" göndermeleri şekle bağlanır.
- Kendini sına maddeleri tıklanabilir sorulara, mini vaka soruları açılır yanıtlara dönüşür.
"""
import html
import json
import re
import sys
import unicodedata
from pathlib import Path

import markdown
from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parent))
from ekler import EK_KAYNAKLAR, GUNCEL, SIM_REHBER, SIMULASYONLAR, SORULAR  # noqa: E402
import vakalar as VAK  # noqa: E402

SRC, OUT = Path(sys.argv[1]), Path(sys.argv[2])
T = SRC.read_text(encoding="utf-8")

# --- Web sürümü için metin düzeltmeleri (docx ve proje içi göndermeler) ---
FIXES = [
    ("Şekilli tam sürüm .docx olarak teslim edildi (Kasım 2026); burada şekillerin yalnızca başlıkları yer alır. "
     "2. sürümdeki ayrıntılı karşılaştırma tabloları için `claude/davranisin-biyolojisi-not-seti-v2.md` belgesine bakın.",
     "Bu web sürümünde 29 şeklin tamamı yer alır."),
    ("Kaynaklar oturumların “Derste öyle, bugün böyle” tablolarında ve not setinin 2. sürümündedir.",
     "Kaynaklar oturumların “Derste öyle, bugün böyle” tablolarındadır; hepsi bu sitenin “İddia ligi” sayfasında bir arada."),
    ("- Proje okuma notlarımız:", "- Hazırlayanın okuma notları:"),
    ("- Proje sunumları: “Çocuk ve ergen ile erişkin arasındaki farklar”; “Dijital çağda gençlik”.",
     "- Hazırlayanın sunumları: “Çocuk ve ergen ile erişkin arasındaki farklar”; “Dijital çağda gençlik” "
     "([web sürümü](https://miracbarisusta.com/brain-rot-mu/))."),
]
for old, new in FIXES:
    assert old in T, f"düzeltilecek metin bulunamadı: {old[:60]}"
    T = T.replace(old, new)
T = T.replace("### Şekiller (docx sürümünde)", "### 🖼 Şekiller")

# --- Ders kayıtları (YouTube) ---
V2010 = ["NNnIGh9g6fA", "Y0Oa4Lp5fLE", "oKNAzl-XN4I", "_dRXA1_e30o", "dFILgg9_hrU", "e0WZx7lUOrY", "RG5fN6KrDJE",
         "P388gUPSq_I", "ISVaoLlW104", "5031rWXgdYo", "uqU9lmFztOU", "yETVsV4zfFw", "kAfz0yAcOyQ", "CAOnSbDSaOw",
         "LOY3QH_jOtE", "95OP9rSjxzw", "JPYmarGO5jM", "wLE71i4JJiM", "EtVfoIkVSu8", "BqP4_4kr7-0", "_njf8jwEGRo",
         "o_ZuWbX-CyE", "SIOQgY1tqrU", "nEnklxGAmak", "-PpDq1WUtAw"]
T2010 = ["Introduction to Human Behavioral Biology", "Behavioral Evolution", "Behavioral Evolution II",
         "Molecular Genetics I", "Molecular Genetics II", "Behavioral Genetics I", "Behavioral Genetics II",
         "Recognizing Relatives", "Ethology", "Introduction to Neuroscience I", "Introduction to Neuroscience II",
         "Endocrinology", "Advanced Neurology and Endocrinology", "Limbic System", "Human Sexual Behavior I",
         "Human Sexual Behavior II", "Human Sexual Behavior III & Aggression I", "Aggression II", "Aggression III",
         "Aggression IV", "Chaos and Reductionism", "Emergence and Complexity", "Language", "Schizophrenia",
         "Individual Differences"]
V2024 = ["mZI2GQlNdJA", "5izfiuLvRpk", "XZW2qBunfkc", "MJzi-E3Rltc", "l6gTya90oE0", "o1UmM6of6C8", "x18sxXomh0Q",
         "011ANS4L-Fk", "wF2sPJ3wDJQ", "MkwLCtOkc94", "xM3nmwUR6Bk", "bnCK78BIX4g", "190aofoVY4g", "T_wOUIxfTdY",
         "2QOle949vRM", "tAmimepUnDc", "4s-WlqZnUvQ", "ux6Qe7ErzIQ", "nuuK95ONPVY", "cQLvY42kjVU", "dQRr2Xgas4o",
         "62JMAX5Vegk", "gtlPr6nFE3U", "lH1ayPzddwk", "dCHTbOyZMgc", "z8Szus2JfXk", "YTXEw0cFo6U", "piu7l2v8JiY",
         "r6tEbbZ630w", "c6cyUQsqk7Q", "q5UiYByBf3Q", "yV0LRviijYw"]
T2024 = (["Introduction"] + [f"Evolution of Behavior {i}" for i in (1, 2, 3)]
         + [f"Molecular Behavior Genetics {i}" for i in (1, 2)] + [f"Behavioral Genetics {i}" for i in (1, 2)]
         + [f"Ethology {i}" for i in (1, 2)] + [f"Limbic System {i}" for i in (1, 2, 3, 4)]
         + [f"Advanced Topics in Neuroendocrinology {i}" for i in (1, 2)] + [f"Emergence {i}" for i in (1, 2)]
         + [f"Sexuality {i}" for i in (1, 2, 3, 4)] + [f"Violence and its Antidotes {i}" for i in range(1, 7)]
         + ["Depression", "Schizophrenia", "Religious Belief", "Individual Differences"])
assert len(V2010) == len(T2010) == 25 and len(V2024) == len(T2024) == 32
PL2010 = "https://www.youtube.com/playlist?list=PL848F2368C90DDC3D"
PL2024 = "https://www.youtube.com/playlist?list=PLzxlKUNNLxmEvjCSUAurMReJBZxaLdD1_"
DEP2023 = "https://www.youtube.com/watch?v=fzUXcBTQXKM"


def esc(s):
    return html.escape(s, quote=True)


def secs(t):
    n = 0
    for p in t.strip().split(":"):
        n = n * 60 + int(p)
    return n


def yt(series, n, t=None):
    vid = (V2010 if series == 2010 else V2024)[n - 1]
    return f"https://www.youtube.com/watch?v={vid}" + (f"&amp;t={secs(t)}s" if t else "")


def ytitle(series, n):
    return (T2010 if series == 2010 else T2024)[n - 1]


def a_yt(series, n, label, t=None):
    when = f", {t.strip()}’den itibaren" if t else ""
    tip = f"{'2010' if series == 2010 else '2024'} · Ders {n}: {ytitle(series, n)}{when} (YouTube, yeni sekme)"
    return (f'<a class="zd" href="{yt(series, n, t)}" target="_blank" rel="noopener" title="{esc(tip)}">'
            f'{label}</a>')


# --- Markdown yardımcıları ---
_MD = markdown.Markdown(extensions=["sane_lists"])


def md(s):
    _MD.reset()
    return _MD.convert(s)


def mdi(s):
    h = md(s).strip()
    m = re.fullmatch(r"<p>(.*)</p>", h, flags=re.S)
    return m.group(1) if m else h


TAG = re.compile(r"(<[^>]+>)")


def on_text(h, fn):
    """fn'i yalnızca etiket dışındaki ve <a> içinde olmayan metin parçalarına uygular."""
    out, in_a = [], 0
    for part in TAG.split(h):
        if part.startswith("<"):
            if re.match(r"<a[\s>]", part):
                in_a += 1
            elif part.startswith("</a"):
                in_a -= 1
            out.append(part)
        else:
            out.append(part if in_a or not part else fn(part))
    return "".join(out)


# 2010: "Ders 01 [00:25:35]", "Ders 03" ; 2024: "2024/23 [1:04–4:10]", "2024/23 [13:55; 45:52]", "2024/11–18", "2024/29 ve 31"
RX_2010 = re.compile(r"Ders (\d{2})(?:–(\d{2}))?(?: \[(\d{1,2}:\d{2}(?::\d{2})?)\])?")
RX_2024 = re.compile(r"2024/(\d{1,2})(?:–(\d{1,2}))?(?: ve (\d{1,2}))?(?: \[([^\]]+)\])?")


def link_ts(s):
    def r2010(m):
        n = int(m.group(1))
        if not 1 <= n <= 25:
            return m.group(0)
        return a_yt(2010, n, m.group(0), m.group(3))

    def r2024(m):
        n = int(m.group(1))
        if not 1 <= n <= 32:
            return m.group(0)
        times = [x.strip() for x in m.group(4).split(";")] if m.group(4) else []
        head = f"2024/{m.group(1)}" + (f"–{m.group(2)}" if m.group(2) else "")
        if not times:
            out = a_yt(2024, n, head)
            if m.group(3):
                out += " ve " + a_yt(2024, int(m.group(3)), m.group(3))
            return out
        if len(times) == 1:
            return a_yt(2024, n, m.group(0), times[0].split("–")[0])
        inner = "; ".join(a_yt(2024, n, t, t.split("–")[0]) for t in times)
        return f'<span class="zd-grup">{head} [{inner}]</span>'

    s = RX_2010.sub(r2010, s)
    return RX_2024.sub(r2024, s)


def link_fig(s):
    return re.sub(r"Şekil (\d+)", lambda m: f'<a class="sekil-ref" href="#sekil-{int(m.group(1))}">Şekil {m.group(1)}</a>'
                  if int(m.group(1)) in FIGS else m.group(0), s)


# --- Kaynakça ---
def slug(s):
    s = s.translate(str.maketrans("çğıöşüÇĞİÖŞÜâîû", "cgiosuCGIOSUaiu"))
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")


REFS = []          # {id, text(plain), html, years}
NAME = r"[A-ZÇĞİÖŞÜ][\w’'\-\.]*"
PART = r"(?: (?:[A-ZÇĞİÖŞÜ][\w’'\-\.]*|de|van|von|der|den|da|di|le|la|v\.))*"
RX_CITE = re.compile(rf"(?P<who>{NAME}{PART}(?: [A-Z]{{1,2}})?(?: ve ark\.| ve (?:de |van |von )?{NAME}{PART})?) "
                     rf"(?P<year>(?:19|20)\d{{2}}(?:–(?:19|20)\d{{2}})?[a-z]?)(?![’'\w])")
UNMATCHED = set()


ALIAS = {"Simons Vakfı": "Simons Foundation"}


def lookup(who, year):
    who = who.replace(" ve ark.", "")
    first, _, second = who.partition(" ve ")
    first = ALIAS.get(first.strip(), first.strip())
    yr = year[:4]
    words = first.split(" ")
    for k in range(len(words)):              # baştaki fazladan büyük harfli sözcükleri sırayla at
        f = " ".join(words[k:])
        c = [r for r in REFS if re.match(r"(?:von |van |de |di |du |der |den )?" + re.escape(f) + r"[ ,.]", r["text"])
             and yr in r["years"]]
        if second and len(c) > 1:
            c = [r for r in c if second.strip() in r["text"][:160]] or c
        if c:
            return c[0]
    return None


def link_cite(s):
    def rep(m):
        r = lookup(m.group("who"), m.group("year"))
        if not r:
            UNMATCHED.add(m.group(0))
            return m.group(0)
        return f'<a class="atif" href="#{r["id"]}" data-k="{r["id"]}">{m.group(0)}</a>'
    return RX_CITE.sub(rep, s)


def link_all(h, cites=True):
    h = on_text(h, link_ts)
    h = on_text(h, link_fig)
    if cites:
        h = on_text(h, link_cite)
    return h


# --- Belgeyi bölümlere ayır ---
lines = T.split("\n")
H1 = lines[0][2:].strip()
INTRO, SECTIONS = [], []
cur = blk = None
for ln in lines[1:]:
    if ln.startswith("## "):
        cur = {"title": ln[3:].strip(), "lead": [], "blocks": []}
        SECTIONS.append(cur)
        blk = None
    elif ln.startswith("### "):
        blk = {"title": ln[4:].strip(), "lines": []}
        cur["blocks"].append(blk)
    elif cur is None:
        INTRO.append(ln)
    elif blk is None:
        cur["lead"].append(ln)
    else:
        blk["lines"].append(ln)

# Şekiller: "- **Şekil N.** başlık"
RX_FIG = re.compile(r"^- \*\*Şekil (\d+)\.\*\* (.*)$")
FIGS = {}
for ln in lines:
    m = RX_FIG.match(ln)
    if m:
        FIGS[int(m.group(1))] = m.group(2).strip()
FIGS[0] = ("Bir davranışı açıklamak, zamanda geriye yürümektir. Sapolsky’nin yöntemi: aynı davranış için her zaman "
           "ölçeğinde ayrı bir soru sorulur; renkli çipler o basamağı işleyen oturumu gösterir (O1–O8). "
           "Sapolsky’nin *Behave* (2017) kitabının bölüm düzeni temel alınmıştır.")
assert sorted(FIGS) == list(range(29)), sorted(FIGS)
FIGDIM = {}
for n in FIGS:
    p = OUT / "sekiller" / f"sekil-{n:02d}.png"
    with Image.open(p) as im:
        FIGDIM[n] = im.size

# Kaynakça önce okunur (atıf bağlantıları için)
KAY = next(s for s in SECTIONS if s["title"] == "Kaynakça")
KAY["blocks"].append({"title": "Güncel kanıt kutuları için eklenenler (Kasım 2026)", "lines": EK_KAYNAKLAR})
seen = set()
for b in KAY["blocks"]:
    b["refs"] = []
    for ln in b["lines"]:
        if not ln.startswith("- "):
            continue
        raw = ln[2:].strip()
        h = mdi(raw)
        plain = re.sub(r"<[^>]+>", "", h)
        plain = html.unescape(plain)
        years = set(re.findall(r"(?:19|20)\d{2}", plain))
        y = re.search(r"\b(?:19|20)\d{2}\b", re.sub(r"https?://\S+", "", plain))
        base = "k-" + slug(re.split(r"[ ,.]", plain, maxsplit=1)[0]) + ("-" + y.group(0) if y else "")
        rid, i = base, 2
        while rid in seen:
            rid, i = f"{base}-{i}", i + 1
        seen.add(rid)
        h = re.sub(r'<a href="(https?://[^"]+)">', r'<a href="\1" target="_blank" rel="noopener">', h)
        ref = {"id": rid, "text": plain, "html": h, "years": years}
        REFS.append(ref)
        b["refs"].append(ref)


# --- Bileşenler ---
HUKUM = {"🟢": ("saglam", "Sağlam", "Sağlam: bulgu bugün de geçerli"),
         "🟡": ("tartismali", "Tartışmalı", "Tartışmalı: kanıt karışık"),
         "🔴": ("coktu", "Çöktü", "Çöktü ya da yanlış"),
         "✏": ("duzeltme", "Düzeltme", "Olgusal düzeltme"),
         "✅": ("guncelledi", "Güncelledi", "Sapolsky 2024’te güncelledi"),
         "🆕": ("yeni", "Yeni", "2024 serisinde yeni eklendi"),
         "⏸": ("surdu", "Sürüyor", "2010’daki gibi sürüyor")}


def badge(sym):
    k = sym.replace("\ufe0f", "").strip()
    if k not in HUKUM:
        return mdi(sym)
    cls, short, full = HUKUM[k]
    return (f'<span class="hukum hukum-{cls}" title="{esc(full)}"><span aria-hidden="true">{sym.strip()}</span> '
            f'{short}</span>')


def cells(row):
    return [c.strip() for c in row.strip().strip("|").split("|")]


def parse_table(ls):
    rows = [l for l in ls if l.startswith("|")]
    head = cells(rows[0])
    body = [cells(r) for r in rows[2:]]
    return head, body


CLAIMS = []   # İddia ligi


def adim_sar(sid, key, ikon, text, body):
    """Oturum bölümü: başlığa tıklanınca daralır; kimliği doğrudan bağlantıların hedefidir."""
    return (f'<section class="adim adim-{key}" id="{sid}" data-adim="{key}" aria-labelledby="{sid}-b">'
            f'<h3 id="{sid}-b"><span class="adim-ikon" aria-hidden="true">{ikon}</span> '
            f'<span class="adim-ad">{esc(text)}</span></h3><div class="adim-govde">{body}</div></section>')


def hukum_suzgec(keys):
    """Hüküm işaretine göre süzgeç (oturum içi kart listeleri için)."""
    say = {}
    for k in keys:
        say[k] = say.get(k, 0) + 1
    if len(say) < 2:
        return ""
    out = [f'<button type="button" data-hk="" aria-pressed="true">Tümü <span class="sayi">{len(keys)}</span></button>']
    for sym, (cls, short, full) in HUKUM.items():
        if say.get(cls):
            out.append(f'<button type="button" class="filtre-{cls}" data-hk="{cls}" aria-pressed="false" title="{esc(full)}">'
                       f'<span aria-hidden="true">{sym}</span> {short} <span class="sayi">{say[cls]}</span></button>')
    return f'<div class="hk-suz" role="group" aria-label="Hükme göre süz">{"".join(out)}</div>'


def render_cards(ls, kind, ctx):
    """Karşılaştırma tablolarını alt alta kartlara çevirir: her satır tek başına okunur, telefonda yana kaymaz."""
    head, body = parse_table(ls)
    items, keys = [], []
    for r in body:
        if kind == "crs":
            items.append(f'<li class="crs-kart" data-ara><h4>{link_all(mdi(r[0]))}</h4>'
                         f'<p class="crs-bulgu">{link_all(mdi(r[1]))}</p>'
                         f'<p class="crs-klinik"><span class="guncel-etiket">Klinikte</span> {link_all(mdi(r[2]))}</p></li>')
            continue
        k = r[0].replace("\ufe0f", "").strip()
        cls = HUKUM[k][0]
        keys.append(cls)
        if kind == "degisen":
            items.append(f'<li class="hk" data-hukum="{cls}" data-ara><div class="hk-ust">{badge(r[0])}'
                         f'<h4>{link_all(mdi(r[1]))}</h4></div>'
                         f'<p class="hk-ders"><span class="iddia-etiket">2024’te</span> <span>{link_all(mdi(r[2]))}</span></p>'
                         f'<p class="hk-bugun"><span class="iddia-etiket">Kanıt</span> <span>{link_all(mdi(r[3]))}</span></p></li>')
            continue
        ders, bugun = link_all(mdi(r[1])), link_all(mdi(r[2]))
        CLAIMS.append({"view": ctx["id"], "label": ctx["short"], "hukum": cls, "sym": r[0], "ders": ders, "bugun": bugun,
                       "seri": "2010" if kind == "derste" else "2024"})
        items.append(f'<li class="hk" data-hukum="{cls}" data-ara><div class="hk-ust">{badge(r[0])}</div>'
                     f'<p class="hk-ders"><span class="iddia-etiket">Derste</span> <span>{ders}</span></p>'
                     f'<p class="hk-bugun"><span class="iddia-etiket">{"Bugün" if kind == "derste" else "Kanıt"}</span> <span>{bugun}</span></p></li>')
    if kind == "crs":
        return f'<ol class="crs-liste">{"".join(items)}</ol>'
    return hukum_suzgec(keys) + f'<ol class="hk-liste">{"".join(items)}</ol>'


def render_table(ls, kind, ctx):
    head, body = parse_table(ls)
    verdict_col = kind in ("derste", "kanit", "degisen")
    labels = list(head)
    if verdict_col:
        labels[0] = "Hüküm"
    th = "".join(f'<th scope="col">{esc(l) if l else "<span class=gizli>Hüküm</span>"}</th>' for l in labels)
    out = [f'<div class="tablo-kap"><table class="tablo tablo-{kind}"><thead><tr>{th}</tr></thead><tbody>']
    for r in body:
        tds = []
        for i, c in enumerate(r):
            inner = badge(c) if (verdict_col and i == 0) else link_all(mdi(c))
            tds.append(f'<td data-label="{esc(labels[i])}">{inner}</td>')
        hk = ""
        if verdict_col:
            k = r[0].replace("\ufe0f", "").strip()
            hk = f' data-hukum="{HUKUM.get(k, ("", ""))[0]}"'
            if kind in ("derste", "kanit"):
                CLAIMS.append({"view": ctx["id"], "label": ctx["short"], "hukum": HUKUM[k][0], "sym": r[0],
                               "ders": link_all(mdi(r[1])), "bugun": link_all(mdi(r[2])),
                               "seri": "2010" if kind == "derste" else "2024"})
        out.append(f'<tr data-ara{hk}>{"".join(tds)}</tr>')
    out.append("</tbody></table></div>")
    return "".join(out)


def figure(n, cls="", fid=None):
    w, h = FIGDIM[n]
    cap = FIGS[n]
    alt = re.sub(r"<[^>]+>", "", mdi(cap))
    alt = html.unescape(alt)
    label = "Harita" if n == 0 else f"Şekil {n}."
    src = f"sekiller/sekil-{n:02d}.png"
    return (f'<figure class="sekil {cls}" id="{fid or f"sekil-{n}"}"{"" if fid else " data-ara"}>'
            f'<a class="sekil-buyut" href="{src}" data-sekil="{n}" aria-label="{esc(label)} Büyüt">'
            f'<img src="{src}" width="{w}" height="{h}" loading="lazy" decoding="async" alt="{esc(label + " " + alt)}"></a>'
            f'<figcaption><span class="sekil-no">{label}</span> {link_all(mdi(cap))}</figcaption></figure>')


def chunks(ls):
    """Satırları paragraf / liste / tablo / şekil öbeklerine ayırır."""
    out, cur, kind = [], [], None

    def flush():
        nonlocal cur, kind
        if cur:
            out.append((kind, cur))
        cur, kind = [], None

    for ln in ls:
        if not ln.strip():
            flush()
            continue
        if RX_FIG.match(ln):
            k = "fig"
        elif ln.startswith("|"):
            k = "table"
        elif re.match(r"^(\s*[-*] |\s*\d+\. )", ln):
            k = "list"
        else:
            k = "para"
        if kind and k != kind:
            flush()
        kind = k
        cur.append(ln)
    flush()
    return out


def render_generic(ls, ctx, cites=True):
    out = []
    for kind, ch in chunks(ls):
        if kind == "fig":
            out += [figure(int(RX_FIG.match(l).group(1))) for l in ch]
        elif kind == "table":
            out.append(render_table(ch, "genel", ctx))
        else:
            h = md("\n".join(ch))
            h = h.replace("<p>", "<p data-ara>", 1) if kind == "para" else h.replace("<li>", "<li data-ara>")
            out.append(link_all(h, cites))
    return "\n".join(out)


def split_tail(s):
    """'metin — *Ders 01 [..]*' → (metin, ref)"""
    m = re.match(r"^(.*) — \*(.+)\*$", s.strip())
    return (m.group(1), m.group(2)) if m else (s, None)


def r_fikirler(ls, ctx):
    items = [re.sub(r"^\d+\.\s*", "", l) for l in ls if re.match(r"^\d+\. ", l)]
    out = ['<ol class="fikirler">']
    for it in items:
        body, ref = split_tail(it)
        tail = f'<p class="ders-ref">{link_all(esc(ref))}</p>' if ref else ""
        out.append(f'<li data-ara><p>{link_all(mdi(body))}</p>{tail}</li>')
    out.append("</ol>")
    return "".join(out)


def r_ornekler(ls, ctx):
    ex = []
    for l in ls:
        if l.startswith("- "):
            ex.append({"main": l[2:], "bugun": []})
        elif l.strip().startswith("- ") and ex:
            ex[-1]["bugun"].append(re.sub(r"^\s*-\s*🆕\s*\*\*Bugün:\*\*\s*", "", l))
    out = ['<div class="ornekler">']
    for e in ex:
        m = re.match(r"^\*\*(\S+)\s+(.+?)\*\*\s*(.*)$", e["main"])
        ikon, baslik, rest = (m.group(1), m.group(2).rstrip("."), m.group(3)) if m else ("", "", e["main"])
        bug = "".join(f'<div class="bugun"><p class="bugun-etiket"><span aria-hidden="true">🆕</span> Bugün</p>'
                      f'<p>{link_all(mdi(b))}</p></div>' for b in e["bugun"])
        out.append(f'<article class="ornek" data-ara><h4><span class="ornek-ikon" aria-hidden="true">{ikon}</span> '
                   f'{link_all(mdi(baslik), False)}</h4><p>{link_all(mdi(rest))}</p>{bug}</article>')
    out.append("</div>")
    return "".join(out)


def r_vaka(ls, ctx, title):
    paras = [l for l in ls if l.strip() and not l.startswith("- ")]
    qs = [l[2:] for l in ls if l.startswith("- ")]
    out = [f'<div class="vaka"><p class="vaka-baslik">{esc(title)}</p>']
    out += [f'<p class="vaka-metin" data-ara>{link_all(mdi(p))}</p>' for p in paras]
    nid = f'{ctx["id"]}-vaka-not'
    out.append(f'<div class="vaka-not"><label for="{nid}">Önce kendi yanıtınızı yazın, sonra soruları açın</label>'
               f'<textarea id="{nid}" data-not="{ctx["id"]}" rows="3" placeholder="Ayırıcı tanı, ilk adımlar, aileye ne '
               f'söylerdiniz?"></textarea><p class="kucuk">Yazdıklarınız yalnızca bu tarayıcıda saklanır.</p></div>')
    for q in qs:
        m = re.match(r"^\*\*(.+?)\*\*\s*(.*)$", q)
        soru, yanit = (m.group(1), m.group(2)) if m else (q, "")
        out.append(f'<details class="vaka-soru" data-ara><summary>{link_all(mdi(soru), False)}</summary>'
                   f'<div class="vaka-yanit"><p>{link_all(mdi(yanit))}</p></div></details>')
    dv = next((v for v in VAK.VAKALAR if v["mini"] == ctx["id"]), None)
    if dv:
        out.append(f'<p class="vaka-dallan"><a class="dugme dugme-ikincil" href="#/vakalar" data-dv-ac="{dv["id"]}">'
                   f'<span aria-hidden="true">🎭</span> Bu vakada kararları siz verin</a></p>')
    out.append("</div>")
    return "".join(out)


def r_sina(ls, ctx):
    out = [f'<p class="sina-ust"><span class="sina-skor" data-skor="{ctx["id"]}" aria-live="polite"></span>'
           f'<button type="button" class="sina-sifirla" data-sifirla="{ctx["id"]}" hidden>Yanıtları sil</button></p>'
           '<ol class="sina">']
    for i, l in enumerate(x for x in ls if x.startswith("- ")):
        m = re.match(r"^- (.*) — \*\*(Doğru|Yanlış)\.\*\* (.*)$", l)
        assert m, l
        dogru = "D" if m.group(2) == "Doğru" else "Y"
        out.append(f'<li class="sina-madde" data-dogru="{dogru}" data-no="{i}" data-ara>'
                   f'<p class="ifade">{link_all(mdi(m.group(1)))}</p>'
                   f'<div class="sina-dugmeler" role="group" aria-label="Bu ifade doğru mu, yanlış mı?">'
                   f'<button type="button" data-yanit="D">Doğru</button><button type="button" data-yanit="Y">Yanlış</button></div>'
                   f'<div class="sina-aciklama"><p><strong>{m.group(2)}.</strong> {link_all(mdi(m.group(3)))}</p></div></li>')
    out.append("</ol>")
    return "".join(out)


def r_akilda(ls, ctx):
    items = [l[2:] for l in ls if l.startswith("- ")]
    return '<ul class="akilda">' + "".join(f"<li data-ara>{link_all(mdi(i))}</li>" for i in items) + "</ul>"


def r_yeni(ls, ctx):
    items = [re.sub(r"^\d+\.\s*", "", l) for l in ls if re.match(r"^\d+\. ", l)]
    out = ['<ol class="fikirler fikirler-yeni">']
    for it in items:
        body, ref = split_tail(it)
        tail = f'<p class="ders-ref">{link_all(esc(ref))}</p>' if ref else ""
        out.append(f'<li data-ara><p>{link_all(mdi(body))}</p>{tail}</li>')
    out.append("</ol>")
    return "".join(out)


ADIM = [  # (başlık öneki, anahtar, kısa ad)
    ("🧠", "fikirler", "Beş ana fikir"), ("🎬", "ornekler", "Örnekler"), ("🔄 Derste", "derste", "Derste / bugün"),
    ("🔄 2024", "degisen", "Ne değişti?"), ("🔎", "kanit", "Kanıt kontrolü"), ("🧸", "crs", "ÇRS literatürü"),
    ("🩺", "vaka", "Mini vaka"), ("✅", "sina", "Kendini sına"), ("🎯", "akilda", "Akılda kalsın"),
    ("🖼", "sekiller", "Şekiller"), ("🆕", "yeni", "Ne yeni?"), ("🔁", "tekrar", "Hızlı tekrar"),
    ("📺", "sonrasi", "2024 sonrası"), ("📰", "guncel", "Güncel kanıt"), ("✍", "test", "Vaka soruları"),
    ("🧪", "sim", "Deneyin"),
]


def adim_of(title):
    for pre, key, short in ADIM:
        if title.startswith(pre):
            return key, short
    return slug(title), title


def render_block(b, ctx):
    key, short = adim_of(b["title"])
    title = b["title"]
    m = re.match(r"^(\S+)\s+(.*)$", title)
    ikon, text = (m.group(1), m.group(2)) if m and not m.group(1)[0].isalnum() else ("", title)
    ls = b["lines"]
    if key == "fikirler":
        body = r_fikirler(ls, ctx)
    elif key == "ornekler":
        body = r_ornekler(ls, ctx)
    elif key in ("derste", "kanit", "crs", "tekrar"):
        pre = [l for l in ls if l.strip() and not l.startswith("|") and not RX_FIG.match(l)]
        figs = [figure(int(RX_FIG.match(l).group(1))) for l in ls if RX_FIG.match(l)]
        tablo = render_table(ls, key, ctx) if key == "tekrar" else render_cards(ls, key, ctx)
        body = "".join(f'<p class="not">{link_all(mdi(p))}</p>' for p in pre) + tablo + "".join(figs)
    elif key == "degisen":
        body = render_cards(ls, key, ctx)
    elif key == "vaka":
        vt = re.sub(r"^🩺\s*Mini vaka:\s*", "", title)
        text = "Mini vaka"
        body = r_vaka(ls, ctx, vt)
    elif key == "sina":
        body = r_sina(ls, ctx)
    elif key == "akilda":
        body = r_akilda(ls, ctx)
    elif key == "sekiller":
        body = '<div class="sekiller">' + "".join(figure(int(RX_FIG.match(l).group(1))) for l in ls if RX_FIG.match(l)) + "</div>"
    elif key == "yeni":
        body = r_yeni(ls, ctx)
    else:
        body = render_generic(ls, ctx)
    sid = f'{ctx["id"]}-{key}'
    ctx["steps"].append((key, short, ikon))
    return adim_sar(sid, key, ikon, text, body)


def r_guncel(vid, ctx):
    items = GUNCEL.get(vid)
    if not items:
        return ""
    sid = f"{vid}-guncel"
    ctx["steps"].append(("guncel", "Güncel kanıt", "📰"))
    arts = []
    for baslik, metin, crs in items:
        yil = re.findall(r"(?:19|20)\d{2}\)", metin)
        yil = yil[-1][:4] if yil else ""
        arts.append(f'<article class="guncel" data-ara><p class="guncel-yil">{yil}</p><h4>{esc(baslik)}</h4>'
                    f'<p>{link_all(mdi(metin))}</p><p class="guncel-crs"><span class="guncel-etiket">ÇRS için</span> '
                    f'{link_all(mdi(crs))}</p></article>')
    return adim_sar(sid, "guncel", "📰", "Güncel kanıt",
                    '<p class="not">Notlara Kasım 2026’da eklendi. Sayılar PubMed’deki özetlerden alındı; künyeler kaynakçada.</p>'
                    f'<div class="guncel-liste">{"".join(arts)}</div>')


HARF = "ABCD"


def r_test(vid, ctx):
    qs = SORULAR.get(vid)
    if not qs:
        return ""
    sid = f"{vid}-test"
    ctx["steps"].append(("test", "Vaka soruları", "✍️"))
    out = [f'<p class="sina-ust"><span class="sina-skor" data-test-skor="{vid}" aria-live="polite"></span>'
           f'<button type="button" class="sina-sifirla" data-test-sifirla="{vid}" hidden>Yanıtları sil</button></p>'
           '<ol class="test">']
    for i, (soru, secenekler, dogru, aciklama, bolum) in enumerate(qs):
        assert 0 <= dogru < len(secenekler) <= 4
        btn = "".join(f'<button type="button" data-secenek="{k}"><span class="harf" aria-hidden="true">{HARF[k]}</span>'
                      f'<span>{link_all(mdi(sec), False)}</span></button>' for k, sec in enumerate(secenekler))
        git_ = (f' <a class="test-git" href="#/{vid}/{bolum}">İlgili bölüm →</a>' if bolum else "")
        out.append(f'<li class="test-madde" data-dogru="{dogru}" data-no="{i}" data-ara><p class="soru">{link_all(mdi(soru), False)}</p>'
                   f'<div class="secenekler" role="group" aria-label="Seçenekler">{btn}</div>'
                   f'<div class="test-aciklama"><p><strong>Doğru yanıt: {HARF[dogru]}.</strong> {link_all(mdi(aciklama))}{git_}</p></div></li>')
    out.append("</ol>")
    return adim_sar(sid, "test", "✍️", "Vaka soruları", "".join(out))


SIM_META = {
    "esik": ("Eşik oyunu", "Kesme puanını kaydırın: kim “hasta”, kim “sağlıklı” oluyor? Ali 68, Ayşe 71, Zeynep 96 puan "
             "aldı. Veriler şematiktir (Şekil 2)."),
    "kisasa": ("Kısasa kısas turnuvası", "Altı strateji birbiriyle 200’er tur mahkûm ikilemi oynar. Sinyal hatasını "
               "artırın ve sıralamanın nasıl değiştiğine bakın (Axelrod ve Hamilton 1981; Şekil 4)."),
    "kalitsallik": ("Bitki IQ’su", "Aynı tohum karışımını farklı topraklara ekin: genler hiç değişmezken kalıtsallık nasıl "
                    "değişiyor? Veriler şematiktir (Ders 07 [00:38:53]; Şekil 6)."),
    "hamilton": ("Hamilton kuralı", "Bir akraba seçin, yararı ve maliyeti ayarlayın: r × B > C sağlanıyor mu? "
                 "(Hamilton 1964; Şekil 3)"),
    "dopamin": ("Dopamin ve “belki”", "Ödül olasılığını değiştirin: dopamin nöronlarının iki ayrı yanıtı nasıl değişiyor? "
                "Şematik (Fiorillo ve ark. 2003; Şekil 15)."),
}


def r_sim(vid, ctx):
    keys = SIMULASYONLAR.get(vid)
    if not keys:
        return ""
    sid = f"{vid}-sim"
    ctx["steps"].append(("sim", "Deneyin", "🧪"))
    return adim_sar(sid, "sim", "🧪", "Deneyin", "".join(sim_kutu(k) for k in keys))


def sim_kutu(k):
    gorevler, soru, yanit = SIM_REHBER[k]
    return (f'<div class="sim" data-sim="{k}" id="sim-{k}"><h4>{esc(SIM_META[k][0])}</h4>'
            f'<p class="sim-aciklama">{link_all(mdi(SIM_META[k][1]))}</p>'
            f'<div class="sim-gorev"><p class="sim-etiket">Deneyin</p><ol>{"".join(f"<li>{esc(g)}</li>" for g in gorevler)}</ol></div>'
            f'<div class="sim-alan"></div><p class="sim-js-yok">Bu etkinlik için tarayıcıda JavaScript açık olmalı.</p>'
            f'<details class="sim-dusun"><summary><span class="sim-etiket">Ne gördünüz?</span> {esc(soru)}</summary>'
            f'<p>{link_all(mdi(yanit))}</p></details></div>')


DUR = re.compile(r"^\d+ sa \d+ dk$")


def lecture_range(s):
    m = re.match(r"(\d+)(?:–(\d+))?", s)
    a = int(m.group(1))
    return list(range(a, int(m.group(2) or a) + 1))


def names_2024(name):
    """'Limbic System 1–4' → [11, 12, 13, 14]"""
    name = re.sub(r"\s*\(.*\)$", "", name).strip()
    m = re.match(r"^(.*?) (\d+)–(\d+)$", name)
    wanted = [f"{m.group(1)} {i}" for i in range(int(m.group(2)), int(m.group(3)) + 1)] if m else [name]
    out = []
    for w in wanted:
        out += [i + 1 for i, t in enumerate(T2024) if t == w or (t.startswith(w + " ") and not m)]
    return out


def chip(series, n):
    return (f'<a class="ders-cip" href="{yt(series, n)}" target="_blank" rel="noopener" '
            f'title="YouTube’da aç (yeni sekme)"><span class="ders-no">{n:02d}</span> {esc(ytitle(series, n))}</a>')


def render_meta(line, ctx):
    rows, extra, dur = [], [], []
    for part in [p.strip() for p in line.split(" · ")]:
        p = part.replace("📼", "").strip()
        if p.startswith("Dersler:"):
            ns = lecture_range(re.sub(r"^Dersler:\s*Ders\s*", "", p))
            ctx["ders2010"] = ns
            rows.append(("2010 kaydı", "".join(chip(2010, n) for n in ns), PL2010))
        elif p.startswith("2024 serisinde:"):
            body = p.split(":", 1)[1].strip()
            note = re.search(r"\(([^)]*)\)\s*$", body)
            ns = []
            for nm in re.sub(r"\s*\([^)]*\)\s*$", "", body).split(";"):
                ns += names_2024(nm.strip())
            if note and note.group(1).startswith("+"):
                for nm in note.group(1)[1:].split(","):
                    ns += names_2024(nm.strip())
            ns = sorted(set(ns))
            tail = (f' <span class="ders-not">({esc(note.group(1))})</span>' if note and not note.group(1).startswith("+") else "")
            rows.append(("2024 serisi", "".join(chip(2024, n) for n in ns) + tail, PL2024))
        elif DUR.match(p):
            dur.append(p)
        elif names_2024(p):
            rows.append(("2024 serisi", "".join(chip(2024, n) for n in names_2024(p)), PL2024))
        elif p.startswith("🔗"):
            m = re.search(r"Oturum (\d+)", p)
            extra.append(f'<a href="#/oturum-{m.group(1)}">{esc(p.replace("🔗", "").strip())}</a>')
        elif p.startswith("🆕 Ayrıca:"):
            extra.append(f'<a href="{DEP2023}" target="_blank" rel="noopener">{esc(p.replace("🆕", "").strip())}</a>')
        else:
            extra.append(esc(p))
    out = []
    merged = {}
    for lab, h, pl in rows:
        merged.setdefault(lab, [h, pl])[0] += "" if merged[lab][0] == h else h
    for lab, (h, pl) in merged.items():
        out.append(f'<div class="dersler-satir"><a class="dersler-etiket" href="{pl}" target="_blank" rel="noopener" '
                   f'title="Oynatma listesi (YouTube)">{lab}</a><div class="dersler-cipler">{h}</div></div>')
    ozet = [f'{h.count("ders-cip")} ders ({lab.split()[0]})' for lab, (h, pl) in merged.items()]
    if dur:
        ozet.append(" + ".join(dur))
        dur = [("Süre (2010 kaydı): " if "2010 kaydı" in merged else "Süre: ") + " + ".join(dur)]
    info = " · ".join(dur + extra)
    if info:
        out.append(f'<p class="dersler-bilgi">{info}</p>')
    ctx["sure"] = dur[0].split(": ", 1)[1] if dur else ""
    return (f'<details class="dersler"><summary><span class="dersler-ozet-ad"><span aria-hidden="true">▶</span> Ders kayıtları</span> '
            f'<span class="dersler-ozet">{esc(" · ".join(ozet))}</span></summary>'
            f'<div class="dersler-ic">{"".join(out)}</div></details>')


# --- Görünümleri kur ---
VIEWS = []   # dict(id, label, short, html, card)


def session_view(sec):
    t = sec["title"]
    m = re.match(r"^Oturum (\d+) — (.+)$", t)
    me = re.match(r"^Ek Oturum (\d+) — (.+?) \((2024/[^)]+)\)$", t)
    if m:
        vid, num, title, kicker, short = f"oturum-{m.group(1)}", m.group(1), m.group(2), f"Oturum {m.group(1)}", f"Oturum {m.group(1)}"
    else:
        vid, num, title, kicker, short = f"ek-{me.group(1)}", me.group(1), me.group(2), f"Ek oturum {me.group(1)} · {me.group(3)}", f"Ek oturum {me.group(1)}"
    ctx = {"id": vid, "short": short, "steps": []}
    lead = [l for l in sec["lead"] if l.strip()]
    motto = lead[0].strip().strip("*").strip() if lead and lead[0].startswith("*") else ""
    meta_line = next((l for l in lead[1:] if l.startswith(("Dersler:", "📼"))), "")
    rest = [l for l in sec["lead"] if l.strip() and l.strip() not in (lead[0].strip() if motto else "", meta_line)]
    meta = render_meta(meta_line, ctx) if meta_line else ""
    parts = []
    keys = [adim_of(b["title"])[0] for b in sec["blocks"]]
    test_after = "sina" if "sina" in keys else "akilda"
    for b, k in zip(sec["blocks"], keys):
        parts.append(render_block(b, ctx))
        if k == "ornekler":
            parts.append(r_sim(vid, ctx))
        elif k == "crs":
            parts.append(r_guncel(vid, ctx))
        elif k == test_after:
            parts.append(r_test(vid, ctx))
    blocks = "".join(parts)
    pre = render_generic(rest, ctx) if rest else ""
    steps = "".join(f'<a href="#/{vid}/{k}" data-adim-bag="{k}"><span aria-hidden="true">{i}</span> {esc(s)}</a>'
                    for k, s, i in ctx["steps"])
    akilda = next((b for b in sec["blocks"] if b["title"].startswith("🎯")), None)
    sozcuk = len(re.sub(r"\([^()]*\d{4}[^()]*\)", "", " ".join(l for b in sec["blocks"] for l in b["lines"])).split())
    dakika = max(5, round(sozcuk * 1.3 / 160))
    bakista = ""
    if akilda:
        maddeler = "".join(f"<li>{link_all(mdi(l[2:]), False)}</li>" for l in akilda["lines"] if l.startswith("- "))
        bakista = (f'<aside class="bakista" aria-label="Tek bakışta"><p class="bakista-ust"><span class="bakista-ad">Tek bakışta</span>'
                   f'<span class="bakista-meta">Yaklaşık {dakika} dk okuma · {len(ctx["steps"])} bölüm</span></p>'
                   f'<ul>{maddeler}</ul></aside>')
    n_fig = sum(1 for l in sum((b["lines"] for b in sec["blocks"]), []) if RX_FIG.match(l))
    n_q = sum(1 for b in sec["blocks"] if b["title"].startswith("✅") for l in b["lines"] if l.startswith("- "))
    head = (f'<header class="oturum-bas"><p class="ust-baslik">{esc(kicker)}</p>'
            f'<h2 tabindex="-1">{esc(title)}</h2>'
            + (f'<p class="slogan">{link_all(mdi(motto), False)}</p>' if motto else "") + meta + "</header>")
    nav = (f'<nav class="adimlar" aria-label="Bu oturumun bölümleri">{steps}'
           f'<button type="button" class="adim-hepsi" aria-pressed="false">Tümünü daralt</button></nav>')
    body = (f'<section class="view oturum" id="v-{vid}" data-view="{vid}" data-baslik="{esc(short)}: {esc(title)}" '
            f'aria-label="{esc(short)}">{head}{bakista}{nav}{pre}{blocks}'
            f'<div class="oturum-son"><button type="button" class="okundu" data-okundu="{vid}" aria-pressed="false">'
            f'Bu oturumu okudum</button><nav class="ileri-geri" aria-label="Oturumlar arasında"></nav></div></section>')
    return {"id": vid, "label": short, "title": title, "motto": motto, "html": body, "kind": "oturum" if m else "ek",
            "num": num, "sure": ctx.get("sure", ""), "ders": ctx.get("ders2010"), "n_fig": n_fig, "n_q": n_q}


def simple_view(vid, label, title, kicker, inner, data_title=None):
    return {"id": vid, "label": label, "title": title,
            "html": (f'<section class="view" id="v-{vid}" data-view="{vid}" data-baslik="{esc(data_title or title)}" '
                     f'aria-label="{esc(label)}"><header class="oturum-bas"><p class="ust-baslik">{esc(kicker)}</p>'
                     f'<h2 tabindex="-1">{esc(title)}</h2></header>{inner}'
                     f'<div class="oturum-son"><nav class="ileri-geri" aria-label="Bölümler arasında"></nav></div></section>')}


SEC = {s["title"]: s for s in SECTIONS}
oturumlar = [session_view(s) for s in SECTIONS if s["title"].startswith("Oturum ")]

kap = next(s for s in SECTIONS if s["title"].startswith("Kapanış"))
ctx_k = {"id": "kapanis", "short": "Kapanış", "steps": []}
kap_inner = render_generic(kap["lead"], ctx_k) + "".join(render_block(b, ctx_k) for b in kap["blocks"])
kapanis = simple_view("kapanis", "Kapanış", kap["title"].split(":", 1)[1].strip().capitalize(), "Kapanış", kap_inner,
                      "Kapanış: " + kap["title"].split(":", 1)[1].strip())

ek = next(s for s in SECTIONS if s["title"].startswith("Ek — 2024"))
ctx_e = {"id": "ek-2024", "short": "Ek · 2024 serisi", "steps": []}
ek_lead = [l for l in ek["lead"] if l.strip()]
ek_motto = ek_lead[0].strip().strip("*").strip()
ek_meta = ek_lead[1]
ek_rest = [l for l in ek["lead"] if l.strip() not in (ek_lead[0].strip(), ek_meta.strip())]
ek_inner = (f'<p class="slogan">{mdi(ek_motto)}</p>'
            f'<p class="dersler-bilgi">{esc(ek_meta.replace("📼", "").strip())} · '
            f'<a href="{PL2024}" target="_blank" rel="noopener">Oynatma listesi ↗</a></p>'
            + render_generic(ek_rest, ctx_e) + "".join(render_block(b, ctx_e) for b in ek["blocks"]))
ek2024 = simple_view("ek-2024", "Ek · 2024 serisi", ek["title"].split(":", 1)[1].strip(), "Ek · 2024 serisi", ek_inner,
                     "Ek · 2024 serisi: " + ek["title"].split(":", 1)[1].strip())
ekler = [session_view(s) for s in SECTIONS if s["title"].startswith("Ek Oturum")]

# İddia ligi
counts = {}
for c in CLAIMS:
    counts[c["hukum"]] = counts.get(c["hukum"], 0) + 1
chips = ['<button type="button" class="filtre" data-filtre="" aria-pressed="true">Tümü '
         f'<span class="sayi">{len(CLAIMS)}</span></button>']
for sym in ("🟢", "🟡", "🔴", "✏"):
    cls, short, full = HUKUM[sym]
    if counts.get(cls):
        chips.append(f'<button type="button" class="filtre filtre-{cls}" data-filtre="{cls}" aria-pressed="false" '
                     f'title="{esc(full)}"><span aria-hidden="true">{sym}</span> {short} <span class="sayi">{counts[cls]}</span></button>')
claim_items = "".join(
    f'<li class="iddia" data-hukum="{c["hukum"]}" data-ara>'
    f'<div class="iddia-ust">{badge(c["sym"])} <a class="iddia-oturum" href="#/{c["view"]}/{"derste" if c["seri"] == "2010" else "kanit"}">'
    f'{esc(c["label"])} · {c["seri"]} dersi</a></div>'
    f'<p class="iddia-ders"><span class="iddia-etiket">Derste</span> {c["ders"]}</p>'
    f'<p class="iddia-bugun"><span class="iddia-etiket">{"Bugün" if c["seri"] == "2010" else "Kanıt"}</span> {c["bugun"]}</p></li>'
    for c in CLAIMS)
iddia_inner = ('<p class="giris-metin">Derslerde geçen iddiaların bugünkü kanıtla karşılaştırması: 2010 kayıtlarındaki '
               '“Derste öyle, bugün böyle” tablolarıyla 2024 serisinin “Kanıt kontrolü” tabloları bir arada. '
               'Süzgeçle bir hüküm türünü seçin; her satır ilgili oturuma bağlanır.</p>'
               '<div class="tahmin" id="iddialar-tahmin"><h3><span aria-hidden="true">🎯</span> Tahmin oyunu</h3>'
               f'<p>Sapolsky’nin derste söylediği iddiayı okuyun ve bugünkü hükmü tahmin edin: sağlam mı, tartışmalı mı, '
               f'çöktü mü, yoksa olgusal bir düzeltme mi gerekiyor? {len(CLAIMS)} iddia, karışık sırayla.</p>'
               '<div class="tahmin-alan" aria-live="polite"></div>'
               '<button type="button" class="dugme tahmin-basla">Oyunu başlat</button></div>'
               + figure(23, "sekil-genis", "sekil-23-lig")
               + f'<div class="filtreler" role="group" aria-label="Hükme göre süz">{"".join(chips)}</div>'
               + f'<p class="filtre-sonuc" aria-live="polite"></p><ol class="iddialar">{claim_items}</ol>')
iddialar = simple_view("iddialar", "İddia ligi", "İddia ligi: derste öyle, bugün böyle", "Araçlar", iddia_inner)

# Hızlı tekrar
akilda_groups = []
for v in oturumlar + ekler:
    sec = next(s for s in SECTIONS if (s["title"].startswith("Oturum " + v["num"] + " ") and v["kind"] == "oturum")
               or (s["title"].startswith("Ek Oturum " + v["num"] + " ") and v["kind"] == "ek"))
    b = next(b for b in sec["blocks"] if b["title"].startswith("🎯"))
    items = "".join(f"<li>{link_all(mdi(l[2:]), False)}</li>" for l in b["lines"] if l.startswith("- "))
    akilda_groups.append(f'<section class="tekrar-grup"><h3><a href="#/{v["id"]}">{esc(v["label"])}</a> '
                         f'<span>{esc(v["title"])}</span></h3><ul class="akilda akilda-kucuk">{items}</ul></section>')
N_SINA = sum(1 for s in SECTIONS for b in s["blocks"] if b["title"].startswith("✅") for l in b["lines"] if l.startswith("- "))
N_TEST = sum(len(v) for v in SORULAR.values())
LT_KUTU = [("Yeniden", "aynı gün"), ("1. kutu", "1 gün"), ("2. kutu", "3 gün"), ("3. kutu", "7 gün"), ("4. kutu", "21 gün")]
kart_secenek = "".join(f'<option value="{v["id"]}">{esc(v["label"])}: {esc(v["title"])}</option>' for v in oturumlar + ekler)
sim_bag = "".join(f'<li><a href="#/{vid}/sim" data-sim-git="sim-{k}">{esc(SIM_META[k][0])}</a> <span>{esc(next(v["label"] for v in oturumlar + ekler if v["id"] == vid))}</span></li>'
                  for vid, ks in SIMULASYONLAR.items() for k in ks)
calis_inner = (
    '<p class="giris-metin">Bütün alıştırmalar tek yerde. Yanıtladığınız her soru ve işaretlediğiniz her kart aralıklı tekrar '
    'kutularına girer: bildikleriniz daha seyrek, bilemedikleriniz daha sık karşınıza çıkar.</p>'
    '<section class="lt-panel" id="calis-tekrar" aria-labelledby="lt-b"><h3 id="lt-b"><span aria-hidden="true">🔁</span> Aralıklı tekrar</h3>'
    '<p class="lt-bilgi" aria-live="polite"></p><ol class="lt-kutular">'
    + "".join(f'<li class="lt-kutu lt-k{i}"><span class="lt-ad">{ad}</span><span class="lt-sayi" data-lt-kutu="{i}">0</span>'
              f'<span class="lt-aralik">{ar}</span></li>' for i, (ad, ar) in enumerate(LT_KUTU))
    + '</ol><div class="karisik-alan" aria-live="polite"></div><p class="karisik-dugmeler">'
    '<button type="button" class="dugme karisik-basla" data-tur="vade">Bugünün tekrarı</button> '
    '<button type="button" class="dugme dugme-ikincil karisik-basla" data-tur="yanlis">Yanlışlarım</button> '
    f'<button type="button" class="dugme dugme-ikincil karisik-basla" data-tur="sina">Doğru mu, yanlış mı? ({N_SINA})</button> '
    f'<button type="button" class="dugme dugme-ikincil karisik-basla" data-tur="test">Vaka soruları ({N_TEST})</button> '
    f'<button type="button" class="dugme dugme-ikincil karisik-basla" data-tur="hepsi">Hepsi karışık ({N_SINA + N_TEST})</button>'
    '</p><p class="sim-js-yok">Alıştırmalar için tarayıcıda JavaScript açık olmalı.</p></section>'
    '<section class="calis-bolum" id="calis-kartlar" aria-labelledby="kart-b"><h3 id="kart-b"><span aria-hidden="true">🃏</span> Bilgi kartları</h3>'
    '<p>Her oturumun beş ana fikri birer kart. Kartı çevirin; bildiklerinizi işaretleyin. Boşluk tuşu kartı çevirir.</p>'
    '<div class="kart-araclar"><label for="kart-suz">Oturum</label><select id="kart-suz">'
    f'<option value="">Bütün oturumlar</option>{kart_secenek}</select>'
    '<button type="button" class="dugme dugme-ikincil kart-karistir">Karıştır</button>'
    '<button type="button" class="sina-sifirla kart-sifirla">Bilinenleri sıfırla</button></div>'
    '<div class="kart-sahne" aria-live="polite"></div><p class="kart-ilerleme"></p></section>'
    '<section class="calis-bolum" id="calis-oyunlar" aria-labelledby="oyun-b"><h3 id="oyun-b"><span aria-hidden="true">🎮</span> Oyunlar ve deneyler</h3>'
    '<ul class="calis-kartlar">'
    f'<li><a href="#/vakalar"><span class="ck-ikon" aria-hidden="true">🎭</span><span class="ck-ad">Vaka simülasyonu</span>'
    f'<span class="ck-alt">{len(VAK.VAKALAR)} dallanan vakada kararları siz verin</span></a></li>'
    f'<li><a href="#/iddialar/tahmin"><span class="ck-ikon" aria-hidden="true">🎯</span><span class="ck-ad">Tahmin oyunu</span>'
    f'<span class="ck-alt">{len(CLAIMS)} iddianın bugünkü hükmünü tahmin edin</span></a></li></ul>'
    f'<p class="calis-etiket">Simülasyonlar</p><ul class="calis-sim">{sim_bag}</ul></section>'
    '<details class="calis-akilda" id="calis-akilda"><summary><span aria-hidden="true">🎯</span> Akılda kalsın: oturum oturum</summary>'
    + "".join(akilda_groups) + "</details>")
calis = simple_view("calis", "Çalış", "Çalış: tekrar, kartlar ve oyunlar", "Araçlar", calis_inner, "Çalış")

# Vaka simülasyonu (dallanan vakalar)
ETIKETLER = {v["id"]: v["label"] for v in oturumlar + ekler}


def dv_dogrula(v):
    sah = v["sahneler"]
    assert v["baslangic"] in sah, v["id"]
    for sid, x in sah.items():
        if "son" in x:
            assert x["son"] in ("iyi", "orta", "kotu") and x["baslik"] and x["metin"], (v["id"], sid)
            continue
        assert 2 <= len(x["secenekler"]) <= 4, (v["id"], sid)
        assert max(o[2] for o in x["secenekler"]) == 2, (v["id"], sid)
        for metin, hedef, puan, gb in x["secenekler"]:
            assert hedef in sah and puan in VAK.PUAN_ETIKET and metin and gb, (v["id"], sid, hedef)
    # her sahneye ulaşılır, döngü yoktur
    gorulen, yol = set(), []

    def gez(sid):
        assert sid not in yol, ("döngü", v["id"], sid)
        gorulen.add(sid)
        if "son" in sah[sid]:
            return
        yol.append(sid)
        for o in sah[sid]["secenekler"]:
            gez(o[1])
        yol.pop()
    gez(v["baslangic"])
    assert gorulen == set(sah), (v["id"], set(sah) - gorulen)


dv_veri, dv_kartlar = [], []
for v in VAK.VAKALAR:
    dv_dogrula(v)
    sahneler = {}
    for sid, x in v["sahneler"].items():
        if "son" in x:
            sahneler[sid] = {"son": x["son"], "baslik": esc(x["baslik"]), "metin": link_all(mdi(x["metin"]))}
        else:
            sahneler[sid] = {"metin": link_all(mdi(x["metin"])),
                             "secenekler": [[link_all(mdi(m), False), h, p, link_all(mdi(g))] for m, h, p, g in x["secenekler"]]}
    dv_veri.append({"id": v["id"], "baslik": esc(v["baslik"]), "baslangic": v["baslangic"], "sahneler": sahneler,
                    "sonSayi": sum(1 for x in v["sahneler"].values() if "son" in x),
                    "oturumlar": [[o, esc(l)] for o, l in v["oturumlar"]]})
    dv_kartlar.append(f'<li class="dv-kart" data-ara><h3>{esc(v["baslik"])}</h3><p>{esc(v["ozet"])}</p>'
                      f'<p class="kucuk">İlgili: ' + ", ".join(f'<a href="#/{o}/vaka">{esc(l)}</a>' for o, l in v["oturumlar"][:1])
                      + f' mini vakası</p><p class="dv-kart-durum kucuk" data-dv-durum="{v["id"]}"></p>'
                      f'<button type="button" class="dugme" data-dv="{v["id"]}">Vakayı başlat</button></li>')
dv_json = json.dumps({"puan": {str(k): t for k, t in VAK.PUAN_ETIKET.items()}, "vakalar": dv_veri},
                     ensure_ascii=False).replace("</", "<\\/")
N_SAHNE = sum(len(v["sahneler"]) for v in VAK.VAKALAR)
vaka_inner = (f'<p class="giris-metin">Oturumlardaki mini vakaların {len(VAK.VAKALAR)} tanesinde kararları siz veriyorsunuz. Vaka '
              'seçtiğiniz yola göre dallanır ve farklı sonlara varır. Her karardan sonra gerekçeyi okuyabilir, istediğiniz karara '
              'dönüp başka bir yolu deneyebilirsiniz.</p>'
              '<p class="dv-lejant">' + "".join(f'<span class="sp sp-{"n" if k < 0 else k}">{esc(t)}</span>'
                                               for k, t in VAK.PUAN_ETIKET.items()) + "</p>"
              f'<div class="dv" id="dv"><ol class="dv-liste">{"".join(dv_kartlar)}</ol><div class="dv-oyun" hidden></div>'
              '<p class="sim-js-yok">Vaka simülasyonu için tarayıcıda JavaScript açık olmalı.</p></div>'
              f'<script type="application/json" id="dv-veri">{dv_json}</script>'
              '<p class="not">Vakalar kurgusaldır. Sayılar ve atıflar notların kendi içeriğindendir; hukuki bilgiler ikincil '
              'kaynaklardan aktarılmıştır.</p>')
vakalar = simple_view("vakalar", "Vaka simülasyonu", "Vaka simülasyonu: kararları siz verin", "Araçlar", vaka_inner,
                      "Vaka simülasyonu")

# Kaynakça
kay_inner = [f'<p class="giris-metin">{link_all(mdi(next(l for l in KAY["lead"] if l.strip())), False)}</p>',
             '<p class="kaynak-ara"><label for="kaynak-suz">Kaynakçada süz</label>'
             '<input id="kaynak-suz" type="search" placeholder="Yazar, yıl ya da başlık" autocomplete="off"></p>'
             '<p class="kaynak-sonuc" aria-live="polite"></p>']
for b in KAY["blocks"]:
    kay_inner.append(f'<section class="kaynak-grup"><h3>{esc(b["title"])} <span class="sayi">{len(b["refs"])}</span></h3>'
                     '<ol class="kaynaklar">' + "".join(f'<li id="{r["id"]}" data-ara>{r["html"]}</li>' for r in b["refs"])
                     + "</ol></section>")
kaynakca = simple_view("kaynakca", "Kaynakça", "Kaynakça", "Araçlar", "".join(kay_inner))

# Giriş
intro = [l for l in INTRO if l.strip()]
lead_p = intro[0]
LEG = {}
for l in intro[1:]:
    m = re.match(r"^\*\*(.+?):\*\*\s*(.*)$", l)
    if m:
        LEG[m.group(1)] = m.group(2)
adimlar = LEG["Her oturumun yedi adımı"].split(". Sondaki")[0].split(" · ")
def buyuk_bas(t):
    i = next(k for k, ch in enumerate(t) if ch.isalpha())
    return t[:i] + {"i": "İ", "ı": "I"}.get(t[i], t[i].upper()) + t[i + 1:]


kurallar = [buyuk_bas(k) for k in LEG["Sapolsky’nin üç kuralı"].rstrip(".").split(" · ")]
hukumler = LEG["Hüküm işaretleri"].split(" · ")

neden = SEC["Neden çocuk psikiyatrisi?"]
yolculuk = SEC["Sapolsky’nin yolculuğu: 2010’dan bugüne"]
ctx_g = {"id": "giris", "short": "Giriş", "steps": []}
yol_items = [l for l in yolculuk["lead"] if l.startswith("- ")]
okumadan = next(l for l in yolculuk["lead"] if l.startswith("**Okumadan önce:**"))


def card(v):
    meta = []
    if v.get("ders"):
        d = v["ders"]
        meta.append(f"Ders {d[0]:02d}–{d[-1]:02d}" if len(d) > 1 else f"Ders {d[0]:02d}")
    if v.get("sure"):
        meta.append(v["sure"])
    if v.get("n_fig"):
        meta.append(f'{v["n_fig"]} şekil')
    num = v["num"] if v.get("num") else "★"
    return (f'<li><a class="kart kart-{v.get("kind", "diger")}" href="#/{v["id"]}" data-kart="{v["id"]}">'
            f'<span class="kart-no" aria-hidden="true">{num}</span><span class="kart-govde">'
            f'<span class="kart-ust">{esc(v["label"])}</span><span class="kart-baslik">{esc(v["title"])}</span>'
            + (f'<span class="kart-slogan">{mdi(v["motto"])}</span>' if v.get("motto") else "")
            + f'<span class="kart-meta">{esc(" · ".join(meta))}</span><span class="kart-durum" data-durum="{v["id"]}"></span>'
            f'</span></a></li>')


ek_card = {"id": "ek-2024", "label": "Ek · 2024 serisi", "title": "Sapolsky dersi yeniden anlatıyor",
           "motto": ek_motto, "kind": "ek", "num": "+", "sure": "32 ders · 38 sa 15 dk"}
kap_card = {"id": "kapanis", "label": "Kapanış", "title": "Sorumluluk, özgür irade ve hızlı tekrar", "kind": "kapanis",
            "num": "∞"}

giris_inner = f"""
<div class="kahraman">
  <p class="ust-baslik">Robert M. Sapolsky · Stanford Üniversitesi · <i lang="en">Human Behavioral Biology</i></p>
  <h1 tabindex="-1">{esc(H1.split(" — ")[0])}</h1>
  <p class="alt-baslik">Öğrenme notları · çocuk ve ergen psikiyatrisi gözüyle</p>
  <p class="kahraman-metin">{link_all(mdi(lead_p))}</p>
  <p class="kahraman-dugmeler"><a class="dugme" href="#/oturum-1">Oturum 1’den başla <span aria-hidden="true">→</span></a>
  <a class="dugme dugme-ikincil" href="#/calis">Çalış</a> <a class="dugme dugme-ikincil" href="#/vakalar">Vaka simülasyonu</a>
  <a class="dugme dugme-ikincil" href="#/iddialar">İddia ligi</a></p>
  <p class="devam" hidden><a class="devam-bag" href="#/"><span class="devam-ust">Kaldığınız yerden devam edin</span>
  <span class="devam-ad"></span></a></p>
  <aside class="yeni-not"><strong>Yeni (14 Kasım 2026):</strong> Oturum sayfaları sadeleşti: bölümler daraltılabiliyor, tablolar
  kart oldu, üstteki <b>Aa</b> düğmesiyle yazı boyutu ve tema seçiliyor. Alıştırmalar aralıklı tekrarla “Çalış” sayfasında
  toplandı; üç mini vaka dallanan simülasyona dönüştü. Güncel kanıt kutularına beş yeni çalışma eklendi
  ({len(EK_KAYNAKLAR)} çalışma, künyeleri PubMed’den doğrulandı).</aside>
</div>
<section class="ilerlemem" id="ilerlemem" hidden aria-labelledby="ilerleme-b"><h2 id="ilerleme-b" class="bolum-baslik">İlerlemem</h2>
<div class="ilerleme-kutular"></div>
<p class="kucuk">İlerleme yalnızca bu tarayıcıda saklanır. Okuma ayarlarınız silinmez. <button type="button" class="sina-sifirla hepsini-sil">Bütün ilerlemeyi sil</button></p></section>
<section class="kurallar" aria-labelledby="kurallar-b"><h2 id="kurallar-b" class="bolum-baslik">Sapolsky’nin üç kuralı</h2>
<ol>{"".join(f'<li data-ara><span class="kural-no">{i + 1}</span> {mdi(k)}</li>' for i, k in enumerate(kurallar))}</ol></section>
{figure(0, "sekil-genis")}
<section class="lejantlar">
  <div><h2 class="bolum-baslik">Her oturumun yedi adımı</h2><ol class="adim-lejant">{"".join(f"<li>{mdi(a)}</li>" for a in adimlar)}</ol>
  <p class="kucuk">Sondaki ek, 2024 serisini özetler.</p></div>
  <div><h2 class="bolum-baslik">Hüküm işaretleri</h2><ul class="hukum-lejant">{"".join(f"<li>{badge(h.split(' ', 1)[0])} <span>{esc(h.split(' ', 1)[1])}</span></li>" for h in hukumler)}</ul></div>
</section>
<section aria-labelledby="oturumlar-b"><h2 id="oturumlar-b" class="bolum-baslik">2010 dersleri: sekiz oturum</h2>
<ol class="kartlar">{"".join(card(v) for v in oturumlar)}{card(kap_card)}</ol></section>
<section aria-labelledby="ek-b"><h2 id="ek-b" class="bolum-baslik">Ek · 2024 serisi</h2>
<ol class="kartlar">{card(ek_card)}{"".join(card(v) for v in ekler)}</ol></section>
<section class="neden" aria-labelledby="neden-b"><h2 id="neden-b" class="bolum-baslik">{esc(neden["title"])}</h2>
{render_generic(neden["lead"], ctx_g)}</section>
<section class="yolculuk" aria-labelledby="yol-b"><h2 id="yol-b" class="bolum-baslik">{esc(yolculuk["title"])}</h2>
<ol class="zaman">{"".join(f"<li data-ara>{link_all(mdi(l[2:]))}</li>" for l in yol_items)}</ol>
<aside class="uyari" data-ara>{link_all(mdi(okumadan))}</aside></section>
"""
giris = {"id": "giris", "label": "Giriş", "title": "Davranışın Biyolojisi",
         "html": f'<section class="view aktif" id="v-giris" data-view="giris" data-baslik="Giriş" aria-label="Giriş">{giris_inner}</section>'}

ORDER = [giris] + oturumlar + [kapanis, ek2024] + ekler + [calis, vakalar, iddialar, kaynakca]


def nav_item(v):
    num = v.get("num") or ""
    return (f'<li><a href="#/{v["id"]}" data-nav="{v["id"]}"><span class="nav-no" aria-hidden="true">{esc(num)}</span>'
            f'<span class="nav-ad">{esc(v["title"] if v.get("kind") in ("oturum", "ek") else v["label"])}</span>'
            f'<span class="nav-durum" data-durum-nav="{v["id"]}"></span></a></li>')


nav = (f'<nav class="yan" id="yan" aria-label="Rehber içeriği"><div class="yan-ic">'
       f'<ol class="nav-liste"><li><a href="#/" data-nav="giris"><span class="nav-no" aria-hidden="true">⌂</span>'
       f'<span class="nav-ad">Giriş</span></a></li></ol>'
       f'<p class="nav-baslik">2010 dersleri</p><ol class="nav-liste">{"".join(nav_item(v) for v in oturumlar)}'
       f'{nav_item(dict(kapanis, num="∞"))}</ol>'
       f'<p class="nav-baslik">Ek · 2024 serisi</p><ol class="nav-liste">{nav_item(dict(ek2024, num="+"))}'
       f'{"".join(nav_item(v) for v in ekler)}</ol>'
       f'<p class="nav-baslik">Araçlar</p><ol class="nav-liste">{nav_item(dict(calis, num="🔁"))}{nav_item(dict(vakalar, num="🎭"))}'
       f'{nav_item(dict(iddialar, num="⚖"))}{nav_item(dict(kaynakca, num="§"))}</ol>'
       f'<p class="ilerleme" data-ilerleme></p></div></nav>')

DESC = ("Robert Sapolsky’nin Stanford “Human Behavioral Biology” derslerinden (2010, 2024) çocuk ve ergen psikiyatrisi "
        "gözüyle hazırlanmış etkileşimli öğrenme notları: 11 oturum, 29 şekil, dallanan vaka simülasyonları, aralıklı tekrar, "
        "simülasyonlar ve PubMed’den doğrulanmış kaynaklar.")

page = f"""<!doctype html>
<html lang="tr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>Davranışın Biyolojisi · Sapolsky’nin dersleri üzerine öğrenme notları · Doç. Dr. Miraç Barış Usta</title>
<meta name="description" content="{esc(DESC)}">
<meta name="author" content="Miraç Barış Usta">
<meta name="theme-color" content="#fbf7f0">
<meta property="og:title" content="Davranışın Biyolojisi: Sapolsky’nin dersleri üzerine öğrenme notları">
<meta property="og:description" content="{esc(DESC)}">
<meta property="og:type" content="website">
<meta property="og:url" content="https://miracbarisusta.com/davranisin-biyolojisi/">
<link rel="canonical" href="https://miracbarisusta.com/davranisin-biyolojisi/">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&amp;family=Lora:ital,wght@0,600;0,700;1,500&amp;display=swap">
<link rel="stylesheet" href="rehber.css">
<script src="rehber.js" defer></script>
</head>
<body>
<a class="atla" href="#icerik">İçeriğe geç</a>
<header class="ust">
  <a class="geri" href="https://miracbarisusta.com/rehberler/"><span aria-hidden="true">←</span> Rehberler</a>
  <a class="marka" href="#/">Davranışın Biyolojisi</a>
  <div class="ara" role="search">
    <label class="gizli" for="ara">Notlarda ara</label>
    <input id="ara" type="search" placeholder="Notlarda ara…" autocomplete="off" aria-controls="ara-sonuc">
    <div class="ara-sonuc" id="ara-sonuc" hidden></div>
  </div>
  <div class="ayar">
    <button type="button" class="ayar-dugme" aria-controls="ayar-panel" aria-expanded="false" aria-label="Okuma ayarları">Aa</button>
    <div class="ayar-panel" id="ayar-panel" hidden>
      <p class="ayar-ad" id="ayar-yazi-b">Yazı boyutu</p>
      <div class="ayar-grup" role="group" aria-labelledby="ayar-yazi-b">
        <button type="button" data-yazi="0" aria-pressed="false">Küçük</button><button type="button" data-yazi="1" aria-pressed="true">Orta</button>
        <button type="button" data-yazi="2" aria-pressed="false">Büyük</button><button type="button" data-yazi="3" aria-pressed="false">Çok büyük</button></div>
      <p class="ayar-ad" id="ayar-tema-b">Tema</p>
      <div class="ayar-grup" role="group" aria-labelledby="ayar-tema-b">
        <button type="button" data-tema="" aria-pressed="true">Cihaz</button><button type="button" data-tema="acik" aria-pressed="false">Açık</button>
        <button type="button" data-tema="koyu" aria-pressed="false">Koyu</button></div>
      <p class="ayar-ad" id="ayar-satir-b">Satır aralığı</p>
      <div class="ayar-grup" role="group" aria-labelledby="ayar-satir-b">
        <button type="button" data-satir="0" aria-pressed="true">Olağan</button><button type="button" data-satir="1" aria-pressed="false">Geniş</button></div>
    </div>
  </div>
  <button type="button" class="menu-dugme" aria-controls="yan" aria-expanded="false">Bölümler</button>
  <div class="okuma-cizgi" aria-hidden="true"><span></span></div>
</header>
<div class="duzen">
{nav}
<main id="icerik" tabindex="-1">
{"".join(v["html"] for v in ORDER)}
</main>
</div>
<footer class="alt">
  <p><strong>Hazırlayan:</strong> Doç. Dr. Miraç Barış Usta · Kasım 2026 · <a href="https://miracbarisusta.com">miracbarisusta.com</a></p>
  <p>Robert M. Sapolsky’nin Stanford Üniversitesi’ndeki <i lang="en">Human Behavioral Biology</i> derslerinin
  (<a href="{PL2010}" target="_blank" rel="noopener">2010</a>; <a href="{PL2024}" target="_blank" rel="noopener">2024</a>)
  Türkçe özetine ve güncel literatürle karşılaştırılmasına dayanır; dersin birebir aktarımı değildir. Ders kayıtları
  Stanford Üniversitesi’ne aittir. Bu çalışma Stanford Üniversitesi ya da Robert Sapolsky ile bağlantılı değildir.</p>
  <p>Eğitim amaçlıdır; bilgiler Kasım 2026 itibarıyladır. Vakalar kurgusaldır; ilaç ve tedavi bilgileri öğrenme amaçlıdır.
  Hukuki bilgiler ikincil kaynaklardandır, kullanmadan önce güncel metinden doğrulanmalıdır.</p>
  <p>© 2026 Miraç Barış Usta · <a href="https://github.com/hypothermia15/davranisin-biyolojisi/blob/main/LICENSE">Kullanım koşulları</a></p>
</footer>
<dialog class="isik" id="isik" aria-label="Şekil">
  <div class="isik-ust"><p class="isik-no"></p>
    <a class="isik-tam" href="#" target="_blank" rel="noopener">Tam boyut ↗</a>
    <button type="button" class="isik-kapat" aria-label="Kapat">✕</button></div>
  <div class="isik-resim"><img alt=""></div>
  <p class="isik-alt"></p>
  <div class="isik-gezinti"><button type="button" class="isik-onceki" aria-label="Önceki şekil">←</button>
    <button type="button" class="isik-sonraki" aria-label="Sonraki şekil">→</button></div>
</dialog>
<div class="atif-pop" id="atif-pop" role="dialog" aria-label="Kaynak" hidden></div>
</body>
</html>
"""
(OUT / "index.html").write_text(page, encoding="utf-8")
n_cite = page.count('class="atif"')
print(f"{len(ORDER)} görünüm, {len(FIGS)} şekil, {len(REFS)} kaynak, {len(CLAIMS)} iddia, {len(VAK.VAKALAR)} dallanan vaka "
      f"({N_SAHNE} sahne), {sum(len(x) for x in GUNCEL.values())} güncel kanıt, {n_cite} atıf bağlantısı, "
      f"{page.count('class=\"zd\"')} zaman damgası → {OUT / 'index.html'} ({len(page) // 1024} KB)")
paren_unmatched = sorted(u for u in UNMATCHED if re.search(r"(ve ark\.|ve [A-Z])", u) or len(u.split()) <= 3)
if paren_unmatched:
    print("Eşleşmeyen atıflar:", "; ".join(paren_unmatched[:80]))
