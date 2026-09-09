# Medya Brief'i (Aşama 9)

Görsel, yazının süsü değil **bilgi taşıyıcısıdır**. Bu dosya üç soruyu cevaplar:
bu yazıya görsel gerekiyor mu, gerekiyorsa hangi türü, ve o görsel nasıl üretilir.

## İçindekiler

- [Sınıflandırma — üç yol](#siniflandirma)
- [Yol A: Diyagram — skill üretir](#diyagram)
- [Yol B: Fotoğraf/illüstrasyon — prompt üretir](#prompt)
- [Kırmızı çizgi: sahte görsel](#sahte)
- [Görsel geldikten sonra](#sonra)

---

## Sınıflandırma — üç yol {#siniflandirma}

Görsel kararı "koyalım mı" değil, **"ne işe yarayacak"** sorusuyla verilir.

| Görselin işi | Yol | Neden |
|---|---|---|
| İlişki, akış, karşılaştırma, hiyerarşi, zaman çizelgesi göstermek | **A · Diyagram** — skill SVG'yi kendi yazar | Yapay zekâ görsel modelleri etiketli şemada okunaksız sahte metin üretir |
| Ortam, ürün, malzeme, insan, atmosfer göstermek | **B · Prompt** — kullanıcı görsel aracıyla üretir | Bunu SVG ile çizmek anlamsız |
| Anlatılan şey zaten metinle ve tabloyla kapanıyorsa | **C · Görsel yok** | Zorlanmaz; görselsiz yayın kabul edilebilir |

**Karar testi:** "Bu görseli kaldırsam okur bir şey kaybeder mi?" Cevap hayırsa C'dir.
Dekoratif stok görsel eklemek, sayfa ağırlığını artırıp hiçbir soruyu cevaplamaz.

---

## Yol A — Diyagram: skill SVG'yi kendi üretir {#diyagram}

Diyagram bir prompt'a devredilmez. Skill SVG yazabilir, üstelik metin ve etiketler
tam kontrolde olur.

**Ev stili (uyulması zorunlu):**

- `viewBox` **her zaman** olsun; `width`/`height` de verilsin ki tarayıcı doğal oranı bilsin.
  (`height:auto` ile ölçeklenebilmesi buna bağlıdır.)
- **Dış font yok.** Sistem yığını kullan: `Helvetica,Arial,sans-serif` ve mono için
  `Menlo,monospace`. Projenin markalı fontu SVG içinde çalışmaz, sessizce yedeğe düşer.
- Renkler **projenin paletinden** alınır, uydurulmaz. Site koyu temalıysa diyagram da koyu
  zeminli olmalı; beyaz zeminli diyagram sayfada delik gibi durur.
- **Erişilebilirlik:** kök `<svg>` üzerinde `role="img"` ve içeriği gerçekten anlatan
  `aria-label`. Bu, alt metnin yerine geçmez — ikisi de yazılır.
- **Metin boyutu ≥ 10,5px** (viewBox ölçeğinde). Daha küçüğü mobilde okunmaz.
- **Kenar payı:** metin sağ kenara 40 birimden fazla yaklaşmasın. Uzun Türkçe cümleler
  tahmin edilenden geniş çıkar ve taşar; kısalt.
- Hedef boyut **< 8 KB**. Daha büyükse diyagram fazla karmaşıktır, ikiye böl.
- Karşılaştırma diyagramlarında **iki panel + ayırıcı** deseni işe yarar: solda sorun,
  sağda çözüm; her panelin altında tek cümlelik sonuç.

**Doğrulama:** SVG geçerli XML mi, `viewBox` var mı, `aria-label` dolu mu, tarayıcıda
gerçekten render oluyor mu. Kaynak dosyaya bakmak yetmez — göreli yol sayfanın servis
edildiği dizine göre kayabilir.

---

## Yol B — Fotoğraf/illüstrasyon: prompt paketi {#prompt}

Skill görsel üretmez; **üretilebilir bir tarif** yazar. Çıktı tam olarak şu altı alandır:

```
KONUM        : Yazının hangi bölümünden sonra, hangi işi görecek
PROMPT       : <araç için tek paragraf; konu + kompozisyon + stil + ışık + palet>
NEGATİF      : <istenmeyenler>
EN-BOY       : 16:9 (gövde) · 1.91:1 (paylaşım kartı) · 1:1 (liste küçük görseli)
DOSYA ADI    : kebab-case, hedef kelimeyi içerir, uzantı .webp
ALT METİN    : <taslak — görsel geldikten sonra gerçeğine göre düzeltilecek>
```

**Prompt yazım kuralları:**

- **Konu somut olsun.** "profesyonel iş ortamı" değil; "kreş bahçesinde kauçuk zeminli
  oyun alanı, sabah ışığı, insan yok".
- **Kompozisyonu söyle:** geniş açı / yakın plan, öznenin konumu, boş alan bırakılacak taraf
  (üstüne metin gelecekse).
- **Paleti projeden ver.** Marka renklerini prompt'a yaz, sonra düzeltmeye çalışma.
- **Negatif kısıtlar neredeyse her zaman aynı:** görüntüde metin/yazı yok, logo yok,
  marka işareti yok, sahte arayüz ya da ekran görüntüsü yok, izlenebilir yüz yok,
  filigran yok.
- **Gerçekçilik seviyesi bilinçli seçilir:** fotogerçekçi bir görsel "bu gerçek bir kayıt"
  izlenimi verir; illüstrasyon vermez. YMYL ve mevzuat içeriğinde illüstrasyon daha güvenlidir.

**Örnek çıktı:**

```
KONUM     : "Zemin tipi mesafeyi değiştirir mi?" bölümünden sonra
PROMPT    : Kreş bahçesinde kauçuk kaplı zemin üzerinde ahşap oyun grubu, geniş açı,
            sabah ışığı, yumuşak gölgeler, insan yok, sakin ve temiz kompozisyon,
            turuncu ve doğal ahşap tonları, sol üçte bir boş bırakılmış
NEGATİF   : metin, yazı, logo, marka işareti, kalabalık, yüz, filigran, aşırı doygun renk
EN-BOY    : 16:9
DOSYA ADI : oyun-grubu-kaucuk-zemin.webp
ALT METİN : Kreş bahçesinde kauçuk zemin üzerine kurulmuş ahşap oyun grubu; zemin
            ekipmanın çevresinde kesintisiz devam ediyor.
```

---

## Kırmızı çizgi: sahte görsel {#sahte}

Uydurma yasağının görsel hâli. **Yapay zekâ ile üretilmiş bir görsel, gerçek gibi sunulan
bir şeyi tasvir edemez.**

Yasak olanlar:

- Sahte ekip / çalışan fotoğrafı ("ekibimiz", "uzmanımız")
- Sahte ürün fotoğrafı — satılan ürünün gerçek fotoğrafı yerine üretilmiş görsel
- Sahte ekran görüntüsü, sahte panel, sahte rapor çıktısı
- Sahte sertifika, belge, ödül, referans logosu
- Gerçek bir kişiye ya da mekâna benzeyen üretilmiş görsel
- Vaka çalışmasında "yapılan iş"i temsil eden üretilmiş görsel

Serbest olanlar: kavramsal illüstrasyon, soyut arka plan, jenerik ortam görseli — **ve bunlar
da gerçek bir kayıt gibi sunulmaz.** Şüphedeyken görsel altına kaynağı yazılır.

**Kural:** Görselin işi *anlatmak* mı yoksa *kanıtlamak* mı? Kanıtlıyorsa üretilemez,
gerçeği kullanılır ya da hiç kullanılmaz.

---

## Görsel geldikten sonra {#sonra}

1. **Alt metni gerçeğine göre düzelt.** Brief'teki alt metin bir tahmindi; gelen görselde
   ne varsa o yazılır. Kelime istifleme yok, "görsel" ya da "resim" kelimesiyle başlama.
2. **Dosya adını uygula** (kebab-case, hedef kelimeli), formatı dönüştür (WebP/AVIF tercih).
3. **Ağırlık:** gövde görseli için 200 KB üstü gerekçe ister; kapak için 300 KB.
4. **Boyut:** gövde genişliğinin en az 1,5 katı piksel genişlik (retina), fazlası israf.
5. **Schema:** `image` alanı **yalnızca sayfada gerçekten görünen görseli** gösterir.
6. `kontrol.py` çalıştır — referans edilen dosya var mı, format ve ağırlık uygun mu,
   SVG ise `viewBox` ve `aria-label` yerinde mi.
