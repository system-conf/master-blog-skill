#!/usr/bin/env python3
"""master-blog: skill dosyalarindan ve terim verisinden siteyi ve skill referansini uretir.

Cikis kodlari: 0 basarili · 1 veri/dogrulama hatasi · 2 ortam hatasi (node yok vb.)
"""
import json, re, subprocess, pathlib, sys
from datetime import date

ROOT    = pathlib.Path(__file__).parent
SKILL   = ROOT / "skills" / "master-blog"
SITE    = ROOT / "site"
DOCS    = ROOT / "docs"          # GitHub Pages: her sayfa gercek bir URL
DIST    = ROOT / "dist"          # Artifact: tek dosya, hash yonlendirme
TERMSJS = SITE / "data" / "terms.js"

BASE     = "/master-blog-skill/"
SITE_URL = "https://system-conf.github.io" + BASE
REPO_URL = "https://github.com/system-conf/master-blog-skill"
TAGLINE  = ("Claude icin uctan uca SEO/GEO blog uretim skill'i: 13 asamali surec, "
            "kanibalizasyon ve oz denetim kapilari, 40 maddelik yayin oncesi kontrol "
            "ve 41 terimlik sozluk.")

KATEGORI_SIRASI = ["Claude", "SEO", "İçerik", "Teknik"]
SEVIYELER  = ["Başlangıç", "Orta", "İleri", "Uzman"]
ZORUNLU    = ["slug", "name", "en", "cat", "level", "short", "simple",
              "technical", "why", "example", "myth", "related", "usedIn"]


def hata(mesaj, kod=1):
    print(f"BUILD HATASI: {mesaj}", file=sys.stderr)
    sys.exit(kod)


# ---------------------------------------------------------------- 1) veriyi oku
def kacis_denetle():
    """terms.js sablon dizelerinde kacilmamis ${...} interpolasyonu var mi?
    Bir kez gercek bir hataya sebep oldu: ${CLAUDE_PLUGIN_ROOT} degisken sanildi."""
    ham = TERMSJS.read_text(encoding="utf-8")
    kotu = [i + 1 for i, satir in enumerate(ham.split("\n"))
            if re.search(r"(?<!\\)\$\{", satir)]
    if kotu:
        hata("terms.js icinde kacilmamis ${...} var (satir: "
             + ", ".join(map(str, kotu)) + "). Kullanmak icin \\${...} yaz.")


def terimleri_oku():
    js = ("const fs=require('fs');"
          f"const t=eval(fs.readFileSync({json.dumps(str(TERMSJS))},'utf8')+'; TERMS');"
          "process.stdout.write(JSON.stringify(t));")
    try:
        p = subprocess.run(["node", "-e", js], capture_output=True, text=True)
    except FileNotFoundError:
        hata("node bulunamadi. terms.js okunamiyor (kurulum: https://nodejs.org).", 2)
    if p.returncode != 0:
        hata("terms.js okunamadi. node ciktisi:\n" + (p.stderr.strip() or "(bos)"))
    return json.loads(p.stdout)


# ------------------------------------------------------------- 2) veriyi dogrula
def dogrula(terms):
    sorunlar, slugs = [], {}
    for i, t in enumerate(terms):
        ad = t.get("slug") or f"#{i}"
        for alan in ZORUNLU:
            if not t.get(alan):
                sorunlar.append(f"{ad}: '{alan}' alani eksik veya bos")
        if t.get("slug"):
            if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", t["slug"]):
                sorunlar.append(f"{ad}: slug kebab-case degil")
            if t["slug"] in slugs:
                sorunlar.append(f"{ad}: slug tekrar ediyor")
            slugs[t["slug"]] = t
        if t.get("level") and t["level"] not in SEVIYELER:
            sorunlar.append(f"{ad}: bilinmeyen seviye '{t['level']}' (gecerli: {', '.join(SEVIYELER)})")
        for k in t.get("src") or []:
            if not (isinstance(k, dict) and k.get("t") and str(k.get("u", "")).startswith("https://")):
                sorunlar.append(f"{ad}: src girdisi {{t, u}} bicimli ve https:// olmali")
    for t in terms:
        for r in t.get("related") or []:
            if r not in slugs:
                sorunlar.append(f"{t.get('slug')}: related '{r}' hicbir terime karsilik gelmiyor")
            elif r == t.get("slug"):
                sorunlar.append(f"{t.get('slug')}: related kendine referans veriyor")
    # yetim terim: sozlukte hicbir terimin baglanti vermedigi terim
    gelen = {t["slug"]: 0 for t in terms if t.get("slug")}
    for t in terms:
        for r in t.get("related") or []:
            if r in gelen:
                gelen[r] += 1
    for slug, n in gelen.items():
        if n == 0:
            sorunlar.append(f"{slug}: hicbir terim buna baglanti vermiyor (yetim terim)")
    if sorunlar:
        hata(f"{len(sorunlar)} veri sorunu:\n  - " + "\n  - ".join(sorunlar))


# ------------------------------------------------- 3) skill terim sozlugunu uret
def sozluk_yaz(terms):
    kategoriler = KATEGORI_SIRASI + [c for c in dict.fromkeys(t["cat"] for t in terms)
                                     if c not in KATEGORI_SIRASI]
    seviye_sira = {s: i for i, s in enumerate(SEVIYELER)}
    ad = {t["slug"]: t["name"] for t in terms}
    satir = ["# Terimler Sözlüğü", "",
             f"Bu dosya `site/data/terms.js` dosyasından üretilir; elle düzenlenmez. {len(terms)} terim.",
             "",
             "Kullanıcıya bir terimi açıklarken buradaki yapıyı kullan: tanım → basit anlatım →",
             "teknik anlatım → neden önemli → örnek → yaygın yanılgı.",
             "",
             "## İçindekiler", ""]
    for cat in kategoriler:
        grup = [t for t in terms if t["cat"] == cat]
        if grup:
            satir.append(f"- **{cat}**: " + ", ".join(t["name"] for t in grup))
    satir.append("")
    yazilan = 0
    for cat in kategoriler:
        grup = sorted([t for t in terms if t["cat"] == cat],
                      key=lambda t: (seviye_sira.get(t["level"], 99), t["name"]))
        if not grup:
            continue
        satir += [f"## {cat}", ""]
        for t in grup:
            yazilan += 1
            satir += [f"### {t['name']} ({t['en']})", "",
                      f"`{t['cat']}` · `{t['level']}` · skill'de: {t['usedIn']}", "",
                      f"**Tanım.** {t['short']}", "",
                      "**Basitçe.**", "", t["simple"], "",
                      "**Teknik olarak.**", "", t["technical"], "",
                      "**Neden önemli.**", "", t["why"], "",
                      "**Örnek.**", "", t["example"], "",
                      "**Yaygın yanılgı.**", "", t["myth"], "",
                      "**İlgili terimler:** " + ", ".join(ad[r] for r in t["related"]), ""]
            if t.get("src"):     # kaynaklar sitede vardi ama skill'e hic ulasmiyordu
                satir += ["**Doğrulanmış kaynaklar.**", ""]
                satir += [f"- [{k['t']}]({k['u']})" for k in t["src"]]
                satir += [""]
            satir += ["---", ""]
    if yazilan != len(terms):
        hata(f"{len(terms) - yazilan} terim hicbir kategoriye yazilamadi (sessiz veri kaybi)")
    (SKILL / "references" / "terimler-sozlugu.md").write_text("\n".join(satir), encoding="utf-8")


# ------------------------------------------------------- 4) skill dosyalari + kurulum
ORDER = ["SKILL.md",
         "references/yayin-oncesi-kontrol.md",
         "references/terimler-sozlugu.md",
         "references/schema-ve-geo.md",
         "references/kaynaklar.md",
         "references/kullanim-senaryolari.md",
         "references/yazim-katmanlari.md",
         "references/yayin-ve-olcum.md",
         "references/medya-brief.md",
         "references/uslup.md",
         "scripts/kontrol.py",
         "scripts/surum-kontrol.py",
         "scripts/olcum.py",
         "scripts/skill-denetim.py",
         "evals/evals.json"]
HEREDOC = "MASTERBLOG_EOF"


def gorsel_yollari(yazilar, mod):
    """Blog gorsel yollarini hedef ortama gore yeniden yazar.

    Kaynak markdown 'gorseller/x.svg' yazar (yazarin gorecegi en dogal bicim).
    - static : BASE + 'blog/gorseller/x.svg'  (goreli yol sayfa dizinine gore kayardi)
    - spa    : data: URI  (Artifact CSP'si dis kaynakli gorseli engelliyor)
    """
    import base64, urllib.parse
    kopya = []
    for y in yazilar:
        govde = y["govde"]

        def cev(m):
            ad = m.group(1)
            if mod == "static":
                return "](" + BASE + "blog/gorseller/" + ad
            p = SITE / "blog" / "gorseller" / ad
            if not p.exists():
                hata(f"gorsel bulunamadi: {p}")
            if p.suffix == ".svg":
                return "](data:image/svg+xml," + urllib.parse.quote(p.read_text(encoding="utf-8"))
            tur = {".png": "image/png", ".jpg": "image/jpeg", ".webp": "image/webp"}.get(p.suffix)
            if not tur:
                hata(f"desteklenmeyen gorsel turu: {p.name}")
            return "](data:" + tur + ";base64," + base64.b64encode(p.read_bytes()).decode()

        govde = re.sub(r"\]\(gorseller/([^)\s\"]+)", cev, govde)
        kopya.append({**y, "govde": govde})
    return kopya


def yazilari_oku():
    """site/blog/*.md -> POSTS. Frontmatter + gövde; en yeni tarih önce."""
    yazilar = []
    dizin = SITE / "blog"
    for p in sorted(dizin.glob("*.md")) if dizin.exists() else []:
        ham = p.read_text(encoding="utf-8-sig")
        m = re.match(r"^---\n(.*?)\n---\n?(.*)$", ham, re.S)
        if not m:
            hata(f"{p.name}: frontmatter bulunamadi")
        fm = {}
        for satir in m.group(1).split("\n"):
            mm = re.match(r'^([a-zA-Z]+):\s*(.*)$', satir)
            if mm:
                deger = mm.group(2).strip()
                if deger.startswith("["):
                    deger = [x.strip().strip('"') for x in deger.strip("[]").split(",") if x.strip()]
                else:
                    deger = deger.strip('"')
                fm[mm.group(1)] = deger
        for alan in ("baslik", "seoBaslik", "ozet", "tarih"):
            if not fm.get(alan):
                hata(f"{p.name}: '{alan}' alani eksik")
        if len(fm["seoBaslik"]) > 60:
            hata(f"{p.name}: seoBaslik {len(fm['seoBaslik'])} karakter (ust sinir 60)")
        yazilar.append({"slug": p.stem, "baslik": fm["baslik"], "seoBaslik": fm["seoBaslik"],
                        "ozet": fm["ozet"], "tarih": fm["tarih"],
                        "hedefKelimeler": fm.get("hedefKelimeler", []),
                        "dakika": fm.get("dakika", ""), "govde": m.group(2).strip()})
    return sorted(yazilar, key=lambda y: y["tarih"], reverse=True)


def dosyalari_topla():
    files = []
    for rel in ORDER:
        p = SKILL / rel
        if not p.exists():
            hata(f"skill dosyasi bulunamadi: {rel}")
        files.append({"name": p.name, "path": f"master-blog/{rel}",
                      "text": p.read_text(encoding="utf-8")})
    return files


AYLAR_TR = ["Oca", "Şub", "Mar", "Nis", "May", "Haz", "Tem", "Ağu", "Eyl", "Eki", "Kas", "Ara"]


def tarih_tr(iso):
    """2026-09-08 -> 8 Eyl 2026"""
    if not iso:
        return ""
    y, a, g = iso.split("-")
    return f"{int(g)} {AYLAR_TR[int(a) - 1]} {y}"


def degisiklikleri_oku():
    """CHANGELOG.md -> [{surum, tarih, ozet}] — sürüm geçmişi tablosu buradan üretilir."""
    p = ROOT / "CHANGELOG.md"
    if not p.exists():
        return []
    kayitlar = []
    for blok in re.split(r"^## ", p.read_text(encoding="utf-8"), flags=re.M)[1:]:
        bas = re.match(r"\[([\d.]+)\]\s*—\s*(\S+)", blok)
        if not bas:
            continue
        maddeler = re.findall(r"^- \*\*(.+?)\*\*|^- (.+)$", blok, re.M)
        ozet = [(a or b).rstrip(".").strip() for a, b in maddeler[:3]]
        kayitlar.append({"surum": bas.group(1), "tarih": bas.group(2),
                         "ozet": [re.sub(r"`|\*\*", "", x)[:110] for x in ozet]})
    return kayitlar


def kur_scripti():
    """~2 KB, okunabilir kurulum scripti. Dosyaları docs/paket/ altından çeker,
    yani her zaman YAYINLANMIŞ GÜNCEL sürümü kurar (240 KB'lık pano yöntemi
    dondurulmuş bir kopya kuruyordu)."""
    dosyalar = " \\\n     ".join(ORDER)
    return f"""#!/bin/sh
# master-blog · kurulum
# Kaynak : {REPO_URL}
# Ne yapar: {len(ORDER)} dosyayı indirir, hedef dizine yazar, kurulumu doğrular.
# Başka hiçbir şey yapmaz — ne PATH'e dokunur, ne kabuk profiline, ne ağa veri yollar.
set -eu

PAKET="{SITE_URL}paket"
HEDEF="$HOME/.claude/skills/master-blog"
KAPSAM="kişisel (tüm projeler)"

if [ "${{1:-}}" = "--proje" ]; then
  HEDEF="$(pwd)/.claude/skills/master-blog"
  KAPSAM="projeye özel ($(pwd))"
elif [ "${{1:-}}" = "--yardim" ] || [ "${{1:-}}" = "-h" ]; then
  echo "Kullanım: sh kur.sh [--proje]"
  echo "  (bayraksız)  ~/.claude/skills/master-blog altına kurar"
  echo "  --proje      bulunduğun projenin .claude/skills/ dizinine kurar"
  exit 0
fi

DOSYALAR="{dosyalar}"

echo "master-blog kuruluyor"
echo "  hedef  : $HEDEF"
echo "  kapsam : $KAPSAM"

mkdir -p "$HEDEF/references" "$HEDEF/scripts" "$HEDEF/evals"

for f in $DOSYALAR; do
  printf '  %s ' "$f"
  if curl -fsSL "$PAKET/$f" -o "$HEDEF/$f"; then echo "ok"; else echo "BAŞARISIZ"; exit 1; fi
done

chmod +x "$HEDEF/scripts/"*.py 2>/dev/null || true

echo
echo "Doğrulama:"
if command -v python3 >/dev/null 2>&1; then
  python3 "$HEDEF/scripts/surum-kontrol.py" --cevrimdisi || true
else
  echo "  python3 bulunamadı — skill çalışır ama mekanik kontrol scripti çalışmaz."
fi

echo
echo "Kuruldu. Yeni bir Claude oturumu başlat ve dene:"
echo "  master-blog skill'iyle içerik envanterimi çıkar"
"""


def kurulum_komutu(files):
    cmd = ["mkdir -p ~/.claude/skills/master-blog/{references,scripts,evals}"]
    for rel, f in zip(ORDER, files):
        if HEREDOC in f["text"]:      # assert degil: python3 -O ile devre disi kalmasin
            hata(f"heredoc sinirlayicisi dosyada geciyor: {rel}")
        cmd.append(f"cat > ~/.claude/skills/master-blog/{rel} <<'{HEREDOC}'\n{f['text'].rstrip()}\n{HEREDOC}")
    cmd.append("chmod +x ~/.claude/skills/master-blog/scripts/kontrol.py")
    cmd.append('echo "master-blog kuruldu -> ~/.claude/skills/master-blog (yeni bir Claude oturumu baslat)"')
    return "\n".join(cmd) + "\n"


# ------------------------------------------------------------------ 5) siteyi uret
def js_gomme_guvenli(s):
    """HTML spec: script literalinde <!--, <script ve </script dizileri ASCII buyuk/kucuk
    harf duyarsiz kacilmali. Onceki surum yalnizca kucuk harfli </script> icin kaciyordu."""
    return re.sub(r"(?i)<(!--|/?script)", lambda m: "\\x3C" + m.group(1), s)


SAYFALAR = [
    ("",               "Master Blog Skill",
     "Claude'a bir web proje­sinde içerik üretmenin tam sürecini öğreten açık kaynak skill: "
     "veriden konu seçimi, kanibalizasyon denetimi, SEO + GEO + E-E-A-T katmanları ve 40 maddelik yayın kapısı."),
    ("skill",          "Skill Dokümantasyonu — Master Blog Skill",
     "master-blog skill'inin 13 aşamalı süreci, iki atlanamaz kapısı, altı dosyası, örnek promptları "
     "ve mekanik kontrol scripti: ne yaptığı ve ne yapmadığı."),
    ("senaryolar",     "Kullanım Senaryoları — Master Blog Skill",
     "master-blog skill'i hangi proje tipinde nasıl davranır: yerel hizmet, üretici/B2B, e-ticaret, "
     "SaaS, klinik ve ajans profilleri; çalışma modu, ilk hafta planı ve eşik uyarlama tablosu."),
    ("nasil-calisir",  "Claude Skills Nasıl Çalışır — Master Blog Skill",
     "Claude Skill nedir, dosya yapısı nasıldır, kademeli açılım nasıl işler ve iyi bir skill neye benzer — "
     "hiç bilmeyen biri için baştan sona."),
    ("terimler",       "Terim Sözlüğü — Master Blog Skill",
     "Claude, SEO, GEO ve içerik dünyasından 41 terim; her biri tanım, basit anlatım, teknik anlatım, "
     "örnek ve yaygın yanılgısıyla."),
    ("kurulum",        "Kurulum — Master Blog Skill",
     "master-blog skill'ini Claude Code ve Claude uygulamasına ekleme yöntemleri: tek komut, depo klonlama "
     "ve elle kurulum."),
    ("blog",           "Blog — Master Blog Skill",
     "Skill'in kendi süreciyle üretilmiş yazılar: yapay zeka içeriğinde sık yapılan hatalar, "
     "teşhis yöntemleri ve ölçüm disiplini."),
    ("kaynaklar",      "Kaynaklar ve Doğrulama Kaydı — Master Blog Skill",
     "Skill'deki zamana bağlı her iddianın tarihi, kaynak sınıfı ve doğrulanmış bağlantısı. "
     "Son doğrulama: 7 Eylül 2026."),
]


def onrender(bundle, yollar):
    """Node ile her rotanin HTML'ini onceden uretir (statik sayfalar icin)."""
    js = """
const APP = {innerHTML:'', classList:{add(){},remove(){},toggle(){}}, offsetWidth:1,
  querySelector:()=>null, setAttribute(){}, focus(){}};
const el = new Proxy(function(){}, {get:(t,k)=>{
  if(k==='classList') return {add(){},remove(){},toggle(){},contains(){return false}};
  if(k==='dataset') return {}; if(k==='style') return {}; if(k==='value') return '';
  if(k==='offsetWidth') return 1; if(k==='getAttribute') return ()=>'';
  if(['addEventListener','scrollIntoView','focus','setAttribute','removeAttribute'].includes(k)) return ()=>{};
  return el; }, set:()=>true, apply:()=>el});
global.document={querySelector:s=>s==='#app'?APP:el, querySelectorAll:()=>[],
  getElementById:()=>null, addEventListener:()=>{}, createElement:()=>el, body:el, title:''};
global.window={addEventListener:()=>{}, self:1, top:1, scrollTo:()=>{}, open:()=>{}};
global.localStorage={getItem:()=>null,setItem:()=>{}};
global.navigator={clipboard:{}};
global.history={pushState:()=>{}};
global.setTimeout=()=>0; global.clearTimeout=()=>{};
global.location={pathname:'BASE_YER', search:'', hash:'', href:''};
const BUNDLE = require('fs').readFileSync(process.argv[2],'utf8');
const YOLLAR = JSON.parse(process.argv[3]);
const cikti = {};
eval(BUNDLE + `
;YOLLAR.forEach(y=>{
  location.pathname = 'BASE_YER' + (y ? y + '/' : '');
  location.search=''; location.hash='';
  ILK_YUKLEME = true;
  render();
  cikti[y] = APP.innerHTML;
});
`);
process.stdout.write(JSON.stringify(cikti));
""".replace("BASE_YER", BASE)
    tmp = ROOT / ".onrender.js"
    bnd = ROOT / ".bundle.js"
    tmp.write_text(js, encoding="utf-8")
    bnd.write_text(bundle, encoding="utf-8")
    try:
        p = subprocess.run(["node", str(tmp), str(bnd), json.dumps(yollar)],
                           capture_output=True, text=True)
        if p.returncode != 0:
            hata("onrender basarisiz. node ciktisi:\n" + (p.stderr.strip() or "(bos)"))
        return json.loads(p.stdout)
    finally:
        tmp.unlink(missing_ok=True); bnd.unlink(missing_ok=True)


def statik_linkler(html):
    """Onrenderda '#/...' hreflerini gercek yollara cevirir (istemci de ayni islemi yapar)."""
    def cev(m):
        s = m.group(1)
        pq, _, frag = s.partition("#")
        yol, _, qs = pq.partition("?")
        yol = yol.lstrip("/")
        return ('href="' + BASE + (yol + "/" if yol else "")
                + ("?" + qs if qs else "") + ("#" + frag if frag else "") + '"')
    return re.sub(r'href="#(/[^"]*)"', cev, html)


def sayfa_yaz(yol, baslik, aciklama, govde, style_href, script_src, kabuk, jsonld=""):
    kanonik = SITE_URL + (yol + "/" if yol else "")
    derinlik = "../" * (len(yol.split("/")) if yol else 0)
    head = f"""<!doctype html>
<html lang="tr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{baslik}</title>
<meta name="description" content="{aciklama}">
<link rel="canonical" href="{kanonik}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Master Blog Skill">
<meta property="og:title" content="{baslik}">
<meta property="og:description" content="{aciklama}">
<meta property="og:url" content="{kanonik}">
<meta property="og:locale" content="tr_TR">
<meta name="twitter:card" content="summary">
<meta name="twitter:title" content="{baslik}">
<meta name="twitter:description" content="{aciklama}">
<meta name="theme-color" content="#050505">
<link rel="icon" href="{derinlik}favicon.svg" type="image/svg+xml">
<link rel="icon" href="{derinlik}favicon.ico" sizes="32x32">
<link rel="apple-touch-icon" href="{derinlik}apple-touch-icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Archivo:wght@500;600;700;800&family=Manrope:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500;700&display=swap">
<link rel="stylesheet" href="{derinlik}{style_href}">
{jsonld}</head>
<body>
"""
    gövde_html = kabuk.replace("<!--__APP__-->", govde)
    html = head + gövde_html + f'<script src="{derinlik}{script_src}" defer></script>\n</body>\n</html>\n'
    hedef = DOCS / yol / "index.html" if yol else DOCS / "index.html"
    hedef.parent.mkdir(parents=True, exist_ok=True)
    hedef.write_text(html, encoding="utf-8")
    return len(html.encode("utf-8"))


def esc_attr(s):
    return (str(s).replace("&", "&amp;").replace('"', "&quot;")
            .replace("<", "&lt;").replace(">", "&gt;"))


def main():
    kacis_denetle()
    terms = terimleri_oku()
    dogrula(terms)
    sozluk_yaz(terms)
    files = dosyalari_topla()
    yazilar = yazilari_oku()

    plugin_bilgi = json.loads((ROOT / ".claude-plugin" / "plugin.json").read_text(encoding="utf-8"))
    _skill_metni = (SKILL / "SKILL.md").read_text(encoding="utf-8")
    fm_bilgi = {k: v for k, v in re.findall(r'^\s*([a-zA-Z-]+):\s*"([^"]+)"\s*$',
                                            _skill_metni.split("---")[1], re.M)}

    tpl = (SITE / "template.html").read_text(encoding="utf-8")
    veri = (TERMSJS.read_text(encoding="utf-8").rstrip().rstrip(";") + ";\n"
            + "const FILES = " + json.dumps(files, ensure_ascii=False) + ";\n"
            + "const POSTS = " + json.dumps(yazilar, ensure_ascii=False) + ";\n"
            + "const SURUM = " + json.dumps({
                "surum": plugin_bilgi["version"],
                "tazelik": fm_bilgi.get("bilgi-tazeligi", ""),
                "tazelikTR": tarih_tr(fm_bilgi.get("bilgi-tazeligi", "")),
                "sonrakiTR": tarih_tr(fm_bilgi.get("sonraki-gozden-gecirme", "")),
                "lisans": plugin_bilgi.get("license", "MIT"),
            }, ensure_ascii=False) + ";\n"
            + "const CHANGELOG = " + json.dumps(degisiklikleri_oku(), ensure_ascii=False) + ";\n"
            + "const INSTALL_CMD = " + json.dumps(kurulum_komutu(files), ensure_ascii=False) + ";\n")

    # ---------- A) Artifact surumu: tek dosya, iskeletsiz, hash yonlendirme ----------
    veri_spa = veri.replace(
        "const POSTS = " + json.dumps(yazilar, ensure_ascii=False),
        "const POSTS = " + json.dumps(gorsel_yollari(yazilar, "spa"), ensure_ascii=False))
    spa = tpl.replace("/*__DATA__*/", js_gomme_guvenli(
        "const MODE='spa'; const BASE='';\n" + veri_spa))
    DIST.mkdir(exist_ok=True)
    (DIST / "artifact.html").write_text(spa, encoding="utf-8")

    # ---------- B) GitHub Pages surumu: sayfa basina gercek URL ----------
    # Sablonda sabit surum/tarih yasak: bu sinif uc kez sessizce bayatladi.
    govde_tpl = tpl.split("<script>", 1)[1] if "<script>" in tpl else tpl
    yasak = []
    for kalip, ad in ((r"v\d+\.\d+", "sabit sürüm (v1.2 gibi)"),
                      (r"\b\d{1,2}\s+(?:Oca|Şub|Mar|Nis|May|Haz|Tem|Ağu|Eyl|Eki|Kas|Ara)\s+20\d\d", "sabit tarih"),
                      (r'"\d+\.\d+\.\d+"', "sabit sürüm dizesi")):
        for m in re.finditer(kalip, govde_tpl):
            satir = govde_tpl[:m.start()].count("\n") + tpl[:tpl.index("<script>")].count("\n") + 1
            yasak.append(f"satir ~{satir}: {ad} -> '{m.group(0)}'")
    if yasak:
        hata("template.html icinde sabit surum/tarih var. SURUM nesnesini kullan:\n  - "
             + "\n  - ".join(yasak))

    stil   = re.search(r"<style>(.*?)</style>", tpl, re.S).group(1)
    script = re.search(r"<script>(.*)</script>", tpl, re.S).group(1)
    kabuk  = tpl.split("</style>", 1)[1].split("<script>", 1)[0]
    if "<main id=\"app\"></main>" not in kabuk:
        hata("sablonda <main id=\"app\"></main> bulunamadi")
    kabuk = statik_linkler(kabuk).replace("<main id=\"app\"></main>",
                                          '<main id="app" tabindex="-1"><!--__APP__--></main>')

    veri_st = veri.replace(
        "const POSTS = " + json.dumps(yazilar, ensure_ascii=False),
        "const POSTS = " + json.dumps(gorsel_yollari(yazilar, "static"), ensure_ascii=False))
    bundle = script.replace("/*__DATA__*/", js_gomme_guvenli(
        f"const MODE='static'; const BASE='{BASE}';\n" + veri_st))

    yollar = ([y for y, _, _ in SAYFALAR] + ["terim/" + t["slug"] for t in terms]
              + ["blog/" + y["slug"] for y in yazilar])
    render_ = onrender(bundle, yollar)

    DOCS.mkdir(exist_ok=True)
    (DOCS / "assets").mkdir(exist_ok=True)
    (DOCS / "assets" / "style.css").write_text(stil, encoding="utf-8")
    (DOCS / "assets" / "app.js").write_text(bundle, encoding="utf-8")
    (DOCS / ".nojekyll").write_text("", encoding="utf-8")

    # ikonlar: site/assets/ kaynaktır, docs/ köküne kopyalanır.
    # tools/favicon-uret.py ile üretilir; marka rengi degismedikce tekrar uretilmez.
    import shutil
    for ikon in ("favicon.svg", "favicon.ico", "apple-touch-icon.png", "og.svg"):
        kaynak = SITE / "assets" / ikon
        if not kaynak.exists():
            hata(f"ikon bulunamadi: {kaynak} (uret: python3 tools/favicon-uret.py)")
        shutil.copyfile(kaynak, DOCS / ikon)

    toplam = 0
    for yol, baslik, aciklama in SAYFALAR:
        ld = ""
        if yol == "":
            ld = ('<script type="application/ld+json">' + json.dumps({
                "@context": "https://schema.org", "@type": "WebSite",
                "name": "Master Blog Skill", "url": SITE_URL,
                "description": aciklama, "inLanguage": "tr-TR",
                "codeRepository": REPO_URL, "license": "https://opensource.org/licenses/MIT",
            }, ensure_ascii=False) + "</script>\n")
        toplam += sayfa_yaz(yol, esc_attr(baslik), esc_attr(aciklama),
                            statik_linkler(render_[yol]),
                            "assets/style.css", "assets/app.js", kabuk, ld)

    for y in yazilar:
        yol = "blog/" + y["slug"]
        ilk_gorsel = re.search(r'!\[[^\]]*\]\(([^)\s]+)', y["govde"])
        ld_veri = {
            "@context": "https://schema.org", "@type": "BlogPosting",
            "headline": y["seoBaslik"], "description": y["ozet"],
            "datePublished": y["tarih"], "dateModified": y["tarih"],
            "author": {"@type": "Organization", "name": "master-blog", "url": REPO_URL},
            "publisher": {"@type": "Organization", "name": "master-blog", "url": SITE_URL},
            "mainEntityOfPage": {"@type": "WebPage", "@id": SITE_URL + yol + "/"},
            "inLanguage": "tr-TR",
        }
        # Kural: schema'daki image sayfada GERÇEKTEN görünen görsel olmalı.
        if ilk_gorsel:
            ld_veri["image"] = SITE_URL + "blog/" + ilk_gorsel.group(1)
        ld = ('<script type="application/ld+json">'
              + json.dumps(ld_veri, ensure_ascii=False) + "</script>\n")
        toplam += sayfa_yaz(yol, esc_attr(y["seoBaslik"] + " — master-blog"), esc_attr(y["ozet"]),
                            statik_linkler(render_[yol]), "assets/style.css", "assets/app.js", kabuk, ld)

    for t in terms:
        yol = "terim/" + t["slug"]
        aciklama = t["short"][:300]
        ld = ('<script type="application/ld+json">' + json.dumps({
            "@context": "https://schema.org", "@type": "DefinedTerm",
            "name": t["name"], "alternateName": t["en"], "description": t["short"],
            "inDefinedTermSet": {"@type": "DefinedTermSet", "name": "Master Blog Skill Terim Sözlüğü",
                                 "url": SITE_URL + "terimler/"},
            "url": SITE_URL + yol + "/", "inLanguage": "tr-TR",
        }, ensure_ascii=False) + "</script>\n")
        toplam += sayfa_yaz(yol, esc_attr(t["name"] + " — Master Blog Skill"), esc_attr(aciklama),
                            statik_linkler(render_[yol]),
                            "assets/style.css", "assets/app.js", kabuk, ld)

    # ---------- C) sitemap + robots ----------
    # lastmod BUILD TARİHİ DEĞİL, kaynağın son anlamlı değişiklik tarihidir.
    # Build tarihi kullanmak (a) build'i deterministik olmaktan çıkarır,
    # (b) skill'in kendi "sahte tazelik yok" kuralını çiğner.
    # Git yoksa alan tamamen atlanır — yanlış tarih yazmaktansa yazmamak doğrudur.
    def son_degisiklik(*yollar_):
        """Kaynagin son ANLAMLI degisiklik tarihi.

        Tuzak: yalnizca 'git log -1' kullanmak build'i deterministik OLMAKTAN CIKARIR.
        Yerelde commit'ten ONCE build alinir (eski tarih), CI ayni kaynagi commit'ten
        SONRA build eder (yeni tarih) -> cikti tutmaz. CI bunu yakaladi.
        Cozum: dosyada commit'lenmemis degisiklik varsa bugun, yoksa son commit tarihi.
        Ikisi de ayni commit icin ayni sonucu verir."""
        tarihler = []
        for yol in yollar_:
            try:
                kirli = subprocess.run(["git", "status", "--porcelain", "--", yol],
                                       capture_output=True, text=True, cwd=ROOT)
                if kirli.returncode == 0 and kirli.stdout.strip():
                    tarihler.append(date.today().isoformat())
                    continue
                p = subprocess.run(["git", "log", "-1", "--format=%cs", "--", yol],
                                   capture_output=True, text=True, cwd=ROOT)
                if p.returncode == 0 and p.stdout.strip():
                    tarihler.append(p.stdout.strip())
            except FileNotFoundError:
                return None
        return max(tarihler) if tarihler else None

    SABLON, TERIMLER = "site/template.html", "site/data/terms.js"
    KAYNAK_HARITASI = {
        "":              [SABLON, TERIMLER, "skills/master-blog/SKILL.md"],
        "skill":         [SABLON, "skills/master-blog"],
        "senaryolar":    [SABLON, "skills/master-blog/references/kullanim-senaryolari.md"],
        "nasil-calisir": [SABLON],
        "terimler":      [SABLON, TERIMLER],
        "kurulum":       [SABLON, "skills/master-blog"],
        "kaynaklar":     [SABLON, "skills/master-blog/references/kaynaklar.md"],
    }
    urls = ""
    for y in yollar:
        kaynaklar = KAYNAK_HARITASI.get(y, [SABLON, TERIMLER])
        tarih = son_degisiklik(*kaynaklar)
        urls += (f"  <url><loc>{SITE_URL}{(y + '/') if y else ''}</loc>"
                 + (f"<lastmod>{tarih}</lastmod>" if tarih else "") + "</url>\n")
    (DOCS / "sitemap.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + urls + "</urlset>\n",
        encoding="utf-8")
    # surum.json: skill'in "daha yeni sürüm var mı" sorusunu sorabileceği kanonik uç nokta.
    # scripts/surum-kontrol.py bunu okur. Kaynak: plugin.json + SKILL.md frontmatter.
    plugin, fm = plugin_bilgi, fm_bilgi
    if plugin["version"] != fm.get("surum"):
        hata(f"surum uyusmazligi: plugin.json {plugin['version']} != SKILL.md {fm.get('surum')}")
    (DOCS / "surum.json").write_text(json.dumps({
        "surum": plugin["version"],
        "bilgi_tazeligi": fm.get("bilgi-tazeligi"),
        "sonraki_gozden_gecirme": fm.get("sonraki-gozden-gecirme"),
        "kontrol_maddesi": len(re.findall(r"^\s*\d+\.\s", (SKILL / "references" / "yayin-oncesi-kontrol.md").read_text(encoding="utf-8"), re.M)),
        "terim_sayisi": len(terms),
        "degisiklikler_url": REPO_URL + "/blob/main/CHANGELOG.md",
        "guncelleme_komutu": "/plugin update master-blog   (dosya kurulumunda: depoyu yeniden kopyala)",
        "kurulum_url": SITE_URL + "kurulum/",
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    # paket/: skill dosyalarının ham hâli — kur.sh buradan indirir
    for rel, f in zip(ORDER, files):
        hedef_dosya = DOCS / "paket" / rel
        hedef_dosya.parent.mkdir(parents=True, exist_ok=True)
        hedef_dosya.write_text(f["text"], encoding="utf-8")
    (DOCS / "kur.sh").write_text(kur_scripti(), encoding="utf-8")

    # blog görselleri
    gorsel_dizin = SITE / "blog" / "gorseller"
    if gorsel_dizin.exists():
        hedef_g = DOCS / "blog" / "gorseller"
        hedef_g.mkdir(parents=True, exist_ok=True)
        for g in gorsel_dizin.iterdir():
            if g.is_file():
                shutil.copyfile(g, hedef_g / g.name)

    (DOCS / "robots.txt").write_text(
        f"User-agent: *\nAllow: /\n\nSitemap: {SITE_URL}sitemap.xml\n", encoding="utf-8")

    print(f"docs/  · {len(yollar)} sayfa · toplam {toplam/1024:.0f} KB "
          f"(app.js {len(bundle.encode()) / 1024:.0f} KB + style.css {len(stil.encode()) / 1024:.0f} KB ortak)")
    print(f"dist/artifact.html · {len(spa.encode()) / 1024:.0f} KB · tek dosya")
    print(f"{len(terms)} terim · {len(files)} skill dosyasi · "
          f"{sum(len(f['text'].splitlines()) for f in files)} satir")


if __name__ == "__main__":
    main()
