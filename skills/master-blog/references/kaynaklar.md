# Kaynaklar ve Doğrulama Kaydı

**Son doğrulama: 7 Eylül 2026** · Sonraki gözden geçirme: en geç 7 Aralık 2026

Bu skill'deki **zamana bağlı** her iddia burada kaynağına bağlanır. Amaç iki yönlü:
(1) iddiaların denetlenebilmesi, (2) bilginin ne zaman tazelenmesi gerektiğinin görülmesi.

**Kaynak sınıfları:** `BİRİNCİL` = Google/sağlayıcı dokümantasyonu veya resmî duyurusu ·
`ÖLÇÜM` = üçüncü taraf veri çalışması · `SEKTÖR` = sektör raporu, resmî duyuru yok.

> **Kural:** Bu tablodaki bir madde 3 aydan eskiyse ve o konuda içerik yazılacaksa,
> yazmadan önce yeniden doğrula. Doğruladığında bu dosyayı güncelle.

---

## 1. Yapılandırılmış veri

| İddia | Tarih | Sınıf | Kaynak |
|---|---|---|---|
| FAQ zengin sonuçları Google Arama'dan kaldırıldı; yalnızca resmî kurum/sağlık siteleri için sürüyor | 7 Mayıs 2026 | SEKTÖR | [Search Engine Journal](https://www.searchenginejournal.com/google-drops-faq-rich-results-from-search/574429/) |
| Search Console raporu ve Zengin Sonuç Testi desteği sona erdi | Haziran 2026 | SEKTÖR | [Passionfruit](https://www.getpassionfruit.com/blog/what-changed-with-google-drops-faq-rich-results-and-what-to-do-now) |
| Search Console API desteği sona erdi | Ağustos 2026 | SEKTÖR | [Passionfruit](https://www.getpassionfruit.com/blog/what-changed-with-google-drops-faq-rich-results-and-what-to-do-now) |
| HowTo zengin sonuçları masaüstünde kaldırıldı; bugün Google SERP kazancı yok | Eylül 2023 | BİRİNCİL | [Google Search Central — HowTo duyurusu](https://developers.google.com/search/blog/2023/08/howto-faq-changes) |
| `Article` / `BlogPosting`, `BreadcrumbList`, `Organization` hâlâ zengin sonuç üretiyor | 2026 | SEKTÖR | [Digital Applied](https://www.digitalapplied.com/blog/structured-data-seo-2026-rich-results-guide) |
| Article yapılandırılmış veri gereksinimleri (headline, image, author, date) | güncel | BİRİNCİL | [Google — Article structured data](https://developers.google.com/search/docs/appearance/structured-data/article) |

**Not:** Google, FAQ kaldırma kararı için blog yazısı yayımlamadı. Bu yüzden takvim
`SEKTÖR` sınıfındadır — birden fazla bağımsız kaynakta aynı tarihlerle raporlanmıştır.

## 2. Core Web Vitals

| İddia | Tarih | Sınıf | Kaynak |
|---|---|---|---|
| Eşikler değişmedi: LCP ≤ 2,5 sn · INP ≤ 200 ms · CLS ≤ 0,1 (75. persentil) | 2026 | BİRİNCİL | [web.dev — Web Vitals](https://web.dev/articles/vitals) |
| Core Web Vitals'ın arama açısından rolü | güncel | BİRİNCİL | [Google — Core Web Vitals ve Arama](https://developers.google.com/search/docs/appearance/core-web-vitals) |
| INP, FID'in yerini aldı | 12 Mart 2024 | BİRİNCİL | [web.dev — INP](https://web.dev/articles/inp) |
| Safari 26.2 ile LCP ve INP tüm büyük tarayıcılarda ölçülebilir hâle geldi | 12 Aralık 2025 | SEKTÖR | [corewebvitals.io](https://www.corewebvitals.io/core-web-vitals) |

## 3. Search Console ve ölçüm

| İddia | Tarih | Sınıf | Kaynak |
|---|---|---|---|
| "Generative AI performance" raporu duyuruldu (AI Overviews + AI Mode gösterimleri) | 3 Haziran 2026 | BİRİNCİL | [Google Search Central Blog](https://developers.google.com/search/blog/2026/06/gen-ai-performance-reports) |
| Rapor **yalnızca gösterim** verir; tıklama/TO/pozisyon yoktur; Search Labs hariçtir; 1.000 satır sınırı geçerlidir | 2026 | BİRİNCİL | [Search Console Yardım](https://support.google.com/webmasters/answer/16984139) |
| Rapor tüm sitelere yayıldı | 31 Ağustos 2026 | BİRİNCİL | [Search Console Yardım](https://support.google.com/webmasters/answer/16984139) |
| AI Mode verisi ana Search Console toplamlarına dâhil edildi | 17 Haziran 2025 | SEKTÖR | [Passionfruit araştırması](https://www.getpassionfruit.com/research/your-search-console-data-has-been-wrong-for-a-year) |
| `&num=100` parametresi kaldırıldı; gösterim ve ortalama pozisyon verisinde kırılma oluştu | 12 Eylül 2025 | SEKTÖR | [Passionfruit araştırması](https://www.getpassionfruit.com/research/your-search-console-data-has-been-wrong-for-a-year) |
| Mayıs 2025'te gösterimleri şişiren kayıt hatası | Mayıs 2025 | SEKTÖR | [Passionfruit araştırması](https://www.getpassionfruit.com/research/your-search-console-data-has-been-wrong-for-a-year) |

**Sonuç:** Bu üç tarihin (Mayıs 2025, 17 Haziran 2025, 12 Eylül 2025) öncesi ve sonrası
**doğrudan karşılaştırılamaz.** "Gösterimler düştü" teşhisi koymadan önce karşılaştırılan
dönemin bu kırılmaları kapsayıp kapsamadığına bakılır.

## 4. Öne çıkan snippet ve AI Overviews

| İddia | Tarih | Sınıf | Kaynak |
|---|---|---|---|
| Snippet SERP görünürlüğü %15,41 → %5,53 (~%64 düşüş, 863.000 anahtar kelime) | Ocak–Haziran 2025 | ÖLÇÜM | [Ahrefs verisi, aktaran Digital Applied](https://www.digitalapplied.com/blog/featured-snippets-ai-overview-era-optimization-2026) |
| Snippet, AI Overviews'lı sorguların ~%19'unda hâlâ görünüyor | 2026 | ÖLÇÜM | [Digital Applied](https://www.digitalapplied.com/blog/featured-snippets-ai-overview-era-optimization-2026) |
| Daha önce snippet kazanan sayfalar AI Overviews'ta ~2 kat daha sık alıntılanıyor | 2026 | ÖLÇÜM | [AirOps](https://www.airops.com/blog/featured-snippets-ai-overviews-position-zero) |

## 5. llms.txt

| İddia | Tarih | Sınıf | Kaynak |
|---|---|---|---|
| Google, llms.txt'i desteklemediğini ve destekleme planı olmadığını açıkladı | Temmuz 2025 | SEKTÖR | [Baseline Labs](https://baselinelabs.ai/blog/llms-txt-google-search) |
| 137.000 alan adı incelemesinde dosyaların %97'si hiç istek almadı; gelen isteklerin %1,1'i AI getirme botu | Mayıs 2026 | ÖLÇÜM | [Ahrefs verisi, aktaran Mecanik](https://mecanik.dev/en/posts/does-llms-txt-do-anything-yet/) |
| Perplexity dosyayı okuduğunu belirten istisna; OpenAI/Anthropic/Meta/Mistral taahhüt vermedi | 2026 | SEKTÖR | [Mecanik](https://mecanik.dev/en/posts/does-llms-txt-do-anything-yet/) |
| Chrome Lighthouse 13.3, llms.txt denetimini varsayılan kategoriye aldı | 7 Mayıs 2026 | SEKTÖR | [Mecanik](https://mecanik.dev/en/posts/does-llms-txt-do-anything-yet/) |

**Sonuç:** llms.txt "yapabilirsin" kategorisindedir, "yapmazsan kaybedersin" değil.
Zararı yok, ölçülebilir getirisi doğrulanmadı.

## 6. AI tarayıcıları (robots.txt)

| İddia | Tarih | Sınıf | Kaynak |
|---|---|---|---|
| Eğitim botları: GPTBot, ClaudeBot, Google-Extended, CCBot, Applebot-Extended, Meta-ExternalAgent, Bytespider | 2026 | SEKTÖR | [HoneyB tarayıcı referansı](https://www.honeyb.ai/blog/ai-crawler-user-agents-reference-2026) |
| Getirme/arama botları: OAI-SearchBot, ChatGPT-User, Claude-SearchBot, Claude-User, PerplexityBot, Perplexity-User | 2026 | SEKTÖR | [HoneyB tarayıcı referansı](https://www.honeyb.ai/blog/ai-crawler-user-agents-reference-2026) |
| `ClaudeBot` engeli `Claude-SearchBot` ve `Claude-User`'ı engellemez | 2026 | SEKTÖR | [No Hacks](https://nohacks.co/blog/ai-user-agents-landscape-2026) |
| Bazı botların robots.txt'i yok saydığı belgelendi | 2026 | SEKTÖR | [No Hacks](https://nohacks.co/blog/ai-user-agents-landscape-2026) |
| Anthropic'in kendi tarayıcı tokenları ve davranışı | güncel | BİRİNCİL | [Anthropic — tarayıcılar](https://support.anthropic.com/en/articles/8896518-does-anthropic-crawl-data-from-the-web-and-how-can-site-owners-block-the-crawler) |
| OpenAI'nin tarayıcı tokenları | güncel | BİRİNCİL | [OpenAI — bots](https://platform.openai.com/docs/bots) |

**Not:** Bot tokenları sağlayıcı dokümantasyonundan doğrulanmalıdır; liste değişkendir.
Karar vermeden önce ilgili sağlayıcının kendi tarayıcı sayfasına bak.

## 7. Google çekirdek güncellemeleri

| İddia | Tarih | Sınıf | Kaynak |
|---|---|---|---|
| Güncelleme takviminin resmî kaydı (çekirdek, spam ve Discover güncellemeleri) | sürekli | BİRİNCİL | [Google Arama Durum Panosu](https://status.search.google.com/products/rGHU1u87FJnkP6W2GwMi/history) |
| Mart 2026 çekirdek güncellemesi: 27 Mart 2026 başlangıç, 12 gün 4 saat sürdü | 27 Mart 2026 | BİRİNCİL | [Google Arama Durum Panosu](https://status.search.google.com/products/rGHU1u87FJnkP6W2GwMi/history) |
| Mayıs 2026 çekirdek güncellemesi: 21 Mayıs 2026 başlangıç, 11 gün 21 saat sürdü | 21 Mayıs 2026 | BİRİNCİL | [Google Arama Durum Panosu](https://status.search.google.com/products/rGHU1u87FJnkP6W2GwMi/history) |
| Yeni sıralama sistemi getirilmedi; rehberlik aynı kaldı (yararlı, insan öncelikli içerik) | 2026 | BİRİNCİL | [Google — Core updates](https://developers.google.com/search/docs/appearance/core-updates) |

**Sonuç:** İçerik ilkeleri değişmedi. Sıralama düşüşü teşhisinde, düşüşün bir çekirdek
güncelleme penceresine denk gelip gelmediği **ilk bakılacak şeydir**. Panoda yalnızca
çekirdek güncellemeler değil, spam ve Discover güncellemeleri de kayıtlıdır — tarih
karşılaştırmasında hepsine bakılır.

**Doğrulama notu (7 Eylül 2026):** Bu dosyadaki dış bağlantıların tamamı `curl` ile
kontrol edilmiş ve 200 döndüğü doğrulanmıştır.

## 8. Kalıcı birincil kaynaklar

Bu sayfalar tarihe bağlı değil; doğrulama yaparken ilk bakılacak yerler.

| Konu | Kaynak |
|---|---|
| Arama Temelleri ve spam politikaları | [Google Search Essentials](https://developers.google.com/search/docs/essentials) |
| Yararlı içerik rehberi / kendi kendini değerlendirme soruları | [Creating helpful content](https://developers.google.com/search/docs/fundamentals/creating-helpful-content) |
| Kalite değerlendirici kılavuzu (E-E-A-T'nin tanımlandığı belge) | [Search Quality Rater Guidelines (PDF)](https://static.googleusercontent.com/media/guidelines.raterhub.com/en//searchqualityevaluatorguidelines.pdf) |
| Title ve meta description rehberi | [Google — Title links](https://developers.google.com/search/docs/appearance/title-link) |
| Canonical ve kopya URL yönetimi | [Google — Canonicalization](https://developers.google.com/search/docs/crawling-indexing/consolidate-duplicate-urls) |
| Site taşıma ve yönlendirme | [Google — Redirects](https://developers.google.com/search/docs/crawling-indexing/301-redirects) |
| robots.txt yorumlama kuralları | [Google — robots.txt](https://developers.google.com/search/docs/crawling-indexing/robots/intro) |
| Zengin sonuç tiplerinin tam listesi | [Google — Search gallery](https://developers.google.com/search/docs/appearance/structured-data/search-gallery) |
| Claude Skills dokümantasyonu | [Anthropic — Agent Skills](https://docs.claude.com/en/docs/agents-and-tools/agent-skills) |

---

## Değişmeyen bilgiler (tazeleme gerektirmez)

Aşağıdakiler mimari/kavramsal gerçeklerdir, sağlayıcı kararına bağlı değildir:
kanibalizasyon mekaniği, arama niyeti sınıfları, iç bağlantı mantığı, 301/canonical
davranışı, ince içeriğin tanımı, E-E-A-T çerçevesinin ne olduğu (ölçülen bir faktör
olmaması dâhil), answer-first yazım ve alıntılanabilirlik ilkeleri.
