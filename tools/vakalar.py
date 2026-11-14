"""Davranışın Biyolojisi: dallanan vaka simülasyonları (Kasım 2026).

Notlardaki üç mini vakanın karar ağacına çevrilmiş hâli. Her vaka bir sahneler grafiğidir.
Karar sahnesi: {"metin", "secenekler": [(seçenek, sonraki sahne, puan, geri bildirim)]}.
Son sahnesi: {"son": "iyi" | "orta" | "kotu", "baslik", "metin"}.
Puan: 2 en uygun, 1 kabul edilebilir, 0 zayıf, -1 zarar verebilir.
Vakalar kurgusaldır. Sayılar ve atıflar notların kendi içeriğinden alınmıştır; atıflar kaynakçadaki künyelere bağlanır.
"""

PUAN_ETIKET = {2: "En uygun", 1: "Kabul edilebilir", 0: "Zayıf", -1: "Zarar verebilir"}

VAKALAR = [
    # ------------------------------------------------------------------ Defne
    dict(
        id="defne",
        baslik="Defne, 15 yaş: “Ergenlik bunalımı mı?”",
        ozet="İki haftadır uyumayan, “Herkes beni izliyor” diyen bir ergen acilde. Hangi kovayı önce açarsınız, hangi tetkiki "
             "istersiniz, aileye ne söylersiniz?",
        oturumlar=[("oturum-1", "Oturum 1")],
        mini="oturum-1",
        baslangic="acil",
        sahneler={
            "acil": dict(
                metin="Defne 15 yaşında. İki haftadır uyumuyor, huzursuz ve “Herkes beni izliyor” diyor. Bir hafta önce grip benzeri "
                      "bir hastalık geçirmiş. Acilde bilinci dalgalı; ağız çevresinde istemsiz hareketler var ve bir kez nöbet "
                      "benzeri bir epizot tarif ediliyor. Öğretmeni “Sosyal medyadan etkilendi” demiş. Acil hekimi sizi “ilk "
                      "psikotik atak” ön tanısıyla çağırıyor.",
                secenekler=[
                    ("Önce organik nedenleri aramak: ayrıntılı öykü ve nörolojik muayene yapmak, çocuk nörolojisini bugün çağırmak",
                     "tetkik", 2,
                     "Akut başlangıç, öncesinde viral benzeri tablo, dalgalı bilinç, ağız çevresi diskinezileri ve nöbet ensefaliti "
                     "düşündürür. Anti-NMDAR ensefalitinde 100 hastanın tamamı psikiyatrik ya da bellek belirtisiyle başvurdu "
                     "(Dalmau ve ark. 2008); tablo çocuk ve ergenlerde de tanımlıdır (Florance ve ark. 2009)."),
                    ("İdrarda madde taraması isteyip sonucu beklemek", "tetkik", 1,
                     "Madde taraması gerekli bir adımdır, ama tek başına yetmez. Dalgalı bilinç ve nöbet, sonucu beklemeden "
                     "nörolojik değerlendirmeyi gerektirir."),
                    ("“İlk psikotik atak” tanısıyla antipsikotik başlayıp psikiyatri servisine yatırmak", "antipsikotik", 0,
                     "“Psikoz” etiketi aramayı bitirmez: etiket bir karar noktasıdır, açıklama değil. Odak nörolojik bulgular "
                     "varken tek kovaya kilitlenmek tanıyı geciktirir."),
                    ("Aileye ekran kısıtlaması önerip haftaya ayaktan kontrole çağırmak", "son-ev", -1,
                     "Bilinci dalgalanan ve nöbet tarif edilen bir ergen eve gönderilmez. “Ergen” kategorisi, kategori içindeki "
                     "büyük farkı gizliyor."),
                ]),
            "antipsikotik": dict(
                metin="Defne psikiyatri servisine yatırıldı ve antipsikotik başlandı. İki gün sonra kaslarında sertlik var, "
                      "bilinci daha da dalgalanıyor ve hemşire ikinci bir nöbet benzeri epizot bildiriyor. Uyku düzelmedi.",
                secenekler=[
                    ("Tanıyı yeniden açmak: ilacı gözden geçirmek ve çocuk nörolojisiyle birlikte BOS, EEG, MR ve antikor "
                     "tetkiklerini istemek", "aile", 2,
                     "Tedaviye beklenen yanıt gelmiyor ve yeni nörolojik bulgular ekleniyor. Hipotezi değiştirmek için en doğru "
                     "an budur; iki gün kaybedildi, ama fırsat hâlâ var."),
                    ("Antipsikotik dozunu artırmak", "son-gecikme", -1,
                     "Aynı kovaya daha derin dalmak, yanlış hipotezi düzeltmez. Kötüleşen bilinç ve yineleyen nöbet artık "
                     "görmezden gelinemez."),
                    ("Sertlik için bir ilaç ekleyip birkaç gün daha izlemek", "son-gecikme", 0,
                     "Belirtiyi tedavi etmek nedeni aramanın yerini tutmaz. Her bekleme günü, tedavinin başlangıcını geciktirir."),
                ]),
            "tetkik": dict(
                metin="Çocuk nörolojisi Defne’yi sizinle birlikte değerlendirdi. Ateşi yok, ense sertliği yok; ama bilinç "
                      "dalgalanması ve ağız çevresindeki hareketler sürüyor. Tetkik planı konuşuluyor.",
                secenekler=[
                    ("BOS incelemesi, EEG, beyin MR’ı, serumda ve BOS’ta antikor ve over görüntülemesi istemek", "aile", 2,
                     "Notlardaki tetkik listesi budur: BOS, EEG, MR, serum ve BOS antikorları, over görüntülemesi. Tek bir teste "
                     "dayanmamak, hipotezi birden çok bağımsız kaynakla sınamaktır."),
                    ("Yalnızca beyin MR’ı istemek; normal çıkarsa psikiyatriye devretmek", "mr-normal", 0,
                     "Tek bir normal sonuç, klinik tablonun düşündürdüğü hipotezi çürütmez. Arama, tablo açıklanana kadar sürer."),
                    ("Yalnızca serumda antikor isteyip sonucu ayaktan izlemek", "son-gecikme", -1,
                     "Dalgalı bilinç ve nöbet öyküsü olan bir ergenin tetkikleri ayaktan beklenmez; listenin yarısı da eksik kalır."),
                ]),
            "mr-normal": dict(
                metin="MR normal geldi. Nöbetçi ekip “Görüntüleme temiz, bu sizin hastanız” diyor. Defne hâlâ uyumuyor, konuşması "
                      "azaldı, ağız çevresindeki hareketler sürüyor.",
                secenekler=[
                    ("Klinik tablonun sürdüğünü belirtip EEG, BOS ve antikor tetkiklerinde ısrar etmek", "aile", 2,
                     "Grup olasılığı bireysel kanıtı ezemez: bu ergende akut başlangıç ve nörolojik bulgular var. Normal bir MR "
                     "bu tabloyu açıklamıyor."),
                    ("Psikiyatri servisine devralıp antipsikotik başlamak", "antipsikotik", 0,
                     "“Görüntüleme temiz” cümlesi aramayı bitirmek için yetmez. Açıklanmamış nörolojik bulgularla tek kovaya "
                     "dönülüyor."),
                ]),
            "aile": dict(
                metin="Tetkikler alındı, sonuçlar bekleniyor. Defne’nin annesi koridorda sizi durduruyor: “Kızım delirdi mi? "
                      "Sosyal medya mı yaptı bunu? Bizim hatamız mı?”",
                secenekler=[
                    ("“Henüz bilmiyoruz; şu tetkiklerle öğreneceğiz. Bulgular beyni etkileyen bir hastalığı düşündürüyor. Sonuçları "
                     "beklerken Defne’yi yakından izleyeceğiz ve öğrendiğimiz her şeyi sizinle paylaşacağız.”", "sonuc", 2,
                     "Belirsizliği dürüstçe söylemek ve planı anlatmak aileyi hem bilgilendirir hem suçluluktan uzak tutar. "
                     "“Henüz bilmiyoruz; şu tetkiklerle öğreneceğiz” cümlesi notların önerdiği yanıttır."),
                    ("“Büyük olasılıkla şizofreni başlangıcı; uzun bir tedaviye hazırlanın.”", "sonuc", -1,
                     "Sonuçlar gelmeden konan bir etiket aileye gereksiz bir yük bindirir ve yanlış çıkarsa güveni zedeler."),
                    ("“Merak etmeyin, ergenlikte olur böyle şeyler.”", "sonuc", 0,
                     "Güvence vermek rahatlatıcı görünür, ama elinizdeki bulgularla bağdaşmıyor. Aile ciddiyeti başkasından "
                     "öğrenirse size güvenmekte zorlanır."),
                ]),
            "sonuc": dict(
                metin="BOS’ta NMDA reseptörüne karşı antikor saptandı; EEG’de yaygın yavaşlama var. Over görüntülemesi planlandı. "
                      "Ekip toplantısında bir meslektaşınız “Önce psikiyatrik belirtileri yatıştıralım, immünoterapiye sonra bakarız” "
                      "diyor.",
                secenekler=[
                    ("İlk basamak immünoterapinin geciktirilmeden başlanmasını desteklemek, tümör taramasını tamamlamak ve "
                     "psikiyatrik belirtileri ekiple birlikte izlemek", "son-iyi", 2,
                     "577 hastalık seride (211’i çocuk) ilk basamak tedavi alanların %53’ü dört haftada düzeldi; 24. ayda "
                     "izlenenlerin %81’i iyi sonuca ulaştı ve erken tedavi iyi sonucu yordadı (Titulaer ve ark. 2013)."),
                    ("Psikiyatrik belirtiler yatışana kadar immünoterapiyi ertelemek", "son-orta", -1,
                     "Psikiyatrik belirtiler hastalığın kendisidir; nedeni tedavi etmeden yatışmasını beklemek tedaviyi geciktirir. "
                     "Erken tedavi iyi sonucu yordar (Titulaer ve ark. 2013)."),
                    ("Hastayı nörolojiye devredip psikiyatri izlemini sonlandırmak", "son-orta", 0,
                     "Tanı nörolojik olsa da belirtilerin çoğu psikiyatriktir. Aile ve ekip, iyileşme sürecinde de psikiyatrinin "
                     "desteğine ihtiyaç duyar."),
                ]),
            "son-iyi": dict(son="iyi", baslik="Kova değil, merdiven",
                            metin="İmmünoterapi başlandı, tümör taraması tamamlandı. Defne dördüncü haftada uyumaya ve ailesini "
                                  "tanımaya başladı; psikiyatri ekibi iyileşme boyunca aileyle çalışmayı sürdürdü. Doğru soruyu "
                                  "ilk gün sormak, tedaviyi haftalarca öne aldı."),
            "son-orta": dict(son="orta", baslik="Tanı doğru, tedavi gecikmeli",
                             metin="Tanı kondu, ama tedavinin başlaması ya da izlemin sürekliliği aksadı. Defne düzeldi; yine de "
                                   "yatış uzadı ve aile bir süre kiminle konuşacağını bilemedi. Erken tedavi iyi sonucu yordar "
                                   "(Titulaer ve ark. 2013)."),
            "son-gecikme": dict(son="kotu", baslik="Günler kaybedildi",
                                metin="Defne’nin bilinci kötüleşti ve yoğun bakıma alındı. Ensefalit tanısı orada, günler sonra "
                                      "kondu. Tek kovaya kilitlenmek, gözünüzün önündeki nörolojik bulguları görünmez kıldı."),
            "son-ev": dict(son="kotu", baslik="Eve gönderilen ensefalit",
                           metin="Defne o gece evde nöbet geçirdi ve ambulansla geri geldi. Aile, ilk başvuruda ciddiye "
                                 "alınmadıklarını düşünüyor. “Ergenlik” etiketi, akut başlangıcı ve nöbet öyküsünü gölgede bıraktı."),
        },
    ),
    # ------------------------------------------------------------------ Baran
    dict(
        id="baran",
        baslik="Baran, 14 yaş: “Biliyordum ama o an duramadım”",
        ozet="Bir akranını yaralamaktan adli süreçte olan bir ergen için rapor isteniyor. Algılama ile yönlendirmeyi nasıl "
             "ayırırsınız, ergen beyni savunmasına ne dersiniz?",
        oturumlar=[("oturum-6", "Oturum 6"), ("ek-9", "Ek oturum 9")],
        mini="oturum-6",
        baslangic="istek",
        sahneler={
            "istek": dict(
                metin="Baran 14 yaşında. Okul çıkışındaki bir tartışmada bir akranını bıçakla yaralamaktan adli süreçte. Mahkeme "
                      "TCK 31/2 kapsamında değerlendirme istiyor. Görüşmeden önce avukatı arıyor: “Ergen beyni gelişmemiş, "
                      "sorumluluğu yok; raporunuza bunu yazarsınız.”",
                secenekler=[
                    ("Değerlendirmeyi iki başlıkta planlamak: fiilin anlamını ve sonuçlarını kavrama (algılama) ve o anki "
                     "davranışı denetleyebilme (yönlendirme). Baran’la, ailesiyle görüşmek; okul ve dosya bilgisini istemek",
                     "gorusme", 2,
                     "“Bilmek, durabilmek değildir” ayrımının hukuktaki karşılığı bu iki başlıktır. Rapor, birden çok kaynaktan "
                     "toplanan bireysel işlev kanıtına dayanır."),
                    ("Yalnızca bir zekâ testi isteyip sonuca göre karar vermek", "gorusme", 0,
                     "Zekâ düzeyi algılama için bir veridir, ama o anki davranışı denetleyebilmeyi tek başına göstermez."),
                    ("Avukatın görüşünü raporun sonucuna taşımak", "son-kotu", -1,
                     "Rapor, tarafların beklentisine göre yazılmaz. Genel bir “ergen beyni” savı, bu ergenin o anki kapasitesi "
                     "hakkında bir şey söylemez."),
                    ("DEHB tanısı olduğu için doğrudan “davranışlarını yönlendiremez” yazmak", "son-kotu", -1,
                     "Tanı tek başına hüküm kurmaz. Bulgu, öykü ve işlevle birlikte yazılır."),
                ]),
            "gorusme": dict(
                metin="Baran görüşmede sakin. Olayı soruyorsunuz: “Bıçak cebimdeydi. Suç olduğunu biliyordum ama o an duramadım.”",
                secenekler=[
                    ("Cümleyi iki soruya ayırmak ve olay anını adım adım sormak: tartışma ne kadar sürdü, kimler vardı, "
                     "öncesinde ne oldu, bıçağı ne zaman çıkardı, sonrasında ne yaptı?", "etkenler", 2,
                     "Günler süren bir kararı ergen beyni tartabilir; saniyelik bir öfkeyi durduramayabilir. Sapolsky’nin 2024’teki "
                     "sorusu da budur: “biliyor mu?” değil, “kaç saniyesi vardı?” (2024/26 [50:00])."),
                    ("“Biliyordum” dediği için algılama ve yönlendirmenin tam olduğunu yazmak", "etkenler", 0,
                     "Kuralı bilmek ile kurala uyabilmek ayrışabilir; yoğun uyarılmada denge değişir. Cümlenin ikinci yarısı "
                     "incelenmeden karar verilmiş olur."),
                    ("“Duramadım” dediği için yönlendirme yeteneğinin olmadığını yazmak", "etkenler", 0,
                     "Ergenin kendi ifadesi bir veridir, kanıtın tamamı değildir. Olay anının ayrıntıları ve öteki kaynaklar "
                     "olmadan bu sonuca varılamaz."),
                ]),
            "etkenler": dict(
                metin="Öyküde üç şey öne çıkıyor: Baran’ın DEHB tanısı var ve ilacını düzensiz kullanıyor; evde şiddete tanık "
                      "olmuş; olay sırasında arkadaşları çevresindeymiş ve onu kışkırtmışlar.",
                secenekler=[
                    ("Üçünü de yükseltici etken olarak tek tek belgelemek, hiçbirini tek başına neden saymamak ve düzensiz "
                     "tedaviyi değiştirilebilir bir risk olarak not etmek", "savunma", 2,
                     "Ergenler akranlar izlerken daha çok risk alır (Gardner ve Steinberg 2005; Chein ve ark. 2011). DEHB ilacı "
                     "kullanılan dönemlerde suç oranı erkeklerde %32 daha düşüktür (Lichtenstein ve ark. 2012). Bunlar riski "
                     "yükseltir, ama tek başına neden değildir."),
                    ("Raporun merkezine akran etkisini koymak: “Arkadaşları yaptırdı”", "savunma", 0,
                     "Tek kovaya dönülüyor. Akran etkisi gerçek bir yükselticidir, ama davranışı tek başına açıklamaz."),
                    ("Ev ortamını rapora almamak, çünkü “mazeret gibi durur”", "savunma", 0,
                     "Biyolojik ve çevresel açıklama ne mazerettir ne mahkûmiyet. Belgelenmeyen bir risk etkeni, önerilerde de "
                     "ele alınamaz."),
                ]),
            "savunma": dict(
                metin="Avukat bir makale gönderiyor: 11 ülkeden 5.227 kişide psikososyal olgunluğun 18 yaşından sonra da "
                      "geliştiğini gösteren çalışma. “Bilim de benim dediğimi söylüyor” diyor.",
                secenekler=[
                    ("Bulguların grup düzeyinde olduğunu, tek bir ergenin o anki kapasitesini göstermediğini açıklamak; raporu "
                     "Baran’a ilişkin bireysel işlev kanıtına dayandırmak", "oneri", 2,
                     "Gelişimsel bulgular gerçektir, ama grup düzeyindedir (Somerville 2016; Icenogle ve ark. 2019). Aynı "
                     "çalışmada bilişsel kapasite yaklaşık 16 yaşta erişkin düzeyine ulaşır. Ortalama, kimsenin adı değildir."),
                    ("Bilimsel bulgulara raporda hiç yer vermemek", "oneri", 1,
                     "Bireysel kanıta dayanmak doğrudur. Yine de gelişimsel çerçeveyi sınırlarıyla birlikte anmak, mahkemenin "
                     "bulguları doğru yorumlamasına yardım eder."),
                    ("Makaleyi rapora kanıt olarak ekleyip sonucu ona bağlamak", "son-orta", 0,
                     "Grup ortalaması bireyin yerine konmuş olur. Rapor itiraza açık hâle gelir, çünkü Baran hakkında bir şey "
                     "söylemez."),
                ]),
            "oneri": dict(
                metin="Değerlendirme tamamlandı. Raporun son bölümünü yazıyorsunuz.",
                secenekler=[
                    ("Kanaati iki başlıkta gerekçesiyle yazmak; ardından değiştirilebilir riskleri ve önerileri eklemek: düzenli "
                     "DEHB tedavisi, aileyle çalışma, okulla iş birliği ve izlem", "son-iyi", 2,
                     "Rapor yalnızca geçmişe bakmaz. Düzensiz DEHB tedavisi değiştirilebilir bir risk etkenidir "
                     "(Lichtenstein ve ark. 2012); DEHB tedavisi yalnız karne değil, güvenlik meselesidir."),
                    ("Yalnızca “vardır” ya da “yoktur” kanaatini yazıp raporu kapatmak", "son-orta", 1,
                     "Soru yanıtlanmış olur, ama Baran’ın yeniden zarar görmesini ya da vermesini önleyebilecek bilgi rapora "
                     "girmez."),
                ]),
            "son-iyi": dict(son="iyi", baslik="Bilmek ile durabilmek ayrı yazıldı",
                            metin="Rapor iki başlıkta, birden çok kaynağa dayanarak ve önerileriyle yazıldı. Mahkeme raporu "
                                  "yeterli buldu; Baran için tedavi ve izlem planı da başladı. Hukuki ayrıntılarda güncel "
                                  "mevzuat esas alınır (7593 sayılı Kanun 2026)."),
            "son-orta": dict(son="orta", baslik="Yanıt var, gerekçe eksik",
                             metin="Rapor bir kanaat bildiriyor, ama bireysel kanıt ya da öneriler eksik kaldı. Mahkeme ek "
                                   "açıklama istedi; Baran’ın tedavisi ise raporun konusu olmadığı için kimsenin gündemine "
                                   "girmedi."),
            "son-kotu": dict(son="kotu", baslik="Rapor geri döndü",
                             metin="Rapor tek bir etkene ya da genel bir sava dayandığı için itiraz edildi ve yeniden "
                                   "değerlendirme istendi. Süreç uzadı; Baran bu arada tedavisiz kaldı. Etiket bir karar "
                                   "noktasıdır, açıklama değil."),
        },
    ),
    # ------------------------------------------------------------------ Arda
    dict(
        id="arda",
        baslik="Arda, 15 yaş: “Bu esrarın işi, bırakınca geçer”",
        ozet="Altı aydır içine kapanan, iki haftadır sesler duyan ve her gün kenevir içen bir ergen. Beklemek mi, başlamak mı? "
             "Aileye ne söylersiniz, ilacı nasıl izlersiniz?",
        oturumlar=[("oturum-8", "Oturum 8")],
        mini="oturum-8",
        baslangic="basvuru",
        sahneler={
            "basvuru": dict(
                metin="Arda 15 yaşında. Son altı ayda içine kapanmış, notları düşmüş. İki haftadır sınıf arkadaşlarının "
                      "telefonla düşüncelerini okuduğunu söylüyor; geceleri kendisi hakkında yorum yapan sesler duyuyor. Bir "
                      "yıldır neredeyse her gün yüksek potensli kenevir içiyor. Babası kapıda söylüyor: “Bu esrarın işi, "
                      "bırakınca geçer.”",
                secenekler=[
                    ("Bugün kapsamlı bir değerlendirme yapmak: ruhsal durum ve risk, toksikoloji, nörolojik muayene; "
                     "gerekirse görüntüleme ve EEG", "baba", 2,
                     "İlk değerlendirmede madde ile tetiklenen psikoz, organik nedenler (ensefalit dahil) ve duygudurum "
                     "bozukluğu dışlanır. Sıralı ve eksiksiz bir başlangıç, sonraki bütün kararları kolaylaştırır."),
                    ("Tetkik istemeden antipsikotik yazıp eve göndermek", "baba", 0,
                     "Belirtiler tedavi gerektirebilir, ama organik nedenler ve risk değerlendirilmeden atılan adım eksiktir."),
                    ("Keneviri bırakmasını söyleyip bir ay sonra kontrole çağırmak", "son-gecikme", -1,
                     "Bırakmak tablonun geçeceğini garanti etmez. İki haftadır süren psikotik belirtilerle bir ay beklemek, "
                     "tedavisiz geçen süreyi uzatır."),
                ]),
            "baba": dict(
                metin="Toksikolojide kenevir pozitif; nörolojik muayene olağan. Babası ısrar ediyor: “Dedim size. Bıraksın, "
                      "bir ay bekleyelim, kendiliğinden düzelir.”",
                secenekler=[
                    ("“Günlük ve yüksek potensli kullanım riski belirgin artırıyor; bırakması tedavinin hedeflerinden biri. Ama "
                     "bırakmak belirtilerin geçeceğini garanti etmez ve beklerken geçen sürenin bir bedeli var. İkisini "
                     "birlikte yapalım.”", "anne", 2,
                     "Günlük kullanım psikotik bozukluk olasılığını yaklaşık üç kat, günlük yüksek potensli kullanım yaklaşık "
                     "beş kat artırıyor (Di Forti ve ark. 2019). Bırakma bir tedavi hedefidir, tedavinin yerini tutmaz; "
                     "gecikmenin bedeli vardır (Kane ve ark. 2016)."),
                    ("“Kenevirle ilgisi yok; bu şizofreni.”", "anne", 0,
                     "İki tek kova arasında gidip gelmek yerine ikisini birlikte tutmak gerekir. Kenevir gerçek bir risk "
                     "etkenidir; tanı ise izlemle netleşir."),
                    ("Babaya katılıp bir ay beklemek", "son-gecikme", -1,
                     "Tedavisiz psikoz süresi uzadıkça kazanç küçülür. İlk atak çalışmasında bu süre ortanca 74 haftaydı ve "
                     "kısa olanlarda ekip temelli bakımın yararı daha büyüktü (Kane ve ark. 2016)."),
                ]),
            "anne": dict(
                metin="Annesi sessizce dinliyor, sonra soruyor: “İki yıl önce boşandık. O zamandan beri böyle içine kapandı. "
                      "Biz mi yaptık bunu?”",
                secenekler=[
                    ("“Boşanma tek başına bu tabloya yol açmaz. Yatkınlıkta kalıtımın payı büyük, ama o da kader değil: tek "
                     "yumurta ikizlerinde bile eşleşme üçte bir. Bugün yapabileceğimiz şeyler var ve sizin katılımınız çok "
                     "önemli.”", "tedavi", 2,
                     "Kalıtsallık %79, tek yumurta ikizinde eşleşme %33’tür (Hilker ve ark. 2018): genetik yük kader değildir. "
                     "Suçluluğu yanıtlayıp konuşmayı bugüne taşımak, aileyi tedavinin ortağı yapar."),
                    ("“Stres tetiklemiş olabilir” deyip konuyu kapatmak", "tedavi", 0,
                     "Yarım bırakılan yanıt, annenin suçluluğunu doğrulanmış gibi bırakır."),
                    ("Soruyu yanıtlamadan ilaç seçeneklerine geçmek", "tedavi", 0,
                     "Yanıtsız kalan suçluluk, ailenin tedaviye katılımını zorlaştırır. Aile girişimi tedavinin bir parçasıdır."),
                ]),
            "tedavi": dict(
                metin="Organik nedenler dışlandı. Belirtiler sürüyor ve Arda okula gidemiyor. Antipsikotik başlamaya karar "
                      "verdiniz.",
                secenekler=[
                    ("Başlamadan kilo, boy ve metabolik ölçümleri almak; ilacı Arda ve ailesiyle birlikte, yan etkileri "
                     "konuşarak seçmek; her vizitte kilo ve metabolik izlem planlamak", "ekip", 2,
                     "İlk kez antipsikotik kullanan 4–19 yaş gençlerde yaklaşık 11 haftada olanzapinle 8,5 kg, ketiapinle 6,1 kg, "
                     "risperidonla 5,3 kg, aripiprazolle 4,4 kg artış görüldü (Correll ve ark. 2009). Başlamadan tart ve ölç."),
                    ("İlacı başlayıp kiloyu “ileride bakarız” diye ertelemek", "ekip", 0,
                     "Belirgin kilo artışı yaklaşık 11 hafta içinde ortaya çıkıyor (Correll ve ark. 2009). Başlangıç ölçümü "
                     "olmadan değişimi izlemek ve aileyle konuşmak zorlaşır."),
                    ("Yan etkilerden çekinip ilaca hiç başlamamak", "son-gecikme", -1,
                     "Yan etki kaygısı izlemle yönetilir. İşlevi bozan ve süren psikotik belirtileri tedavisiz bırakmak "
                     "gecikmeyi uzatır."),
                ]),
            "ekip": dict(
                metin="İlaç başlandı. Sıra izlem planında. Arda “Okula dönemem, herkes biliyor” diyor.",
                secenekler=[
                    ("Ekip temelli bir plan kurmak: aile eğitimi, okulla iş birliği, kenevir için ayrı bir hedef ve düzenli "
                     "izlem", "son-iyi", 2,
                     "İlk atakta ekip temelli kapsamlı bakım, yaşam kalitesini ve belirtileri olağan bakımdan daha çok düzeltti "
                     "(Kane ve ark. 2016). Gecikme prognozdur: erken yönlendir, ekiple çalış."),
                    ("Ayda bir ilaç kontrolüne çağırmak", "son-orta", 0,
                     "İlaç izlemi gerekli, ama yeterli değil. Okul, aile ve madde kullanımı planın dışında kalıyor."),
                ]),
            "son-iyi": dict(son="iyi", baslik="Erken ve ekiple",
                            metin="Arda’nın sesleri haftalar içinde azaldı. Okula kademeli döndü; ailesi neye dikkat edeceğini "
                                  "biliyor, kenevir için ayrı bir hedef konuşuluyor. Kilo ve metabolik izlem her vizitte "
                                  "sürüyor."),
            "son-orta": dict(son="orta", baslik="İlaç var, plan eksik",
                             metin="Belirtiler azaldı, ama Arda okula dönemedi ve kenevir kullanımı sürüyor. Ailesi kontroller "
                                   "arasında kime danışacağını bilmiyor. Tedavi ilaçtan ibaret kaldı."),
            "son-gecikme": dict(son="kotu", baslik="Bekleyerek kaybedilen aylar",
                                metin="Arda aylar sonra, belirtileri ağırlaşmış ve okulu bırakmış olarak yeniden getirildi. "
                                      "Beklemek tarafsız bir karar değildi: tedavisiz geçen süre uzadı (Kane ve ark. 2016)."),
        },
    ),
]
