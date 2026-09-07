# Yazım Katmanları (Aşama 5-9)

Bu dosya, gövde yazılmadan önce **okunur**. Beş katman sırayla uygulanır; hiçbiri
"zaten biliyorum" diye atlanmaz. Ana dosyadaki brief (Aşama 4) onaylandıktan sonra açılır.

## İçindekiler

- [Aşama 5 — SEO katmanı](#asama-5) · başlık, kapsam, semantik alan, okunabilirlik
- [Aşama 6 — GEO katmanı](#asama-6) · alıntılanabilirlik, fan-out kapsamı
- [Aşama 7 — E-E-A-T katmanı](#asama-7) · deneyim, uzmanlık, yazar varlığı
- [Aşama 8 — Bağlantı mimarisi](#asama-8) · iç/dış link, arşiv kör noktası
- [Aşama 9 — Teknik paket](#asama-9) · frontmatter, medya, schema

---

## Aşama 5 — SEO katmanı {#asama-5}

- **Title (`<title>` / seoBaslik):** 60 karakteri geçme (piksel sınırı ~580px). Hedef
  kelime **başta**. Marka adı sona, ayraçla. Tıklama vaadi taşısın.
- **Meta description:** 140-160 karakter. Sıralama faktörü değildir; **tıklama oranı**
  faktörüdür. Sorunun cevabını ima et, spoiler verme.
- **H1:** sayfada tek. Title ile aynı olmak zorunda değil; H1 insana, title SERP'e yazılır.
- **H2/H3 hiyerarşisi:** atlama yok (H2'den H4'e sıçrama yok). H2'ler tarama dostu.
- **İlk 100 kelime:** ana kelime doğal biçimde geçsin ve **soruya cevap başlasın**.
  "Giriş cümlesi" tuzağına düşme ("Günümüzde teknoloji hızla gelişmektedir" = sıfır değer).
- **Kapsam:** kelime sayısı hedef değil, **sorunun kapanması** hedeftir. Yine de pratik
  bant: bilgi rehberi 900-1.800, karşılaştırma 1.200-2.200, tanım yazısı 600-900.
  600'ün altına düşüyorsa konu incedir — kapsamı genişlet ya da başka konuyla birleştir.
- **Semantik alan:** ana kelimenin eş anlamlıları, varyantları ve komşu kavramları metne
  yayılır. Modern arama motoru kelime değil **varlık (entity)** eşleştirir.
- **Kelime istifleme yasak:** aynı kelimeyi paragraf başına 1'den fazla zorlama. Yoğunluk
  hedefi diye bir metrik yok; doğal dil hedef.
- **Okunabilirlik:** paragraf ≤ 4 satır, cümle ortalaması ≤ 20 kelime, edilgen yapı azaltılır,
  her 250-300 kelimede bir görsel/tablo/liste ile ritim kırılır.
- **Slug:** kebab-case, hedef kelimeyi içerir, tarih ve stop-word içermez, kısa ve
  **kalıcıdır**. Yayın sonrası slug değişirse 301 zorunludur.

---

## Aşama 6 — GEO / AEO katmanı {#asama-6}

Amaç: içeriğin **parça olarak alıntılanabilir** olması. AI motorları sayfayı değil, sayfadaki
kendi kendine yeten bloğu alıntılar.

- **Answer-first:** her bölümün İLK cümlesi başlıktaki sorunun doğrudan cevabıdır; gerekçe
  sonra gelir. (Ters piramit.)
- **Bağımsız tanım cümlesi:** en az bir kavram tek cümlede, bağlamdan koparılabilir biçimde
  tanımlanır: "Güvenlik alanı, ekipmanın etrafında boş bırakılması gereken ... alandır."
- **Soru biçimli H2'ler:** kullanıcının yazdığı sorgunun aynısı ya da çok yakını.
- **En az bir tablo:** karşılaştırma/karar tablosu ideal. Tablolar AI motorlarının en çok
  alıntıladığı yapıdır.
- **Somut sayı ve adlandırılmış örnek:** "uzun ömürlüdür" değil, "3 mm et kalınlığı".
  Rakamsız cümle alıntılanmaz.
- **Terim tutarlılığı:** aynı kavrama iki farklı ad verme; varyantı bir kez parantezde ver.
- **Özet bölümü:** sonda "## Özet" — 5-7 madde, her madde **tek başına anlamlı**.
- **Tarih ve kimlik görünür:** yayın/güncelleme tarihi ve yazar sayfada görünür olmalı;
  AI motorları tazelik ve kaynak kimliği arar.
- **Kısa cümle:** 15-25 kelimelik bağımsız cümleler alıntılanmaya en uygun birimdir.

### Fan-out kapsamı — alıntılanma biriminin gerçek ölçüsü

Google'ın yapay zekâ özellikleri (AI Overviews, AI Mode) tek sorgu çalıştırmaz; konuyu alt
konulara ve veri kaynaklarına dağıtıp **birden çok ilgili arama** yapar. Buna *query fan-out*
denir. Sonuç: alıntılanma olasılığını belirleyen şey "hedef sorgunun cevabı" değil,
**alt soruların kapsanma oranıdır**.

Uygulama:
1. Aşama 4 briefindeki `Fan-out alt sorular` listesini (8-12 satır) aç.
2. Her alt soruyu **bir H2'ye ya da bağımsız bir bloğa eşle**. Eşlenmemiş alt soru kalırsa
   ya bir bölüm eklenir ya da o alt soru bilinçli olarak kapsam dışı bırakılıp brief'e not düşülür.
3. Alt sorunun cevabı, kendi bloğunda **kendi kendine yeter** biçimde verilir; "yukarıda
   anlattığımız gibi" ifadesi alıntılanabilirliği yok eder.

> Google'ın kendi dokümanı bu özellikler için "ek bir gereklilik ya da özel optimizasyon
> yok" diyor. Bu yüzden fan-out kapsamı bir **taktik değil, kapsam kararıdır**: konuyu
> gerçekten kapatıp kapatmadığının ölçüsü. Kaynak: `kaynaklar.md` → AI özellikleri.

### Önizlemeyi engelleyen direktifler (Aşama 0'da bakılır, burada doğrulanır)

`nosnippet`, `data-nosnippet`, `max-snippet:0` ve `noindex` yalnızca klasik snippet'i değil,
**yapay zekâ özelliklerinde görünürlüğü de** kapatır. Bu direktifler yürürlükteyken Aşama 12'de
"AI Overviews'ta görünmüyoruz" gözlemi içerik zayıflığına değil teknik engele işaret eder —
ve yanlış teşhis üretir. Yazıya başlamadan önce Aşama 0'daki tarama sonucuna bak; engel
varsa kullanıcıya bildir ve bunun bilinçli bir karar olup olmadığını sor.

---

## Aşama 7 — E-E-A-T katmanı {#asama-7}

E-E-A-T doğrudan ölçülen bir sıralama faktörü değil, kalite çerçevesidir. Bu yüzden
"E-E-A-T ekle" diye bir iş yoktur; **eksik olan somut şeyi ekle**:

- **Deneyim (Experience):** birinci elden gözlem kalıpları — "sahada en sık gördüğümüz
  hata...", "keşifte ilk ölçtüğümüz mesafe budur". **Yalnızca proje verisinde karşılığı
  olan gözlemler.** Deneyim uydurulmaz.
- **Uzmanlık (Expertise):** iddia ölçülebilir olur. "Sağlamdır" değil, "profil kesiti ve
  et kalınlığı sorulur, TS EN ... kapsamında değerlendirilir".
- **Otorite (Authoritativeness):** yazar ismi + uzmanlığa bağlanan kısa bio. "X ekibi" en
  zayıf imzadır. Mevzuat/YMYL konusunda resmî kaynak linki zorunlu.
- **Güven (Trust):** iletişim bilgisi, güncelleme tarihi, düzeltme şeffaflığı, tutarlılık.
  **Aynı konuda iki yazı birbiriyle çelişemez** — yazmadan önce eski yazının ne dediğini oku.

### Yazar varlığı (author entity)

İsim tek başına sinyal değildir; yazarın **ayırt edilebilir bir varlık** olarak bağlanması gerekir.

- Yazar sayfası yoksa **üretilecek ilk şey odur**: ad, unvan (`jobTitle`), konuyla bağlantılı
  somut kanıt (deneyim, sertifika, yayın), iletişim.
- Schema'da `author` mümkünse `Person` olur ve **`url` veya `sameAs`** ile gerçek profillere
  bağlanır (kurum sayfası, meslek odası kaydı, akademik profil, yayın listesi).
- `author.name` yalnızca adı içerir — unvan, kurum adı ya da anahtar kelime eklenmez.
- Birden çok yazar varsa **her biri ayrı `author` alanına** yazılır, tek alanda birleştirilmez.
- Bağlanan her profil URL'i yayından önce doğrulanır (`curl -sI` → 200). Kırık profil linki,
  hiç link olmamasından kötüdür.

YMYL içerikte (sağlık, finans, hukuk, güvenlik) isimli uzman ve doğrulanabilir profil
**zorunludur**; anonim içerik bu alanda ciddi dezavantajdır.

---

## Aşama 8 — Bağlantı mimarisi {#asama-8}

**İç bağlantı (internal linking) — 4-6 adet, zorunlu:**

- Hedefler: ilgili blog yazıları + ilgili kategori/hizmet sayfası + huninin bir alt basamağı
  (fiyat/teklif/kayıt).
- **Anchor metni tanımlayıcı ve çeşitli** olmalı. Aynı sayfaya iki link veriliyorsa farklı
  anchor kullan. "Buraya tıklayın" yasak.
- **Ters yön:** yayından sonra mevcut 1-2 eski yazıdan yeni yazıya link ekle (kullanıcı
  onayıyla). Yeni yazının yetim (orphan) kalmaması buna bağlıdır.
- Hub-spoke dokusu: spoke hub'ına, hub spoke'a link verir.

**Dış bağlantı — 0-2 adet:**

- Yalnızca güven katan otoriter kaynak (standart kuruluşu, resmî kurum, birincil araştırma).
- **Her URL yayına girmeden doğrulanır:** `curl -sI <url> | head -1` → 200 dönmeli.
  Kırık ya da tahminî URL yasak. Rakip siteye link verilmez.
- Otoriter kaynak yoksa dış link zorlanmaz; yokluğu kusur değildir.

**Arşiv ve sayfalama kör noktası:**

Yeni yazı bugün blog listesinin ilk sayfasındadır; birkaç ay sonra 2. ya da 3. sayfaya düşer.
Liste **`#` fragment'ıyla** ya da **sonsuz kaydırmayla** sayfalanıyorsa o noktadan sonra
yazıya giden **taranabilir hiçbir link kalmaz** — Aşama 8'de eklenen 1-2 iç link tek yaşam
desteği olur. Google sayfalama fragment'larını yok sayar.

Bu yüzden:
- Aşama 0'da liste/arşiv sayfalama biçimi tespit edilir (`?page=n` mi, `#` mi, sonsuz kaydırma mı;
  her sayfa kendi canonical'ına mı işaret ediyor).
- Fragment ya da sonsuz kaydırma varsa **iç link kotası 4-6 değil 6-8'dir** ve bunların en az
  ikisi kalıcı bir hub/kategori sayfasından gelir.
- Kontrol: yazıya, arşivden bağımsız olarak en az iki kalıcı sayfadan `<a href>` ile erişilebiliyor mu?

---

## Aşama 9 — Teknik paket {#asama-9}

- **Frontmatter:** projenin şemasına birebir. Alan uydurma, alan atlama.
- **Medya paketi.** Görsel isteğe bağlı değildir eğer schema'da `image` alanı doldurulacaksa —
  bu iki karar birbirine bağlıdır ve çelişmemelidir:
  - En az bir **gerçek `<img>`** (CSS arka plan görseli indekslenmez), anlamlı kebab-case
    dosya adı, metne komşu konum, `srcset`/`<picture>`, modern format (WebP/AVIF).
  - `alt` metni görseli tarif eder, kelime istiflemez; dekoratifse `alt=""` bırakılır.
  - Schema'daki `image` **sayfada gerçekten görünen görselin URL'i** olmalıdır.
  - Proje görsel sitemap kullanıyorsa yeni görsel oraya eklenir.
  - **Video varsa:** kendi izleme sayfası + `VideoObject` (`name`, `description`,
    `thumbnailUrl` her video için benzersiz) ve thumbnail görsel tarayıcılara açık olmalı.
    Video yoksa zorlanmaz.
  - Hiç görsel kullanılmayacaksa schema'da `image` alanı da doldurulmaz. Görselsiz yayın
    kabul edilebilir; **sayfada olmayan görseli iddia etmek** kabul edilemez.
- **Yapılandırılmış veri (schema):** projede zaten bir schema katmanı varsa aynı desenle
  devam et. Yoksa `BlogPosting` + `BreadcrumbList` + `Organization` öner — 2026'da içerik
  yayıncısı için zengin sonuç üreten omurga budur.
  **`FAQPage` ve `HowTo` zengin sonuç için ÖNERİLMEZ.** İşaretleme schema.org açısından
  geçerli olmaya devam eder ama kullanıcıya "zengin sonuç kazanırsın" diye sunulmaz.
  Güncel durum ve tarihler: `kaynaklar.md` → yapılandırılmış veri.
  **Kural:** schema, sayfada görünmeyen bilgiyi iddia edemez. Ayrıntı ve kanıt için
  `references/schema-ve-geo.md` ve `references/kaynaklar.md`.
- **Tazelik:** mevcut bir yazıya dokunulduysa `guncelleme: YYYY-MM-DD` eklenir.
  **Tarih sahteciliği yasak** — içerik değişmeden tarih tazelemek güven kaybıdır.
- **Çok dillilik:** proje çok dilliyse `hreflang` sözleşmesine uy; tek dilli blogda
  çeviri üretme.

---
