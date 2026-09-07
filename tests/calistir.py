#!/usr/bin/env python3
"""
master-blog regresyon testleri — yalnızca standart kütüphane, ek bağımlılık yok.

Her test, geçmişte gerçekten görülmüş bir hatayı temsil eder. Çalıştır:
    python3 tests/calistir.py
Çıkış kodu: başarısız test varsa 1.
"""
import json, pathlib, subprocess, sys

KOK = pathlib.Path(__file__).resolve().parent.parent
FIX = KOK / "tests" / "fixtures"
KONTROL = KOK / "skills" / "master-blog" / "scripts" / "kontrol.py"

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

# --- Hata 3: soru sezgiseli alt dize araması yapıyordu ---
def t_sahte_soru():
    r, _ = calistir("sahte-soru-h2.md")
    m = madde(r, 19, "Soru")
    assert m["durum"] == "uyari", f"4 sahte soru başlığı soru sayıldı: {m['detay']}"
    assert m["detay"].startswith("0/4"), f"0/4 bekleniyordu: {m['detay']}"

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

# --- Blokajlı yazı gerçekten 1 döndürmeli ---
def t_blokaj_kodu():
    r, kod = calistir("tireli-kelimeler.md")
    assert r["blokaj"] > 0 and kod == 1, f"blokaj={r['blokaj']} kod={kod}"


print("kontrol.py regresyon testleri")
print("-" * 60)
for ad, fn in [
    ("madde 16 · seoBaslik alanı H1 kaynağı sayılıyor", t_seo_baslik),
    ("madde 14+18 · Türkçe İ ile başlayan hedef kelime", t_turkce_i),
    ("madde 19 · sahte soru başlıkları soru sayılmıyor", t_sahte_soru),
    ("madde 22 · kelime içi tireler sayımı şişirmiyor", t_tire),
    ("BOM'lu dosyada frontmatter okunuyor", t_bom),
    ("madde 36 · iç link tam eşleşme arıyor", t_onek_link),
    ("eksik dosyada çıkış kodu 2 (blokaj değil)", t_eksik_dosya),
    ("temiz yazı blokaj almıyor", t_temiz),
    ("eşikler config dosyasından okunuyor", t_config),
    ("bilinmeyen eşik reddediliyor (kod 2)", t_config_bilinmeyen),
    ("blokajlı yazı çıkış kodu 1 döndürüyor", t_blokaj_kodu),
]:
    test(ad, fn)

print("-" * 60)
print(f"{sonuc['gecti']} geçti · {sonuc['kaldi']} kaldı")
sys.exit(1 if sonuc["kaldi"] else 0)
