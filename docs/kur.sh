#!/bin/sh
# master-blog · kurulum
# Kaynak : https://github.com/system-conf/master-blog-skill
# Ne yapar: 13 dosyayı indirir, hedef dizine yazar, kurulumu doğrular.
# Başka hiçbir şey yapmaz — ne PATH'e dokunur, ne kabuk profiline, ne ağa veri yollar.
set -eu

PAKET="https://system-conf.github.io/master-blog-skill/paket"
HEDEF="$HOME/.claude/skills/master-blog"
KAPSAM="kişisel (tüm projeler)"

if [ "${1:-}" = "--proje" ]; then
  HEDEF="$(pwd)/.claude/skills/master-blog"
  KAPSAM="projeye özel ($(pwd))"
elif [ "${1:-}" = "--yardim" ] || [ "${1:-}" = "-h" ]; then
  echo "Kullanım: sh kur.sh [--proje]"
  echo "  (bayraksız)  ~/.claude/skills/master-blog altına kurar"
  echo "  --proje      bulunduğun projenin .claude/skills/ dizinine kurar"
  exit 0
fi

DOSYALAR="SKILL.md \
     references/yayin-oncesi-kontrol.md \
     references/terimler-sozlugu.md \
     references/schema-ve-geo.md \
     references/kaynaklar.md \
     references/kullanim-senaryolari.md \
     references/yazim-katmanlari.md \
     references/yayin-ve-olcum.md \
     scripts/kontrol.py \
     scripts/surum-kontrol.py \
     scripts/olcum.py \
     scripts/skill-denetim.py \
     evals/evals.json"

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
