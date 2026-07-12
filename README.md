# Yerel RAG Asistanı

Bu proje, Microsoft Foundry Local ile çalışan basit bir yerel RAG uygulamasıdır.
Amaç, kendi bilgisayarımda çalışan bir yapay zeka asistanının yerel dokümanlardan
bilgi bulup cevap vermesini göstermekti.

Uygulama buluttaki bir modele istek atmıyor. İlk model indirmesi dışında cevap
üretme süreci yerelde çalışıyor.

## Kısaca Ne Yapıyor?

Kullanıcı bir soru soruyor. Uygulama önce `data/docs` klasöründeki dokümanlarda
alakalı parçaları arıyor. Sonra bulduğu parçaları Foundry Local ile çalışan yerel
modele bağlam olarak veriyor. Model de bu bağlama göre cevap üretiyor.

Eğer dokümanlarda yeterli bilgi yoksa cevap uydurmak yerine şunu söylüyor:

```text
Yerel dokümanlarda bu bilgi yok.
```

## Neden Bu Projeyi Yaptım?

Microsoft Foundry Local ve RAG mantığını öğrenmek için yaptım. Proje özellikle şu
konuları göstermek için hazırlandı:

- Foundry Local ile yerel model çalıştırma
- Dokümanları küçük parçalara ayırma
- Embedding üretme
- SQLite içinde yerel bilgi tabanı tutma
- Soruya en alakalı doküman parçalarını bulma
- Bulunan bağlamla cevap üretme
- Bilgi yoksa güvenli şekilde cevap vermeme

## Nasıl Çalışıyor?

Akış basit:

```text
Soru
  -> embedding
  -> SQLite içinde arama
  -> en alakalı doküman parçaları
  -> Foundry Local modeli
  -> kaynaklı cevap
```

Ana parçalar:

```text
data/docs/          Yerel dokümanlar
data/rag.db         SQLite bilgi tabanı
src/documents.py    Doküman okuma ve parçalama
src/embeddings.py   Embedding üretimi
src/retrieval.py    Benzerlik araması
src/rag.py          Cevap üretme akışı
scripts/ingest.py   Dokümanları veritabanına işler
scripts/ask.py      Tek soru sormak için
scripts/chat.py     Terminalde sohbet için
scripts/web.py      Web arayüzü için
```

## Kurulum

Önce bağımlılıkları kur:

```powershell
pip install -r requirements.txt
```

Foundry Local native paketleri kurulu değilse şunu çalıştır:

```powershell
foundry-local-install
```

Not: Bu komut PATH içinde görünmüyorsa Python `Scripts` klasöründeki
`foundry-local-install.exe` dosyasını çalıştırmak gerekebilir.

## Dokümanları Hazırlama

Dokümanlar `data/docs` klasöründe duruyor. Yeni doküman ekledikten veya mevcut
dokümanları değiştirdikten sonra bilgi tabanını yeniden oluşturmak gerekiyor:

```powershell
python scripts/ingest.py
```

Bu komut dokümanları okur, parçalara böler, embedding üretir ve sonucu
`data/rag.db` içine kaydeder.

## Çalıştırma

Tek soru sormak için:

```powershell
python scripts/ask.py "RAG nedir?"
```

Terminalde sohbet etmek için:

```powershell
python scripts/chat.py
```

Web arayüzünü açmak için:

```powershell
python scripts/web.py
```

Sonra tarayıcıdan şu adrese gir:

```text
http://127.0.0.1:8000
```

## Deneme Soruları

Şunları deneyebilirsin:

```powershell
python scripts/ask.py "Foundry Local çevrimdışı yapay zekaya nasıl yardımcı olur?"
python scripts/ask.py "SQLite bu projede neden yararlıdır?"
python scripts/ask.py "Dokümanları değiştirdikten sonra ne yapmalıyım?"
```

Bir de bilerek dokümanlarda olmayan bir soru sor:

```powershell
python scripts/ask.py "Fransa'nın başkenti nedir?"
```

Beklenen cevap:

```text
Yerel dokümanlarda bu bilgi yok.
```

## Test

Unit testleri çalıştırmak için:

```powershell
python -m unittest discover -s tests
```

Demo sorularını topluca denemek için:

```powershell
python scripts/evaluate.py
```

## Notlar

Bu proje öğrenme ve demo amacıyla yapıldı. SQLite üzerindeki arama küçük doküman
setleri için yeterli. Çok büyük doküman koleksiyonlarında daha gelişmiş bir
vektör veritabanı daha doğru olur.

Küçük yerel modeller Türkçe cevaplarda bazen zayıf kalabiliyor. Bu yüzden
uygulamada düşük kaliteli cevap algılanırsa en alakalı kaynak metinden kısa bir
cevap üreten ek koruma var.

## Durum

Şu an proje çalışır durumda:

- Dokümanlar işleniyor.
- SQLite bilgi tabanı oluşuyor.
- Retrieval çalışıyor.
- Foundry Local modeliyle cevap üretiliyor.
- Web arayüzü Türkçe çalışıyor.
- Bilgi yoksa cevap uydurmuyor.
