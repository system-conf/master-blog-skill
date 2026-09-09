# Üslup Katmanı (Aşama 5.5)

SEO ile GEO arasında duran katman. **Sırası tesadüf değil:** başlık ve hedef kelime
netleştikten sonra, alıntılanabilirlik kurulmadan önce gelir — çünkü kötü yazılmış bir
metni tablo kurtarmaz.

> **Kaynak notu:** Bu katmanın büyük kısmı bir **dış saha geri bildiriminden** geldi
> (Eylül 2026, Türkçe bir SaaS'ın 53 yazılık arşivinden çıkarılmış iç doktrin).
> Eşikler ölçülmüş değil, o ekibin kalibrasyonu — `kaynaklar.md`'de `SEKTÖR` sınıfında
> kayıtlı. Projede kalibre edilmeleri beklenir, olduğu gibi kabul edilmez.

## İçindekiler

- [Açılış kuralı](#acilis)
- [Cümle ritmi](#ritim)
- [Üslup klişeleri](#klise)
- [Karşı-tez bölümü](#karsi-tez)
- [Kopyalanabilir varlık](#varlik)
- [Ticari köprü doktrini](#kopru)
- [Dile özgü kurallar](#dil)

---

## Açılış kuralı {#acilis}

**Yazı, konuyu tanıtan bir cümleyle başlamaz.** İlk paragraf dört şeyden biriyle açılır:
somut bir olay · bir nesne · bir diyalog · doğrulanabilir bir rakam.

Mekanik olarak yakalanan klişe açılışlar: *günümüzde · bu yazıda · ele alacağız ·
büyük önem · sıkça sorulan · hızla gelişen · son yıllarda*.

**Açılış tipi tekrarı.** Tek tek doğal olan açılışlar arka arkaya yayınlanınca desen
üretir. Arşivdeki son 5 yazının açılış tipi kayıtlıysa altıncı yazı aynı tipi
tekrarlamamalı. (Geri bildirimi veren ekip bunu kendi arşivinde yaşamış: sekiz yazı üst
üste "şehir + isim + senaryo" ile açmış.)

---

## Cümle ritmi {#ritim}

Yapay zekâ metninin en belirgin imzası uzun cümle değil, **uzunluğu hiç değişmeyen cümle
dizisidir.** Ortalama bunu göstermez; **standart sapma** gösterir.

Ortalaması 14 olan iki metinden biri "hep 14 kelime", diğeri "22, 4, 17, 6, 11" olabilir.
İkincisi insan yazımıdır.

| Ölçüt | Varsayılan eşik | Neden |
|---|---|---|
| Ortalama cümle uzunluğu | 10-18 kelime | Üstü akademik, altı telgraf |
| **Standart sapma** | **≥ 5** | En kritik ölçüt; düşük sapma tekdüze ritim demektir |
| 25+ kelimelik cümle oranı | ≤ %5 | Uzun cümle nefesi keser |
| Paragraf başına cümle | ≤ 4 | Mobil okunabilirlik |

**Ölçüm tuzağı — bu maddeyi uygularken en sık yapılan hata:** cümle bölücü kaba yazılırsa
sonuç tamamen değişir. İki nokta üst üsteden (`:`) de bölen bir bölücü, bu skill'in kendi
yazılarında cümle sayısını **%20 şişirdi**, ortalamayı 10,8'den 8,5'e, sapmayı 5,8'den
3,9'a düşürdü — yani metni olduğundan tekdüze gösterdi ve **yanlış bir bulgu üretti.**

Doğru bölücü: yalnızca `.!?` sonrası, ardından boşluk ve büyük harf; kısaltmalar
(`vb. vs. bkz. Dr.`) ve ondalık sayılar korunur. Tablo satırları, kod blokları, başlıklar
ve alıntılar hesaba katılmaz.

---

## Üslup klişeleri {#klise}

Bunlar yanlış bilgi değil; **hiçbir insanın kurmadığı cümlelerdir.** Okur bunları gördüğü
an metnin kimliğine dair bir karar verir.

| Sınıf | Örnekler |
|---|---|
| Bağlaç şişirmesi | bu bağlamda · bu çerçevede · bu doğrultuda · söz konusu |
| İçi boş vurgu | şüphesiz · tartışmasız · son derece |
| Meta-anlatım | bu yazıda · ele alacağız · inceleyeceğiz · gördüğümüz gibi |
| Pazarlama şişirmesi | devrim niteliğinde · oyunun kurallarını değiştiren · çığır açan |
| Boş kapanış | başarılar dileriz · doğru adımlarla başarıya ulaşabilirsiniz |

**Eşik: bin kelimede 2.** Aşılırsa uyarı — **blokaj değil.** Sebebi: bu ifadelerin meşru
kullanımları vardır ("söz konusu madde" hukuki metinde doğrudur). Liste
`master-blog.toml` içinde `kliseler = [...]` ile genişletilir.

---

## Karşı-tez bölümü {#karsi-tez}

Bir metnin gerçek deneyimden geldiğini en güçlü gösteren şey, **kendi tezinin zayıf
tarafını da yazabilmesidir.** Kitaptan okuyan tek yanlı yazar; sahada çalışan, karşı
tarafın haklı olduğu yeri bilir.

**Koşullu madde:** Yazı bir tez savunuyorsa karşı argümana en az bir bölüm ayrılır ve
karşı argüman **dürüstçe** kurulur — çürütmek için zayıflatılmaz. Tanım yazısında
("kanibalizasyon nedir") bu madde uygulanmaz; savunulan bir tez yoktur.

Örnekler: kâğıt defterin yetersizliğini anlatan yazıda *"defterin hâlâ iyi olduğu üç şey"* ·
ücretsiz yazılımın tuzaklarını anlatan yazıda *"kime yeter, kime tuzak"*.

Yan fayda: ticari içerikte güven maliyetini düşürür. Okurun itirazını okurdan önce
yazmış olursunuz.

---

## Kopyalanabilir varlık {#varlik}

Kontrol listesi tabloyu zaten blokaj yapıyor, ama gerekçesi makine tarafında:
*"alıntılanabilirliği artırır."* Eksik olan gerekçe şu: tablo aynı zamanda **okurun alıp
kullanabileceği** bir varlıktır.

Bu ayrım tablonun içeriğini değiştirir. GEO için yazılmış tablo bilgiyi özetler; okur için
yazılmış tablo ekrandan kopyalanıp ajandaya, sözleşmeye ya da telefona geçer.

Varlık tipleri: konuşma metni (telefon açılışı, itiraz karşılama) · karar tablosu ·
haftalık uygulama planı · görüşmede sorulacak soru listesi · hazır onay/sözleşme cümlesi.

**Madde:** Yazı, okurun kopyalayıp kendi işinde kullanabileceği en az bir varlık içeriyor mu?

---

## Ticari köprü doktrini {#kopru}

Bağlantı kurallarımız (Aşama 8) **nereye** link verileceğini söylüyor ama **nerede ve hangi
mantıkla** ürün bahsi geçeceğini söylemiyor. Ticari içerikte metnin reklam mı rehber mi
okunduğunu belirleyen tek şey budur.

1. **Ürün adı yazının ilk yarısında geçmez.** Geçtiği anda metin tanıtım olarak okunmaya
   başlar ve okur savunmaya geçer.
2. **Ürün, bir tezin sonucu olarak girer; çözüm önerisi olarak değil.** Yazı boyunca bir
   argüman kurulur; ürün o argümanın adı olarak son bölümde görünür. **Vaat değil tarif:**
   "şunu ve şunu tek yerde tutar" — "hayatınızı kolaylaştırır" değil.
3. **Yazı ürünle bitmez.** Son paragraf açılıştaki örneğe döner ve anlatıyı kapatır.
   Okurun son okuduğu cümle satış cümlesi olmamalı.

---

## Dile özgü kurallar {#dil}

- **Hitap tutarlılığı:** Bir yazı ya "sen" ya "siz" kullanır, ikisi karışmaz. Mekanik
  olarak denetlenir; çeviri kökenli metinlerin en sık kırdığı kuraldır.
- **Çeviri kokusu:** `-abilirsiniz` yığılması, "önemlidir" ile biten cümle serileri,
  İngilizce yapının birebir aktarılması ("Bu, şu anlama gelir ki…").
- **Yerli benzetme:** Metaforlar hedef ülkede yaşayan birinin kuracağı türden olmalı.
  Mekanik denetlenemez; brief aşamasında hatırlatılır.

---

## Ölçümle ilişkisi — ve bir sınır

Üslubun işe yarayıp yaramadığı Aşama 12'de görülebilir:

| Gözlem | Editoryal yorum | İşlem |
|---|---|---|
| Pozisyon iyi, tıklama iyi, okuma derinliği düşük | Başlık vaadi metinle örtüşmüyor ya da giriş tutmuyor | Açılışı ve ilk 200 kelimeyi yeniden yaz |
| Tıklama iyi, dönüşüm sıfır | Metin bilgilendiriyor ama sonraki adımı vermiyor | Ticari köprüyü ve kapanışı gözden geçir |

**Sınır — bu satırlar sıralama sinyali değildir.** Google, okuma süresi (dwell time) ve
hemen çıkma oranını doğrudan sıralama faktörü olarak kullandığını **reddediyor**; 2024 API
sızıntısı içeride "uzun tıklama / kısa tıklama" izlendiğini gösteriyor, yani konu
tartışmalı. Bu yüzden tablo **editoryal teşhis** olarak kullanılır, "Google bunu görüyor"
diye gerekçelendirilmez (12. kırmızı çizgi).

Ayrıca bu iki satır **analytics erişimi olan projelerde** çalışır. Search Console okuma
süresi vermez; erişim yoksa satırlar atlanır ve raporda "ölçülemedi" yazılır.
