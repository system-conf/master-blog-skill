#!/usr/bin/env python3
"""
master-blog · mekanik yayın öncesi kontrol

Yayın öncesi kontrol listesinin ÖLÇÜLEBİLİR maddelerini gerçekten sayar.
Yargı gerektiren maddeler (niyet, kanibalizasyon, E-E-A-T, deneyim gerçekliği)
bu scriptin işi DEĞİLDİR — onları model değerlendirir.

Kullanım:
    python3 kontrol.py <yazi.md> [--kelime "hedef kelime"] [--net] [--json]
    python3 kontrol.py <yazi.md> --icerik-dizini src/content/blog --net

Bayraklar:
    --kelime   Hedef kelime (14, 18, 20 numaralı maddeler için gerekli)
    --net      Dış linklere gerçekten HTTP isteği atar (madde 35)
    --json     Makine okunur çıktı
    --icerik-dizini  İç linklerin hedefini dosya sisteminde doğrular

Çıkış kodu: blokaj varsa 1, yoksa 0.
"""
import argparse, json, os, re, sys, unicodedata, urllib.request, urllib.error


SAPKA = str.maketrans("âÂîÎûÛ", "aAiIuU")


def tr_kucult(s):
    """Türkçeye duyarlı küçültme + şapka katlaması.

    İki tuzak: (1) Python'un lower()'ı 'İ' -> 'i'+U+0307 üretir, bu hedef kelime
    aramalarını sessizce bozar. (2) Türkçede 'zekâ' ve 'zeka' aynı kelimedir ama
    farklı kod noktalarıdır; katlanmazsa başlıkta geçen kelime 'geçmiyor' sayılır."""
    s = str(s).translate(SAPKA).replace("İ", "i").replace("I", "ı")
    return unicodedata.normalize("NFC", s).lower()

# ---------- eşikler ----------
# VARSAYILANLAR orta ölçekli, yerleşik bir site içindir.
# Projene göre uyarlamak için skill dizinindeki bu dosyayı DEĞİL, projenin kökünde
# bir `master-blog.toml` (veya `.master-blog.json`) oluştur — skill güncellendiğinde
# uyarlaman silinmez. Profil bazlı önerilen değerler:
# references/kullanim-senaryolari.md → eşik uyarlama tablosu.
VARSAYILAN = {
    "TITLE_MAX": 60,        # SERP'te kırpılma sınırı
    "DESC_MIN": 140,        # kırpılmadan bilgi verebilen alt sınır
    "DESC_MAX": 160,        # üstünde kesilme riski
    "KELIME_MIN": 600,      # bulgu DEĞİL, "dur ve oku" tetikleyicisi
    "IC_LINK_MIN": 4,       # yeni sitelerde 2'ye indirilir; 4 link verecek sayfa olmayabilir
    "DIS_LINK_MAX": 2,      # fazlası dikkat dağıtır; B2B/SaaS'ta 3-4 makul
    "SORU_ORANI": 0.5,      # H2'lerin en az yarısı soru/karar başlığı (GEO)
    "PARA_MAX_KELIME": 90,  # üstü okunabilirliği düşürür; yerel hizmette 70
    # --- üslup katmanı (Aşama 5.5) ---
    # Bu dört eşik ÖLÇÜLMÜŞ değildir; bir saha ekibinin kendi korpusundan bildirdiği
    # değerlerdir (bkz. kaynaklar.md → dış katkı). Projede kalibre edilmeleri beklenir.
    "CUMLE_ORT_ALT": 10,    # altı telgraf üslubu
    "CUMLE_ORT_UST": 18,    # üstü akademik
    "CUMLE_SAPMA_MIN": 5,   # en kritik ölçüt: düşük sapma = tekdüze ritim
    "UZUN_CUMLE_ORAN": 5,   # 25+ kelimelik cümlelerin yüzdesi, üst sınır
    "KLISE_BIN_KELIME": 2,  # bin kelimede izin verilen üslup klişesi sayısı
}
E = dict(VARSAYILAN)        # yürürlükteki eşikler; main() içinde config ile güncellenir
E_KAYNAK = "varsayılan"


def esikleri_yukle(yol=None):
    """--config, ./master-blog.toml, ./.master-blog.json sırasıyla aranır."""
    global E, E_KAYNAK
    adaylar = [yol] if yol else ["master-blog.toml", ".master-blog.json"]
    for a in adaylar:
        if not a or not os.path.exists(a):
            continue
        try:
            if a.endswith(".json"):
                veri = json.load(open(a, encoding="utf-8"))
            else:
                import tomllib
                veri = tomllib.load(open(a, "rb"))
            veri = veri.get("esikler", veri)
        except Exception as e:
            print(f"HATA: '{a}' okunamadi: {e}", file=sys.stderr)
            sys.exit(2)
        for alan, hedef in (("kliseler", KLISELER), ("yasak_acilis", YASAK_ACILIS)):
            if alan in veri:
                if not isinstance(veri[alan], list):
                    print(f"HATA: '{a}' icinde {alan} liste olmali", file=sys.stderr)
                    sys.exit(2)
                hedef.extend(str(x) for x in veri.pop(alan))
        bilinmeyen = [k for k in veri if k not in VARSAYILAN]
        if bilinmeyen:
            print(f"HATA: '{a}' icinde bilinmeyen esik: {', '.join(bilinmeyen)}", file=sys.stderr)
            sys.exit(2)
        E.update({k: veri[k] for k in veri})
        E_KAYNAK = a
        return
    if yol:
        print(f"HATA: config dosyasi bulunamadi: {yol}", file=sys.stderr)
        sys.exit(2)
JENERIK_ANCHOR = ["buraya tıkla", "buraya tıklayın", "tıklayın", "buradan", "bu link",
                  "click here", "read more", "devamı", "detaylı bilgi için tıkla"]
TITLE_ALAN = ["seoBaslik", "seoTitle", "title", "seo_title", "baslik"]
DESC_ALAN  = ["ozet", "description", "metaDescription", "excerpt", "aciklama"]
TARIH_ALAN = ["tarih", "date", "publishedAt", "pubDate"]

# Alt dize araması yanlış pozitif üretiyordu ("mimarisi" -> " mi", "kaçınılmaz" -> "kaç").
# Kelime sınırı + "neden sonuç" gibi bileşik kalıplar için negatif ileri bakış.
SORU_DESENI = re.compile(
    r"\?|\b(?:mi|mı|mu|mü|midir|mıdır|mudur|müdür)\b"
    r"|\b(?:nasıl|niçin|nerede|nereden|hangi|nedir|kim|kaç|ne kadar|ne zaman)\b"
    r"|\bneden\b(?!\s*[-–—]?\s*sonu[çc])")


def soru_mu(baslik):
    return bool(SORU_DESENI.search(tr_kucult(baslik)))


def frontmatter_ayir(text):
    m = re.match(r"^---\n(.*?)\n---\n?(.*)$", text, re.S)
    if not m:
        return {}, text
    fm, body = {}, m.group(2)
    for line in m.group(1).split("\n"):
        mm = re.match(r'^([A-Za-zçğıöşüÇĞİÖŞÜ_][\w_]*)\s*:\s*(.*)$', line)
        if mm:
            fm[mm.group(1)] = mm.group(2).strip().strip('"').strip("'")
    return fm, body


def govde_temizle(body):
    """Kod blokları, tablo işaretleri, URL'ler ve markdown sözdizimi düşülür."""
    t = re.sub(r"```.*?```", " ", body, flags=re.S)
    t = re.sub(r"`[^`]*`", " ", t)
    t = re.sub(r"!\[[^\]]*\]\([^)]*\)", " ", t)   # başlıklı görsel dâhil
    t = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", t)
    t = re.sub(r"^\s*\|.*$", " ", t, flags=re.M)
    t = re.sub(r"https?://\S+", " ", t)
    t = re.sub(r"(?m)^\s*[-*+]\s+", " ", t)      # madde imleri
    t = re.sub(r"(?m)^\s*-{3,}\s*$", " ", t)     # yatay çizgi
    t = re.sub(r"\s-\s", " ", t)                 # tek başına tire
    t = re.sub(r"[#>*_~]", " ", t)                # kelime içi tire KORUNUR
    return t


def kelime_say(text):
    return len([w for w in re.split(r"\s+", text) if re.search(r"[0-9A-Za-zçğıöşüÇĞİÖŞÜ]", w)])


def http_durum(url, timeout=12):
    req = urllib.request.Request(url, method="HEAD", headers={"User-Agent": "Mozilla/5.0 (master-blog kontrol)"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.status
    except urllib.error.HTTPError as e:
        if e.code in (403, 405):   # HEAD reddi olabilir, GET dene
            try:
                req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (master-blog kontrol)"})
                with urllib.request.urlopen(req, timeout=timeout) as r:
                    return r.status
            except Exception:
                return e.code
        return e.code
    except Exception:
        return 0


def sayfa_getir(url, timeout=15):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (master-blog kontrol)"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.status, r.read().decode("utf-8", "replace")


def canli_denetle(url, r, title, desc, kelime):
    """Madde 40: yayindaki sayfa gercekten dogru render edildi mi?

    Markdown'da dogru olan sey sablonda kaybolabilir — bu skill'in kendi sitesinde
    tam olarak bu oldu: doctype ve viewport eksikti, sayfa quirks mode'daydi ve
    mobil kurallari hic calismiyordu. Kaynak dosyaya bakan hicbir kontrol bunu goremez.
    """
    try:
        durum, html = sayfa_getir(url)
    except Exception as e:
        r.ekle(40, "Canlı URL", "blokaj", f"{url} alınamadı: {type(e).__name__}")
        return
    if durum != 200:
        r.ekle(40, "Canlı URL", "blokaj", f"HTTP {durum}")
        return
    r.ekle(40, "Canlı URL", "gecti", f"HTTP 200 · {len(html) // 1024} KB")

    bas = html[:4000].lower()
    r.ekle(40, "Belge iskeleti", "gecti" if bas.lstrip().startswith("<!doctype") else "blokaj",
           "doctype var" if bas.lstrip().startswith("<!doctype") else "doctype YOK — sayfa quirks mode'da")
    r.ekle(40, "lang özniteliği", "gecti" if re.search(r"<html[^>]*\slang=", bas) else "uyari",
           "var" if re.search(r"<html[^>]*\slang=", bas) else "yok — ekran okuyucu yanlış telaffuz eder")
    vp = re.search(r'<meta[^>]+name=["\']viewport["\']', bas)
    r.ekle(40, "viewport meta", "gecti" if vp else "blokaj",
           "var" if vp else "YOK — mobilde responsive kurallar çalışmaz")

    h1 = re.findall(r"<h1[\s>]", html, re.I)
    r.ekle(40, "Render edilmiş H1", "gecti" if len(h1) == 1 else "blokaj", f"{len(h1)} adet")

    m = re.search(r"<title[^>]*>(.*?)</title>", html, re.S | re.I)
    canli_title = re.sub(r"\s+", " ", m.group(1)).strip() if m else ""
    if not canli_title:
        r.ekle(40, "Render edilmiş title", "blokaj", "boş")
    elif title and tr_kucult(title) not in tr_kucult(canli_title):
        r.ekle(40, "Render edilmiş title", "uyari",
               f"frontmatter ile örtüşmüyor: '{canli_title[:60]}'")
    else:
        r.ekle(40, "Render edilmiş title", "gecti", f"{len(canli_title)} karakter")

    md = re.search(r'<meta[^>]+name=["\']description["\'][^>]*content=["\'](.*?)["\']', html, re.S | re.I)
    if not md:
        r.ekle(40, "Render edilmiş meta description", "blokaj", "yok")
    elif desc and tr_kucult(desc[:60]) not in tr_kucult(md.group(1)):
        r.ekle(40, "Render edilmiş meta description", "uyari", "frontmatter ile örtüşmüyor")
    else:
        r.ekle(40, "Render edilmiş meta description", "gecti", f"{len(md.group(1))} karakter")

    can = re.search(r'<link[^>]+rel=["\']canonical["\'][^>]*href=["\'](.*?)["\']', html, re.I)
    if not can:
        r.ekle(40, "Canonical", "uyari", "yok")
    else:
        ayni = can.group(1).rstrip("/") == url.rstrip("/")
        r.ekle(40, "Canonical", "gecti" if ayni else "uyari",
               "kendine işaret ediyor" if ayni else f"başka sayfaya: {can.group(1)}")

    for direktif in ("nosnippet", "noindex", "max-snippet:0"):
        if re.search(r'<meta[^>]+robots[^>]*' + re.escape(direktif), bas):
            r.ekle(40, "Önizleme direktifi", "blokaj",
                   f"'{direktif}' bulundu — bu sayfa arama önizlemelerinde görünmez")

    govde = re.sub(r"<(script|style)[^>]*>.*?</\1>", " ", html, flags=re.S | re.I)
    govde = re.sub(r"<[^>]+>", " ", govde)
    if kelime and kelime not in tr_kucult(govde):
        r.ekle(40, "Hedef kelime render edildi", "blokaj",
               "render edilmiş gövdede yok — içerik JavaScript'te kalmış olabilir")
    elif kelime:
        r.ekle(40, "Hedef kelime render edildi", "gecti", "var")


# --- üslup katmanı desenleri ---
# Kaynak: saha geri bildirimi (SEKTÖR sınıfı). master-blog.toml ile genişletilebilir.
YASAK_ACILIS = ["günümüzde", "bu yazıda", "ele alacağız", "büyük önem",
                "sıkça sorulan", "hızla gelişen", "son yıllarda"]
KLISELER = ["bu bağlamda", "bu çerçevede", "bu doğrultuda", "söz konusu",
            "önemle belirtmek gerekir", "unutulmamalıdır ki", "şüphesiz",
            "tartışmasız", "son derece", "ele alacağız", "inceleyeceğiz",
            "gördüğümüz gibi", "devrim niteliğinde", "oyunun kurallarını değiştiren",
            "çığır açan", "başarılar dileriz", "büyük önem taşımaktadır"]
SIZ_DESEN = re.compile(r"\b(siz|sizin|size|sizi|sizce)\b|\w+(?:sınız|siniz|sunuz|sünüz)\b", re.I)
SEN_DESEN = re.compile(r"\b(sen|senin|sana|seni|sence)\b|\w+(?:abilirsin|ebilirsin|malısın|melisin)\b", re.I)


def cumlelere_bol(duz):
    """Cümlelere böler. Kısaltma ve ondalık sayı yüzünden yanlış bölmeyi azaltır.
    Tablo, kod bloğu ve başlıklar zaten govde_temizle ile düşülmüş olmalıdır."""
    t = re.sub(r"\b(vb|vs|bkz|ör|Dr|Av|Prof|Doç|No|Sn)\.", r"\1<NOKTA>", duz)
    t = re.sub(r"(\d)\.(\d)", r"\1<NOKTA>\2", t)
    parcalar = re.split(r"(?<=[.!?])\s+(?=[A-ZÇĞİÖŞÜ\"'(])", t)
    return [p.replace("<NOKTA>", ".").strip() for p in parcalar if len(p.split()) >= 3]


def uslup_denetle(body, duz, r):
    """Aşama 5.5 — üslup katmanının ölçülebilir maddeleri (47-50)."""
    # 47 · açılış kalıbı
    # İlk paragraf, ilk PROZA paragrafıdır. govde_temizle başlıkları silmiyor,
    # yalnızca # işaretini boşluğa çeviriyor; başlık kalıntısını ilk paragraf sanmak
    # kontrolü sessizce işlevsiz bırakıyordu.
    proza = re.sub(r"^#{1,6}.*$", "", body, flags=re.M)
    proza = re.sub(r"```.*?```", " ", proza, flags=re.S)
    proza = re.sub(r"^\s*\|.*$|^!\[.*$|^>\s.*$", "", proza, flags=re.M)
    paragraflar = [x.strip() for x in re.split(r"\n\s*\n", proza) if len(x.split()) >= 5]
    ilk = tr_kucult(paragraflar[0]) if paragraflar else ""
    yakalanan = [k for k in YASAK_ACILIS if k in ilk]
    r.ekle(47, "Açılış kalıbı", "gecti" if not yakalanan else "uyari",
           "somut açılış" if not yakalanan
           else "klişe açılış: " + ", ".join(f"'{k}'" for k in yakalanan))

    # 48 · cümle ritmi
    cumleler = cumlelere_bol(duz)
    uz = [len(c.split()) for c in cumleler]
    if len(uz) < 10:
        r.ekle(48, "Cümle ritmi", "atlandi", f"{len(uz)} cümle — ölçüm için az")
    else:
        ort = sum(uz) / len(uz)
        sapma = (sum((x - ort) ** 2 for x in uz) / len(uz)) ** 0.5
        uzun = sum(1 for x in uz if x >= 25) / len(uz) * 100
        detay = f"ort {ort:.1f} · sapma {sapma:.1f} · 25+ %{uzun:.0f} ({len(uz)} cümle)"
        sorun = []
        if not (E["CUMLE_ORT_ALT"] <= ort <= E["CUMLE_ORT_UST"]):
            sorun.append(f"ortalama {E['CUMLE_ORT_ALT']}-{E['CUMLE_ORT_UST']} bandı dışında")
        if sapma < E["CUMLE_SAPMA_MIN"]:
            sorun.append(f"sapma {E['CUMLE_SAPMA_MIN']} altında — tekdüze ritim")
        if uzun > E["UZUN_CUMLE_ORAN"]:
            sorun.append(f"uzun cümle oranı %{E['UZUN_CUMLE_ORAN']} üstünde")
        r.ekle(48, "Cümle ritmi", "gecti" if not sorun else "uyari",
               detay + ("" if not sorun else " → " + "; ".join(sorun)))

    # 49 · üslup klişeleri
    kw = kelime_say(duz) or 1
    bulunan = {}
    alcak = tr_kucult(duz)
    for k in KLISELER:
        n = alcak.count(tr_kucult(k))
        if n:
            bulunan[k] = n
    toplam = sum(bulunan.values())
    bin_basi = toplam / kw * 1000
    r.ekle(49, "Üslup klişeleri", "gecti" if bin_basi <= E["KLISE_BIN_KELIME"] else "uyari",
           f"{toplam} eşleşme · bin kelimede {bin_basi:.1f}"
           + ("" if not bulunan else " → " + ", ".join(f"'{k}'×{n}" for k, n in
                                                       sorted(bulunan.items(), key=lambda x: -x[1])[:4])))

    # 50 · hitap tutarlılığı
    siz = len(SIZ_DESEN.findall(duz))
    sen = len(SEN_DESEN.findall(duz))
    if siz + sen < 3:
        r.ekle(50, "Hitap tutarlılığı", "gecti", "doğrudan hitap az kullanılmış")
    else:
        azinlik = min(siz, sen)
        oran = azinlik / (siz + sen) * 100
        r.ekle(50, "Hitap tutarlılığı", "gecti" if oran < 15 else "uyari",
               f"siz {siz} · sen {sen}" + ("" if oran < 15 else " → ikisi karışmış"))


GORSEL_UZANTI = {".webp", ".avif", ".png", ".jpg", ".jpeg", ".svg", ".gif"}
GORSEL_AGIRLIK = 200 * 1024        # gövde görseli için üst sınır


def png_boyut(veri):
    if veri[:8] == b"\x89PNG\r\n\x1a\n" and veri[12:16] == b"IHDR":
        return int.from_bytes(veri[16:20], "big"), int.from_bytes(veri[20:24], "big")
    return None


def gorselleri_denetle(dosya_yolu, gorseller, r):
    """Madde 44: referans edilen görsel dosyası gerçekten var mı, formatı ve ağırlığı uygun mu.

    Kırık görsel yolu daha önce yalnızca tarayıcıda fark edildi; kaynak dosyaya bakan
    hiçbir kontrol yakalamamıştı. Bu fonksiyon o boşluğu kapatır.
    """
    kok = os.path.dirname(os.path.abspath(dosya_yolu))
    eksik, agir, kotu_format, svg_sorun = [], [], [], []
    for alt, src in gorseller:
        if src.startswith(("http://", "https://", "data:")):
            continue
        yol = os.path.normpath(os.path.join(kok, src))
        if not os.path.exists(yol):
            eksik.append(src)
            continue
        uzanti = os.path.splitext(yol)[1].lower()
        if uzanti not in GORSEL_UZANTI:
            kotu_format.append(src)
            continue
        boyut = os.path.getsize(yol)
        if uzanti != ".svg" and boyut > GORSEL_AGIRLIK:
            agir.append(f"{src} ({boyut // 1024} KB)")
        if uzanti == ".svg":
            try:
                icerik = open(yol, encoding="utf-8").read(4000)
            except OSError:
                svg_sorun.append(f"{src} (okunamadı)")
                continue
            if "viewBox" not in icerik:
                svg_sorun.append(f"{src} (viewBox yok — ölçeklenmez)")
            elif not re.search(r'aria-label="[^"]{10,}"', icerik):
                svg_sorun.append(f"{src} (aria-label yok ya da çok kısa)")

    if eksik:
        r.ekle(44, "Görsel dosyaları", "blokaj", "referans var dosya yok: " + ", ".join(eksik[:3]))
    elif not gorseller:
        r.ekle(44, "Görsel dosyaları", "gecti", "görsel yok")
    else:
        r.ekle(44, "Görsel dosyaları", "gecti", f"{len(gorseller)} görselin tamamı mevcut")
    if kotu_format:
        r.ekle(44, "Görsel formatı", "uyari", "desteklenmeyen uzantı: " + ", ".join(kotu_format[:3]))
    if agir:
        r.ekle(44, "Görsel ağırlığı", "uyari",
               f"{GORSEL_AGIRLIK // 1024} KB üstü: " + ", ".join(agir[:3]))
    if svg_sorun:
        r.ekle(44, "SVG ev stili", "uyari", "; ".join(svg_sorun[:3]))


class Rapor:
    def __init__(self):
        self.satir = []
        self.blokaj = self.uyari = self.gecti = 0

    def ekle(self, madde, ad, durum, detay):
        # durum: "gecti" | "uyari" | "blokaj" | "atlandi"
        self.satir.append({"madde": madde, "ad": ad, "durum": durum, "detay": detay})
        if durum == "blokaj": self.blokaj += 1
        elif durum == "uyari": self.uyari += 1
        elif durum == "gecti": self.gecti += 1

    def yaz(self):
        SIM = {"gecti": "  OK  ", "uyari": " UYARI", "blokaj": "BLOKAJ", "atlandi": "ATLAND"}
        for s in self.satir:
            print(f"{SIM[s['durum']]}  {s['madde']:>2}  {s['ad']:<34} {s['detay']}")
        print("-" * 78)
        print(f"Sonuç: {self.gecti} geçti · {self.uyari} uyarı · {self.blokaj} blokaj")
        if self.blokaj:
            print("BLOKAJ VAR — yayın yapılmaz. Yukarıdaki maddeleri düzelt.")
        print("Not: Bu script yalnızca ÖLÇÜLEBİLİR maddeleri kontrol eder.")
        print("Niyet, kanibalizasyon, kaynak gerçekliği ve E-E-A-T maddeleri modelin işidir.")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("dosya")
    ap.add_argument("--kelime", default="")
    ap.add_argument("--net", action="store_true")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--icerik-dizini", default="")
    ap.add_argument("--config", default="", help="esik dosyasi (toml/json)")
    ap.add_argument("--url", default="", help="yayindaki URL: render edilmis sayfayi denetler")
    a = ap.parse_args()
    esikleri_yukle(a.config or None)

    try:
        raw = open(a.dosya, encoding="utf-8-sig").read()   # utf-8-sig: BOM'lu dosyalar
    except FileNotFoundError:
        print(f"HATA: '{a.dosya}' bulunamadı. Yazının tam yolunu ver.", file=sys.stderr)
        sys.exit(2)          # 1 = blokaj, 2 = çağrı hatası
    except OSError as e:
        print(f"HATA: '{a.dosya}' okunamadı: {e}", file=sys.stderr)
        sys.exit(2)
    fm, body = frontmatter_ayir(raw)
    duz = govde_temizle(body)
    kelime = tr_kucult(a.kelime.strip())
    r = Rapor()

    # --- 14 · title ---
    title = next((fm[k] for k in TITLE_ALAN if fm.get(k)), "")
    if not title:
        r.ekle(14, "Title", "blokaj", "frontmatter'da title alanı bulunamadı")
    else:
        n = len(title)
        if n > E['TITLE_MAX']:
            r.ekle(14, "Title uzunluğu", "blokaj", f"{n} karakter (üst sınır {E['TITLE_MAX']})")
        else:
            r.ekle(14, "Title uzunluğu", "gecti", f"{n} karakter")
        if kelime:
            idx = tr_kucult(title).find(kelime)
            sinir = max(15, len(title) // 3)
            if idx < 0:
                r.ekle(14, "Hedef kelime title'da", "uyari", f"'{kelime}' title'da hiç geçmiyor")
            else:
                r.ekle(14, "Hedef kelime title'da başta", "gecti" if idx <= sinir else "uyari",
                       f"{idx}. karakterde" + ("" if idx <= sinir else f" — ilk {sinir} karaktere çek"))

    # --- 15 · meta description ---
    desc = next((fm[k] for k in DESC_ALAN if fm.get(k)), "")
    if not desc:
        r.ekle(15, "Meta description", "uyari", "frontmatter'da açıklama alanı yok")
    else:
        n = len(desc)
        durum = "gecti" if E['DESC_MIN'] <= n <= E['DESC_MAX'] else "uyari"
        r.ekle(15, "Meta description uzunluğu", durum, f"{n} karakter (hedef {E['DESC_MIN']}-{E['DESC_MAX']})")

    # --- 16 · tek H1 ---
    h1 = re.findall(r"^#\s+(.+)$", body, re.M)
    # Frontmatter'da herhangi bir başlık alanı varsa H1 şablondan gelir.
    # Önceden yalnızca ("baslik","title") kontrol ediliyordu; seoBaslik/seoTitle kullanan
    # doğru biçimli yazılar haksız yere BLOKAJ alıyordu.
    fm_baslikta = bool(next((fm[k] for k in TITLE_ALAN if fm.get(k)), ""))
    if fm_baslikta:
        r.ekle(16, "Gövdede H1", "gecti" if len(h1) == 0 else "blokaj",
               "H1 frontmatter'dan geliyor" if len(h1) == 0 else f"gövdede {len(h1)} adet H1 var (çift H1)")
    else:
        r.ekle(16, "Tek H1", "gecti" if len(h1) == 1 else "blokaj", f"{len(h1)} adet H1")

    # --- 17 · başlık hiyerarşisi ---
    basliklar = [(len(m.group(1)), m.group(2).strip())
                 for m in re.finditer(r"^(#{1,6})\s+(.+)$", body, re.M)]
    sicrama = [b for i, b in enumerate(basliklar)
               if i and b[0] - basliklar[i - 1][0] > 1]
    r.ekle(17, "Başlık hiyerarşisi", "gecti" if not sicrama else "uyari",
           "atlamasız" if not sicrama else "sıçrama: " + "; ".join(f"H{b[0]} '{b[1][:28]}'" for b in sicrama[:3]))

    # --- 18 · ilk 100 kelimede hedef kelime ---
    if kelime:
        ilk100 = tr_kucult(" ".join(duz.split()[:100]))
        r.ekle(18, "İlk 100 kelimede hedef kelime", "gecti" if kelime in ilk100 else "uyari",
               "var" if kelime in ilk100 else "yok")

    # --- 19 · soru biçimli H2 oranı ---
    h2 = [b[1] for b in basliklar if b[0] == 2]
    soru = [h for h in h2 if soru_mu(h)]
    if h2:
        oran = len(soru) / len(h2)
        r.ekle(19, "Soru/karar biçimli H2", "gecti" if oran >= E['SORU_ORANI'] else "uyari",
               f"{len(soru)}/{len(h2)} = %{oran*100:.0f} (hedef ≥%{E['SORU_ORANI']*100:.0f})")
    else:
        r.ekle(19, "H2 başlıkları", "blokaj", "hiç H2 yok")

    # --- 20 · kelime istifleme (paragraf başına 1) ---
    if kelime:
        paragraflar = [p for p in re.split(r"\n\s*\n", govde_temizle(body)) if p.strip()]
        asiri = [i for i, p in enumerate(paragraflar) if tr_kucult(p).count(kelime) > 1]
        r.ekle(20, "Kelime istifleme", "gecti" if not asiri else "uyari",
               "yok" if not asiri else f"{len(asiri)} paragrafta hedef kelime 1'den fazla")

    # --- 21 · slug ---
    slug = os.path.splitext(os.path.basename(a.dosya))[0]
    slug_ok = bool(re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", slug))
    detay = slug if slug_ok else f"{slug} — kebab-case değil (büyük harf/Türkçe karakter/alt çizgi)"
    if slug_ok and kelime:
        cev = str.maketrans("ıığüşöç", "iigusoc")
        anahtar = re.sub(r"[^a-z0-9]+", "-", kelime.translate(cev)).strip("-")
        parcalar = [x for x in anahtar.split("-") if len(x) > 2]
        if parcalar and not any(x in slug for x in parcalar):
            detay += " · hedef kelime slug'da geçmiyor"
    r.ekle(21, "Slug formatı", "gecti" if slug_ok else "blokaj", detay)

    # --- 22 · kelime sayısı ---
    kw = kelime_say(duz)
    r.ekle(22, "Kelime sayısı", "gecti" if kw >= E['KELIME_MIN'] else "uyari",
           f"{kw} kelime" + ("" if kw >= E['KELIME_MIN'] else f" — {E['KELIME_MIN']} altı: DUR VE OKU, konu gerçekten kapandı mı?"))

    # --- 25 · tablo / yapılandırılmış karşılaştırma ---
    tablo = len(re.findall(r"^\s*\|.*\|\s*$", body, re.M)) >= 3
    r.ekle(25, "Tablo veya yapılandırılmış blok", "gecti" if tablo else "blokaj",
           "var" if tablo else "yok — GEO katmanı en az bir tablo ister")

    # --- 27 · özet bölümü ---
    ozet = bool(re.search(r"^#{2,3}\s*(Özet|Sonuç|Kısaca)", body, re.M | re.I))
    r.ekle(27, "Özet bölümü", "gecti" if ozet else "uyari", "var" if ozet else "yok")

    # --- 33/34/35/36 · linkler ---
    linkler = re.findall(r"\[([^\]]+)\]\(([^)\s]+)\)", body)
    ic  = [(t, u) for t, u in linkler if not u.startswith(("http://", "https://", "mailto:"))]
    dis = [(t, u) for t, u in linkler if u.startswith(("http://", "https://"))]

    r.ekle(33, "İç bağlantı sayısı", "gecti" if len(ic) >= E['IC_LINK_MIN'] else "blokaj",
           f"{len(ic)} adet (en az {E['IC_LINK_MIN']})")

    jenerik = [t for t, _ in linkler if tr_kucult(t.strip()) in JENERIK_ANCHOR]
    anchorlar = [tr_kucult(t.strip()) for t, _ in ic]
    tekrar = {x for x in anchorlar if anchorlar.count(x) > 1}
    sorun = []
    if jenerik: sorun.append(f"jenerik anchor: {', '.join(sorted(set(jenerik))[:3])}")
    if tekrar:  sorun.append(f"tekrar eden anchor: {', '.join(sorted(tekrar)[:3])}")
    r.ekle(34, "Anchor metinleri", "gecti" if not sorun else "uyari",
           "tanımlayıcı ve çeşitli" if not sorun else " · ".join(sorun))

    if len(dis) > E['DIS_LINK_MAX']:
        r.ekle(35, "Dış link sayısı", "uyari", f"{len(dis)} adet (önerilen üst sınır {E['DIS_LINK_MAX']})")
    if not dis:
        r.ekle(35, "Dış link doğrulaması", "gecti", "dış link yok")
    elif not a.net:
        r.ekle(35, "Dış link doğrulaması", "atlandi", f"{len(dis)} link — doğrulamak için --net")
    else:
        kotu = []
        for _, u in dis:
            s = http_durum(u)
            if s != 200:
                kotu.append(f"{s or 'baglanti yok'} {u}")
        r.ekle(35, "Dış link HTTP durumu", "gecti" if not kotu else "blokaj",
               f"{len(dis)} link 200" if not kotu else "; ".join(kotu[:3]))

    if a.icerik_dizini:
        try:
            mevcut = {os.path.splitext(f)[0] for f in os.listdir(a.icerik_dizini)}
        except OSError as e:
            print(f"HATA: içerik dizini okunamadı: {e}", file=sys.stderr)
            sys.exit(2)
        eksik = []
        for _, u in ic:
            hedef = u.split("#")[0].split("?")[0].strip("/").split("/")[-1]
            hedef = os.path.splitext(hedef)[0]
            if hedef and hedef not in mevcut:      # önek değil, tam eşleşme
                eksik.append(u)
        r.ekle(36, "İç link hedefleri", "gecti" if not eksik else "uyari",
               "hepsi mevcut" if not eksik else f"bulunamadı: {', '.join(eksik[:3])}")

    # --- 38 · görsel alt metni ---
    # Markdown görsel başlığı: ![alt](src "açıklama") — eski desen boşluk yüzünden eşleşmiyordu
    gorseller = re.findall(r'!\[([^\]]*)\]\(([^)\s]+)(?:\s+"[^"]*")?\)', body)
    if not gorseller:
        r.ekle(38, "Görsel alt metni", "gecti", "görsel yok")
    else:
        bos = [u for t, u in gorseller if len(t.strip()) < 8]
        istif = [u for t, u in gorseller if kelime and tr_kucult(t).count(kelime) > 1]
        d = []
        if bos:   d.append(f"{len(bos)} görselde alt metni yok/çok kısa")
        if istif: d.append(f"{len(istif)} alt metninde kelime istifleme")
        r.ekle(38, "Görsel alt metni", "gecti" if not d else "uyari",
               f"{len(gorseller)} görsel, hepsi tarif ediyor" if not d else " · ".join(d))

    # --- ek: uzun paragraf ---
    uzun = [p for p in re.split(r"\n\s*\n", duz) if kelime_say(p) > E['PARA_MAX_KELIME']]
    r.ekle(0, "Paragraf uzunluğu", "gecti" if not uzun else "uyari",
           "tamamı okunabilir" if not uzun else f"{len(uzun)} paragraf {E['PARA_MAX_KELIME']}+ kelime")

    # --- ek: frontmatter tarih ---
    tarih = next((fm[k] for k in TARIH_ALAN if fm.get(k)), "")
    r.ekle(0, "Yayın tarihi alanı", "gecti" if tarih else "uyari", tarih or "yok")

    uslup_denetle(body, duz, r)
    gorselleri_denetle(a.dosya, gorseller, r)

    # --- 40 · canli URL: markdown'da dogru olan sablonda kaybolabilir ---
    if a.url:
        canli_denetle(a.url, r, title, desc, kelime)

    if a.json:
        print(json.dumps({"dosya": a.dosya, "esikler": E, "esik_kaynagi": E_KAYNAK,
                          "kelime_sayisi": kw, "ic_link": len(ic),
                          "dis_link": len(dis), "h2": len(h2), "blokaj": r.blokaj,
                          "uyari": r.uyari, "gecti": r.gecti, "maddeler": r.satir},
                         ensure_ascii=False, indent=2))
    else:
        print(f"master-blog mekanik kontrol · {a.dosya}")
        print(f"eşikler: {E_KAYNAK}")
        print("-" * 78)
        r.yaz()
    sys.exit(1 if r.blokaj else 0)


if __name__ == "__main__":
    main()
