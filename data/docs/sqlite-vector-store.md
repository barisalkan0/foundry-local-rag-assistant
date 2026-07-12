---
title: SQLite Vektör Deposu
source: örnek
---

# SQLite Vektör Deposu

Bu projede SQLite yerel depolama katmanı olarak kullanılır. Her doküman
parçasının metni, kaynak başlığı, kaynak yolu, chunk indeksi ve embedding
vektörü JSON olarak saklanır.

SQLite başlangıç için iyi bir seçimdir; çünkü ayrı bir veritabanı sunucusu
gerektirmez. Tüm bilgi tabanı `data/rag.db` adlı tek bir dosyada yaşayabilir.

Küçük bir doküman koleksiyonu için uygulama SQLite'taki tüm embedding'leri
yükleyip cosine similarity hesabını Python içinde yapabilir. Bu yaklaşım basit
ve anlaşılırdır. Büyük bir üretim sistemi için özel bir vektör veritabanı veya
SQLite vektör eklentisi daha iyi olur; çünkü brute-force benzerlik araması chunk
sayısı arttıkça yavaşlar.
