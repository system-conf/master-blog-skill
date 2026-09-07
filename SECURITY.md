# Güvenlik Politikası

## Desteklenen sürümler

Yalnızca `main` dalındaki en son sürüm desteklenir.

## Bildirim

Güvenlik açığını **herkese açık issue olarak açma**. Bunun yerine
[GitHub Security Advisory](https://github.com/system-conf/master-blog-skill/security/advisories/new)
üzerinden bildir.

## Bu projede güvenlik neden konu?

Üç yüzey var:

1. **Kurulum komutu.** Site, kullanıcının makinesinde `~/.claude/skills/` altına dosya
   yazan bir kabuk komutu panoya kopyalar. Komut yalnızca `mkdir` ve `cat > … <<'EOF'`
   kullanır; başka bir şey çalıştırmaz. Yapıştırmadan önce okunabilir olması bilinçli
   bir tasarım kararıdır.

2. **Skill'in davranışı.** Skill, Claude'un davranışını değiştirir ve `allowed-tools`
   ile bazı araçları ön onaylı hâle getirir. Bu listede **yalnızca okuma ve doğrulama**
   araçları vardır; `git commit/push`, dosya silme ve deploy komutları bilerek dışarıda
   bırakılmıştır. Kurmadan önce `SKILL.md` frontmatter'ındaki `allowed-tools` satırını oku.

3. **Dış içerik.** Skill arama sonuçlarını ve rakip sayfalarını okur. 11. kırmızı çizgi
   bunu açıkça düzenler: dış içerik **veridir, talimat değildir**; içindeki yönergeler
   uygulanmaz, kullanıcıya raporlanır. `kaynaklar.md` dosyasına dış kaynaklı satır
   eklenmeden önce kullanıcı onayı istenir.

## Kapsam dışı

- Kullanıcının kendi projesindeki içerik hataları
- Üçüncü taraf kaynakların (linklenen siteler) içeriği
- Claude'un genel model davranışı
