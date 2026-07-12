---
title: Proje İş Akışı
source: örnek
---

# Proje İş Akışı

Proje iş akışı beş pratik adımdan oluşur.

İlk olarak Markdown dokümanları `data/docs` klasörüne yerleştirilir. İkinci
olarak ingestion scripti bu dokümanları okur ve chunk'lara böler. Üçüncü olarak
embedding modeli her chunk'ı sayısal bir vektöre dönüştürür. Dördüncü olarak
chunk'lar ve vektörler SQLite'a kaydedilir. Beşinci olarak kullanıcı soru sorar
ve uygulama chat modelini çağırmadan önce en benzer chunk'ları bulur.

Dokümanları değiştirdikten sonra ingestion komutunu tekrar çalıştır. Bu adım
yapılmazsa SQLite hâlâ eski bilgi tabanını içerir ve asistan yeni dokümanları
kullanmaz.

Demo için hem cevaplanabilir hem de cevaplanmaması gereken sorular hazırla.
Cevaplanabilir sorular retrieval'ın çalıştığını gösterir. Cevaplanmaması gereken
sorular ise asistanın desteksiz cevap vermekten kaçındığını gösterir.
