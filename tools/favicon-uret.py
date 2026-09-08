#!/usr/bin/env python3
"""Favicon üretici — sitenin logosunu (turuncu kare + >_ ) ikon dosyalarına çevirir.

Marka rengi ya da glif değişmedikçe tekrar çalıştırmaya gerek yok:
    python3 tools/favicon-uret.py
Çıktı: site/assets/{favicon.svg, favicon.ico, apple-touch-icon.png}
build.py bu dosyaları docs/ içine kopyalar.

Bağımlılık yok: PNG, zlib + struct ile elle yazılır.
"""
import math, pathlib, struct, zlib

KOK = pathlib.Path(__file__).parent.parent
CIKTI = KOK / "site" / "assets"

ZEMIN = (0xFF, 0x6A, 0x00)   # --or
GLIF  = (0x10, 0x06, 0x00)   # buton metni rengi
YARICAP = 0.22               # köşe yuvarlaklığı (kenarın oranı)
ORNEK = 4                    # kenar başına süper örnekleme


def _yuvarlak_kare(x, y):
    """Birim karede yuvarlatılmış köşe testi."""
    r = YARICAP
    cx = min(max(x, r), 1 - r)
    cy = min(max(y, r), 1 - r)
    return (x - cx) ** 2 + (y - cy) ** 2 <= r * r


def _cizgi_mesafe(px, py, ax, ay, bx, by):
    dx, dy = bx - ax, by - ay
    uzunluk = dx * dx + dy * dy
    t = 0.0 if uzunluk == 0 else max(0.0, min(1.0, ((px - ax) * dx + (py - ay) * dy) / uzunluk))
    return math.hypot(px - (ax + t * dx), py - (ay + t * dy))


def _glif(x, y):
    """'>' çift çizgisi + '_' alt çizgisi."""
    kalinlik = 0.062
    if _cizgi_mesafe(x, y, 0.27, 0.29, 0.47, 0.50) <= kalinlik: return True
    if _cizgi_mesafe(x, y, 0.47, 0.50, 0.27, 0.71) <= kalinlik: return True
    if 0.53 <= x <= 0.78 and 0.645 <= y <= 0.715: return True
    return False


def piksel(boyut):
    """RGBA satırları üretir (süper örneklemeli kenar yumuşatma)."""
    satirlar = []
    for py in range(boyut):
        satir = bytearray()
        for px in range(boyut):
            zemin_ic = glif_ic = 0
            for sy in range(ORNEK):
                for sx in range(ORNEK):
                    x = (px + (sx + 0.5) / ORNEK) / boyut
                    y = (py + (sy + 0.5) / ORNEK) / boyut
                    if _yuvarlak_kare(x, y):
                        zemin_ic += 1
                        if _glif(x, y):
                            glif_ic += 1
            toplam = ORNEK * ORNEK
            if zemin_ic == 0:
                satir += bytes((0, 0, 0, 0))
                continue
            oran = glif_ic / zemin_ic
            renk = tuple(round(ZEMIN[i] * (1 - oran) + GLIF[i] * oran) for i in range(3))
            satir += bytes((*renk, round(255 * zemin_ic / toplam)))
        satirlar.append(bytes(satir))
    return satirlar


def png(boyut):
    ham = b"".join(b"\x00" + s for s in piksel(boyut))

    def parca(tip, veri):
        return (struct.pack(">I", len(veri)) + tip + veri
                + struct.pack(">I", zlib.crc32(tip + veri) & 0xFFFFFFFF))

    return (b"\x89PNG\r\n\x1a\n"
            + parca(b"IHDR", struct.pack(">IIBBBBB", boyut, boyut, 8, 6, 0, 0, 0))
            + parca(b"IDAT", zlib.compress(ham, 9))
            + parca(b"IEND", b""))


def ico(boyut):
    """ICO içine PNG gömme (Vista+ destekler)."""
    govde = png(boyut)
    baslik = struct.pack("<HHH", 0, 1, 1)
    girdi = struct.pack("<BBBBHHII", boyut % 256, boyut % 256, 0, 0, 1, 32,
                        len(govde), 22)
    return baslik + girdi + govde


SVG = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" role="img" aria-label="master-blog">
  <rect width="100" height="100" rx="22" fill="#{ZEMIN[0]:02X}{ZEMIN[1]:02X}{ZEMIN[2]:02X}"/>
  <g stroke="#{GLIF[0]:02X}{GLIF[1]:02X}{GLIF[2]:02X}" stroke-width="12.4" stroke-linecap="round" stroke-linejoin="round" fill="none">
    <path d="M27 29 L47 50 L27 71"/>
    <path d="M56.5 68 L74.5 68"/>
  </g>
</svg>
"""

CIKTI.mkdir(parents=True, exist_ok=True)
(CIKTI / "favicon.svg").write_text(SVG, encoding="utf-8")
(CIKTI / "favicon.ico").write_bytes(ico(32))
(CIKTI / "apple-touch-icon.png").write_bytes(png(180))
for f in ("favicon.svg", "favicon.ico", "apple-touch-icon.png"):
    print(f"{f:24} {(CIKTI / f).stat().st_size:>7} bayt")
