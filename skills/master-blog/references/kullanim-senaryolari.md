# Kullanım Senaryoları

Skill projeye özel değildir; ama **her proje tipi aynı tuzaklara düşmez**. Bu dosya, sık
karşılaşılan altı proje profili için sürecin nerede saptığını, hangi eşiğin uyarlanması
gerektiğini ve ilk hafta ne yapılacağını anlatır.

Aşama 0'da proje tipi belirlendikten sonra buradaki ilgili bölüm okunur. Tanımlanan
profillerden hiçbirine uymuyorsa genel akış aynen uygulanır; profil uydurulmaz.

## İçindekiler

- [Çalışma modu: tam / kısıtlı](#calisma-modu)
- [İlk hafta planı](#ilk-hafta)
- [Profil 1 — Yerel hizmet işletmesi](#profil-1)
- [Profil 2 — Üretici / B2B](#profil-2)
- [Profil 3 — E-ticaret](#profil-3)
- [Profil 4 — SaaS / yazılım ürünü](#profil-4)
- [Profil 5 — Klinik / sağlık (YMYL)](#profil-5)
- [Profil 6 — Ajans / çok müşterili kurulum](#profil-6)
- [Eşik uyarlama tablosu](#esikler)

---

## Çalışma modu: tam / kısıtlı {#calisma-modu}

Skill dosya okur ve komut çalıştırır. Bu yüzden **ilk belirlenecek şey, projeye erişimin
ne kadar olduğudur.** Aşama 0'da tespit edilir ve kullanıcıya tek satırla bildirilir.

| Mod | Koşul | Skill ne yapabilir | Ne yapamaz |
|---|---|---|---|
| **TAM** | İçerik dosyaları çalışma dizininde (Astro, Next, Hugo, Eleventy, düz Markdown, Git deposu) | Bütün aşamalar | — |
| **KISITLI** | İçerik panelde yaşıyor (WordPress, Wix, Shopify blog, headless CMS erişimi yok) | Aşama 1-2, 4-9: konu, niyet, brief, yazım | Aşama 0 envanteri, Aşama 3 kanibalizasyon kapısı, Aşama 10a mekanik kontrol, Aşama 11 canlı doğrulama |

**Kısıtlı modda davranış kuralı — atlanamaz:**

1. Kullanıcıya en başta söyle: *"İçerik dosyalarına erişemiyorum. Kanibalizasyon kapısı ve
   mekanik kontrol çalışmayacak; taslak üretip elle kontrol listesi vereceğim."*
2. **Kapıları "geçti" sayma.** Rapor `Kanibalizasyon: DENETLENEMEDİ (kısıtlı mod)` yazar.
   Sahte onay vermek, hiç kontrol etmemekten daha zararlıdır.
3. Kullanıcıdan **mevcut yazı başlıklarının ve hedef kelimelerinin listesini iste** —
   bu liste geldiğinde Aşama 3 elle çalıştırılabilir. Liste gelmezse kapı kapalı kalır.
4. Yayın sonrası kontrol listesini kullanıcının elle yapabileceği biçimde ver
   (URL 200 mü, sitemap'te var mı, iç linkler çalışıyor mu).

**Kısıtlı modu tam moda çevirmenin yolu:** içeriği dışa aktarıp bir dizine koymak.
WordPress'te "Araçlar → Dışa Aktar" ile alınan XML'i Markdown'a çevirip yerel bir klasöre
koymak, en azından envanter ve kanibalizasyon denetimini mümkün kılar. Bu bir öneridir,
zorunluluk değil.

---

## İlk hafta planı {#ilk-hafta}

Skill yeni kurulduğunda ilk iş yazı yazmak **değildir**. Sırasıyla:

1. **Gün 1 — Envanter.** `master-blog skill'iyle içerik envanterimi çıkar, yazı yazma.`
   Çıktı: her yazının hedef sorgusu, niyeti, kelime sayısı, iç link sayısı.
2. **Gün 1 — Kanibalizasyon taraması (geriye dönük).** `Mevcut yazılar arasında
   kanibalizasyon var mı?` Yeni yazı yazmadan önce mevcut çakışmaları görmek, ilk yazının
   nereye konumlanacağını belirler.
3. **Gün 2 — Eşik uyarlaması.** Aşağıdaki tabloya göre `kontrol.py` eşiklerini projene
   göre ayarla. Özellikle yeni sitelerde `IC_LINK_MIN = 4` gerçekçi değildir.
4. **Gün 2 — Kırmızı çizgi kontrolü.** Projenin kendi yasakları varsa (marka dili, fiyat
   yayınlamama kararı, rakip adı anmama) `SKILL.md`'nin kırmızı çizgiler bölümüne ekle.
5. **Gün 3 — İlk yazı.** Tercihen mevcut hiçbir yazıyla çakışmayan, veri gerekçesi en net
   olan konudan başla.
6. **Gün 31 — Ölçüm.** Aşama 12'yi çalıştır. İlk yazının işe yarayıp yaramadığını değil,
   **sürecin işleyip işlemediğini** değerlendir.

---

## Profil 1 — Yerel hizmet işletmesi {#profil-1}

*Su tesisatçısı, klima servisi, çilingir, elektrikçi, haşere kontrol.*

**Proje profili:** Az sayfa, yüksek ticari niyet, coğrafi hedefleme, acil arama davranışı.
Genellikle 5-15 hizmet sayfası ve 0-10 blog yazısı.

**En sık hata:** Ticari sorguyu blogla hedeflemek. "Su kaçağı tespiti fiyatları" için blog
yazmak, kendi hizmet sayfanı kanibalize eder. Aşama 2 bunu yakalar ve blog yerine hizmet
sayfası güçlendirmesi önerir.

**Aşama sapmaları:**
- **Aşama 1:** Search Console verisi genelde zayıftır. Aday kaynağı sırası değişir:
  gelen telefon/WhatsApp sorularının tekrar edenleri > Google Ads arama terimleri >
  hizmet sayfalarında geçmeyen alt hizmetler.
- **Aşama 2:** Niyet dağılımı ağırlıklı **işlem**dir. Blog yalnızca bilgi varyantını
  hedefler ve **her yazı huninin altına link verir** (teklif/arama/randevu).
- **Aşama 7:** Yerel deneyim en güçlü ayrışma noktasıdır — ama uydurulmaz. "Kadıköy'deki
  eski binalarda galvaniz boru hâlâ yaygın" cümlesi ancak proje verisinde karşılığı varsa
  yazılır.
- **Aşama 8:** İç link hedefleri arasında **hizmet sayfası ve bölge sayfası zorunludur**.
- **Doorway riski yüksek:** İlçe başına aynı metni çoğaltmak bu sektörde çok yaygın.
  Her bölge sayfasında gerçekten farklı veri (o bölgede yapılan iş, ulaşım süresi, yapı
  stoku farkı) yoksa üretilmez.

**Örnek prompt:**
```
master-blog skill'iyle "su kaçağı nasıl anlaşılır" konusunu hazırla.

Ticari sayfamı kanibalize etmediğinden emin ol; yazının sonunda
kaçak tespiti hizmet sayfasına doğal bir geçiş olsun.
Ölçü ve fiyat uydurma — repoda yoksa genel ifade kullan.
```

**Beklenen ilk çıktı:** Aşama 2'de niyet etiketi ve "bu sorgu blog için uygun / uygun
değil" kararı; ardından brief.

---

## Profil 2 — Üretici / B2B {#profil-2}

*Park ekipmanı, makine imalatı, endüstriyel ürün, mühendislik hizmeti.*

**Proje profili:** Uzun satın alma döngüsü, teknik şartname arayan okur, standart ve
mevzuat referansları, seri/model bazlı ürün verisi.

**En sık hata:** Ürün kataloğunu blog diye yeniden yazmak. Seri sayfası zaten "X serisi
nedir"i anlatıyorsa blog aynı şeyi anlatmaz; **karar desteği** üretir ("hangi seri hangi
yaş grubuna uygun").

**Aşama sapmaları:**
- **Aşama 0:** Ürün veri dosyaları (`seriler.ts`, `urunler.json`) birinci kaynaktır. Teknik
  bilginin tamamı buradan gelir.
- **Aşama 5:** Kapsam bandı yukarı kayar (1.200-2.200). Alıcı karşılaştırma arar.
- **Aşama 6:** Tablo isteğe bağlı değil, zorunludur. Şartname karşılaştırması bu sektörde
  en çok alıntılanan yapıdır.
- **Aşama 7:** Standart adı **yalnızca projede geçenler** kullanılır (TS EN vb.). Numara
  uydurmak bu sektörde en ağır güven kaybıdır.
- **Aşama 8:** Blog → seri/kategori sayfası bağlantısı zorunlu; blog ana ticari kelimeyi
  birebir hedeflemez.

**Örnek prompt:**
```
master-blog skill'iyle "oyun grubu nasıl seçilir" karar rehberi yaz.

Teknik bilgiyi yalnızca src/data/seriler.ts'ten al.
Yaş grubu / alan ihtiyacı / zemin tipi karşılaştırma tablosu koy.
Seri sayfalarına en az 3 iç link ver, ana ticari kelimeyi hedefleme.
```

---

## Profil 3 — E-ticaret {#profil-3}

*Ürün kataloğu, çok sayıda kategori ve varyant.*

**En sık hata:** Kategori sayfasıyla blog yazısının aynı sorguyu hedeflemesi. E-ticarette
kanibalizasyonun en pahalı biçimi budur: kategori sayfası para kazandıran sayfadır, blog
onun önüne geçerse dönüşüm düşer.

**Aşama sapmaları:**
- **Aşama 2:** "en iyi X", "X mi Y mi" gibi ticari araştırma sorguları blogun asıl alanıdır;
  "X satın al" kategori sayfasınındır. Bu ayrım her yazıda açıkça yazılır.
- **Aşama 3:** Kanibalizasyon denetimi **kategori ve filtre sayfalarını da** kapsar, sadece
  blogu değil. Filtre kombinasyonlarından doğan sayfalar en sık gözden kaçan çakışmadır.
- **Aşama 9:** Ürün adı geçen yazılarda schema'da sayfada görünmeyen fiyat/stok iddiası
  yazılmaz.
- **Aşama 12:** Ölçüm yalnızca gösterim/pozisyon değil, **yazının yönlendirdiği kategori
  sayfasının** performansını da içerir.

---

## Profil 4 — SaaS / yazılım ürünü {#profil-4}

**En sık hata:** Ürün dokümantasyonuyla blogun aynı sorguyu hedeflemesi ("nasıl X yapılır"
hem dokümanda hem blogda). Dokümantasyon çoğunlukla daha güçlü sinyal taşır; blog onu yer.

**Aşama sapmaları:**
- **Aşama 0:** Envantere **dokümantasyon sayfaları da dâhil edilir.** Yalnızca `blog/`
  dizinine bakmak bu profilde yanlış sonuç verir.
- **Aşama 3:** Kanibalizasyon karşılaştırması blog ↔ doküman arasında da yapılır. Kural:
  "nasıl yapılır" dokümana, "neden / hangi durumda / karşılaştırma" bloga aittir.
- **Aşama 6:** Kod bloğu ve komut örneği alıntılanabilirliği artırır; ama **çalıştığı
  doğrulanmamış kod yayınlanmaz** (skill'in uydurma yasağı koda da uygulanır).
- **Aşama 12:** Sürüm değişiklikleri içeriği hızlı eskitir. Tazeleme aralığı 3 ay değil,
  **sürüm bazlıdır**: ilgili özellik değiştiyse yazı da güncellenir.

---

## Profil 5 — Klinik / sağlık (YMYL) {#profil-5}

*Diş kliniği, fizyoterapi, diyetisyen, estetik, veteriner.*

**Bu profilde çıta yükselir; skill'in varsayılan davranışı sertleştirilir.**

- **İsimli uzman zorunlu.** "Klinik ekibi" imzası kabul edilmez; yazar adı, unvanı ve
  uzmanlık alanı sayfada görünür olur. Yazar sayfası yoksa üretilecek ilk şey odur.
- **Resmî kaynak zorunlu.** Sağlık Bakanlığı, ilgili uzmanlık derneği veya birincil
  araştırma. Kaynak yoksa iddia yazılmaz.
- **Tedavi vaadi ve garanti dili yasaktır.** "Kesin sonuç", "%100 başarı", "ağrısız" gibi
  ifadeler üretilmez. Sonuçların kişiden kişiye değiştiği belirtilir.
- **Fiyat yazılmaz** (mevzuat ve etik kısıtları değişkendir); fiyat sorusu iletişime
  yönlendirilir.
- **Aşama 10'da ek kapı:** Yazıda tanı koyan, tedavi öneren veya ilaç adı geçen bir cümle
  varsa yayın durur ve kullanıcıya sorulur.
- Tazelik kritik: mevzuat ve kılavuz değişiklikleri içeriği hızla geçersiz kılar.

---

## Profil 6 — Ajans / çok müşterili kurulum {#profil-6}

**Kurulum kararı:** Skill'i kişisel dizine (`~/.claude/skills/`) değil, **her müşteri
projesinin kendi deposuna** (`<proje>/.claude/skills/`) kur. Sebebi: eşikler, kırmızı
çizgiler ve marka dili müşteriden müşteriye değişir; kişisel kurulum hepsine aynı kuralı
dayatır.

**Müşteri başına uyarlanması gerekenler:**
- `kontrol.py` eşikleri (aşağıdaki tablo)
- Kırmızı çizgiler bölümüne müşteriye özel yasaklar (rakip adı anmama, fiyat yayınlamama,
  belirli iddiaları kullanmama)
- Aşama 1'in aday kaynak sırası (hangi veriye erişim var)
- Aşama 7'nin yazar/imza kuralı

**Ölçek notu:** Aynı anda birden çok müşteride çalışırken Aşama 0 envanteri her projede
yeniden çıkarılır; bir müşterinin envanteri diğerine taşınmaz. Bu, bağlam karışmasının en
sık kaynağıdır.

---

## Eşik uyarlama tablosu {#esikler}

`scripts/kontrol.py` başındaki sabitler. Varsayılanlar orta ölçekli, yerleşik bir site
içindir. Yeni sitede varsayılanları kullanmak sürekli blokaj üretir.

| Sabit | Varsayılan | Yeni site (< 10 yazı) | Yerel hizmet | Üretici / B2B | SaaS |
|---|---|---|---|---|---|
| `KELIME_MIN` | 600 | 400 | 500 | 800 | 600 |
| `IC_LINK_MIN` | 4 | **2** | 3 | 5 | 5 |
| `DIS_LINK_MAX` | 2 | 2 | 2 | 3 | 4 |
| `TITLE_MAX` | 60 | 60 | 60 | 60 | 60 |
| `DESC_MIN` / `DESC_MAX` | 140 / 160 | aynı | aynı | aynı | aynı |
| `SORU_ORANI` | 0,5 | 0,5 | **0,6** | 0,4 | 0,5 |
| `PARA_MAX_KELIME` | 90 | 90 | **70** | 110 | 90 |

**Gerekçeler:** Yeni sitede 4 iç link verecek kadar sayfa yoktur — eşik yazıyı bozar, o
yüzden 2'ye iner. Yerel hizmette okur acele eder; paragraflar kısalır ve başlıklar daha
çok soru biçimi alır. B2B'de okur teknik derinlik arar; paragraf ve kapsam genişler.
SaaS'ta dokümantasyona verilen iç link sayısı doğal olarak yüksektir.

**Kural:** Eşiği değiştirdiğinde **neden değiştirdiğini dosyaya yorum olarak yaz.**
Gerekçesiz sabit, altı ay sonra kimsenin dokunamadığı bir sayıya dönüşür.
