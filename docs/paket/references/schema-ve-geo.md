# Yapılandırılmış Veri ve AI Motoru Optimizasyonu

> **Son doğrulama: 7 Eylül 2026.** Bu dosyadaki zamana bağlı iddiaların kaynakları
> `kaynaklar.md` dosyasındadır. Yapılandırılmış veri ve AI arama tarafı hızlı değişiyor;
> 3 aydan eski bir doğrulamayla çalışıyorsan önce kaynakları tazele.

## 1. Temel kural

Yapılandırılmış veri (schema markup), sayfadaki bilgiyi **arama motoruna makine okunur**
biçimde tekrar anlatır. İki değişmez kural:

1. **Schema, sayfada görünmeyen bilgiyi iddia edemez.** Görünmeyen içeriği işaretlemek
   spam politikası ihlalidir ve zengin sonuç yetkisini kaybettirir.
2. **Schema sıralama faktörü değildir.** Zengin sonuç (rich result) uygunluğu sağlar;
   tıklama oranını etkiler, sıralamayı doğrudan değil.

## 2. Blog yazısı için minimum paket

`BlogPosting` (ya da `Article`), `BreadcrumbList` ve `Organization` üçlüsü, içerik
yayıncıları için 2026'da hâlâ zengin sonuç üreten omurgadır.

```json
{
  "@context": "https://schema.org",
  "@type": "BlogPosting",
  "headline": "110 karakteri aşmayan başlık",
  "description": "Meta description ile aynı",
  "datePublished": "2026-09-07",
  "dateModified": "2026-09-07",
  "author": { "@type": "Person", "name": "Gerçek yazar adı", "url": "https://.../yazar" },
  "publisher": { "@type": "Organization", "name": "Marka", "logo": { "@type": "ImageObject", "url": "https://.../logo.png" } },
  "image": ["https://.../16x9.jpg", "https://.../4x3.jpg", "https://.../1x1.jpg"],
  "mainEntityOfPage": { "@type": "WebPage", "@id": "https://.../yazi-slug" },
  "inLanguage": "tr-TR"
}
```

**Notlar**
- `author` mümkünse `Person` olsun ve `url` ile bir yazar sayfasına bağlansın;
  `Organization` yazar kimliği sinyalini zayıflatır.
- `image` için üç en-boy oranı (16:9, 4:3, 1:1) önerilir.
- `dateModified` yalnızca içerik gerçekten değiştiyse güncellenir.
- `headline` 110 karakteri aşarsa Google alanı yok sayar.

## 3. Duruma göre eklenecek tipler — ve artık eklenmeyecekler

| Tip | 2026 durumu | Karar |
|---|---|---|
| `BlogPosting` / `Article` | Zengin sonuç üretiyor | **Kullan** |
| `BreadcrumbList` | Zengin sonuç üretiyor | **Kullan** |
| `Organization` | Zengin sonuç / bilgi paneli sinyali | **Kullan** |
| `FAQPage` | **7 Mayıs 2026'da zengin sonuç kaldırıldı**; yalnızca resmî kurum ve sağlık siteleri için sürüyor | Zengin sonuç için ekleme; SSS bölümü sayfada kalsın |
| `HowTo` | Masaüstünde Eylül 2023'te kaldırıldı; Google SERP kazancı yok | Zengin sonuç için ekleme |
| `ItemList` | Sınırlı; çoğu yayıncıda görünür kazanç yok | İsteğe bağlı |

**FAQ takvimi (kanıt için):** zengin sonuçlar 7 Mayıs 2026'da SERP'ten kalktı;
Search Console raporu ve Zengin Sonuç Testi desteği Haziran 2026'da, Search Console API
desteği Ağustos 2026'da sona erdi.

**Ne yapmalı?** `FAQPage` işaretlemesi schema.org açısından geçerli olmaya devam ediyor ve
sayfadan kaldırılması zorunlu değil — ancak **Google'da görünür bir kazanç beklentisi
kurulamaz.** Yazıdaki SSS bölümünü kullanıcı ve alıntılanabilirlik için tut; işaretlemeyi
"zengin sonuç taktiği" diye sunma.

## 4. Doğrulama

- Zengin Sonuç Testi ve Schema.org doğrulayıcısı ile kontrol et.
- Search Console → "Zengin sonuçlar" raporunda hata/uyarı takip edilir.
- **Kural:** doğrulanmamış schema yayına çıkmaz.
- **Tuzak:** Bir tipin doğrulayıcıdan geçmesi, Google'ın onu görsel bir zengin sonuca
  çevireceği anlamına gelmez. Geçerlilik ile görünürlük ayrı şeylerdir.

---

## 5. GEO (Generative Engine Optimization)

GEO, içeriğin **üretken yapay zekâ motorları** (Google AI Overviews ve AI Mode, ChatGPT,
Perplexity, Claude, Copilot) tarafından bulunup **alıntılanma** olasılığını artırma
pratiğidir. Klasik SEO'nun yerine geçmez; üzerine biner.

### Neden farklı?

Klasik SEO'da hedef **sayfanın sıralanması**, GEO'da hedef **bir bloğun alıntılanmasıdır**.
Model sayfayı bütün olarak sunmaz; kendi kendine yeten bir parçayı alır ve kaynak gösterir.
Bu yüzden GEO'nun birimi sayfa değil **paragraf/tablo/tanım cümlesidir**.

### Alıntılanabilirliği artıran yapılar

1. **Kendi kendine yeten blok:** bağlamdan koparıldığında da anlamlı 2-4 cümlelik parça.
2. **Tanım cümlesi:** "X, ...dır." kalıbı.
3. **Tablo:** karşılaştırma verisi tabloda olduğunda alıntılanma olasılığı artar.
4. **Sayı ve isim:** "3 mm", "TS EN 1176", "28 gün" — belirsiz sıfatlar alıntılanmaz.
5. **Soru = başlık:** kullanıcının sorduğu cümlenin aynısı başlıkta geçsin.
6. **Tarih ve yazar görünürlüğü:** kaynak güvenilirliği sinyali.
7. **Tutarlı terminoloji:** aynı kavramın tek adı olsun.

**Öne çıkan snippet bağlantısı:** Öne çıkan snippet'e uygun yazmak GEO'ya da hizmet eder —
daha önce snippet kazanan sayfaların AI Overviews'ta yaklaşık **iki kat** daha sık
alıntılandığı ölçülmüştür. Ancak snippet'in kendisi seyrekleşti: SERP görünürlüğü
Ocak 2025'te %15,41 iken Haziran 2025'te %5,53'e indi (~%64 düşüş).

### Teknik taraf

- **Sunucu tarafı render:** içerik yalnızca JavaScript ile geliyorsa birçok AI tarayıcısı
  göremez. Kritik metin HTML'de olmalı.
- **robots.txt — eğitim ve getirme botlarını AYIR.** Bu, tek satırlık bir karar değildir:

  | Amaç | Tipik tokenlar |
  |---|---|
  | Eğitim (model eğitimi için toplama) | `GPTBot`, `ClaudeBot`, `Google-Extended`, `CCBot`, `Applebot-Extended`, `Meta-ExternalAgent`, `Bytespider` |
  | Getirme / arama (cevap anında alıntı) | `OAI-SearchBot`, `ChatGPT-User`, `Claude-SearchBot`, `Claude-User`, `PerplexityBot`, `Perplexity-User` |

  Yaygın strateji: eğitim botlarını kapatıp getirme botlarını açık bırakmak — böylece
  içerik model eğitimine gitmez ama AI aramalarında alıntılanabilir kalır.
  **Tuzak:** `ClaudeBot`'u engellemek `Claude-SearchBot` ve `Claude-User`'ı engellemez;
  her token ayrı satır ister. Ayrıca bazı botların (ör. Bytespider ve Perplexity'nin bazı
  istekleri) robots.txt'i yok saydığı belgelenmiştir — gerçek engelleme sunucu/WAF katmanında olur.
- **`llms.txt`:** öneri niteliğinde bir dosya; standart değil ve büyük sağlayıcılar
  desteklemiyor. Ayrıntı ve kanıt için `terimler-sozlugu.md` içindeki *llms.txt* maddesi.

### Ölçüm — 2026'da artık resmî bir kaynak var

Google, **3 Haziran 2026'da Search Console'a "Generative AI performance" raporunu**
ekledi; 31 Ağustos 2026 itibarıyla tüm sitelere yayıldı.

| Ne var | Ne yok |
|---|---|
| AI Overviews **ve** AI Mode gösterimleri | **Tıklama, TO ve pozisyon yok** |
| Sayfa, ülke, cihaz, tarih kırılımı | Search Labs deneyleri dâhil değil |
| Web arama türünün alt kümesi olarak | 1.000 satır sınırı ve gecikmeli/ön veri uyarısı geçerli |

Bu rapor GEO ölçümünü **kısmen** çözer: görünürlüğü gösterir, trafiği göstermez.
Tamamlayıcı yöntemler hâlâ gerekli:

- Referrer verisinde `chatgpt.com`, `perplexity.ai`, `claude.ai` kaynaklı trafiği izlemek.
- Marka ve ürün sorularını modellere sorup alıntı durumunu elle kontrol etmek.

**Uyarı:** GEO alanında kesin oran veren iddiaların çoğu doğrulanmamıştır. Bu skill,
ölçülemeyen vaatleri metne yazmaz.
