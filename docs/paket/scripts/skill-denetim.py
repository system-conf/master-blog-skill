#!/usr/bin/env python3
"""
master-blog · skill iç tutarlılık denetimi

Skill büyüdükçe metin ile gerçek arasında sessiz sürüklenme oluşur: kontrol listesi
43 maddeye çıkar ama açıklamada "40 maddelik" yazmaya devam eder; terim sayısı değişir
ama dosyalar bayatlar; referans dosyası yeniden adlandırılır ama atıf eski kalır.
Bu script o sınıfı kapatır.

Kullanım:
    python3 skill-denetim.py [skill_dizini]     # varsayılan: script'in üst dizini
    python3 skill-denetim.py --json

Çıkış kodu: 0 tutarlı · 1 tutarsızlık var · 2 çağrı hatası
"""
import argparse, json, re, sys
from pathlib import Path


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("dizin", nargs="?", default=None)
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()

    kok = Path(a.dizin) if a.dizin else Path(__file__).resolve().parent.parent
    skill = kok / "SKILL.md"
    if not skill.exists():
        print(f"HATA: {skill} bulunamadi.", file=sys.stderr)
        sys.exit(2)

    metin = skill.read_text(encoding="utf-8-sig")
    sorunlar, kontrol_sayisi = [], 0

    def bulgu(ad, mesaj):
        sorunlar.append({"kontrol": ad, "mesaj": mesaj})

    # --- 1. frontmatter ---
    kontrol_sayisi += 1
    fm_m = re.match(r"^---\n(.*?)\n---", metin, re.S)
    if not fm_m:
        bulgu("frontmatter", "SKILL.md frontmatter ile baslamiyor")
        fm = {}
    else:
        fm = {k: v.strip().strip('"') for k, v in
              re.findall(r'^\s*([a-zA-Z-]+):\s*(.+)$', fm_m.group(1), re.M)}
        for alan in ("name", "description"):
            if not fm.get(alan):
                bulgu("frontmatter", f"zorunlu alan eksik: {alan}")
        if fm.get("name") and fm["name"] != kok.name:
            bulgu("frontmatter", f"name '{fm['name']}' dizin adi '{kok.name}' ile ayni degil")

    # --- 2. atif yapilan her dosya var mi ---
    kontrol_sayisi += 1
    for yol in sorted(set(re.findall(r'`((?:references|scripts|evals)/[\w.\-]+)`', metin))):
        if not (kok / yol).exists():
            bulgu("dosya-atfi", f"SKILL.md '{yol}' dosyasina atif yapiyor ama dosya yok")

    # --- 3. kontrol listesi madde sayisi iddiasi ---
    kontrol_sayisi += 1
    liste = kok / "references" / "yayin-oncesi-kontrol.md"
    if liste.exists():
        liste_metni = liste.read_text(encoding="utf-8")
        gercek = len(re.findall(r"^\s*(\d+)\.\s", liste_metni, re.M))
        numaralar = [int(x) for x in re.findall(r"^\s*(\d+)\.\s", liste_metni, re.M)]
        if numaralar and numaralar != list(range(1, len(numaralar) + 1)):
            bulgu("kontrol-listesi", f"madde numaralari surekli degil (1..{len(numaralar)} bekleniyordu)")
        # Yalnizca GUNCEL BUYUKLUK IDDIALARI denetlenir ("43 maddelik liste").
        # Tarihsel anlatim ("o zaman 41 terim vardi") iddia degildir, elenir.
        for kaynak, ad in ((metin, "SKILL.md"), (liste_metni, "yayin-oncesi-kontrol.md")):
            for iddia in set(re.findall(r"(\d+)\s*maddelik", kaynak)):
                if int(iddia) != gercek:
                    bulgu("sayi-suruklenmesi",
                          f"{ad} '{iddia} maddelik' diyor ama listede {gercek} madde var")
            for iddia in set(re.findall(r"__/(\d+)|/(\d+)\s*gecti", kaynak)):
                sayi = next((x for x in iddia if x), None)
                if sayi and int(sayi) != gercek:
                    bulgu("sayi-suruklenmesi", f"{ad} rapor sablonunda /{sayi} yaziyor, dogrusu /{gercek}")
        # SKILL.md'de atif yapilan madde numaralari listede var mi
        for no in set(re.findall(r"[Mm]adde(?:si|leri)?\s+(\d+)", metin)):
            if int(no) > gercek:
                bulgu("madde-atfi", f"SKILL.md madde {no}'e atif yapiyor ama listede {gercek} madde var")
    else:
        bulgu("dosya-atfi", "references/yayin-oncesi-kontrol.md yok")

    # --- 4. terim sayisi iddiasi ---
    kontrol_sayisi += 1
    sozluk = kok / "references" / "terimler-sozlugu.md"
    if sozluk.exists():
        sozluk_metni = sozluk.read_text(encoding="utf-8")
        gercek_terim = len(re.findall(r"^### ", sozluk_metni, re.M))
        for kaynak, ad in ((metin, "SKILL.md"), (sozluk_metni, "terimler-sozlugu.md")):
            for iddia in set(re.findall(r"(\d+)\s*terimlik", kaynak)):
                if int(iddia) != gercek_terim:
                    bulgu("sayi-suruklenmesi",
                          f"{ad} '{iddia} terim' diyor ama sozlukte {gercek_terim} terim var")

    # --- 5. yol haritasindaki her asamanin bolumu var mi ---
    kontrol_sayisi += 1
    haritadaki = set(re.findall(r"^\|\s*\*?\*?([\d.]+)\*?\*?\s*\|", metin, re.M))
    bolumler = " ".join(re.findall(r"^## .*$", metin, re.M))
    for asama in sorted(haritadaki):
        if not re.search(r"Aşama\s+" + re.escape(asama) + r"\b", bolumler) and \
           not re.search(r"Aşama\s+\d+-\d+", bolumler):
            bulgu("asama-atfi", f"yol haritasi Asama {asama} diyor ama basligi yok")

    # --- 6. script'ler calisabilir mi ---
    kontrol_sayisi += 1
    for s in sorted((kok / "scripts").glob("*.py")) if (kok / "scripts").exists() else []:
        try:
            compile(s.read_text(encoding="utf-8"), str(s), "exec")
        except SyntaxError as e:
            bulgu("script", f"{s.name}: sozdizimi hatasi satir {e.lineno}")

    # --- 7. evals gecerli mi ---
    kontrol_sayisi += 1
    ev = kok / "evals" / "evals.json"
    if ev.exists():
        try:
            veri = json.loads(ev.read_text(encoding="utf-8"))
            for i, senaryo in enumerate(veri):
                for alan in ("query", "expected_behavior"):
                    if not senaryo.get(alan):
                        bulgu("evals", f"senaryo {i}: '{alan}' eksik")
        except json.JSONDecodeError as e:
            bulgu("evals", f"gecersiz JSON: {e}")

    # --- 8. tazelik alani makul mu ---
    kontrol_sayisi += 1
    if fm.get("bilgi-tazeligi") and not re.fullmatch(r"\d{4}-\d{2}-\d{2}", fm["bilgi-tazeligi"]):
        bulgu("frontmatter", f"bilgi-tazeligi '{fm['bilgi-tazeligi']}' YYYY-MM-DD bicimde degil")

    if a.json:
        print(json.dumps({"dizin": str(kok), "kontrol": kontrol_sayisi,
                          "sorun": len(sorunlar), "sorunlar": sorunlar},
                         ensure_ascii=False, indent=2))
    else:
        print(f"master-blog ic tutarlilik denetimi · {kok}")
        print("-" * 70)
        if not sorunlar:
            print(f"{kontrol_sayisi} kontrol calisti · tutarsizlik yok")
        else:
            for s in sorunlar:
                print(f"  [{s['kontrol']}] {s['mesaj']}")
            print("-" * 70)
            print(f"{kontrol_sayisi} kontrol · {len(sorunlar)} tutarsizlik")
    sys.exit(1 if sorunlar else 0)


if __name__ == "__main__":
    main()
