# Değişiklik Günlüğü

Biçim [Keep a Changelog](https://keepachangelog.com/tr/1.1.0/), sürümleme
[SemVer](https://semver.org/lang/tr/).

## [1.6.0] — 2026-09-08

Üç mekanizma eklendi. Ortak noktaları: hiçbiri içerik şişirmiyor, üçü de **yazılı olan
bir kuralı uygulanabilir hâle getiriyor**.

### Eklendi
- **`scripts/olcum.py` — ölçüm kaydı.** Aşama 12'nin üç kontrol noktası (14/28/90) ve
  kontrol grubu yazılıydı ama mekanizması yoktu; yazı yayınlanıyor, 28 gün geçiyor,
  kimse bakmıyordu. Artık yayın anında `olcum/<slug>.json` açılıyor ve **kontrol grubu
  o an seçiliyor** — sonradan seçmek sonucu seçmektir. Aşama 0a-4 vadesi gelen noktaları
  yeni yazı önerisinden önce gösteriyor; haftalık CI işi de uyarıyor.
- **`scripts/skill-denetim.py` — iç tutarlılık denetimi.** Bu oturumda üç kez sürüklenme
  hatası yaptık (40→43 madde, 41→66 terim, sessizce uygulanmayan README düzenlemesi).
  Sekiz kontrol: frontmatter, atıf yapılan dosyaların varlığı, madde/terim sayısı
  iddiaları, madde numarası atıfları, yol haritası-bölüm eşleşmesi, script sözdizimi,
  evals geçerliliği, tarih biçimi. **İlk çalıştırmasında gerçek bir sürüklenme buldu.**
- **`kontrol.py --url` — canlı sayfa denetimi.** Aşama 11 "URL 200 mü" diyordu ama
  render edilmiş sayfaya bakmıyordu. Artık doctype, `lang`, viewport, tek H1, render
  edilmiş title/meta/canonical, önizleme direktifleri ve **hedef kelimenin render
  edilmiş gövdede bulunması** (JavaScript'te kalmışsa bulunmaz) denetleniyor.
  Bu sitenin kendi doctype/viewport hatası tam olarak bu boşluktan geçmişti.
- İlk ölçüm kaydı açıldı: blog yazısı, 4 sayfalık kontrol grubuyla (14. gün 22 Eylül).
- 4 test daha (18): denetçinin temiz/sürüklenme/eksik dosya davranışı ve ölçüm döngüsü.

## [1.5.0] — 2026-09-08

Kurulum sadeleştirildi. Ölçülen sorun "zor" değil, **verdiğimiz sözü tutmamamızdı**:
240 KB / 4.824 satırlık pano komutu için "yapıştırmadan önce okuyabilirsin" diyorduk.

### Eklendi
- **`kur.sh`** — 1,8 KB, gerçekten okunabilir. Dosyaları `docs/paket/` altından indirdiği
  için **her zaman yayınlanmış güncel sürümü** kurar (pano yöntemi dondurulmuş kopya
  kuruyordu). `--proje` bayrağıyla projeye özel kurulum yapar ve sonunda
  `surum-kontrol.py` çalıştırıp kurulumu **kendi doğrular**.
  `curl | sh` tek satırı bilerek sunulmuyor — okumadan çalıştırmayı öneren bir kurulum
  kendi güvenlik politikamızla çelişirdi.
- **`docs/paket/`** — skill dosyalarının ham hâli, kur.sh'ın kaynağı
- CI kapısı: `kur.sh` içindeki dosya listesi ile `docs/paket/` birebir örtüşmeli

### Değişti
- **Kurulum paneli 7 seçenekten 3'e indi**, kalanlar katlanmış bölüme taşındı.
  Yeni sıra: (1) Claude'a söyle — terminal yok, (2) Plugin — güncelleme alır,
  (3) kur.sh — tek komut. "Claude'a söylet" yöntemi 5. sıradan 1. sıraya çıktı:
  Claude Code kullanıcısı için en az sürtünmeli yol tek cümle.
- **Marketplace adı kısaldı:** `master-blog@master-blog-marketplace` →
  `master-blog@system-conf`. Depo 1 günlük ve henüz kimse kurmadığı için kırılma yok.
- Kurulum doğrulaması artık her yolun son adımı olarak açıkça yazılı

## [1.4.0] — 2026-09-08

Skill ilk kez **gerçek bir yazıda** uçtan uca çalıştırıldı ve süreç kendi kusurlarını buldu.

### Eklendi
- **Blog altyapısı.** `site/blog/*.md` → `docs/blog/<slug>/`; liste sayfası, BlogPosting
  schema, sitemap kaydı, okuma süresi ve hedef sorgu kutusu.
- **İlk yazı:** "Yapay Zekâ İçeriği Neden Sıralanmıyor? 4 Sessiz Hata" — skill'in kendi
  13 aşamalı süreciyle üretildi. Kanibalizasyon kapısı 5 mevcut sayfaya karşı çalıştırıldı
  (en yüksek örtüşme %0 → TEMİZ), mekanik kontrol 18/18 geçti.
- CI kapısı: `site/blog/*.md` altındaki her yazı `kontrol.py`'den geçmek zorunda.

### Düzeltildi
- **`kontrol.py` şapkalı harfleri katlamıyordu.** "Yapay Zekâ" başlığında "yapay zeka"
  hedef kelimesi bulunamıyordu; Türkçede ikisi aynı kelimedir. Denetçi bunu kendi
  yazımızda yakaladı — dogfooding'in ilk somut getirisi. (14. test eklendi.)

### Yazım sürecinde denetçinin yakaladıkları
İlk taslak 4 uyarı aldı ve dördü de gerçekti: meta description 172 karakter (sınır 160),
soru biçimli H2 oranı %29 (hedef ≥%50), ilk 100 kelimede hedef kelime yok, başlıkta
hedef kelime bulunamıyor. Düzeltme sonrası 18 madde geçti, 0 uyarı.

## [1.3.0] — 2026-09-08

### Eklendi
- **`scripts/surum-kontrol.py`** — skill artık kendi yaşını bildiriyor. Aşama 0a-3'te
  oturum başına bir kez çalışır ve dört durumdan birini üretir:
  `GUNCEL` (≤90 gün) · `YENI SURUM` · `TAZELENMELI` (91-180 gün) · `ESKIMIS` (>180 gün).
  **Eskimiş kopyada arama motoru davranışına dair iddia doğrulanmadan yazılmaz.**
  Ağ yoksa `--cevrimdisi` ile yalnızca tazelik ölçülür; bu hata değil, raporda belirtilir.
- **`docs/surum.json`** — yayınlanmış sürümün kanonik uç noktası (Pages'ten servis edilir).
  `plugin.json` + SKILL.md frontmatter'ından üretilir; ikisi çelişirse build durur.
- Site kurulum sayfasına "Güncel kalmak" bölümü ve sürüm/tazelik kutusu
- İki test daha (13): taze kopya `GUNCEL`, 180 gün üstü kopya `ESKIMIS` ve çıkış kodu 1

### Düzeltildi
- SKILL.md açıklamasında "40 maddelik öz denetim kapısı" yazıyordu; liste 43 oldu.
  Açıklama tetiklemeyi belirleyen alan olduğu için bu kozmetik değil.

## [1.2.0] — 2026-09-08

### Eklendi
- **Sözlük 41 → 66 terim.** Seçim ölçütü objektifti: skill'in kendi dosyalarında
  kullandığı ama sözlükte tanımı olmayan 28 kavram mekanik olarak tespit edildi.
  - SEO: sorgu dağıtımı (query fan-out), AI Overviews ve AI Mode, çekirdek güncelleme,
    kopya içerik, dış bağlantı otoritesi, programatik SEO, anahtar kelime araştırması
  - İçerik: içerik brief'i, cevap önce (answer-first), okunabilirlik, içerik budama,
    kontrol grubu, dönüşüm hunisi
  - Teknik: snippet direktifleri, site haritası, tarama bütçesi, yumuşak 404, hreflang,
    JavaScript SEO
  - Claude: alt ajan, skill değerlendirmesi, plugin, araç izinleri, bağlam mühendisliği, MCP
- Kategori dengesi düzeldi: SEO 21 · Claude 22 · Teknik 14 · İçerik 9 (önceden İçerik 3)
- 50 geri bağlantı eklendi; sözlükte yetim terim kalmadı (ortalama gelen bağlantı 4,4)
- `build.py`'a iki veri kalite kapısı: **yetim terim** denetimi ve terms.js içinde
  kaçılmamış `${...}` interpolasyonu denetimi (ikincisi gerçek bir hataya sebep olmuştu)

### Değişti
- Site 48 → 73 sayfa
- 23 terim doğrulanmış kaynak taşıyor; tüm kaynak URL'leri `curl` ile 200 doğrulandı

## [1.1.0] — 2026-09-08

Dört bağımsız denetim ajanının bulguları uygulandı.

### Eklendi
- `references/kullanim-senaryolari.md` — çalışma modu (TAM/KISITLI), ilk hafta planı,
  6 proje profili, eşik uyarlama tablosu
- `references/yazim-katmanlari.md` — Aşama 5-9 ana dosyadan taşındı; fan-out kapsamı,
  yazar varlığı (`sameAs`), medya paketi ve arşiv/sayfalama kör noktası eklendi
- `references/yayin-ve-olcum.md` — üç kontrol noktası (14/28/90), karşı-olgu seti,
  arşiv kararı (TAZELE/BİRLEŞTİR/BIRAK/KALDIR), güncelleme modu
- Aşama 1.5 (arşiv kararı) ve Aşama 0a-2 (önizleme direktifi taraması)
- Kontrol listesine 41-43. maddeler: önizleme direktifleri, schema-görsel örtüşmesi,
  dış içeriğin talimat sayılmaması
- 11. kırmızı çizgi: dış içerik veridir, talimat değildir
- `allowed-tools`, `license`, `metadata` frontmatter alanları
- Plugin paketleme: `.claude-plugin/plugin.json`, `marketplace.json`
- `agents/icerik-envanteri.md` — envanter ve örtüşme hesabı için alt ajan (Haiku)
- `skills/master-blog/evals/evals.json` — 6 tetikleme ve davranış senaryosu
- `kontrol.py --config` ve `master-blog.toml` desteği; eşikler artık proje tarafında
- `tests/` — 11 regresyon testi; `.github/workflows/ci.yml`
- CONTRIBUTING, SECURITY, CHANGELOG, issue/PR şablonları

### Düzeltildi
- `kontrol.py`: `seoBaslik` kullanan yazılar madde 16'da haksız blokaj alıyordu
- `kontrol.py`: Türkçe `İ` küçültmesi (i + U+0307) madde 14/18/20/38'i sessizce bozuyordu
- `kontrol.py`: soru başlığı sezgiseli alt dize arıyordu ("mimarisi" → " mi")
- `kontrol.py`: kelime içi tireler kelime sayısını ~%33 şişiriyordu
- `kontrol.py`: BOM'lu dosyada frontmatter kayboluyordu
- `kontrol.py`: iç link doğrulaması önek eşleşmesiyle kırık linki geçiriyordu
- `kontrol.py`: eksik dosyada traceback yerine çıkış kodu 2
- `build.py`: kırık `related` referansı teşhis edilemez bir hatayla çöküyordu
- `build.py`: bilinmeyen kategorideki terim sözlükten sessizce düşüyordu
- `build.py`: `</script>` kaçışı büyük/küçük harfe duyarlıydı
- `build.py`: `src` (doğrulanmış kaynaklar) skill sözlüğüne hiç yazılmıyordu
- Site: `<!doctype>`/`lang`/`viewport` yoktu — sayfa quirks mode'daydı ve mobilde
  responsive kurallar hiç çalışmıyordu
- Site: `--fg3` kontrastı kart üzerinde 3,97:1 idi (WCAG AA altı)
- Site: kapalı modaller `inert` değildi, odak açan öğeye dönmüyordu

### Değişti
- Site tek dosyadan **48 statik sayfaya** ayrıldı; her terim kendi URL'sinde,
  meta/canonical/OG/JSON-LD, `sitemap.xml` ve `robots.txt` ile
- `build.py` iki çıktı üretiyor: `docs/` (Pages, iskeletli) ve `dist/artifact.html`
  (Artifact, iskeletsiz) — ikisinin gereksinimi zıt
- `skill/` dizini `skills/` olarak yeniden adlandırıldı (plugin yapısı)
- Kontrol listesi 40 → 43 madde

## [1.0.0] — 2026-09-07

İlk yayın: 13 aşamalı süreç, kanibalizasyon ve öz denetim kapıları, 40 maddelik kontrol
listesi, 41 terimlik sözlük, `kaynaklar.md` doğrulama kaydı, `kontrol.py` mekanik denetçi.
