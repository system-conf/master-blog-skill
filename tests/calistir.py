#!/usr/bin/env python3
"""
master-blog regresyon testleri — yalnızca standart kütüphane, ek bağımlılık yok.

Her test, geçmişte gerçekten görülmüş bir hatayı temsil eder. Çalıştır:
    python3 tests/calistir.py
Çıkış kodu: başarısız test varsa 1.
"""
import json, pathlib, re, subprocess, sys

KOK = pathlib.Path(__file__).resolve().parent.parent
FIX = KOK / "tests" / "fixtures"
KONTROL = KOK / "skills" / "master-blog" / "scripts" / "kontrol.py"
SURUM   = KOK / "skills" / "master-blog" / "scripts" / "surum-kontrol.py"
DENETIM = KOK / "skills" / "master-blog" / "scripts" / "skill-denetim.py"
OLCUM   = KOK / "skills" / "master-blog" / "scripts" / "olcum.py"

sonuc = {"gecti": 0, "kaldi": 0}
hatalar = []


def calistir(dosya, *args):
    p = subprocess.run([sys.executable, str(KONTROL), str(FIX / dosya), "--json", *args],
                       capture_output=True, text=True)
    try:
        return json.loads(p.stdout), p.returncode
    except json.JSONDecodeError:
        raise AssertionError(f"JSON çıktı alınamadı (kod {p.returncode}): {p.stderr[:300]}")


def _fold(s):
    return str(s).replace("İ", "i").replace("I", "ı").lower()


def madde(rapor, no, ad_parca=""):
    for m in rapor["maddeler"]:
        if m["madde"] == no and _fold(ad_parca) in _fold(m["ad"]):
            return m
    raise AssertionError(f"madde {no} '{ad_parca}' raporda yok")


def test(ad, fn):
    global sonuc
    try:
        fn()
        sonuc["gecti"] += 1
        print(f"  GEÇTİ  {ad}")
    except AssertionError as e:
        sonuc["kaldi"] += 1
        hatalar.append((ad, str(e)))
        print(f"  KALDI  {ad}\n         -> {e}")


# --- Hata 1: seoBaslik kullanan yazı haksız BLOKAJ alıyordu (kontrol.py:155) ---
def t_seo_baslik():
    r, _ = calistir("seo-baslik-alani.md")
    m = madde(r, 16, "H1")
    assert m["durum"] == "gecti", f"madde 16 '{m['durum']}' döndü, 'gecti' bekleniyordu: {m['detay']}"

# --- Hata 2: Türkçe 'İ' küçültmesi hedef kelime aramalarını bozuyordu ---
def t_turkce_i():
    r, _ = calistir("turkce-i-baslik.md", "--kelime", "içerik pazarlaması")
    m14 = madde(r, 14, "title")
    assert m14["durum"] == "gecti", f"madde 14 title'da kelimeyi bulamadı: {m14['detay']}"
    m18 = madde(r, 18, "ilk 100")
    assert m18["durum"] == "gecti", f"madde 18 ilk 100 kelimede bulamadı: {m18['detay']}"

# --- Şapkalı harf: "zekâ" ile "zeka" aynı kelimedir ---
def t_sapka():
    f = FIX / "sapkali.md"
    f.write_text("""---
baslik: "Yapay Zekâ Testi"
seoBaslik: "Yapay Zekâ İçeriği Nedir?"
ozet: "Şapkalı harflerin hedef kelime aramasını bozup bozmadığını ölçen fixture dosyasıdır bu."
tarih: 2026-09-08
---

## Bölüm

Yapay zekâ içeriği hakkında kısa bir metin.

| A | B |
|---|---|
| 1 | 2 |
""", encoding="utf-8")
    try:
        r, _ = calistir("sapkali.md", "--kelime", "yapay zeka")
        m = madde(r, 14, "title")
        assert m["durum"] == "gecti", f"'zekâ' başlığında 'zeka' bulunamadı: {m['detay']}"
    finally:
        f.unlink(missing_ok=True)

# --- Hata 3: soru sezgiseli alt dize araması yapıyordu ---
def t_sahte_soru():
    r, _ = calistir("sahte-soru-h2.md")
    m = madde(r, 19, "Soru")
    assert m["durum"] == "uyari", f"4 sahte soru başlığı soru sayıldı: {m['detay']}"
    assert m["detay"].startswith("0/4"), f"0/4 bekleniyordu: {m['detay']}"

# --- Görsel: ![alt](src "başlık") biçimi tanınmalı, alt metni denetlenmeli ---
def t_gorsel_baslikli():
    f = FIX / "gorselli.md"
    f.write_text("""---
baslik: "Görsel Testi"
ozet: "Markdown görsel başlığı sözdiziminin alt metin denetimini bozup bozmadığını ölçen fixture dosyasıdır."
tarih: 2026-09-08
---

## Bölüm

![Kreş bahçesinde iki kişilik ahşap salıncak, çevresinde kauçuk zemin](a.svg "Açıklama satırı")

![](b.svg "Alt metni olmayan görsel")

| A | B |
|---|---|
| 1 | 2 |
""", encoding="utf-8")
    try:
        r, _ = calistir("gorselli.md")
        m = madde(r, 38, "Görsel")
        assert "görsel yok" not in m["detay"], "başlıklı görseller hiç görülmedi"
        assert m["durum"] == "uyari" and "alt metni yok" in m["detay"], \
            f"alt metni boş görsel yakalanmadı: {m['detay']}"
    finally:
        f.unlink(missing_ok=True)

# --- Madde 48: kaba cümle bölücü yanlış bulgu üretiyordu; kısaltma ve ondalık korunmalı ---
def t_cumle_bolucu():
    kaynak = KONTROL.read_text(encoding="utf-8")
    ns = {}
    exec(kaynak.split("def main(")[0], ns)
    metin = ("Bir cümle burada bitiyor. Ikinci cümle de burada. "
             "Ölçü 3.5 metre olmalı yani yaklaşık bu kadar. "
             "Kısaltma vb. ifadeler cümleyi bölmemeli tamam mı. "
             "Şu da bir başlık gibi: ama iki nokta cümle sonu değildir.")
    c = ns["cumlelere_bol"](metin)
    assert len(c) == 5, f"5 cümle bekleniyordu, {len(c)} bulundu: {c}"
    assert any("3.5" in x for x in c), "ondalık sayı bölünmüş"
    assert any("vb." in x for x in c), "kısaltma bölünmüş"

# --- Madde 47/49/50: üslup kontrolleri tetikleniyor mu ---
def t_uslup():
    f = FIX / "uslupsuz.md"
    f.write_text("""---
baslik: "Üslup Testi"
ozet: "Klişe açılış, üslup klişeleri ve karışık hitap kullanan bir metnin denetimden nasıl geçtiğini ölçen fixture."
tarih: 2026-09-09
---

## Bölüm

Günümüzde bu konu büyük önem taşımaktadır. Bu yazıda konuyu ele alacağız.

Bu bağlamda şunu söylemek gerekir. Bu doğrultuda ilerleyebilirsiniz. Söz konusu durum
şüphesiz son derece önemlidir. Bu çerçevede sen de bunu yapabilirsin.

| A | B |
|---|---|
| 1 | 2 |
""", encoding="utf-8")
    try:
        r, _ = calistir("uslupsuz.md")
        m47 = madde(r, 47, "Açılış")
        assert m47["durum"] == "uyari", f"klişe açılış yakalanmadı: {m47['detay']}"
        m49 = madde(r, 49, "klişe")
        assert m49["durum"] == "uyari", f"üslup klişeleri yakalanmadı: {m49['detay']}"
        m50 = madde(r, 50, "Hitap")
        assert m50["durum"] == "uyari", f"sen/siz karışımı yakalanmadı: {m50['detay']}"
    finally:
        f.unlink(missing_ok=True)

# --- Madde 44: kırık görsel yolu BLOKAJ olmalı (daha önce yalnızca tarayıcıda görülmüştü) ---
def t_gorsel_kirik_yol():
    f = FIX / "kirik-gorsel.md"
    f.write_text("""---
baslik: "Kırık Görsel"
ozet: "Var olmayan bir görsele referans verildiğinde denetçinin blokaj verip vermediğini ölçen fixture."
tarih: 2026-09-09
---

## Bölüm

![Bu görsel dosya sisteminde yok](gorseller/olmayan.svg "açıklama")

| A | B |
|---|---|
| 1 | 2 |
""", encoding="utf-8")
    try:
        r, kod = calistir("kirik-gorsel.md")
        m = madde(r, 44, "Görsel dosya")
        assert m["durum"] == "blokaj", f"kırık görsel yolu blokaj vermedi: {m['detay']}"
        assert kod == 1
    finally:
        f.unlink(missing_ok=True)

# --- Madde 44: SVG ev stili (viewBox + aria-label) denetleniyor mu ---
def t_gorsel_svg_stili():
    d = FIX / "gorseller"; d.mkdir(exist_ok=True)
    svg = d / "eksik.svg"; f = FIX / "svg-stili.md"
    svg.write_text('<svg xmlns="http://www.w3.org/2000/svg" width="10" height="10"></svg>',
                   encoding="utf-8")
    f.write_text("""---
baslik: "SVG Stili"
ozet: "viewBox ve aria-label eksik bir SVG'nin ev stili denetiminden geçip geçmediğini ölçen fixture."
tarih: 2026-09-09
---

## Bölüm

![Ev stiline uymayan bir vektör diyagram örneği burada](gorseller/eksik.svg)

| A | B |
|---|---|
| 1 | 2 |
""", encoding="utf-8")
    try:
        r, _ = calistir("svg-stili.md")
        m = madde(r, 44, "SVG ev stili")
        assert m["durum"] == "uyari" and "viewBox" in m["detay"], f"viewBox eksikliği yakalanmadı: {m}"
    finally:
        f.unlink(missing_ok=True); svg.unlink(missing_ok=True)
        try: d.rmdir()
        except OSError: pass

# --- Hata 4: kelime içi tireler kelime sayısını şişiriyordu ---
def t_tire():
    r, _ = calistir("tireli-kelimeler.md")
    assert r["kelime_sayisi"] == 10, f"10 kelime bekleniyordu, {r['kelime_sayisi']} sayıldı"

# --- Hata 9: BOM'lu dosyada frontmatter kayboluyordu ---
def t_bom():
    r, _ = calistir("bom.md")
    m = madde(r, 14, "Title uzunlu")
    assert m["durum"] == "gecti", f"BOM'lu dosyada title okunamadı: {m['detay']}"

# --- Hata 10: iç link doğrulaması önek eşleşmesiyle kırık linki geçiriyordu ---
def t_onek_link():
    r, _ = calistir("onek-ic-link.md", "--icerik-dizini", str(FIX / "icerik"))
    m = madde(r, 36, "İç link")
    assert m["durum"] == "uyari", f"/blog/seo kırık linki yakalanmadı: {m['detay']}"

# --- Çağrı hatası 1 (blokaj) ile karışmamalı: çıkış kodu 2 ---
def t_eksik_dosya():
    p = subprocess.run([sys.executable, str(KONTROL), str(FIX / "yok-boyle-dosya.md")],
                       capture_output=True, text=True)
    assert p.returncode == 2, f"çıkış kodu 2 bekleniyordu, {p.returncode} döndü"

# --- Temiz yazı blokaj almamalı ---
def t_temiz():
    r, kod = calistir("temiz.md", "--kelime", "güvenlik mesafesi")
    assert r["blokaj"] == 0, f"temiz yazıda {r['blokaj']} blokaj: " + \
        "; ".join(m["ad"] + ": " + m["detay"] for m in r["maddeler"] if m["durum"] == "blokaj")
    assert kod == 0, f"çıkış kodu 0 bekleniyordu, {kod}"

# --- Eşikler config dosyasından okunmalı (skill dizini düzenlenmeden) ---
def t_config():
    cfg = FIX / "esik.toml"
    cfg.write_text("[esikler]\nIC_LINK_MIN = 2\nKELIME_MIN = 400\n", encoding="utf-8")
    try:
        r, _ = calistir("tireli-kelimeler.md", "--config", str(cfg))
        assert r["esikler"]["IC_LINK_MIN"] == 2, "config'teki IC_LINK_MIN uygulanmadı"
        assert r["esikler"]["KELIME_MIN"] == 400, "config'teki KELIME_MIN uygulanmadı"
        assert r["esik_kaynagi"].endswith("esik.toml"), "eşik kaynağı raporlanmadı"
    finally:
        cfg.unlink(missing_ok=True)

# --- Bilinmeyen eşik sessizce yutulmamalı ---
def t_config_bilinmeyen():
    cfg = FIX / "kotu.toml"
    cfg.write_text("[esikler]\nOLMAYAN = 1\n", encoding="utf-8")
    try:
        p = subprocess.run([sys.executable, str(KONTROL), str(FIX / "temiz.md"),
                            "--config", str(cfg)], capture_output=True, text=True)
        assert p.returncode == 2, f"çıkış kodu 2 bekleniyordu, {p.returncode}"
        assert "OLMAYAN" in p.stderr, "hangi eşiğin bilinmediği yazılmadı"
    finally:
        cfg.unlink(missing_ok=True)

# --- Sürüm kontrolü: taze kopya GUNCEL demeli, çıkış kodu 0 ---
def t_surum_taze():
    p = subprocess.run([sys.executable, str(SURUM), "--cevrimdisi", "--json"],
                       capture_output=True, text=True)
    r = json.loads(p.stdout)
    assert r["yerel_surum"] != "bilinmiyor", "SKILL.md frontmatter'ından sürüm okunamadı"
    assert r["bilgi_tazeligi"], "bilgi-tazeligi alanı okunamadı"
    assert r["durum"] == "guncel", f"taze kopyada durum '{r['durum']}' çıktı"
    assert p.returncode == 0, f"çıkış kodu 0 bekleniyordu, {p.returncode}"

# --- Sürüm kontrolü: eski tarihli kopya ESKIMIS demeli ---
def t_surum_eski():
    import shutil, tempfile
    kaynak = KOK / "skills" / "master-blog"
    with tempfile.TemporaryDirectory() as t:
        hedef = pathlib.Path(t) / "master-blog"
        shutil.copytree(kaynak, hedef)
        md = hedef / "SKILL.md"
        md.write_text(re.sub(r'(?m)^(\s*bilgi-tazeligi:\s*)"[^"]*"',
                             r'\g<1>"2020-01-01"', md.read_text(encoding="utf-8"), count=1),
                      encoding="utf-8")
        p = subprocess.run([sys.executable, str(hedef / "scripts" / "surum-kontrol.py"),
                            "--cevrimdisi", "--json"], capture_output=True, text=True)
        r = json.loads(p.stdout)
        assert r["durum"] == "eskimis", f"180 gün üstü kopyada durum '{r['durum']}'"
        assert p.returncode == 1, f"çıkış kodu 1 bekleniyordu, {p.returncode}"

# --- Skill denetçisi: temiz skill'de sorun bulmamalı ---
def t_denetim_temiz():
    p = subprocess.run([sys.executable, str(DENETIM), "--json"], capture_output=True, text=True)
    r = json.loads(p.stdout)
    assert r["sorun"] == 0, "temiz skill'de tutarsızlık: " + str(r["sorunlar"])
    assert r["kontrol"] >= 8, f"beklenenden az kontrol çalıştı: {r['kontrol']}"
    assert p.returncode == 0

# --- Skill denetçisi: sayı sürüklenmesini yakalamalı (geçmişte 3 kez oldu) ---
def t_denetim_suruklenme():
    import shutil, tempfile
    with tempfile.TemporaryDirectory() as t:
        hedef = pathlib.Path(t) / "master-blog"
        shutil.copytree(KOK / "skills" / "master-blog", hedef)
        md = hedef / "SKILL.md"
        liste = (hedef / "references" / "yayin-oncesi-kontrol.md").read_text(encoding="utf-8")
        gercek = len(re.findall(r"^\s*\d+\.\s", liste, re.M))
        md.write_text(re.sub(r"\b\d+(\s*maddelik)", str(gercek - 3) + r"\1",
                             md.read_text(encoding="utf-8")), encoding="utf-8")
        p = subprocess.run([sys.executable, str(DENETIM), str(hedef), "--json"],
                           capture_output=True, text=True)
        r = json.loads(p.stdout)
        assert any(s["kontrol"] == "sayi-suruklenmesi" for s in r["sorunlar"]), \
            "40 vs 43 sürüklenmesi yakalanmadı"
        assert p.returncode == 1

# --- Skill denetçisi: olmayan dosyaya atfı yakalamalı ---
def t_denetim_eksik_dosya():
    import shutil, tempfile
    with tempfile.TemporaryDirectory() as t:
        hedef = pathlib.Path(t) / "master-blog"
        shutil.copytree(KOK / "skills" / "master-blog", hedef)
        (hedef / "references" / "yazim-katmanlari.md").unlink()
        p = subprocess.run([sys.executable, str(DENETIM), str(hedef), "--json"],
                           capture_output=True, text=True)
        r = json.loads(p.stdout)
        assert any(s["kontrol"] == "dosya-atfi" for s in r["sorunlar"]), \
            "silinen referans dosyası yakalanmadı"

# --- Ölçüm kaydı: aç, bekleyeni gör, işle ---
def t_olcum():
    import tempfile, os
    with tempfile.TemporaryDirectory() as t:
        ort = dict(os.environ)
        c = lambda *a: subprocess.run([sys.executable, str(OLCUM), *a],
                                      capture_output=True, text=True, cwd=t, env=ort)
        p = c("kaydet", "test-yazi", "--sorgu", "test sorgu",
              "--kontrol-grubu", "a,b,c", "--yayin", "2026-01-01")
        assert p.returncode == 0, p.stderr
        kayit = json.loads((pathlib.Path(t) / "olcum" / "test-yazi.json").read_text(encoding="utf-8"))
        assert kayit["noktalar"]["14"]["tarih"] == "2026-01-15", kayit["noktalar"]["14"]
        assert kayit["kontrol_grubu"] == ["a", "b", "c"]
        p = c("bekleyen")
        assert p.returncode == 1 and "test-yazi" in p.stdout, "vadesi geçmiş nokta listelenmedi"
        p = c("isle", "test-yazi", "28", "--gosterim", "100", "--kontrol-medyan", "5")
        assert p.returncode == 0, p.stderr
        kayit = json.loads((pathlib.Path(t) / "olcum" / "test-yazi.json").read_text(encoding="utf-8"))
        assert kayit["noktalar"]["28"]["veri"]["gosterim"] == 100
        # aynı slug ikinci kez açılamaz
        assert c("kaydet", "test-yazi", "--sorgu", "x").returncode == 2

# --- Blokajlı yazı gerçekten 1 döndürmeli ---
def t_blokaj_kodu():
    r, kod = calistir("tireli-kelimeler.md")
    assert r["blokaj"] > 0 and kod == 1, f"blokaj={r['blokaj']} kod={kod}"


print("kontrol.py regresyon testleri")
print("-" * 60)
for ad, fn in [
    ("madde 16 · seoBaslik alanı H1 kaynağı sayılıyor", t_seo_baslik),
    ("madde 14+18 · Türkçe İ ile başlayan hedef kelime", t_turkce_i),
    ("madde 14 · şapkalı harf katlanıyor (zekâ = zeka)", t_sapka),
    ("madde 19 · sahte soru başlıkları soru sayılmıyor", t_sahte_soru),
    ("madde 38 · başlıklı görsel tanınıyor, alt metni denetleniyor", t_gorsel_baslikli),
    ("madde 48 · cümle bölücü kısaltma ve ondalığı koruyor", t_cumle_bolucu),
    ("madde 47/49/50 · üslup kontrolleri tetikleniyor", t_uslup),
    ("madde 44 · kırık görsel yolu blokaj veriyor", t_gorsel_kirik_yol),
    ("madde 44 · SVG ev stili denetleniyor", t_gorsel_svg_stili),
    ("madde 22 · kelime içi tireler sayımı şişirmiyor", t_tire),
    ("BOM'lu dosyada frontmatter okunuyor", t_bom),
    ("madde 36 · iç link tam eşleşme arıyor", t_onek_link),
    ("eksik dosyada çıkış kodu 2 (blokaj değil)", t_eksik_dosya),
    ("temiz yazı blokaj almıyor", t_temiz),
    ("eşikler config dosyasından okunuyor", t_config),
    ("bilinmeyen eşik reddediliyor (kod 2)", t_config_bilinmeyen),
    ("sürüm kontrolü: taze kopya GUNCEL", t_surum_taze),
    ("sürüm kontrolü: eski kopya ESKIMIS", t_surum_eski),
    ("skill denetçisi: temiz skill'de sorun yok", t_denetim_temiz),
    ("skill denetçisi: sayı sürüklenmesini yakalıyor", t_denetim_suruklenme),
    ("skill denetçisi: eksik referans dosyasını yakalıyor", t_denetim_eksik_dosya),
    ("ölçüm kaydı: aç / bekleyen / işle döngüsü", t_olcum),
    ("blokajlı yazı çıkış kodu 1 döndürüyor", t_blokaj_kodu),
]:
    test(ad, fn)

print("-" * 60)
print(f"{sonuc['gecti']} geçti · {sonuc['kaldi']} kaldı")
sys.exit(1 if sonuc["kaldi"] else 0)
