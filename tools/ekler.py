"""Web rehberine eklenen içerik (Kasım 2026): güncel kanıt kutuları, vaka soruları ve ek kaynaklar.

Güncel kanıt maddelerindeki sayılar PubMed kayıtlarındaki özetlerden alınmıştır (13 Kasım 2026).
Vaka soruları notların kendi içeriğine ve buradaki güncel kanıt maddelerine dayanır.
"""

# Oturum kimliği → [(başlık, metin, ÇRS notu)]
GUNCEL = {
    "oturum-1": [
        ("Dünyada 5–24 yaş: yaklaşık her dokuz kişiden biri",
         "Küresel Hastalık Yükü verilerine göre 2019’da 5–24 yaşındaki 2,5 milyar kişinin 293 milyonunda (%11,6) en az bir "
         "ruhsal bozukluk vardı. Sıklık 5–9 yaşta %6,8, 10–14 yaşta %12,4, 15–19 yaşta %14,0, 20–24 yaşta %13,6. Bu yaş "
         "grubunda bütün nedenlere bağlı engellilik yılının (YLD) %20,3’ü ruhsal bozukluklardan; ruhsal bozukluklara bağlı "
         "yaşam boyu YLD’nin %24,9’u 25 yaşından önce (Kieling ve ark. 2024).",
         "Hizmeti “çocuk” ve “erişkin” diye iki kovaya değil, yaş dilimlerine göre planla."),
        ("p etkeni çocuklukta da güçlü",
         "2–17 yaşı kapsayan 65 çalışmanın meta-analizinde genel psikopatoloji etkeni, belirtilerdeki güvenilir varyansın "
         "yaklaşık %56’sını açıkladı; bu güç yaşla değişmedi (Harris ve ark. 2024).",
         "Eş tanı istisna değil: tek etiketin yanında genel yatkınlığı ve işlevi de değerlendir."),
    ],
    "oturum-2": [
        ("14 bozukluk, beş genetik etken",
         "1.056.201 olguyu kapsayan çalışmada beş ortak genomik etken, 14 çocukluk ve erişkin başlangıçlı bozukluğun genetik "
         "varyansının ortalama yaklaşık %66’sını açıkladı ve 238 pleiotropik lokusla ilişkiliydi. Şizofreni–bipolar etkeni ile "
         "depresyon, TSSB ve kaygıdan oluşan içselleştirme etkeninde bozukluğa özgü lokus çok azdı (Grotzinger ve ark. 2026).",
         "Genetik de kovadan çok boyutu destekliyor: aile öyküsünde aynı tanıyı değil, yakın bozukluk ailesini sor."),
        ("Otizm: 8 yaşta 31 çocukta bir",
         "ABD’de 16 merkezde 8 yaşındaki çocuklarda otizm sıklığı 2022’de binde 32,2 idi (31’de 1); erkeklerde kızlardan 3,4 "
         "kat sık. 48. aya kadar tanı alma 2018 doğumlularda 2014 doğumlulara göre daha yüksekti; rapor bunu erken tanımanın "
         "arttığı şeklinde yorumluyor (Shaw ve ark. 2025).",
         "Kalıtsallığı yüksek bir bozuklukta birkaç yılda artan sıklık, genlerden çok tanıma ve tanı pratiğindeki değişimi "
         "düşündürür."),
    ],
    "oturum-3": [
        ("Bükreş, 16. yıl: bakımın niteliği kortekse işliyor",
         "Koruyucu aileye kurayla yerleştirilmenin 16 yaştaki korteks yapısına etkisinde bakımın niteliği aracı oldu (sol alt "
         "frontal girusta kalınlık, sağ lateral oksipital kortekste yüzey alanı). En erken bakım deneyimleri, ergenlikteki "
         "korteks kalınlığıyla ayrıca ve tutarlı biçimde ilişkiliydi (Lurie ve ark. 2025).",
         "Yerleştirme kararı kadar yerleştirilen evdeki bakımın niteliği de izlenmeli; en değerli dönem en erken dönem."),
    ],
    "oturum-4": [
        ("Erişkinlerin yaklaşık %60’ı en az bir olumsuz çocukluk yaşantısı bildiriyor",
         "22 ülkeden 206 çalışmada (546.458 erişkin) hiç olumsuz çocukluk yaşantısı bildirmeyenler %39,9, dört ya da daha "
         "fazlasını bildirenler %16,1 idi. Dört ve üzeri yaşantı, ruhsal bozukluğu olanlarda %47,5’e, madde bağımlılığında "
         "%55,2’ye, evsizlerde %59,7’ye çıkıyordu (Madigan ve ark. 2023).",
         "Olumsuz yaşantıları sormak öykünün parçasıdır; yüksek puan bir risk işaretidir, hüküm değil."),
        ("Kurumda büyümek: boy, baş çevresi ve DEHB",
         "Bükreş’te kurumda büyüyen çocukların %27’si bir ya da iki ölçümde DEHB araştırma ölçütlerini karşıladı. Yavaş ve "
         "uzamış boy ve baş çevresi büyümesi hem DEHB ile hem de koruyucu aileye geç yerleşmeyle ilişkiliydi; ilişki "
         "koruyucu ailenin yararından bağımsız sürdü (Arnett ve ark. 2025).",
         "Erken yoksunluk öyküsü olan çocukta büyüme eğrisi ile dikkat değerlendirmesini birlikte oku."),
    ],
    "oturum-5": [
        ("Önce sosyal medya, sonra depresif belirti",
         "ABCD çalışmasında başlangıçta ortalama 9,9 yaşındaki 11.876 çocuk izlendi. Çocuğun kendi ortalamasının üzerindeki "
         "sosyal medya artışı ertesi yıl daha fazla depresif belirtiyle ilişkiliydi (β 0,07 ve 0,09); depresif belirtiler ise "
         "sonraki sosyal medya kullanımını yordamadı (Nagata ve ark. 2025).",
         "Yön tartışmasında kanıt “önce kullanım” lehine; etkiler küçük, yine de erken ergenlik hassas bir dönem."),
        ("Süre değil, bağımlı kullanım örüntüsü",
         "Ortalama 10 yaşındaki 4.285 genç izlendi; gençlerin yaklaşık üçte birinde sosyal medya ya da telefonda bağımlı "
         "kullanım 11 yaştan itibaren artıyordu. Artan bağımlı sosyal medya kullanımı, düşük örüntüye göre intihar "
         "davranışı riskiyle ilişkiliydi (risk oranı 2,14). Başlangıçtaki toplam ekran süresi sonuçlarla ilişkili değildi "
         "(Xiao ve ark. 2025).",
         "Ekran öyküsünde dakikayı değil kontrol kaybını sor: bırakabiliyor mu, uyku ve okul ne durumda?"),
    ],
    "oturum-6": [
        ("Fiziksel ceza davranış sorununu artırıyor",
         "69 ileriye dönük çalışmanın derlemesinde fiziksel ceza, davranış sorunlarındaki artışı zaman içinde tutarlı "
         "biçimde yordadı ve hiçbir olumlu sonuçla ilişkili değildi. Yarı deneysel çalışmalarda da davranışı kötüleştirdi; "
         "ilişkiler çocuk ve ebeveyn özelliklerine göre değişmeden tutarlıydı ve doz–yanıt ilişkisine dair bazı kanıtlar vardı "
         "(Heilmann ve ark. 2021).",
         "Davranım sorununda disiplin yöntemlerini ayrıntılı sor; fiziksel cezayı bırakmak tedavinin parçasıdır."),
    ],
    "oturum-7": [
        ("Ekran açıkken konuşma azalıyor",
         "Avustralya’da 220 ailede 12–36 ay boyunca kayıt alındı. 36. ayda ekran süresindeki her ek dakika 6,6 daha az "
         "yetişkin sözcüğü, 4,9 daha az çocuk seslendirmesi ve 1,1 daha az karşılıklı konuşma dönüşüyle ilişkiliydi "
         "(Brushe ve ark. 2024).",
         "Dil gecikmesinde ekranın zararı, konuşma sırasını elinden almasıdır: karşılıklı konuşma bir tedavi aracıdır."),
        ("Erken müdahalede saat değil nitelik",
         "Otizmli küçük çocuklarda 144 çalışmayı (9.038 çocuk) birleştiren meta-analizde müdahale miktarının hiçbir ölçüsü, "
         "aynı müdahale türü içinde etki büyüklüğüyle anlamlı ve pozitif ilişki göstermedi (Sandbank ve ark. 2024).",
         "Yoğun müdahaleyi destekleyen sağlam kanıt az: aileye saati değil, uygunluğu ve sürdürülebilirliği öner."),
    ],
    "oturum-8": [
        ("Kenevir riski yaşa bağlı",
         "Ontario’da 12–24 yaşındaki 11.363 kişide kenevir kullanımı, ergenlikte psikotik bozuklukla güçlü biçimde "
         "ilişkiliydi (düzeltilmiş HR 11,2), genç erişkinlikte ise anlamlı değildi (HR 1,3). Ergenlikteki ilişki önceki "
         "çalışmalardakinden güçlüydü; yazarlara göre bu, kenevirin artan potensini yansıtıyor olabilir (McDonald ve ark. 2024).",
         "Ergende kenevir sorusu, psikoz riskini değerlendirirken atlanmamalı."),
        ("Glutamat yoluyla bilişe ilaç: üç faz 3’te sonuç yok",
         "Glisin taşıyıcı-1 inhibitörü iklepertin, 41 ülkede 1.835 hastayı kapsayan üç faz 3 çalışmada (CONNEX) 26. haftada "
         "bilişsel bileşik puanda plasebodan farklı değildi (Keefe ve ark. 2025).",
         "Sapolsky’nin 2024’te andığı glutamat yaklaşımı için önemli bir olumsuz sonuç; bilişsel güçlükte psikososyal ve "
         "işlevsel destek yerinde durmalı."),
    ],
    "ek-9": [
        ("Okulda sosyal-duygusal öğrenme",
         "53 ülkeden 424 çalışmada (575.361 öğrenci) okul temelli evrensel sosyal-duygusal öğrenme programları; beceri, "
         "tutum, davranış, okul iklimi ve güvenliği, akran ilişkileri ve akademik başarıyı iyileştirdi. Etki, programın "
         "içeriği ve uygulama niteliğine göre değişti (Cipriano ve ark. 2023).",
         "Panzehir okulda da verilir; ama uygulama niteliği düşükse kazanç da düşer."),
    ],
    "ek-10": [
        ("Egzersiz bir tedavi",
         "218 çalışmada (14.170 katılımcı) yürüyüş ya da koşu (Hedges g −0,62), yoga (−0,55) ve kuvvet antrenmanı (−0,49) "
         "aktif kontrollere göre depresyonu orta düzeyde azalttı; etki önerilen yoğunlukla arttı. Kanıtın güveni düşük ya da "
         "çok düşük (Noetel ve ark. 2024).",
         "Egzersiz, tedavi planına somut bir reçete olarak yazılabilir; kanıtın güven düzeyi de aileyle paylaşılmalı."),
        ("Esketamin tek başına da etkili",
         "Tedaviye dirençli depresyonu olan 378 erişkinde burun içi esketamin tek başına (56 ve 84 mg), 28. günde MADRS "
         "puanını plaseboya göre 5,1 ve 6,8 puan daha fazla düşürdü; fark ilk dozdan yaklaşık 24 saat sonra da anlamlıydı. En "
         "sık yan etkiler bulantı (%24,8) ve dissosiyasyondu (%24,3) (Janik ve ark. 2025).",
         "Veriler erişkinlerde; ergende kanıt hâlâ küçük bir randomize çalışmayla sınırlı (Dwyer ve ark. 2021)."),
    ],
    "ek-11": [
        ("Örtük önyargı: kilo, yaş ve engellilikte değişim yok",
         "Project Implicit’teki 7,1 milyon testte 2007–2020 arasında bütün açık önyargılar azaldı (%22 ile %98 arasında). "
         "Örtük önyargı cinsel yönelimde %65, ırkta %26, ten renginde %25 azaldı; yaş, engellilik ve kiloya yönelik örtük "
         "önyargıda ise uzun dönemde neredeyse hiç değişim olmadı (Charlesworth ve Banaji 2022).",
         "Obez çocuğa yönelik önyargı kendiliğinden azalmıyor; klinikte kullanılan dil de tedavinin parçası."),
        ("Ergen obezitesinde ilaç",
         "Obezitesi olan 201 ergende haftalık semaglutid, 68. haftada beden kitle indeksini %16,1 azalttı (plasebo +%0,6); "
         "semaglutid grubunun %73’ü en az %5 kilo verdi (plaseboda %18) (Weghuber ve ark. 2022).",
         "Biyolojik tedavinin etkisi “iradesizlik” anlatısını zayıflatıyor; ilaç kararı yeme davranışı ve beden imgesi "
         "değerlendirmesiyle birlikte verilmeli."),
    ],
}

# Kaynakçaya eklenecek künyeler (PubMed, 13 Kasım 2026)
EK_KAYNAKLAR = [
    "- Arnett AB, Antúnez M, Zeanah C, Fox NA, Nelson CA. Physical and neurophysiological maturation associated with ADHD among previously institutionalized children: a randomized controlled trial. J Child Psychol Psychiatry. 2025;66(7):967–979. [doi:10.1111/jcpp.14110](https://doi.org/10.1111/jcpp.14110)",
    "- Brushe ME, Haag DG, Melhuish EC, Reilly S, Gregory T. Screen Time and Parent-Child Talk When Children Are Aged 12 to 36 Months. JAMA Pediatr. 2024;178(4):369–375. [doi:10.1001/jamapediatrics.2023.6790](https://doi.org/10.1001/jamapediatrics.2023.6790)",
    "- Charlesworth TES, Banaji MR. Patterns of Implicit and Explicit Attitudes: IV. Change and Stability From 2007 to 2020. Psychol Sci. 2022;33(9):1347–1371. [doi:10.1177/09567976221084257](https://doi.org/10.1177/09567976221084257)",
    "- Cipriano C, Strambler MJ, Naples LH, Ha C, Kirk M, Wood M, ve ark. The state of evidence for social and emotional learning: A contemporary meta-analysis of universal school-based SEL interventions. Child Dev. 2023;94(5):1181–1204. [doi:10.1111/cdev.13968](https://doi.org/10.1111/cdev.13968)",
    "- Grotzinger AD, Werme J, Peyrot WJ, Frei O, de Leeuw C, Bicks LK, ve ark. Mapping the genetic landscape across 14 psychiatric disorders. Nature. 2026;649(8096):406–415. [doi:10.1038/s41586-025-09820-3](https://doi.org/10.1038/s41586-025-09820-3)",
    "- Harris JL, Swanson B, Petersen IT. A Developmentally Informed Systematic Review and Meta-Analysis of the Strength of General Psychopathology in Childhood and Adolescence. Clin Child Fam Psychol Rev. 2024;27(1):130–164. [doi:10.1007/s10567-023-00464-1](https://doi.org/10.1007/s10567-023-00464-1)",
    "- Heilmann A, Mehay A, Watt RG, Kelly Y, Durrant JE, van Turnhout J, ve ark. Physical punishment and child outcomes: a narrative review of prospective studies. Lancet. 2021;398(10297):355–364. [doi:10.1016/S0140-6736(21)00582-1](https://doi.org/10.1016/S0140-6736(21)00582-1)",
    "- Janik A, Qiu X, Lane R, Popova V, Drevets WC, Canuso CM, ve ark. Esketamine Monotherapy in Adults With Treatment-Resistant Depression: A Randomized Clinical Trial. JAMA Psychiatry. 2025;82(9):877–887. [doi:10.1001/jamapsychiatry.2025.1317](https://doi.org/10.1001/jamapsychiatry.2025.1317)",
    "- Keefe RSE, Harvey PD, Correll CU, Falkai P, Hashimoto N, Klein H, ve ark. Efficacy and safety of iclepertin for cognitive impairment associated with schizophrenia (CONNEX programme): results from three phase 3 randomised controlled trials. Lancet Psychiatry. 2025;12(12):906–920. [doi:10.1016/S2215-0366(25)00296-2](https://doi.org/10.1016/S2215-0366(25)00296-2)",
    "- Kieling C, Buchweitz C, Caye A, Silvani J, Ameis SH, Brunoni AR, ve ark. Worldwide Prevalence and Disability From Mental Disorders Across Childhood and Adolescence: Evidence From the Global Burden of Disease Study. JAMA Psychiatry. 2024;81(4):347–356. [doi:10.1001/jamapsychiatry.2023.5051](https://doi.org/10.1001/jamapsychiatry.2023.5051)",
    "- Lurie LA, Gruhn MA, Garrisi K, McLaughlin KA, Humphreys KL, Zeanah CH, ve ark. Caregiving Quality and Adolescent Cortical Structure: A 16-Year Longitudinal Study of Institutionally Reared Youth. Dev Sci. 2025;28(5):e70043. [doi:10.1111/desc.70043](https://doi.org/10.1111/desc.70043)",
    "- Madigan S, Deneault AA, Racine N, Park J, Thiemann R, Zhu J, ve ark. Adverse childhood experiences: a meta-analysis of prevalence and moderators among half a million adults in 206 studies. World Psychiatry. 2023;22(3):463–471. [doi:10.1002/wps.21122](https://doi.org/10.1002/wps.21122)",
    "- McDonald AJ, Kurdyak P, Rehm J, Roerecke M, Bondy SJ. Age-dependent association of cannabis use with risk of psychotic disorder. Psychol Med. 2024;54(11):2926–2936. [doi:10.1017/S0033291724000990](https://doi.org/10.1017/S0033291724000990)",
    "- Nagata JM, Otmar CD, Shim J, Balasubramanian P, Cheng CM, Li EJ, ve ark. Social Media Use and Depressive Symptoms During Early Adolescence. JAMA Netw Open. 2025;8(5):e2511704. [doi:10.1001/jamanetworkopen.2025.11704](https://doi.org/10.1001/jamanetworkopen.2025.11704)",
    "- Noetel M, Sanders T, Gallardo-Gómez D, Taylor P, Del Pozo Cruz B, van den Hoek D, ve ark. Effect of exercise for depression: systematic review and network meta-analysis of randomised controlled trials. BMJ. 2024;384:e075847. [doi:10.1136/bmj-2023-075847](https://doi.org/10.1136/bmj-2023-075847)",
    "- Sandbank M, Pustejovsky JE, Bottema-Beutel K, Caldwell N, Feldman JI, Crowley LaPoint S, ve ark. Determining Associations Between Intervention Amount and Outcomes for Young Autistic Children: A Meta-Analysis. JAMA Pediatr. 2024;178(8):763–773. [doi:10.1001/jamapediatrics.2024.1832](https://doi.org/10.1001/jamapediatrics.2024.1832)",
    "- Shaw KA, Williams S, Patrick ME, Valencia-Prado M, Durkin MS, Howerton EM, ve ark. Prevalence and Early Identification of Autism Spectrum Disorder Among Children Aged 4 and 8 Years - Autism and Developmental Disabilities Monitoring Network, 16 Sites, United States, 2022. MMWR Surveill Summ. 2025;74(2):1–22. [doi:10.15585/mmwr.ss7402a1](https://doi.org/10.15585/mmwr.ss7402a1)",
    "- Weghuber D, Barrett T, Barrientos-Pérez M, Gies I, Hesse D, Jeppesen OK, ve ark. Once-Weekly Semaglutide in Adolescents with Obesity. N Engl J Med. 2022;387(24):2245–2257. [doi:10.1056/NEJMoa2208601](https://doi.org/10.1056/NEJMoa2208601)",
    "- Xiao Y, Meng Y, Brown TT, Keyes KM, Mann JJ. Addictive Screen Use Trajectories and Suicidal Behaviors, Suicidal Ideation, and Mental Health in US Youths. JAMA. 2025;334(3):219–228. [doi:10.1001/jama.2025.7829](https://doi.org/10.1001/jama.2025.7829)",
]

# Vaka soruları: oturum → [(soru, [seçenekler], doğru seçenek sırası, açıklama, ilgili bölüm)]
SORULAR = {
    "oturum-1": [
        ("Kesme puanı 70 olan bir ölçekte Ali 68, Ayşe 71, Zeynep 96 puan aldı. Kategorik düşünmenin “yakın farkı "
         "abartma” hatası hangisidir?",
         ["Ayşe ile Zeynep’in aynı etiketi alması", "Ali ile Ayşe arasındaki 3 puanın “sağlıklı” ve “hasta” diye iki ayrı "
          "dünyaya bölünmesi", "Eşik değiştiğinde yaygınlığın değişmesi", "Zeynep’in puanının ölçüm hatası sayılması"],
         1, "Üç hata: yakın farkı abartmak (Ali–Ayşe), büyük farkı görmemek (Ayşe–Zeynep), büyük resmi kaçırmak. Eşik bir "
         "karar noktasıdır, doğa yasası değil (Şekil 2).", "fikirler"),
        ("Ağustos doğumlu, sınıfın en küçüğü olan 6 yaşındaki bir çocuk “yerinde duramıyor” yakınmasıyla getirildi. "
         "Notlara göre ilk akılda tutulacak bulgu hangisi?",
         ["Ağustos doğumlularda astım ve diyabet de daha sık tanılanır", "Ağustos doğumlularda DEHB tanısı Eylül "
          "doğumlulardan daha sıktır; olgunlaşmamışlık bozukluk sanılabilir", "Doğum ayı tanı sıklığını etkilemez",
          "Göreli yaş etkisi yalnızca ergenlikte görülür"],
         1, "407.846 çocukta DEHB tanısı Ağustos doğumlularda 10.000’de 85,1, Eylül doğumlularda 63,6; astım, diyabet ve "
         "obezitede fark yok (Layton ve ark. 2018). Tanıdan önce doğum ayını sor.", "crs"),
        ("Küresel Hastalık Yükü 2019 verilerine göre 5–24 yaşta ruhsal bozukluk sıklığı en yüksek hangi yaş dilimindedir?",
         ["5–9 yaş", "10–14 yaş", "15–19 yaş", "Bütün dilimlerde aynıdır"],
         2, "5–9 yaşta %6,8, 10–14’te %12,4, 15–19’da %14,0, 20–24’te %13,6 (Kieling ve ark. 2024).", "guncel"),
    ],
    "oturum-2": [
        ("Bir anne “DEHB’nin kalıtsallığı %74 ise ilaç da terapi de boşuna” diyor. En doğru yanıt hangisi?",
         ["Haklı; kalıtsallık yüksekse çevrenin etkisi yoktur", "Kalıtsallık bir nüfusun, bir yerin ve bir zamanın "
          "fotoğrafıdır; yüksek kalıtsallık “değişmez” demek değildir", "Kalıtsallık, çocuğun sorununun yüzde kaçının "
          "genetik olduğunu söyler", "Tedavi, ticari DEHB gen paneline göre seçilmelidir"],
         1, "Beş ana fikir 2: kalıtsallık bir fotoğraftır, kader değil. “DEHB geni” yoktur; ticari panel tanı koydurmaz.",
         "fikirler"),
        ("Açıklanamayan gelişimsel gecikmesi, zihinsel yetersizliği ve otizmi olan çocukta notlara göre tanı verimi en "
         "yüksek genetik tetkik hangisidir?",
         ["Ticari risk paneli", "Mikrodizin", "Ekzom dizileme", "Poligenik risk skoru"],
         2, "Ekzom dizilemenin tanı verimi yaklaşık %36, mikrodizininki %15–20 (Srivastava ve ark. 2019). Sonuç izlemi ve "
         "aile danışmanlığını değiştirir.", "crs"),
        ("14 psikiyatrik bozukluğu birlikte inceleyen 2026 tarihli genom çalışmasının ana bulgusu hangisidir?",
         ["Her bozukluğun kendine özgü, ayrı bir genetik mimarisi vardır", "Beş ortak genomik etken genetik varyansın "
          "ortalama yaklaşık üçte ikisini açıkladı", "Tek bir “psikiyatri geni” bulundu",
          "Çocukluk başlangıçlı bozukluklar erişkin bozukluklarıyla genetik olarak örtüşmez"],
         1, "Beş etken ortalama %66’yı açıkladı, 238 pleiotropik lokus; iki etkende bozukluğa özgü lokus çok az "
         "(Grotzinger ve ark. 2026).", "guncel"),
    ],
    "oturum-3": [
        ("Maymunlar videodaki yılandan korkmayı öğrendi, çiçekten korkmayı öğrenmedi. Bu bulgu hangi ilkeyi gösterir?",
         ["Korku tümüyle doğuştandır", "Beyin bazı derslere hazırdır", "Etoloji yalnız laboratuvar verisine dayanır",
          "Her korku eşit kolaylıkla öğrenilir"],
         1, "Beş ana fikir 4: öğrenmenin biyolojik bir hazırlığı vardır; küçük çocuklar da yılanı çiçekten hızlı bulur.",
         "fikirler"),
        ("Bükreş Erken Müdahale Projesi’nde koruyucu aileye yerleşmenin bağlanmaya yararı en çok hangi koşulda belirgindi?",
         ["24 aydan önce yerleşenlerde", "Yerleşme yaşının önemi yoktu", "Yalnızca 6 yaşından sonra yerleşenlerde",
          "Yarar ergenlikte tümüyle kayboldu"],
         0, "24 aydan önce yerleşenlerde güvenli bağlanma daha sık (Smyke ve ark. 2010); kazanç 16–18 yaşta sürüyor (King ve ark. 2023). "
         "Gecikme, doz kaybıdır.", "crs"),
        ("Bükreş’in 16. yıl verisinde koruyucu aileye kurayla yerleşmenin ergen korteksine etkisinde ne aracılık etti?",
         ["Ailenin gelir düzeyi", "Bakımın niteliği", "Çocuğun IQ’su", "Okul türü"],
         1, "Bakımın niteliği aracı oldu; en erken bakım deneyimleri korteks kalınlığıyla ayrıca ilişkiliydi (Lurie ve ark. "
         "2025).", "guncel"),
    ],
    "oturum-4": [
        ("Parkinson ilacı psikoz, antipsikotik parkinsonizm yapabiliyor. Bunu en iyi hangi ilke açıklar?",
         ["Dopamin yalnızca hareketi düzenler", "Aynı molekül, farklı devre", "Antipsikotikler dopamin sentezini artırır",
          "Levodopa serotonini azaltır"],
         1, "Beş ana fikir 1: dopamin dört ayrı yolda dört ayrı iş yapar (Şekil 12).", "fikirler"),
        ("Ebeveyn desteği 9–10 yaşındaki çocukta kortizol yanıtını ortadan kaldırırken 15–16 yaşında etkisizdi. Klinik "
         "çıkarım hangisidir?",
         ["Ergenlerde stres yanıtı yoktur", "Çocukta ebeveyni odaya al; ergende tampon akrana ve terapötik ilişkiye kayar",
          "Ergenlikte ebeveyn görüşmeden tümüyle çıkarılmalıdır", "Kortizol yanıtı yaşla azalır, ergen daha dayanıklıdır"],
         1, "Ebeveyn tamponu yaşla değişir (Hostinar ve ark. 2015).", "crs"),
        ("546.458 erişkini kapsayan meta-analizde dört ya da daha fazla olumsuz çocukluk yaşantısı bildirenlerin oranı "
         "yaklaşık kaçtır?",
         ["%4", "%16", "%40", "%60"],
         1, "%16,1; hiç bildirmeyenler %39,9, yani yaklaşık %60’ı en az bir yaşantı bildiriyor (Madigan ve ark. 2023).",
         "guncel"),
    ],
    "oturum-5": [
        ("Maymunlara ödülü farklı olasılıklarla haber veren ipuçları öğretildi. Bekleme sırasındaki dopamin etkinliği hangi "
         "olasılıkta en yüksekti?",
         ["%0", "%25", "%50", "%100"],
         2, "Belirsizlik en yüksekken, yani %50’de (Fiorillo ve ark. 2003). Kumar makinesi ve bildirim aynı eğriyi kullanır.",
         "fikirler"),
        ("Kaygı bozukluğu olan 7–17 yaş çocuk ve ergenlerde (CAMS) 12. haftada en yüksek yanıt hangisindeydi?",
         ["Sertralin tek başına", "BDT tek başına", "Sertralin ile BDT birlikte", "Plasebo"],
         2, "Birlikte %80,7; BDT %59,7; sertralin %54,9; plasebo %23,7 (Walkup ve ark. 2008).", "crs"),
        ("ABCD verisinde aşağıdakilerden hangisi intihar davranışıyla ilişkiliydi?",
         ["Başlangıçtaki toplam ekran süresi", "Sosyal medya ya da telefonda artan bağımlı kullanım örüntüsü",
          "Video oyunu oynamamak", "Hiçbiri"],
         1, "Artan bağımlı sosyal medya kullanımında risk oranı 2,14; toplam ekran süresi ilişkili değildi (Xiao ve ark. "
         "2025).", "guncel"),
    ],
    "oturum-6": [
        ("16 yaşında bir genç “Biliyordum ama o an duramadım” diyor. Notlara göre bunu en iyi açıklayan ilke hangisidir?",
         ["Ergen kuralı bilmez", "Bilmek, durabilmek değildir; yoğun uyarılmada denge amigdaladan yana kayar",
          "Saldırganlık yalnızca düşük serotoninle açıklanır", "Ergen beyni erişkin beyninden farksızdır"],
         1, "Beş ana fikir 3; bilişsel kapasite yaklaşık 16 yaşta, psikososyal olgunluk 18’den sonra (Icenogle ve ark. "
         "2019).", "fikirler"),
        ("Davranım bozukluğu olan çocukta duygusuz–acımasız özellikler neden ayrıca sorulmalıdır?",
         ["Tanı ölçütlerinden çıkarıldığı için", "Davranım sorunları içinde ayrı bir alt grubu tanımladığı için",
          "Yalnızca kızlarda görüldüğü için", "İlaç seçimini doğrudan belirlediği için"],
         1, "Duygusuz–acımasız özellikler ayrı bir alt grubu tanımlar (Frick ve ark. 2014).", "crs"),
        ("69 ileriye dönük çalışmanın derlemesine göre fiziksel ceza için hangisi doğrudur?",
         ["Kısa vadede davranışı düzeltir", "Davranış sorunlarındaki artışı tutarlı biçimde yordar ve hiçbir olumlu sonuçla "
          "ilişkili değildir", "Yalnızca dışa yönelim sorunu olan çocuklarda zararlıdır",
          "Etkisi ebeveyn özelliklerine göre tümüyle değişir"],
         1, "İlişkiler çocuk ve ebeveyn özelliklerine göre değişmeden tutarlıydı (Heilmann ve ark. 2021).", "guncel"),
    ],
    "oturum-7": [
        ("Okula başlayan çocuklarda gelişimsel dil bozukluğunun sıklığı yaklaşık kaçtır?",
         ["%0,7", "%2", "%7,6", "%15"],
         2, "%7,58, bilinen bir tıbbi neden olmadan (Norbury ve ark. 2016). Davranış ve okuma sorununda önce dili "
         "değerlendir.", "crs"),
        ("Ani başlayan, karmaşık ve gösterişli tikleri olan 15 yaşında bir kız. Notlara göre hangi öykü özellikle alınmalı?",
         ["Streptokok enfeksiyonu", "Sosyal medya öyküsü", "Kafa travması", "Kafein tüketimi"],
         1, "“TikTok tikleri”nde kol hareketleri ve koprolali baskın; tablo işlevsel tiklerle uyumlu (Olvera ve ark. 2021).",
         "crs"),
        ("Otizmli küçük çocuklarda 144 çalışmalık meta-analiz, müdahale miktarı hakkında ne buldu?",
         ["Saat arttıkça etki doğrusal olarak artıyor", "Miktar ile etki arasında anlamlı pozitif ilişki yok",
          "Yalnızca çok yoğun programlar etkili", "Miktar arttıkça etki azalıyor"],
         1, "Hiçbir miktar ölçüsü etkiyle anlamlı pozitif ilişki göstermedi (Sandbank ve ark. 2024).", "guncel"),
    ],
    "oturum-8": [
        ("11 yaşında bir çocuk zaman zaman adının seslenildiğini duyduğunu söylüyor; işlevi korunmuş. En doğru yaklaşım hangisi?",
         ["Şizofreni tanısı koyup antipsikotik başlamak", "Belirti bu yaşta sık; işleve ve eşlik eden belirtilere bakmak",
          "Belirtiyi tümüyle göz ardı etmek", "Önlemek için düşük doz antipsikotik başlamak"],
         1, "Psikotik belirti 9–12 yaşta %17 (Kelleher ve ark. 2012); belirti sık, bozukluk nadir.", "crs"),
        ("Klinik yüksek riskteki gençlerde psikoza geçiş 3 yılda yaklaşık kaçtır?",
         ["%5", "%25", "%50", "%75"],
         1, "1 yılda %15, 2 yılda %19, 3 yılda %25 (Salazar de Pablo ve ark. 2021). Çoğu geçiş yapmaz.", "crs"),
        ("Ontario kohortunda kenevir kullanımı ile psikotik bozukluk arasındaki ilişki nasıldı?",
         ["Her yaşta aynı güçte", "Ergenlikte güçlü, genç erişkinlikte anlamlı değil", "Yalnızca genç erişkinlikte anlamlı",
          "İlişki yok"],
         1, "Ergenlikte düzeltilmiş HR 11,2; genç erişkinlikte 1,3 (McDonald ve ark. 2024).", "guncel"),
    ],
    "ek-9": [
        ("Hakikat ve Uzlaşma Komisyonlarında uzlaşma için şart olan neydi?",
         ["Özür dilemek", "Her şeyi anlatmak ve bir daha yapmayacağına ikna etmek", "Maddi tazminat", "Cezanın infazı"],
         1, "Beş ana fikir 2: uzlaşma bağışlama değildir.", "fikirler"),
        ("Erken başlangıçlı davranış sorunu olan 891 çocukta 10 yıllık çok bileşenli program 25 yaşta ne sağladı?",
         ["Hiçbir etki", "Herhangi bir psikiyatrik sorun %69 yerine %59", "Psikiyatrik sorun %20’ye indi",
          "Yalnızca akademik başarı arttı"],
         1, "Tedavi için gereken sayı 8; şiddet ve madde suçu mahkûmiyetleri daha az (Dodge ve ark. 2015).", "crs"),
        ("424 çalışmalık meta-analize göre okul temelli sosyal-duygusal öğrenme programları için hangisi doğrudur?",
         ["Yalnızca akademik başarıyı artırdı", "Beceri, davranış, okul iklimi ve akademik başarıyı iyileştirdi; etki "
          "uygulama niteliğine göre değişti", "Davranışı kötüleştirdi", "Yalnızca bir ülkede çalışıldı"],
         1, "53 ülke, 575.361 öğrenci (Cipriano ve ark. 2023).", "guncel"),
    ],
    "ek-10": [
        ("Sapolsky’nin “dört haberci, dört belirti” şemasında anhedoni hangi haberciyle eşleşir?",
         ["Serotonin", "Noradrenalin", "Dopamin", "Glutamat"],
         2, "Serotonin ruminasyon, noradrenalin psikomotor yavaşlama, dopamin anhedoni (Şekil 26).", "fikirler"),
        ("Ani ebeveyn kaybı yaşayan gençlerde yeni depresyon en çok hangi grupta görüldü?",
         ["12 yaş ve altında kayıp yaşayanlarda", "18 yaşından sonra kayıp yaşayanlarda", "Kayıptan beş yıl sonra",
          "Gruplar arasında fark yoktu"],
         0, "Tepe ilk iki yıl; yeni depresyon en çok 12 yaş ve altında kayıp yaşayanlarda (Pham ve ark. 2018).", "crs"),
        ("Egzersiz ve depresyon ağ meta-analizinde hangisi doğrudur?",
         ["Egzersizin etkisi yok", "Yürüyüş/koşu, yoga ve kuvvet antrenmanı orta düzeyde etkili; etki yoğunlukla artıyor",
          "Yalnızca yoga etkili", "Etki yoğunluktan bağımsız"],
         1, "Kanıtın güveni ise düşük ya da çok düşük (Noetel ve ark. 2024).", "guncel"),
    ],
    "ek-11": [
        ("Denetim duygusunu yitiren insanlar rastgele veride ne yapma eğilimindedir?",
         ["Daha az örüntü görür", "Daha çok örüntü görür", "Karar vermeyi bırakır", "Hiçbir değişiklik olmaz"],
         1, "Belirsizlik örüntü aratır (Whitson ve Galinsky 2008).", "fikirler"),
        ("Ağır, erken başlangıçlı obezitesi olan bir çocuk “iradesiz” diye etiketleniyor. Hangi bulgu bu etiketi zayıflatır?",
         ["Obez çocukların yarısında tek gen mutasyonu var", "Ağır çocukluk obezitesi olan 500 çocuğun %5,8’inde MC4R "
          "mutasyonu", "Obezite tümüyle çevreseldir", "Örtük önyargı ortadan kalktı"],
         1, "Farooqi ve ark. 2003; erken başlangıçlı ağır obezitede genetik değerlendirmeyi akılda tut.", "crs"),
        ("Project Implicit’in 2007–2020 verisinde hangi örtük önyargıda uzun dönemli değişim neredeyse yoktu?",
         ["Cinsel yönelim", "Irk", "Kilo", "Ten rengi"],
         2, "Yaş, engellilik ve kiloya yönelik örtük önyargıda değişim neredeyse yoktu (Charlesworth ve Banaji 2022).",
         "guncel"),
    ],
}

# Simülasyonlar: oturum → [anahtar]
SIMULASYONLAR = {
    "oturum-1": ["esik", "kisasa"],
    "oturum-2": ["kalitsallik"],
    "oturum-3": ["hamilton"],
    "oturum-5": ["dopamin"],
}
