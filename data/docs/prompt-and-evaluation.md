---
title: Prompt ve Değerlendirme
source: örnek
---

# Prompt ve Değerlendirme

Sistem prompt'u asistana yalnızca verilen bağlamdan cevap vermesini söyler.
Ayrıca yerel bağlam cevabı içermiyorsa bilmediğini söylemesini ister.

Prompt talimatları yararlıdır, fakat tek başına yeterli değildir. Küçük yerel
modeller, retrieval bağlamı zayıf olduğunda hâlâ genel bilgiden cevap verebilir.
Bu nedenle uygulama minimum retrieval skoru kullanır. En iyi chunk skoru çok
düşükse asistan chat modelini çağırmadan fallback cevap döndürür.

Değerlendirme üç kontrol içermelidir: cevap doğru mu, gösterilen kaynak alakalı
mı, eksik bilgi fallback cevap üretiyor mu? Güçlü bir demo bu üç durumu da
gösterir.
