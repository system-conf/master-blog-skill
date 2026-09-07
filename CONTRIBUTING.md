# Katkı Rehberi

Teşekkürler. Bu depo iki şeyi barındırıyor: bir Claude skill'i ve onu anlatan site.
İkisi de **tek bir kaynaktan üretiliyor**, bu yüzden neyi düzenleyeceğin önemli.

## Elle düzenlenen dosyalar

| Dosya | Ne için |
|---|---|
| `skills/master-blog/SKILL.md` | Sürecin kendisi (13 aşama, kapılar, kırmızı çizgiler) |
| `skills/master-blog/references/*.md` | Derin referanslar — **`terimler-sozlugu.md` hariç** |
| `skills/master-blog/scripts/kontrol.py` | Mekanik denetçi |
| `site/data/terms.js` | Terim sözlüğünün tek doğruluk kaynağı |
| `site/template.html` | Site kabuğu (CSS + JS) |
| `agents/`, `.claude-plugin/`, `tests/` | Alt ajan, plugin tanımı, testler |

## Üretilen dosyalar — elle düzenleme

- `skills/master-blog/references/terimler-sozlugu.md`
- `docs/**` (48 statik sayfa, `assets/`, `sitemap.xml`, `robots.txt`)
- `dist/artifact.html`

Bunlar `python3 build.py` ile üretilir ve **commit'lenir**. CI, üretilen çıktının
commit'lenenle aynı olduğunu `git diff --exit-code` ile denetler; build'i çalıştırmayı
unutursan PR kırmızı olur.

## Akış

```bash
python3 build.py            # docs/ + dist/ + terim sözlüğü
python3 tests/calistir.py   # regresyon testleri
git add -A && git commit
```

## Terim eklerken

`site/data/terms.js` içine tüm zorunlu alanlarla ekle: `slug, name, en, cat, level, short,
simple, technical, why, example, myth, related[], usedIn`. İsteğe bağlı `src[]` alanı
`{t, u}` biçiminde ve `https://` ile başlamalı.

Kurallar:
- `related` içindeki her slug var olmalı; kendine referans yasak. Build bunu denetler.
- Zamana bağlı bir iddia yazıyorsan (**arama motoru davranışı, metrik eşiği, rapor alanı,
  bot adı**) `references/kaynaklar.md` dosyasına tarih + kaynak + sınıf ile ekle:
  `BİRİNCİL` (sağlayıcı dokümantasyonu) · `ÖLÇÜM` (üçüncü taraf veri, örneklemiyle) ·
  `SEKTÖR` (resmî duyuru yok).
- Kaynak URL'ini eklemeden önce `curl` ile 200 döndüğünü doğrula.
- Sayısal vaat yazma ("trafiği %40 artırır") — ölçülmüş bir çalışma yoksa iddia edilmez.

## `kontrol.py` değiştirirken

Her davranış değişikliği için `tests/fixtures/` altına bir örnek dosya ve
`tests/calistir.py` içine bir test ekle. Mevcut testlerin hepsi geçmişte **gerçekten
görülmüş** bir hatayı temsil eder; yenisi de öyle olmalı.

Eşikleri (`TITLE_MAX`, `KELIME_MIN`, `IC_LINK_MIN` …) koddan değiştirme — bunlar artık
`master-blog.toml` ile projeye özel ayarlanıyor. Varsayılanı değiştirmen gerekiyorsa
**gerekçesini yorum olarak yaz**.

## Sürümleme

[SemVer](https://semver.org/lang/tr/). Sürüm üç yerde birden güncellenir:
`.claude-plugin/plugin.json`, `SKILL.md` frontmatter `metadata.surum`, `CHANGELOG.md`.
