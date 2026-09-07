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


def tr_kucult(s):
    """Türkçeye duyarlı küçültme. Python'un lower()'ı 'İ' -> 'i'+U+0307 üretir;
    bu, hedef kelime aramalarını sessizce bozar."""
    return unicodedata.normalize("NFC", str(s).replace("İ", "i").replace("I", "ı")).lower()

# ---------- eşikler (projene göre uyarlanabilir) ----------
TITLE_MAX   = 60
DESC_MIN, DESC_MAX = 140, 160
KELIME_MIN  = 600          # altına düşerse "dur ve oku" tetikleyicisi
IC_LINK_MIN = 4
DIS_LINK_MAX = 2
SORU_ORANI  = 0.5          # H2'lerin en az yarısı soru/karar başlığı
PARA_MAX_KELIME = 90
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
    t = re.sub(r"!\[[^\]]*\]\([^)]*\)", " ", t)
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
    a = ap.parse_args()

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
        if n > TITLE_MAX:
            r.ekle(14, "Title uzunluğu", "blokaj", f"{n} karakter (üst sınır {TITLE_MAX})")
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
        durum = "gecti" if DESC_MIN <= n <= DESC_MAX else "uyari"
        r.ekle(15, "Meta description uzunluğu", durum, f"{n} karakter (hedef {DESC_MIN}-{DESC_MAX})")

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
        r.ekle(19, "Soru/karar biçimli H2", "gecti" if oran >= SORU_ORANI else "uyari",
               f"{len(soru)}/{len(h2)} = %{oran*100:.0f} (hedef ≥%{SORU_ORANI*100:.0f})")
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
    r.ekle(22, "Kelime sayısı", "gecti" if kw >= KELIME_MIN else "uyari",
           f"{kw} kelime" + ("" if kw >= KELIME_MIN else f" — {KELIME_MIN} altı: DUR VE OKU, konu gerçekten kapandı mı?"))

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

    r.ekle(33, "İç bağlantı sayısı", "gecti" if len(ic) >= IC_LINK_MIN else "blokaj",
           f"{len(ic)} adet (en az {IC_LINK_MIN})")

    jenerik = [t for t, _ in linkler if tr_kucult(t.strip()) in JENERIK_ANCHOR]
    anchorlar = [tr_kucult(t.strip()) for t, _ in ic]
    tekrar = {x for x in anchorlar if anchorlar.count(x) > 1}
    sorun = []
    if jenerik: sorun.append(f"jenerik anchor: {', '.join(sorted(set(jenerik))[:3])}")
    if tekrar:  sorun.append(f"tekrar eden anchor: {', '.join(sorted(tekrar)[:3])}")
    r.ekle(34, "Anchor metinleri", "gecti" if not sorun else "uyari",
           "tanımlayıcı ve çeşitli" if not sorun else " · ".join(sorun))

    if len(dis) > DIS_LINK_MAX:
        r.ekle(35, "Dış link sayısı", "uyari", f"{len(dis)} adet (önerilen üst sınır {DIS_LINK_MAX})")
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
    gorseller = re.findall(r"!\[([^\]]*)\]\(([^)\s]+)\)", body)
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
    uzun = [p for p in re.split(r"\n\s*\n", duz) if kelime_say(p) > PARA_MAX_KELIME]
    r.ekle(0, "Paragraf uzunluğu", "gecti" if not uzun else "uyari",
           "tamamı okunabilir" if not uzun else f"{len(uzun)} paragraf {PARA_MAX_KELIME}+ kelime")

    # --- ek: frontmatter tarih ---
    tarih = next((fm[k] for k in TARIH_ALAN if fm.get(k)), "")
    r.ekle(0, "Yayın tarihi alanı", "gecti" if tarih else "uyari", tarih or "yok")

    if a.json:
        print(json.dumps({"dosya": a.dosya, "kelime_sayisi": kw, "ic_link": len(ic),
                          "dis_link": len(dis), "h2": len(h2), "blokaj": r.blokaj,
                          "uyari": r.uyari, "gecti": r.gecti, "maddeler": r.satir},
                         ensure_ascii=False, indent=2))
    else:
        print(f"master-blog mekanik kontrol · {a.dosya}")
        print("-" * 78)
        r.yaz()
    sys.exit(1 if r.blokaj else 0)


if __name__ == "__main__":
    main()
