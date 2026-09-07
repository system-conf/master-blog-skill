# master-blog

Claude için uçtan uca SEO/GEO blog üretim skill'i + skill'i anlatan tek dosyalık web sitesi.

## Klasör yapısı

```
skill/master-blog/          ← kurulacak skill (bu klasörü kopyala)
  SKILL.md                    13 aşamalı süreç, 2 atlanamaz kapı
  references/
    yayin-oncesi-kontrol.md   40 maddelik denetim listesi
    terimler-sozlugu.md       ÜRETİLİR — elle düzenleme
    schema-ve-geo.md          yapılandırılmış veri + AI motoru notları
    kaynaklar.md              zamana bağlı iddiaların kaynak kaydı (3 ayda bir tazele)
  scripts/
    kontrol.py                mekanik yayın öncesi kontrol (Aşama 10a)

site/
  template.html             site kabuğu (CSS + JS)
  data/terms.js             terim sözlüğünün TEK doğruluk kaynağı

build.py                    terms.js + skill dosyaları → dist/index.html
dist/index.html             yayınlanabilir tek dosyalık site (~425 KB)
```

## Kurulum (skill)

```bash
cp -r skill/master-blog ~/.claude/skills/          # kişisel
# veya
cp -r skill/master-blog <proje>/.claude/skills/    # projeye özel
```

Sonra yeni bir Claude Code oturumu aç ve: `master-blog skill'iyle yeni yazı hazırla`

## Siteyi yeniden üret

```bash
python3 build.py
```

Terim eklemek/düzenlemek için yalnızca `site/data/terms.js` düzenlenir; `build.py`
hem siteyi hem skill'in terim sözlüğü referansını yeniden üretir.

`terms.js` alanları: `slug, name, en, cat, level, short, simple, technical, why,
example, myth, related[], usedIn`. `related` içindeki slug'lar var olmalı — build
sırasında kırık bağlantı sessizce kartlardan düşer, bu yüzden ekledikten sonra kontrol et:

```bash
node -e "const t=eval(require('fs').readFileSync('site/data/terms.js','utf8')+'; TERMS');
const s=new Set(t.map(x=>x.slug));t.forEach(x=>x.related.forEach(r=>{if(!s.has(r))console.log('kirik:',x.slug,'->',r)}));
console.log(t.length,'terim')"
```

## Mekanik kontrol

40 maddelik listenin ölçülebilir kısmını gerçekten sayar — modelin "muhtemelen tamam"
demesini engeller:

```bash
python3 skill/master-blog/scripts/kontrol.py <yazi.md> --kelime "hedef kelime" --net
```

Ölçtükleri: kelime sayısı (frontmatter/kod/URL hariç), H1 adedi, başlık hiyerarşisi
sıçraması, title ve meta description karakter uzunluğu, hedef kelimenin title'daki konumu,
slug formatı, soru biçimli H2 oranı, iç link sayısı, jenerik ve tekrar eden anchor'lar,
dış linklerin HTTP durumu (`--net`), tablo ve özet bölümü varlığı, görsel alt metinleri,
paragraf uzunluğu, yayın tarihi alanı.

Blokaj varsa çıkış kodu **1** döner — CI'da kullanılabilir. Eşikler dosyanın başındaki
sabitlerden (`TITLE_MAX`, `KELIME_MIN`, `IC_LINK_MIN` …) projene göre uyarlanır.

Yargı gerektiren maddeler (niyet, kanibalizasyon, kaynak gerçekliği, E-E-A-T) script'in
işi değildir; onları model değerlendirir.

## Yayın

Site tek dosyadır (`dist/index.html`). Cloudflare Workers ile yayınlamak için:

```bash
npx wrangler login     # bir kez, tarayıcı açar
npx wrangler deploy    # wrangler.jsonc dist/ klasörünü yayınlar
```

## Bilgi tazeliği

`skill/master-blog/references/kaynaklar.md` zamana bağlı iddiaların kaynak kaydıdır
(son doğrulama: 7 Eylül 2026). SEO/GEO tarafı hızlı değiştiği için 3 ayda bir gözden
geçir; güncellediğinde `build.py` çalıştır — site de tazelenir.

## Notlar

- Site tek dosyadır; herhangi bir statik sunucuya `dist/index.html` olarak konabilir.
- Sitedeki "İndir" düğmesi gömülü çerçevede (iframe) çalışmaz — o durumda kopyalama
  paneli açılır. Kendi sunucunda barındırıldığında normal indirme çalışır.
- Lisans: MIT.
