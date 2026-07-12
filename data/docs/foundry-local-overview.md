---
title: Foundry Local Genel Bakış
source: örnek
---

# Foundry Local Genel Bakış

Foundry Local, bir uygulamanın yapay zeka modellerini kullanıcının kendi
cihazında çalıştırmasını sağlar. Uygulama inference sırasında bulut API'sine
ihtiyaç duymadan çalışabilir. Bu özellik veri gizliliği, düşük gecikme veya
çevrimdışı erişim gerektiğinde önemlidir.

Runtime, optimize edilmiş yerel modelleri indirir, önbelleğe alır, yükler ve
çalıştırır. Küçük bir model hızlı demo için yararlıdır; daha hızlı başlar ve daha
az bellek kullanır. Daha büyük bir model daha iyi cevap üretebilir, fakat daha
fazla disk alanı, bellek ve zaman ister.

Bu projede Foundry Local, yerel dil modeli runtime'ı olarak kullanılır. RAG hattı
ilgili yerel doküman parçalarını bulur ve bunları modele bağlam olarak verir. Bu
sayede cevap, modelin genel eğitim bilgisine değil yerel dokümanlara dayanır.

İlk çalıştırmada modelleri indirmek için internet gerekir. Modeller önbelleğe
alındıktan sonra normal inference yerelde çalışabilir.
