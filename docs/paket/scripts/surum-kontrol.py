#!/usr/bin/env python3
"""
master-blog · sürüm ve bilgi tazeliği kontrolü

Bu skill'in bilgi tabanı zamanla bayatlar: arama motoru davranışı, zengin sonuç
tipleri, rapor alanları ve bot adları değişir. Dosya olarak kurulmuş bir skill
güncelleme almadığı için kullanıcı bunu fark edemez. Bu script iki soruyu cevaplar:

  1. Elimdeki kopya kaç günlük? (çevrimdışı — tarih aritmetiği)
  2. Yayınlanmış daha yeni bir sürüm var mı? (çevrimiçi — isteğe bağlı)

Kullanım:
    python3 surum-kontrol.py                 # yerel + uzak kontrol
    python3 surum-kontrol.py --cevrimdisi    # ağa çıkmadan yalnızca tazelik
    python3 surum-kontrol.py --json

Çıkış kodu: 0 güncel · 1 güncelleme/tazeleme gerekli · 2 çağrı hatası
"""
import argparse, json, re, sys, urllib.error, urllib.request
from datetime import date, datetime
from pathlib import Path

UZAK = "https://system-conf.github.io/master-blog-skill/surum.json"
TAZE_GUN, ESKI_GUN = 90, 180      # kaynaklar.md'nin kendi tazeleme kuralı: 3 ay


def skill_dosyasi():
    """SKILL.md'yi script'in konumundan yukarı doğru arar."""
    for kok in (Path(__file__).resolve().parent.parent, Path.cwd()):
        aday = kok / "SKILL.md"
        if aday.exists():
            return aday
    return None


def frontmatter(yol):
    metin = yol.read_text(encoding="utf-8-sig")
    m = re.match(r"^---\n(.*?)\n---", metin, re.S)
    if not m:
        return {}
    alanlar = {}
    for satir in m.group(1).split("\n"):
        mm = re.match(r'^\s*([a-zA-Z-]+):\s*"?([^"\n]+?)"?\s*$', satir)
        if mm:
            alanlar[mm.group(1)] = mm.group(2)
    return alanlar


def uzak_surum(zaman_asimi=6):
    istek = urllib.request.Request(UZAK, headers={"User-Agent": "master-blog surum-kontrol"})
    with urllib.request.urlopen(istek, timeout=zaman_asimi) as r:
        return json.loads(r.read().decode("utf-8"))


def surum_dizisi(s):
    return tuple(int(x) for x in re.findall(r"\d+", str(s))[:3] or [0])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cevrimdisi", action="store_true", help="ağa çıkma")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()

    yol = skill_dosyasi()
    if not yol:
        print("HATA: SKILL.md bulunamadi. Script'i skill dizininden calistir.", file=sys.stderr)
        sys.exit(2)

    fm = frontmatter(yol)
    yerel_surum = fm.get("surum", "bilinmiyor")
    tazelik = fm.get("bilgi-tazeligi", "")
    try:
        gun = (date.today() - datetime.strptime(tazelik, "%Y-%m-%d").date()).days
    except ValueError:
        gun = None

    rapor = {"yerel_surum": yerel_surum, "bilgi_tazeligi": tazelik or None,
             "gun": gun, "uzak_surum": None, "uzak_tazelik": None,
             "durum": "bilinmiyor", "aksiyon": []}

    # --- tazelik ---
    if gun is None:
        rapor["durum"] = "tarih-okunamadi"
        rapor["aksiyon"].append("SKILL.md frontmatter'inda bilgi-tazeligi alani yok ya da bozuk.")
    elif gun <= TAZE_GUN:
        rapor["durum"] = "guncel"
    elif gun <= ESKI_GUN:
        rapor["durum"] = "tazelenmeli"
        rapor["aksiyon"].append(
            f"Bilgi tabani {gun} gunluk. references/kaynaklar.md kaydini WebSearch ile tazele "
            f"ya da yeni surume gec.")
    else:
        rapor["durum"] = "eskimis"
        rapor["aksiyon"].append(
            f"Bilgi tabani {gun} gunluk. Arama motoru davranisina dair iddialar dogrulanmadan "
            f"KULLANILMAMALI. Once guncelle, sonra yaz.")

    # --- uzak surum ---
    if not a.cevrimdisi:
        try:
            u = uzak_surum()
            rapor["uzak_surum"] = u.get("surum")
            rapor["uzak_tazelik"] = u.get("bilgi_tazeligi")
            if surum_dizisi(rapor["uzak_surum"]) > surum_dizisi(yerel_surum):
                rapor["aksiyon"].append(
                    f"Yeni surum var: {yerel_surum} -> {rapor['uzak_surum']}. "
                    f"Degisiklikler: {u.get('degisiklikler_url', '')}")
                rapor["aksiyon"].append("Guncelleme: " + (u.get("guncelleme_komutu") or ""))
                if rapor["durum"] == "guncel":
                    rapor["durum"] = "yeni-surum-var"
        except (urllib.error.URLError, OSError, ValueError, TimeoutError) as e:
            rapor["aksiyon"].append(f"Uzak surum kontrol edilemedi ({type(e).__name__}). "
                                    f"Yalnizca yerel tazelik degerlendirildi.")

    if a.json:
        print(json.dumps(rapor, ensure_ascii=False, indent=2))
    else:
        SIM = {"guncel": "GUNCEL", "yeni-surum-var": "YENI SURUM", "tazelenmeli": "TAZELENMELI",
               "eskimis": "ESKIMIS", "tarih-okunamadi": "BELIRSIZ", "bilinmiyor": "BELIRSIZ"}
        print(f"master-blog · surum {yerel_surum} · bilgi tazeligi {tazelik or '?'}"
              + (f" ({gun} gun)" if gun is not None else ""))
        if rapor["uzak_surum"]:
            print(f"yayinlanmis surum: {rapor['uzak_surum']} · {rapor['uzak_tazelik']}")
        print("-" * 66)
        print(f"Durum: {SIM.get(rapor['durum'], rapor['durum'])}")
        for x in rapor["aksiyon"]:
            print(f"  - {x}")
        if rapor["durum"] == "guncel":
            print("  - Yapilacak bir sey yok.")

    sys.exit(0 if rapor["durum"] == "guncel" else 1)


if __name__ == "__main__":
    main()
