# Yayın, Ölçüm ve Arşiv Bakımı (Aşama 11-12 + arşiv kararı)

Bu dosya yayın anında ve yayından sonra okunur. İçindekiler:

- [Aşama 11 — Yayın ve canlı doğrulama](#asama-11)
- [Aşama 12 — Ölçüm](#asama-12) · üç kontrol noktası, karşı-olgu, veri kırılmaları
- [Arşiv kararı](#arsiv) · TAZELE / BİRLEŞTİR / BIRAK / KALDIR
- [Güncelleme modu](#guncelleme)

---

## Aşama 11 — Yayın ve canlı doğrulama {#asama-11}

1. Build çalıştır; hata varsa yayın yok.
2. Değişiklikleri commit'le (mesaj: `içerik: <slug> eklendi` gibi net), push et.
3. Deploy bitince **canlı URL'i doğrula**: 200 dönüyor mu, başlık/meta doğru render
   edilmiş mi, iç linkler 404 vermiyor mu.
4. Sitemap'te yeni URL var mı, `lastmod` doğru mu.
5. Search Console'da URL denetimi + indeksleme talebi (kullanıcı yapacaksa adımı yaz).
6. Kullanıcıya **tek ekranlık yayın raporu** ver: URL, hedef sorgu, kanibalizasyon kararı,
   öz denetim skoru, eklenen iç linkler, ölçüm tarihi (yayın + 28 gün).

---

## Aşama 12 — Ölçüm {#asama-12}

### Üç kontrol noktası — tek ölçüm karar üretmez

| Gün | Ne bakılır | Karar üretir mi |
|---|---|---|
| **14** | İndekslendi mi, gösterim başladı mı | Hayır — yalnızca teknik sorun teşhisi |
| **28** | Pozisyon bandı, gösterim/tıklama | Evet — başlık ve kapsam kararları |
| **90** | Kalıcı eğilim, dönüşüm katkısı | Evet — derinleştir / birleştir / bırak |

14. günde pozisyon yorumlamak erkendir; yeni URL'ler oturmamıştır.

### Karşı-olgu seti — bu adım atlanırsa teşhis yanlış çıkar

Yayın anında, **aynı kategoriden ve benzer yaştan, o dönemde dokunulmayacak 3-5 yazı**
seçilip yayın raporuna "kontrol grubu" olarak yazılır.

28. ve 90. günde hedef yazının değişimi **bu grubun medyan değişimiyle birlikte** raporlanır:

- Kontrol grubu da aynı yönde hareket ettiyse → sebep tekil sayfa değildir (mevsimsellik,
  çekirdek güncelleme, SERP bileşen değişimi). **Sayfa bazlı teşhis yapılmaz.**
- Yalnızca hedef yazı hareket ettiyse → karar tablosu uygulanır.

Bu, "yazı işe yaradı mı" sorusunu cevaplanabilir kılan tek ucuz yöntemdir. A/B testi
yapılacaksa alternatif URL'lere `rel=canonical` konur ve **301 değil 302** kullanılır;
test biter bitmez tüm test bileşenleri kaldırılır.

### Karar tablosu

Yayından 28 gün sonra bakılacaklar ve karar kuralları:

| Gözlem | Karar |
|---|---|
| Gösterim var, tıklama yok | Title + meta description yeniden yaz (içeriğe dokunma) |
| Pozisyon 8-20 | İçeriği derinleştir, iç link ekle, kapsam boşluğunu kapat |
| Pozisyon 30+ | Niyet uyumsuz olabilir; SERP formatını yeniden incele |
| Hiç gösterim yok | İndeksleme sorunu: canonical, robots, sitemap kontrol |
| Eski yazı düşüyor | Yeni yazı kanibalize etmiş olabilir — Aşama 3'ü geriye dönük çalıştır |
| Sitede genel düşüş | Önce çekirdek güncelleme takvimine bak; tarih örtüşüyorsa tekil sayfa teşhisi yapma |
| AI Overviews'ta görünürlük | Search Console → **Generative AI performance** raporu (yalnızca gösterim) |

**Veri kırılması uyarısı — atlanırsa yanlış teşhis üretir.** Search Console'da şu üç
tarihin öncesi ve sonrası doğrudan karşılaştırılamaz: Mayıs 2025 (gösterimleri şişiren
kayıt hatası), 17 Haziran 2025 (AI Mode verisinin toplamlara dâhil edilmesi),
12 Eylül 2025 (`&num=100` parametresinin kaldırılması — gösterim ve ortalama pozisyonda
kırılma). Karşılaştırılan dönem bu tarihleri kapsıyorsa "düştü/çıktı" yorumu yapmadan
önce bunu raporda belirt. Kaynaklar: `references/kaynaklar.md`.

**GEO ölçümü artık kısmen resmî.** Google, 3 Haziran 2026'da Search Console'a
"Generative AI performance" raporunu ekledi (31 Ağustos 2026 itibarıyla tüm sitelerde):
AI Overviews ve AI Mode **gösterimlerini** verir; **tıklama, TO ve pozisyon vermez.**
Yani görünürlük ölçülebilir, trafik ölçülemez — raporda bu ayrım korunur.

**Güncelleme modu** (argüman olarak mevcut yazı verildiğinde): yazıyı tam metin oku →
neyin eskidiğini listele → yalnızca eskiyeni değiştir → `guncelleme` tarihini gerçek
değişiklikle birlikte at → değişiklik özetini raporla.

---

---

## Arşiv kararı — portföy düzeyinde bakım {#arsiv}

Skill tek yazı odaklı çalışır; ama 20+ içeriği olan bir sitede **yeni yazı yazmanın marjinal
getirisi, çürümüş beş yazıyı tazelemenin getirisinden düşük olabilir.** Bu karşılaştırma
yapılmadan "yeni yazı" önerisi eksik bir öneridir.

**Ne zaman çalışır:** Aşama 1'de argüman boşsa ve envanterde 15+ içerik varsa, aday konu
önerisiyle **birlikte** sunulur.

**Nasıl çalışır:** Envanterdeki her URL için üç sinyal toplanır — *son anlamlı güncelleme
yaşı*, *pozisyon bandı*, *gösterim hacmi*. Sonra dört kovadan birine yerleştirilir:

| Kova | Koşul | Aksiyon |
|---|---|---|
| **TAZELE** | Pozisyon 8-30, gösterim var, içerik eskimiş | İçeriği derinleştir, eskiyeni değiştir, iç link ekle |
| **BİRLEŞTİR** | Başka bir yazıyla aynı niyet, örtüşme ≥ %50 | Özgün bölümleri kanoniğe taşı, zayıf URL'i **301** ile bağla |
| **BIRAK** | Düşük hacim ama doğru ve tutarlı | Dokunma. Her sayfanın trafik getirmesi gerekmez |
| **KALDIR** | Kurtarılamaz, trafiksiz, konu dışı | Eşdeğeri varsa 301; yoksa kalıcı kaldırmada **404/410** döndür, `noindex` ile gizleme |

**Kurallar:**
- İçerik silmek **son çaredir** ve yalnızca kurtarılamayacağı gösterildiğinde önerilir.
- Kaldırma önerisi her zaman yönlendirme planıyla gelir; onaysız uygulanmaz.
- `lastmod` ve `dateModified` yalnızca **anlamlı** değişiklikte güncellenir. Ana içerik,
  yapılandırılmış veri veya bağlantılar değiştiyse anlamlıdır; telif yılını güncellemek
  anlamlı değildir. Tutarsız `lastmod` değeri arama motoru tarafından yok sayılır.
- Tazeleme kuyruğunda 3+ madde varsa kullanıcıya "önce bunları toparlayalım mı" diye sorulur.

---

## Güncelleme modu {#guncelleme}

Argüman olarak mevcut bir yazı yolu verildiğinde:

1. Yazıyı **tam metin** oku (özetleme, başlıktan çıkarım yapma).
2. Neyin eskidiğini listele: tarih, rakam, mevzuat, ekran görüntüsü, kırık link, geçersiz
   tavsiye, artık var olmayan özellik.
3. **Yalnızca eskiyeni değiştir.** Gövdeyi baştan yazmak, çalışan bölümleri de riske atar.
4. `guncelleme` / `dateModified` alanını **gerçek değişiklikle birlikte** at.
5. Değişiklik özetini raporla: ne değişti, neden, hangi kaynağa dayanarak.
6. Aşama 10 kapısını yeniden çalıştır — güncellenen yazı da yeni yazı gibi denetlenir.
