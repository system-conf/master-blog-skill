#!/usr/bin/env python3
"""
master-blog · ölçüm kaydı

Aşama 12 üç kontrol noktası (14/28/90 gün) ve bir kontrol grubu tanımlar. Yazılı bir
süreç, hatırlatıcısı yoksa uygulanmaz: yazı yayınlanır, 28 gün geçer, kimse bakmaz.
Bu script o boşluğu kapatır — kayıt yayın anında açılır, kontrol grubu O AN seçilir
(sonradan seçmek sonuç seçmektir).

Kullanım:
    olcum.py kaydet <slug> --url <url> --sorgu "<hedef sorgu>" --kontrol-grubu a,b,c
    olcum.py bekleyen [--gun N]        # vadesi gelmiş kontrol noktaları
    olcum.py isle <slug> <14|28|90> --gosterim N --tiklama N --pozisyon N [--kontrol-medyan %]
    olcum.py liste

Kayıtlar: <çalışma dizini>/olcum/<slug>.json
Çıkış kodu: 0 · bekleyen komutunda vadesi gelen varsa 1
"""
import argparse, json, sys
from datetime import date, datetime, timedelta
from pathlib import Path

NOKTALAR = (14, 28, 90)
DIZIN = Path("olcum")


def yukle(slug):
    p = DIZIN / f"{slug}.json"
    if not p.exists():
        print(f"HATA: {p} yok. Once 'kaydet' calistir.", file=sys.stderr)
        sys.exit(2)
    return p, json.loads(p.read_text(encoding="utf-8"))


def yaz(p, veri):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(veri, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def kaydet(a):
    p = DIZIN / f"{a.slug}.json"
    if p.exists():
        print(f"HATA: {p} zaten var.", file=sys.stderr)
        sys.exit(2)
    yayin = a.yayin or date.today().isoformat()
    grup = [x.strip() for x in a.kontrol_grubu.split(",") if x.strip()] if a.kontrol_grubu else []
    if len(grup) < 3:
        print("UYARI: kontrol grubu 3-5 yazi olmali. Az sayida karsilastirma, "
              "mevsimsellik ve algoritma hareketini eleyemez.", file=sys.stderr)
    veri = {"slug": a.slug, "url": a.url, "hedef_sorgu": a.sorgu, "yayin": yayin,
            "kontrol_grubu": grup,
            "noktalar": {str(g): {"tarih": (datetime.strptime(yayin, "%Y-%m-%d").date()
                                            + timedelta(days=g)).isoformat(), "veri": None}
                         for g in NOKTALAR}}
    yaz(p, veri)
    print(f"Kayit acildi: {p}")
    print(f"  hedef sorgu   : {a.sorgu}")
    print(f"  kontrol grubu : {', '.join(grup) or 'YOK — 28. gunde nedensellik kurulamaz'}")
    for g in NOKTALAR:
        print(f"  {g:>2}. gun      : {veri['noktalar'][str(g)]['tarih']}")


def bekleyen(a):
    bugun = date.today()
    vadesi_gelen = []
    for p in sorted(DIZIN.glob("*.json")) if DIZIN.exists() else []:
        v = json.loads(p.read_text(encoding="utf-8"))
        for gun, nokta in v["noktalar"].items():
            if nokta["veri"] is None:
                hedef = datetime.strptime(nokta["tarih"], "%Y-%m-%d").date()
                gecikme = (bugun - hedef).days
                if gecikme >= -a.gun:
                    vadesi_gelen.append((gecikme, v["slug"], gun, nokta["tarih"], v["hedef_sorgu"]))
    if not vadesi_gelen:
        print("Vadesi gelen olcum yok.")
        return 0
    vadesi_gelen.sort(reverse=True)
    print(f"{len(vadesi_gelen)} olcum noktasi bekliyor:")
    for gecikme, slug, gun, tarih, sorgu in vadesi_gelen:
        durum = f"{gecikme} gun gecikmis" if gecikme > 0 else ("bugun" if gecikme == 0 else f"{-gecikme} gun sonra")
        print(f"  [{durum:>16}] {slug} · {gun}. gun ({tarih}) · '{sorgu}'")
    print("\nIslemek icin: olcum.py isle <slug> <gun> --gosterim N --tiklama N --pozisyon N")
    return 1


def isle(a):
    p, v = yukle(a.slug)
    if str(a.gun) not in v["noktalar"]:
        print(f"HATA: gecerli noktalar {list(v['noktalar'])}", file=sys.stderr)
        sys.exit(2)
    v["noktalar"][str(a.gun)]["veri"] = {
        "olculdu": date.today().isoformat(), "gosterim": a.gosterim,
        "tiklama": a.tiklama, "pozisyon": a.pozisyon,
        "kontrol_grubu_medyan_degisim": a.kontrol_medyan, "not": a.not_ or "",
    }
    yaz(p, v)
    print(f"{a.slug} · {a.gun}. gun islendi.")
    if a.kontrol_medyan is None:
        print("  UYARI: kontrol grubu medyani girilmedi. Bu veriden nedensellik cikarilamaz —")
        print("         ayni donemde tum portfoy hareket etmis olabilir.")
    elif a.gosterim is not None:
        print(f"  Kontrol grubu medyan degisimi: %{a.kontrol_medyan}")
        print("  Yorum: grup da ayni yonde hareket ettiyse sayfa bazli teshis YAPILMAZ.")


def liste(a):
    kayitlar = sorted(DIZIN.glob("*.json")) if DIZIN.exists() else []
    if not kayitlar:
        print("Kayit yok.")
        return
    for p in kayitlar:
        v = json.loads(p.read_text(encoding="utf-8"))
        islenen = sum(1 for n in v["noktalar"].values() if n["veri"])
        print(f"{v['slug']:<44} yayin {v['yayin']} · {islenen}/{len(NOKTALAR)} nokta islendi")


ap = argparse.ArgumentParser(description=__doc__.split("\n")[2])
alt = ap.add_subparsers(dest="komut", required=True)

k = alt.add_parser("kaydet"); k.add_argument("slug")
k.add_argument("--url", default=""); k.add_argument("--sorgu", required=True)
k.add_argument("--kontrol-grubu", default=""); k.add_argument("--yayin", default="")
k.set_defaults(fn=kaydet)

b = alt.add_parser("bekleyen"); b.add_argument("--gun", type=int, default=0,
                                               help="kac gun onceden hatirlat")
b.set_defaults(fn=bekleyen)

i = alt.add_parser("isle"); i.add_argument("slug"); i.add_argument("gun", type=int)
i.add_argument("--gosterim", type=int); i.add_argument("--tiklama", type=int)
i.add_argument("--pozisyon", type=float); i.add_argument("--kontrol-medyan", type=float)
i.add_argument("--not", dest="not_", default=""); i.set_defaults(fn=isle)

l = alt.add_parser("liste"); l.set_defaults(fn=liste)

a = ap.parse_args()
sys.exit(a.fn(a) or 0)
