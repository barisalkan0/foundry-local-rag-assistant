---
title: RAG Temelleri
source: örnek
---

# RAG Temelleri

Retrieval-Augmented Generation, yani RAG, üç ana adımdan oluşur. Önce doküman
koleksiyonundan alakalı bilgi getirilir. Sonra model prompt'u getirilen bilgiyle
zenginleştirilir. En sonunda model bu bağlama dayalı cevap üretir.

RAG, halüsinasyonu azaltmaya yardımcı olur; çünkü model yalnızca genel eğitim
bilgisine dayanmak yerine yerel dokümanlardan getirilen bağlamla cevap verir.

Retrieval adımı kritiktir. Uygulama yanlış chunk getirirse model zayıf bağlam
alır ve cevap eksik veya hatalı olabilir. Bu nedenle proje her cevapta kaynak
başlıklarını ve benzerlik skorlarını gösterir.

Yeterince alakalı chunk bulunamadığında uygulama chat modelini çağırmamalıdır.
Bunun yerine "Yerel dokümanlarda bu bilgi yok." gibi bir fallback cevap
döndürmelidir. Bu davranış, modelin ilgisiz genel bilgiden cevap vermesini
azaltır.
