# master-blog

[![CI](https://github.com/system-conf/master-blog-skill/actions/workflows/ci.yml/badge.svg)](https://github.com/system-conf/master-blog-skill/actions/workflows/ci.yml)

**Türkçe** · [English](README.en.md)

Claude için uçtan uca SEO/GEO içerik üretim skill'i + onu anlatan dokümantasyon sitesi.

## Klasör yapısı

```
skills/master-blog/          ← kurulacak skill (bu klasörü kopyala)
  SKILL.md                    13 aşamalı süreç, 2 atlanamaz kapı
  references/
    yayin-oncesi-kontrol.md   53 maddelik denetim listesi
    terimler-sozlugu.md       ÜRETİLİR — elle düzenleme
    schema-ve-geo.md          yapılandırılmış veri + AI motoru notları
    kaynaklar.md              zamana bağlı iddiaların kaynak kaydı (3 ayda bir tazele)
    kullanim-senaryolari.md   6 proje profili, çalışma modu, eşik uyarlama tablosu
    medya-brief.md            görsel kararı: diyagram / prompt / gerek yok + sahte görsel yasağı
    uslup.md                  Aşama 5.5: açılış, cümle ritmi, klişe, karşı-tez, ticari köprü
    yazim-katmanlari.md       Aşama 5-9: SEO, GEO, E-E-A-T, bağlantı, teknik
    yayin-ve-olcum.md         Aşama 11-12 + arşiv kararı + güncelleme modu
  scripts/kontrol.py          mekanik yayın öncesi kontrol (Aşama 10a)
  scripts/surum-kontrol.py    sürüm ve bilgi tazeliği kontrolü (Aşama 0a-3)
  scripts/olcum.py            ölçüm kaydı: 14/28/90 gün + kontrol grubu (Aşama 0a-4, 11)
  scripts/skill-denetim.py    skill'in kendi iç tutarlılığı (sayı sürüklenmesi, ölü atıf)
  evals/evals.json            tetikleme ve davranış senaryoları

site/
  template.html             site kabuğu (CSS + JS)
  assets/                   favicon.svg · favicon.ico · apple-touch-icon.png
                            (tools/favicon-uret.py ile üretilir, bağımlılık yok)
  data/terms.js             terim sözlüğünün TEK doğruluk kaynağı

tests/
  calistir.py               regresyon testleri (ek bağımlılık yok)
  fixtures/                 her testin dayandığı gerçek hata örneği

build.py                    terms.js + skill dosyaları → docs/ + dist/
docs/                       GitHub Pages: 47 statik sayfa, her terim kendi URL'sinde
  assets/{app.js,style.css} ortak paket (sayfalar arası önbelleklenir)
  sitemap.xml, robots.txt
dist/artifact.html          tek dosyalık sürüm (Claude Artifact için, iskeletsiz)
```

## Kurulum

**Plugin olarak (önerilen — sürüm alır, güncellenir):**

```
/plugin marketplace add system-conf/master-blog-skill
/plugin install master-blog@system-conf
```

**Tek komutla (her zaman güncel sürüm):**

```bash
curl -fsSL https://system-conf.github.io/master-blog-skill/kur.sh -o kur.sh
less kur.sh     # 1,8 KB — okumadan çalıştırma
sh kur.sh       # projeye özel: sh kur.sh --proje
```

**Terminal istemiyorsan** Claude Code'a tek cümle yeter:
*github.com/system-conf/master-blog-skill deposundan skills/master-blog klasörünü ~/.claude/skills/ altına kur*

**Dosya olarak:**

```bash
cp -r skills/master-blog ~/.claude/skills/          # kişisel
# veya
cp -r skills/master-blog <proje>/.claude/skills/    # projeye özel, ekiple paylaşılır
```

Dosya kurulumunda güncelleme almazsın; `kaynaklar.md` 3 ayda bir tazelendiği için
plugin kurulumu bu proje özelinde belirgin avantajlıdır.

### Eşikleri projene göre ayarla

Skill dizinindeki `kontrol.py`'yi **düzenleme** — güncellemede silinir. Projenin köküne
`master-blog.toml` koy:

```toml
[esikler]
IC_LINK_MIN = 2      # yeni sitede 4 link verecek kadar sayfa yok
KELIME_MIN  = 400
PARA_MAX_KELIME = 70
```

Profil bazlı önerilen değerler: `references/kullanim-senaryolari.md` → eşik uyarlama tablosu.

Sonra yeni bir Claude Code oturumu aç ve: `master-blog skill'iyle yeni yazı hazırla`

## Siteyi yeniden üret

```bash
python3 build.py       # docs/ (47 sayfa) + dist/artifact.html üretir
python3 tests/calistir.py
```

`build.py` iki farklı çıktı üretir çünkü iki ortamın gereksinimi zıt:

| Çıktı | Yönlendirme | Belge iskeleti | Neden |
|---|---|---|---|
| `docs/` | gerçek URL (`pushState`) | `<!doctype>` + `lang` + `viewport` **var** | Arama motoru her terimi ayrı belge olarak indeksleyebilsin |
| `dist/artifact.html` | hash (`#/terim/x`) | **yok** | Artifact runtime iskeleti kendisi ekler; `<html>` yazmak yasak |

**Veri doğrulama build'in parçasıdır.** Kırık `related` referansı, tekrar eden slug,
eksik zorunlu alan, geçersiz seviye veya bozuk `src` girdisi build'i **hata koduyla
durdurur** — sessizce geçmez.

Terim eklemek/düzenlemek için yalnızca `site/data/terms.js` düzenlenir; `build.py`
hem siteyi hem skill'in terim sözlüğü referansını yeniden üretir.
`docs/`, `dist/` ve `terimler-sozlugu.md` üretilen dosyalardır — elle düzenlenmez,
ama commit'lenir (CI ikisinin uyuştuğunu `git diff --exit-code` ile denetler).

`terms.js` alanları:

| Alan | Zorunlu | Not |
|---|---|---|
| `slug` | evet | kebab-case, benzersiz |
| `name`, `en` | evet | Türkçe ad ve İngilizce karşılığı |
| `cat` | evet | serbest; yeni kategori otomatik eklenir |
| `level` | evet | `Başlangıç` \| `Orta` \| `İleri` \| `Uzman` |
| `short`, `simple`, `technical`, `why`, `example`, `myth` | evet | markdown (tablo, liste, kod, link) |
| `related[]` | evet | var olan slug'lar; kendine referans yasak |
| `usedIn` | evet | skill'de hangi aşamada geçtiği |
| `src[]` | hayır | `{t, u}` — doğrulanmış kaynak; `https://` zorunlu |

Hepsi `python3 build.py` ile denetlenir; hatalı veri build'i durdurur.

## Test ve CI

```bash
python3 tests/calistir.py
```

`tests/fixtures/` altındaki her dosya, geçmişte gerçekten görülmüş bir hatayı temsil eder:
Türkçe `İ` katlaması, `seoBaslik` alanının H1 kaynağı sayılmaması, sahte soru başlıkları,
kelime içi tirelerin sayımı şişirmesi, BOM'lu dosya, iç link önek eşleşmesi.

`.github/workflows/ci.yml` her push'ta testleri ve build determinizmini denetler;
3 ayda bir de `kaynaklar.md` içindeki dış bağlantıların hâlâ 200 döndüğünü kontrol eder.

## Çalışma modu — repo yoksa ne olur?

Skill dosya okur ve komut çalıştırır. Erişim yoksa bazı aşamalar çalışamaz ve skill
bunu **gizlemez**:

| Mod | Koşul | Sonuç |
|---|---|---|
| **TAM** | İçerik dosyaları çalışma dizininde (Astro, Next, Hugo, düz Markdown) | Bütün aşamalar |
| **KISITLI** | İçerik panelde (WordPress, Wix, Shopify) | Kanibalizasyon kapısı, mekanik kontrol ve canlı doğrulama çalışmaz |

Kısıtlı modda skill kapıları "geçti" saymaz; rapora `DENETLENEMEDİ (kısıtlı mod)` yazar.
Sahte onay vermek, hiç kontrol etmemekten daha zararlıdır.

## Proje profilleri

`references/kullanim-senaryolari.md` altı profil tanımlar ve her biri için sürecin nerede
saptığını yazar: **yerel hizmet** (tesisatçı, klima servisi), **üretici/B2B**,
**e-ticaret**, **SaaS**, **klinik/sağlık (YMYL)**, **ajans/çok müşterili kurulum**.
Aynı dosyada eşik uyarlama tablosu var — yeni bir sitede `IC_LINK_MIN = 4` sürekli blokaj
üretir, 2'ye indirilmesi gerekir.

## Mekanik kontrol

53 maddelik listenin ölçülebilir kısmını gerçekten sayar — modelin "muhtemelen tamam"
demesini engeller:

```bash
python3 skills/master-blog/scripts/kontrol.py <yazi.md> --kelime "hedef kelime" --net
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

Site tek dosyadır ve **GitHub Pages** üzerinden yayınlanır:
<https://system-conf.github.io/master-blog-skill/>

Pages kaynağı: `main` dalı, `/docs` klasörü. Yayın akışı:

```bash
python3 build.py     # docs/index.html üretir
git add -A && git commit -m "site güncellendi" && git push
```

Push'tan ~1 dakika sonra canlıya çıkar. Ayrı bir CI adımı yoktur.

Alternatif olarak `wrangler.jsonc` ile Cloudflare Workers'a da dağıtılabilir
(`npx wrangler deploy`); şu an kullanılmıyor.

## Güncel kalmak

Skill her oturumun başında kendi yaşını kontrol eder:

```bash
python3 skills/master-blog/scripts/surum-kontrol.py
```

| Durum | Anlamı | Davranış |
|---|---|---|
| `GUNCEL` | ≤ 90 gün | Sessizce devam eder |
| `YENI SURUM` | Yayınlanmış daha yeni sürüm var | Tek satır bildirir |
| `TAZELENMELI` | 91-180 gün | Zamana bağlı iddia yazılmadan önce kaynak kaydı tazelenir |
| `ESKIMIS` | > 180 gün | Uyarır ve izin ister; doğrulanmamış iddia yazmaz |

Yayınlanmış sürüm <https://system-conf.github.io/master-blog-skill/surum.json> adresinden
okunur. Plugin kurulumunda güncelleme `/plugin update master-blog`; dosya kurulumunda
skill "yeni sürüm var" der ama kopyalamayı sen yaparsın.

## Dış katkılar

Skill'e dışarıdan gelen ve uygulanan katkılar `references/kaynaklar.md` → *Dış katkılar*
bölümünde, kaynak sınıfıyla birlikte kayıtlıdır. Üslup katmanı (Aşama 5.5) bu yolla geldi.

Kural iki yönlü: dış geri bildirimin **önerileri** değerlendirilir, **dosya gözlemleri**
her zaman kaynaktan doğrulanır. Bir öneri sıralama iddiasına dayanıyorsa, iddia
`kaynaklar.md` disipliniyle ayrıca doğrulanır — doğrulanamıyorsa öneri alınır, gerekçesi
alınmaz.

## Bilgi tazeliği

`skills/master-blog/references/kaynaklar.md` zamana bağlı iddiaların kaynak kaydıdır
(son doğrulama: 7 Eylül 2026). SEO/GEO tarafı hızlı değiştiği için 3 ayda bir gözden
geçir; güncellediğinde `build.py` çalıştır — site de tazelenir.

## Bilerek yapılmayanlar

Denetimlerde önerilen ama **gerekçeyle uygulanmayan** üç şey:

- **`terms.js` → JSON'a taşınmadı.** `eval` bir enjeksiyon havuzudur, doğru; ama burada
  okunan dosya deponun kendi kaynak dosyası, kullanıcı girdisi değil. JSON'a taşımak
  çok satırlı Türkçe metinleri `\n` kaçışlarına gömer ve elle düzenlemeyi pratikte
  bitirir. Asıl risk olan **doğrulama eksikliği** `build.py` içinde çözüldü: zorunlu
  alanlar, slug biçimi, seviye enum'ı, kırık `related` ve bozuk `src` build'i durduruyor.
- **`og:image` hâlâ yok — ama kaynağı hazır.** `site/assets/og.svg` üretildi ve yayında.
  Eksik olan güvenilir bir SVG→PNG dönüştürücü: macOS'un `qlmanage` aracı SVG'yi dikey
  olarak geriyor (1200×630 viewBox → 1200×985 çıktı), bu yüzden kullanılmadı. Sosyal
  kartlar çoğu platformda SVG'yi desteklemediği için alan boş bırakıldı; bozuk oranlı
  bir kart koymaktansa koymamak doğru. Doğru rasterleştirme yapıldığında tek satırda bağlanır.
- **İngilizce sürüm yok.** Altyapı maliyeti orta, içerik maliyeti kalıcı: 66 terim × 6 uzun
  alan + 19 KB `SKILL.md`, ve her güncelleme iki dilde bakım demek. Talep gelirse
  `kullanim-senaryolari.md` içindeki dil profili yaklaşımıyla kademeli yapılabilir.

## Notlar

- Site tek dosyadır; herhangi bir statik sunucuya `docs/index.html` olarak konabilir.
- Sitedeki "İndir" düğmesi gömülü çerçevede (iframe) çalışmaz — o durumda kopyalama
  paneli açılır. Kendi sunucunda barındırıldığında normal indirme çalışır.
- Lisans: MIT.
- Katkı: [CONTRIBUTING.md](CONTRIBUTING.md) · Güvenlik: [SECURITY.md](SECURITY.md) ·
  Değişiklikler: [CHANGELOG.md](CHANGELOG.md)
