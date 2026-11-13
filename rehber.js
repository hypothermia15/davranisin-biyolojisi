/* Davranışın Biyolojisi — görünümler, kendini sına, vaka soruları, bilgi kartları, tahmin oyunu,
   simülasyonlar, şekil kutusu, atıf penceresi, arama */
(function () {
  "use strict";
  var kok = document.documentElement;
  kok.classList.add("js");

  var ANAHTAR = "davranisin-biyolojisi:v1";
  var durum = oku();
  ["sina", "okundu", "test", "kart", "not"].forEach(function (k) { durum[k] = durum[k] || {}; });
  function oku() { try { return JSON.parse(localStorage.getItem(ANAHTAR) || "{}") || {}; } catch (e) { return {}; } }
  function yaz() { try { localStorage.setItem(ANAHTAR, JSON.stringify(durum)); } catch (e) { /* özel pencere */ } }

  function $(s, r) { return (r || document).querySelector(s); }
  function $$(s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); }
  function kacis(s) { return String(s).replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; }); }
  function parla(el) { el.classList.remove("parla"); void el.offsetWidth; el.classList.add("parla"); }
  function katla(s) { return s.toLocaleLowerCase("tr").replace(/ı/g, "i").normalize("NFD").replace(/[̀-ͯ]/g, ""); }
  function sayi(x, b) { return x.toFixed(b === undefined ? 0 : b).replace(".", ","); }
  function karistir(a) {
    for (var i = a.length - 1; i > 0; i--) { var j = Math.floor(Math.random() * (i + 1)); var t = a[i]; a[i] = a[j]; a[j] = t; }
    return a;
  }

  var gorunumler = $$(".view");
  var oturumGorunumleri = gorunumler.filter(function (v) { return !!v.querySelector(".okundu"); });
  var etkin = null;
  function baslik(v) { return v.getAttribute("data-baslik") || ""; }
  function adres(v) { return v.dataset.view === "giris" ? "#/" : "#/" + v.dataset.view; }

  /* Önceki / sonraki bağlantıları */
  gorunumler.forEach(function (v, i) {
    var nav = $(".ileri-geri", v);
    if (!nav) return;
    var h = "";
    if (i > 0) h += '<a href="' + adres(gorunumler[i - 1]) + '"><span>← Önceki</span>' + kacis(baslik(gorunumler[i - 1])) + "</a>";
    if (i < gorunumler.length - 1) h += '<a href="' + adres(gorunumler[i + 1]) + '"><span>Sonraki →</span>' + kacis(baslik(gorunumler[i + 1])) + "</a>";
    nav.innerHTML = h;
  });

  /* Görünüm değiştirme */
  function goster(ad, alt, odakla) {
    var v = document.getElementById("v-" + ad) || document.getElementById("v-giris");
    ad = v.dataset.view;
    if (etkin !== v) {
      gorunumler.forEach(function (x) { x.classList.toggle("aktif", x === v); });
      etkin = v;
      $$(".yan a[data-nav]").forEach(function (a) {
        if (a.dataset.nav === ad) a.setAttribute("aria-current", "page"); else a.removeAttribute("aria-current");
      });
      document.title = (ad === "giris" ? "" : baslik(v) + " · ") + "Davranışın Biyolojisi · Doç. Dr. Miraç Barış Usta";
      atifKapat();
      if (ad === "giris") ilerlemeCiz();
      if (ad === "kartlar") kartBaslat(false);
    }
    menuKapat();
    var hedef = alt ? document.getElementById(ad + "-" + alt) : null;
    if (hedef) {
      hedef.scrollIntoView({ block: "start" });
    } else {
      window.scrollTo(0, 0);
      if (odakla !== false) { var h = $("h1, h2", v); if (h) h.focus({ preventScroll: true }); }
    }
  }

  function git(v, el) {
    if (location.hash !== adres(v)) history.pushState(null, "", adres(v));
    goster(v.dataset.view, null, false);
    var det = el.closest("details");
    if (det) det.open = true;
    el.scrollIntoView({ block: "center" });
    parla(el);
  }

  var ilk = true;
  function rota() {
    var h = location.hash || "";
    var m = h.match(/^#\/([\w-]*)(?:\/([\w-]+))?$/);
    var odak = !ilk;
    ilk = false;
    if (!h || h === "#" || (m && !m[1])) return goster("giris", null, odak);
    if (m) return goster(m[1], m[2], odak);
    var el = document.getElementById(decodeURIComponent(h.slice(1)));
    var v = el && el.closest(".view");
    if (v) { goster(v.dataset.view, null, false); el.scrollIntoView({ block: "center" }); parla(el); }
  }
  window.addEventListener("hashchange", rota);

  /* Mobil menü */
  var menuD = $(".menu-dugme");
  function menuKapat() {
    document.body.classList.remove("menu-acik");
    if (menuD) menuD.setAttribute("aria-expanded", "false");
  }
  if (menuD) menuD.addEventListener("click", function () {
    var acik = document.body.classList.toggle("menu-acik");
    menuD.setAttribute("aria-expanded", acik ? "true" : "false");
  });

  /* Yanıt etiketi (kendini sına ve vaka soruları) */
  function etiket(kutu, bildi) {
    if (!kutu) return;
    var et = $(".sonuc-etiket", kutu);
    if (!et) { et = document.createElement("span"); et.className = "sonuc-etiket"; kutu.insertBefore(et, kutu.firstChild); }
    et.textContent = bildi ? "✓ Bildiniz" : "✗ Bu sefer olmadı";
  }

  /* Kendini sına (doğru–yanlış) */
  function sinaUygula(m, yanit) {
    var bildi = yanit === m.dataset.dogru;
    m.classList.add("cevaplandi");
    m.classList.toggle("bildi", bildi);
    m.classList.toggle("bilemedi", !bildi);
    $$("button[data-yanit]", m).forEach(function (b) {
      b.setAttribute("aria-pressed", b.dataset.yanit === yanit ? "true" : "false");
      b.disabled = true;
    });
    etiket($(".sina-aciklama", m), bildi);
    return bildi;
  }
  function sinaTemizle(m) {
    m.classList.remove("cevaplandi", "bildi", "bilemedi");
    $$("button[data-yanit]", m).forEach(function (b) { b.removeAttribute("aria-pressed"); b.disabled = false; });
    var et = $(".sonuc-etiket", m);
    if (et) et.remove();
  }

  /* Vaka soruları (çoktan seçmeli) */
  function testUygula(m, k) {
    var dogru = +m.dataset.dogru, bildi = k === dogru;
    m.classList.add("cevaplandi");
    m.classList.toggle("bildi", bildi);
    m.classList.toggle("bilemedi", !bildi);
    $$("button[data-secenek]", m).forEach(function (b) {
      var s = +b.dataset.secenek;
      b.disabled = true;
      b.classList.toggle("secenek-dogru", s === dogru);
      b.classList.toggle("secenek-yanlis", s === k && !bildi);
      b.setAttribute("aria-pressed", s === k ? "true" : "false");
    });
    etiket($(".test-aciklama", m), bildi);
    return bildi;
  }
  function testTemizle(m) {
    m.classList.remove("cevaplandi", "bildi", "bilemedi");
    $$("button[data-secenek]", m).forEach(function (b) {
      b.disabled = false; b.classList.remove("secenek-dogru", "secenek-yanlis"); b.removeAttribute("aria-pressed");
    });
    var et = $(".sonuc-etiket", m);
    if (et) et.remove();
  }

  function say(vid, tur) {
    var v = document.getElementById("v-" + vid);
    var sec = tur === "test" ? ".adim-test .test-madde" : ".sina-madde";
    var maddeler = v ? $$(sec, v) : [];
    var cev = durum[tur][vid] || {}, n = 0, d = 0;
    maddeler.forEach(function (m) {
      var y = cev[m.dataset.no];
      if (y === undefined || y === null) return;
      n++;
      if (String(y) === m.dataset.dogru) d++;
    });
    return { toplam: maddeler.length, n: n, d: d };
  }
  function skorYaz(vid) {
    [["sina", "data-skor", "data-sifirla", "ifade"], ["test", "data-test-skor", "data-test-sifirla", "soru"]].forEach(function (t) {
      var s = say(vid, t[0]);
      var sk = $("[" + t[1] + '="' + vid + '"]');
      if (sk) sk.textContent = s.n ? (s.d + " / " + s.toplam + " doğru" + (s.n < s.toplam ? " · " + (s.toplam - s.n) + " " + t[3] + " kaldı" : "")) : "";
      var sf = $("[" + t[2] + '="' + vid + '"]');
      if (sf) sf.hidden = !s.n;
    });
    durumGuncelle(vid);
  }
  function durumGuncelle(vid) {
    var s = say(vid, "sina"), t = say(vid, "test"), p = [];
    if (durum.okundu[vid]) p.push("✓ Okundu");
    if (s.n) p.push("Doğru–yanlış " + s.d + "/" + s.toplam);
    if (t.n) p.push("Sorular " + t.d + "/" + t.toplam);
    var kart = $('[data-durum="' + vid + '"]');
    if (kart) kart.textContent = p.join(" · ");
    var nav = $('[data-durum-nav="' + vid + '"]');
    if (nav) nav.textContent = durum.okundu[vid] ? "✓" : "";
    var ok = oturumGorunumleri.filter(function (v) { return durum.okundu[v.dataset.view]; }).length;
    var il = $("[data-ilerleme]");
    if (il) il.textContent = ok ? ok + " / " + oturumGorunumleri.length + " oturum okundu" : "";
  }

  /* Karışık test (doğru–yanlış ya da vaka soruları) */
  var kAlan = $(".karisik-alan"), kListe = [], kSira = 0, kDogru = 0, kTur = "sina";
  function kGoster() {
    var butonlar = $(".karisik-dugmeler");
    if (kSira >= kListe.length) {
      var oran = kDogru / kListe.length;
      kAlan.innerHTML = '<p class="karisik-son">' + kDogru + " / " + kListe.length + " doğru</p><p>" +
        (oran >= 0.85 ? "Çok iyi. Kova yok, merdiven var." : oran >= 0.6 ? "İyi. Kaçırdığınız soruların oturumlarına dönmek iyi olur."
          : "Oturumların “Beş ana fikir” bölümleriyle başlamak iyi bir tekrar olur.") + "</p>";
      if (butonlar) butonlar.hidden = false;
      var b = $(".karisik-basla", butonlar);
      if (b) b.focus();
      return;
    }
    var asil = kListe[kSira], m = asil.cloneNode(true);
    if (kTur === "test") testTemizle(m); else sinaTemizle(m);
    m.removeAttribute("data-ara");
    var kaynak = asil.closest(".view");
    kAlan.innerHTML = '<p class="karisik-ilerleme">' + (kTur === "test" ? "Soru " : "İfade ") + (kSira + 1) + " / " + kListe.length +
      ' · <a href="' + adres(kaynak) + '">' + kacis(baslik(kaynak)) + "</a></p>";
    var ol = document.createElement("ol");
    ol.className = (kTur === "test" ? "test" : "sina") + " sina-tek";
    ol.appendChild(m);
    kAlan.appendChild(ol);
    var ilkB = $("button[data-yanit], button[data-secenek]", m);
    if (ilkB) ilkB.focus();
  }
  $$(".karisik-basla").forEach(function (b) {
    b.addEventListener("click", function () {
      kTur = b.dataset.tur || "sina";
      kListe = karistir(kTur === "test" ? $$(".view .adim-test .test-madde") : $$(".view.oturum .sina-madde"));
      kSira = 0; kDogru = 0;
      var butonlar = $(".karisik-dugmeler");
      if (butonlar) butonlar.hidden = true;
      kGoster();
    });
  });
  function kSonraki(m, bildi) {
    if (bildi) kDogru++;
    var sn = document.createElement("button");
    sn.type = "button";
    sn.className = "dugme karisik-sonraki";
    sn.textContent = kSira + 1 < kListe.length ? (kTur === "test" ? "Sonraki soru →" : "Sonraki ifade →") : "Sonucu gör";
    kAlan.appendChild(sn);
    sn.focus();
  }

  /* Bilgi kartları */
  var kartlar = [];
  oturumGorunumleri.forEach(function (v) {
    $$(".adim-fikirler .fikirler li", v).forEach(function (li, i) {
      var p = $("p", li), st = p && $("strong", p);
      if (!st) return;
      var arka = p.cloneNode(true);
      $("strong", arka).remove();
      kartlar.push({ id: v.dataset.view + "-" + i, vid: v.dataset.view, etiket: baslik(v).split(":")[0],
        on: st.textContent.trim().replace(/[:;,.]$/, ""), arka: arka.innerHTML.trim().replace(/^[:;,.]\s*/, ""),
        ref: (($(".ders-ref", li) || {}).innerHTML) || "" });
    });
  });
  var deste = [], dSira = 0, kSahne = $(".kart-sahne"), kSuz = $("#kart-suz");
  function kartBaslat(karisik) {
    if (!kSahne) return;
    var f = kSuz ? kSuz.value : "";
    var secili = kartlar.filter(function (k) { return !f || k.vid === f; });
    var bilinmeyen = secili.filter(function (k) { return !durum.kart[k.id]; });
    var bilinen = secili.filter(function (k) { return durum.kart[k.id]; });
    deste = (karisik ? karistir(bilinmeyen) : bilinmeyen).concat(karistir(bilinen));
    dSira = 0;
    kartCiz();
  }
  function kartIlerleme() {
    var f = kSuz ? kSuz.value : "";
    var secili = kartlar.filter(function (k) { return !f || k.vid === f; });
    var bil = secili.filter(function (k) { return durum.kart[k.id]; }).length;
    var el = $(".kart-ilerleme");
    if (el) el.textContent = "Bilinen: " + bil + " / " + secili.length + (dSira < deste.length ? " · Kart " + (dSira + 1) + " / " + deste.length : "");
  }
  function kartCiz() {
    if (dSira >= deste.length) {
      kSahne.innerHTML = '<div class="bilgi-kart bitti"><p class="kart-on-metin">Deste bitti.</p>' +
        '<p>Bilmediğiniz kartlar bir sonraki turda önce gelir.</p><button type="button" class="dugme kart-yeniden">Yeniden başla</button></div>';
      kartIlerleme();
      return;
    }
    var k = deste[dSira];
    kSahne.innerHTML = '<div class="bilgi-kart" tabindex="0" role="button" aria-pressed="false" aria-label="Kartı çevir: ' + kacis(k.on) + '">' +
      '<div class="kart-yuz kart-on"><span class="kart-oturum">' + kacis(k.etiket) + (durum.kart[k.id] ? " · biliniyor" : "") + "</span>" +
      '<p class="kart-on-metin">' + kacis(k.on) + '</p><span class="kart-ipucu">Çevirmek için tıklayın ya da boşluk tuşuna basın</span></div>' +
      '<div class="kart-yuz kart-arka"><span class="kart-oturum"><a href="#/' + k.vid + '/fikirler">' + kacis(k.etiket) + " ↗</a></span>" +
      "<p>" + k.arka + "</p>" + (k.ref ? '<p class="ders-ref">' + k.ref + "</p>" : "") + "</div></div>" +
      '<div class="kart-dugmeler"><button type="button" class="dugme dugme-ikincil kart-tekrar">↺ Tekrar sor</button>' +
      '<button type="button" class="dugme kart-biliyorum">✓ Biliyorum</button></div>';
    kartIlerleme();
  }
  function kartCevir() {
    var k = $(".bilgi-kart:not(.bitti)", kSahne);
    if (!k) return;
    var c = k.classList.toggle("cevrildi");
    k.setAttribute("aria-pressed", c ? "true" : "false");
  }
  if (kSuz) kSuz.addEventListener("change", function () { kartBaslat(true); });
  if (kSahne) kSahne.addEventListener("keydown", function (e) {
    if ((e.key === " " || e.key === "Enter") && e.target.classList.contains("bilgi-kart")) { e.preventDefault(); kartCevir(); }
  });

  /* İddia tahmin oyunu */
  var HUKUM = [["saglam", "🟢", "Sağlam"], ["tartismali", "🟡", "Tartışmalı"], ["coktu", "🔴", "Çöktü"], ["duzeltme", "✏️", "Düzeltme"]];
  var tAlan = $(".tahmin-alan"), tBasla = $(".tahmin-basla"), tListe = [], tSira = 0, tDogru = 0;
  function icerik(el) { var c = el.cloneNode(true); var e = $(".iddia-etiket", c); if (e) e.remove(); return c.innerHTML.trim(); }
  function tGoster() {
    if (tSira >= tListe.length) {
      var en = Math.max((durum.tahmin && durum.tahmin.en) || 0, tDogru);
      durum.tahmin = { en: en, son: tDogru, toplam: tListe.length };
      yaz();
      tAlan.innerHTML = '<p class="karisik-son">' + tDogru + " / " + tListe.length + " doğru tahmin</p><p>En iyi skorunuz: " + en +
        ". Sapolsky’nin iddialarının bir bölümü çöktü, bir bölümü ayakta; asıl ders, hükmün kanıta göre güncellenmesi.</p>";
      tBasla.hidden = false;
      tBasla.textContent = "Yeniden oyna";
      tBasla.focus();
      return;
    }
    var c = tListe[tSira];
    tAlan.innerHTML = '<p class="karisik-ilerleme">İddia ' + (tSira + 1) + " / " + tListe.length + " · " + c.kaynak + "</p>" +
      '<div class="tahmin-kart"><p class="tahmin-ders"><span class="iddia-etiket">Derste</span> ' + c.ders + "</p>" +
      '<div class="tahmin-dugmeler" role="group" aria-label="Bugünkü hüküm">' +
      HUKUM.map(function (h) { return '<button type="button" data-tahmin="' + h[0] + '"><span aria-hidden="true">' + h[1] + "</span> " + h[2] + "</button>"; }).join("") +
      '</div><div class="tahmin-sonuc" hidden></div></div>';
    var b = $("button[data-tahmin]", tAlan);
    if (b) b.focus();
  }
  if (tBasla) tBasla.addEventListener("click", function () {
    tListe = karistir($$(".iddia").map(function (li) {
      return { h: li.dataset.hukum, ders: icerik($(".iddia-ders", li)), bugun: icerik($(".iddia-bugun", li)),
        rozet: $(".hukum", li).outerHTML, kaynak: $(".iddia-oturum", li).outerHTML,
        bugunEt: $(".iddia-bugun .iddia-etiket", li).textContent };
    }));
    tSira = 0; tDogru = 0;
    tBasla.hidden = true;
    tGoster();
  });

  /* Mini vaka notları */
  $$("textarea[data-not]").forEach(function (t) {
    var id = t.dataset.not, zam = null;
    if (durum.not[id]) t.value = durum.not[id];
    t.addEventListener("input", function () {
      clearTimeout(zam);
      zam = setTimeout(function () {
        if (t.value.trim()) durum.not[id] = t.value; else delete durum.not[id];
        yaz();
      }, 400);
    });
  });

  /* İlerleme paneli */
  var silOnay = 0;
  function ilerlemeCiz() {
    var panel = $("#ilerlemem");
    if (!panel) return;
    var ok = oturumGorunumleri.filter(function (v) { return durum.okundu[v.dataset.view]; }).length;
    var s = { n: 0, d: 0, t: 0 }, q = { n: 0, d: 0, t: 0 };
    oturumGorunumleri.forEach(function (v) {
      var a = say(v.dataset.view, "sina"), b = say(v.dataset.view, "test");
      s.n += a.n; s.d += a.d; s.t += a.toplam; q.n += b.n; q.d += b.d; q.t += b.toplam;
    });
    var bil = kartlar.filter(function (k) { return durum.kart[k.id]; }).length;
    var th = durum.tahmin;
    var var_ = ok || s.n || q.n || bil || th;
    panel.hidden = !var_;
    if (!var_) return;
    function kutu(ad, deger, alt, adr) {
      return '<a class="ilerleme-kutu" href="' + adr + '"><span class="ik-ad">' + ad + '</span><span class="ik-deger">' + deger +
        '</span><span class="ik-alt">' + alt + "</span></a>";
    }
    $(".ilerleme-kutular", panel).innerHTML =
      kutu("Okunan oturum", ok + " / " + oturumGorunumleri.length, ok ? "devam edin" : "henüz yok", "#/oturum-1") +
      kutu("Doğru mu, yanlış mı?", s.d + " / " + s.t, s.n + " ifade yanıtlandı", "#/tekrar") +
      kutu("Vaka soruları", q.d + " / " + q.t, q.n + " soru yanıtlandı", "#/tekrar") +
      kutu("Bilgi kartları", bil + " / " + kartlar.length, "biliniyor", "#/kartlar") +
      kutu("Tahmin oyunu", th ? th.en + " / " + th.toplam : "–", th ? "en iyi skor" : "henüz oynanmadı", "#/iddialar");
  }

  /* Şekil kutusu */
  var isik = $("#isik"), sekiller = [], sekilNo = 0, gorulen = {};
  $$("figure.sekil").forEach(function (f) {
    var n = f.querySelector(".sekil-buyut").dataset.sekil;
    if (!gorulen[n]) { gorulen[n] = true; sekiller.push(f); }
  });
  sekiller.sort(function (a, b) { return a.querySelector(".sekil-buyut").dataset.sekil - b.querySelector(".sekil-buyut").dataset.sekil; });
  function sekilSirasi(n) {
    for (var i = 0; i < sekiller.length; i++) if (+sekiller[i].querySelector(".sekil-buyut").dataset.sekil === n) return i;
    return -1;
  }
  function sekilAc(i) {
    if (!isik || typeof isik.showModal !== "function" || i < 0) return false;
    sekilNo = (i + sekiller.length) % sekiller.length;
    var f = sekiller[sekilNo], img = $("img", f), a = $(".sekil-buyut", f), cap = $("figcaption", f).cloneNode(true);
    var no = $(".sekil-no", cap);
    var ad = no ? no.textContent.replace(/\.$/, "") : "";
    if (no) no.remove();
    var buyuk = $(".isik-resim img", isik);
    buyuk.src = img.getAttribute("src");
    buyuk.alt = img.alt;
    $(".isik-no", isik).textContent = ad;
    $(".isik-alt", isik).innerHTML = cap.innerHTML;
    $(".isik-tam", isik).href = a.getAttribute("href");
    if (!isik.open) isik.showModal();
    return true;
  }
  if (isik) {
    $(".isik-kapat", isik).addEventListener("click", function () { isik.close(); });
    $(".isik-onceki", isik).addEventListener("click", function () { sekilAc(sekilNo - 1); });
    $(".isik-sonraki", isik).addEventListener("click", function () { sekilAc(sekilNo + 1); });
    isik.addEventListener("click", function (e) { if (e.target === isik) isik.close(); });
    isik.addEventListener("keydown", function (e) {
      if (e.key === "ArrowRight") { e.preventDefault(); sekilAc(sekilNo + 1); }
      else if (e.key === "ArrowLeft") { e.preventDefault(); sekilAc(sekilNo - 1); }
    });
  }

  /* Atıf penceresi */
  var pop = $("#atif-pop"), aktifAtif = null;
  function atifKapat() {
    if (pop && !pop.hidden) { pop.hidden = true; if (aktifAtif && document.activeElement && pop.contains(document.activeElement)) aktifAtif.focus(); }
    aktifAtif = null;
  }
  function atifAc(a) {
    var li = document.getElementById(a.dataset.k);
    if (!li || !pop) return false;
    if (aktifAtif === a && !pop.hidden) { atifKapat(); return true; }
    pop.innerHTML = "<p>" + li.innerHTML + '</p><p class="atif-alt"><a href="#/kaynakca" data-git="' + li.id +
      '">Kaynakçada gör</a><button type="button" class="atif-kapat">Kapat ✕</button></p>';
    pop.hidden = false;
    var r = a.getBoundingClientRect(), w = pop.offsetWidth, h = pop.offsetHeight, sx = window.scrollX, gen = document.documentElement.clientWidth;
    var ust = r.bottom + 8 + h > window.innerHeight && r.top - h - 8 > 64;
    pop.style.left = Math.max(12, Math.min(r.left, gen - w - 12)) + sx + "px";
    pop.style.top = window.scrollY + (ust ? r.top - h - 8 : r.bottom + 8) + "px";
    aktifAtif = a;
    return true;
  }

  /* Tıklamalar */
  document.addEventListener("click", function (e) {
    var t = e.target;
    var s = t.closest("a.sekil-ref, a.sekil-buyut");
    if (s && !e.ctrlKey && !e.metaKey && !e.shiftKey) {
      var n = s.classList.contains("sekil-ref") ? parseInt(s.getAttribute("href").slice(7), 10) : parseInt(s.dataset.sekil, 10);
      if (sekilAc(sekilSirasi(n))) { e.preventDefault(); atifKapat(); }
      return;
    }
    var at = t.closest("a.atif");
    if (at && !e.ctrlKey && !e.metaKey) { if (atifAc(at)) e.preventDefault(); return; }
    var g = t.closest("[data-git]");
    if (g) {
      e.preventDefault();
      var hedef = document.getElementById(g.dataset.git);
      atifKapat();
      if (hedef) git(hedef.closest(".view"), hedef);
      return;
    }
    if (t.closest(".atif-kapat")) { atifKapat(); return; }
    if (pop && !pop.hidden && !t.closest("#atif-pop")) atifKapat();

    var y = t.closest(".sina-madde button[data-yanit]");
    if (y && !y.disabled) {
      var m = y.closest(".sina-madde"), bildi = sinaUygula(m, y.dataset.yanit);
      if (m.closest(".karisik-alan")) { kSonraki(m, bildi); return; }
      var vid = m.closest(".view").dataset.view;
      (durum.sina[vid] = durum.sina[vid] || {})[m.dataset.no] = y.dataset.yanit;
      yaz();
      skorYaz(vid);
      return;
    }
    var sc = t.closest(".test-madde button[data-secenek]");
    if (sc && !sc.disabled) {
      var tm = sc.closest(".test-madde"), k = +sc.dataset.secenek, tb = testUygula(tm, k);
      if (tm.closest(".karisik-alan")) { kSonraki(tm, tb); return; }
      var tv = tm.closest(".view").dataset.view;
      (durum.test[tv] = durum.test[tv] || {})[tm.dataset.no] = k;
      yaz();
      skorYaz(tv);
      return;
    }
    if (t.closest(".karisik-sonraki")) { kSira++; kGoster(); return; }
    var sf = t.closest("[data-sifirla], [data-test-sifirla]");
    if (sf) {
      var tur = sf.hasAttribute("data-test-sifirla") ? "test" : "sina";
      var id = sf.getAttribute(tur === "test" ? "data-test-sifirla" : "data-sifirla");
      delete durum[tur][id];
      yaz();
      $$(tur === "test" ? "#v-" + id + " .adim-test .test-madde" : "#v-" + id + " .sina-madde").forEach(tur === "test" ? testTemizle : sinaTemizle);
      skorYaz(id);
      return;
    }
    var ok = t.closest(".okundu");
    if (ok) {
      var o = ok.dataset.okundu;
      if (durum.okundu[o]) delete durum.okundu[o]; else durum.okundu[o] = true;
      yaz();
      ok.setAttribute("aria-pressed", durum.okundu[o] ? "true" : "false");
      durumGuncelle(o);
      return;
    }
    var th = t.closest("button[data-tahmin]");
    if (th && !th.disabled) {
      var c = tListe[tSira], dogruMu = th.dataset.tahmin === c.h;
      if (dogruMu) tDogru++;
      $$("button[data-tahmin]", tAlan).forEach(function (b) {
        b.disabled = true;
        b.classList.toggle("secenek-dogru", b.dataset.tahmin === c.h);
        b.classList.toggle("secenek-yanlis", b === th && !dogruMu);
      });
      var so = $(".tahmin-sonuc", tAlan);
      so.innerHTML = '<p><strong class="' + (dogruMu ? "iyi" : "kotu") + '">' + (dogruMu ? "✓ Doğru tahmin." : "✗ Bugünkü hüküm başka:") +
        "</strong> " + c.rozet + "</p><p><span class=\"iddia-etiket\">" + kacis(c.bugunEt) + "</span> " + c.bugun + "</p>" +
        '<button type="button" class="dugme tahmin-sonraki">' + (tSira + 1 < tListe.length ? "Sonraki iddia →" : "Sonucu gör") + "</button>";
      so.hidden = false;
      $(".tahmin-sonraki", so).focus();
      return;
    }
    if (t.closest(".tahmin-sonraki")) { tSira++; tGoster(); return; }
    if (t.closest(".bilgi-kart:not(.bitti)") && !t.closest("a")) { kartCevir(); return; }
    if (t.closest(".kart-biliyorum") || t.closest(".kart-tekrar")) {
      var kk = deste[dSira];
      if (t.closest(".kart-biliyorum")) durum.kart[kk.id] = 1;
      else { delete durum.kart[kk.id]; deste.splice(Math.min(deste.length, dSira + 4), 0, kk); }
      yaz();
      dSira++;
      kartCiz();
      var kartEl = $(".bilgi-kart", kSahne);
      if (kartEl) kartEl.focus();
      return;
    }
    if (t.closest(".kart-yeniden") || t.closest(".kart-karistir")) { kartBaslat(true); return; }
    if (t.closest(".kart-sifirla")) {
      var f = kSuz ? kSuz.value : "";
      kartlar.forEach(function (x) { if (!f || x.vid === f) delete durum.kart[x.id]; });
      yaz();
      kartBaslat(true);
      return;
    }
    var hs = t.closest(".hepsini-sil");
    if (hs) {
      if (Date.now() - silOnay > 4000) { silOnay = Date.now(); hs.textContent = "Emin misiniz? Silmek için yeniden tıklayın"; return; }
      durum = { sina: {}, okundu: {}, test: {}, kart: {}, not: {} };
      yaz();
      location.reload();
      return;
    }
    if (document.body.classList.contains("menu-acik") && !t.closest(".yan, .menu-dugme")) menuKapat();
    if (araS && !araS.hidden && !t.closest(".ara")) araS.hidden = true;
  });

  /* İddia ligi süzgeci */
  $$(".filtre").forEach(function (b) {
    b.addEventListener("click", function () {
      var f = b.dataset.filtre;
      $$(".filtre").forEach(function (x) { x.setAttribute("aria-pressed", x === b ? "true" : "false"); });
      var n = 0;
      $$(".iddia").forEach(function (li) { var g = !f || li.dataset.hukum === f; li.hidden = !g; if (g) n++; });
      var r = $(".filtre-sonuc");
      if (r) r.textContent = f ? n + " iddia gösteriliyor." : "";
    });
  });

  /* Kaynakça süzgeci */
  var ksuz = $("#kaynak-suz");
  if (ksuz) ksuz.addEventListener("input", function () {
    var q = katla(ksuz.value.trim()), n = 0;
    $$(".kaynaklar li").forEach(function (li) {
      var g = !q || katla(li.textContent).indexOf(q) >= 0;
      li.hidden = !g;
      if (g) n++;
    });
    $(".kaynak-sonuc").textContent = q ? n + " kaynak bulundu." : "";
  });

  /* Arama */
  var araK = $("#ara"), araS = $("#ara-sonuc"), dizin = null;
  function dizinKur() {
    dizin = $$("[data-ara]").filter(function (el) { return !el.closest(".karisik-alan") && el.closest(".view"); }).map(function (el) {
      var v = el.closest(".view"), adim = el.closest(".adim"), yer = baslik(v);
      if (adim) { var h = $("h3", adim); if (h) yer += " › " + h.textContent.trim(); }
      var t = el.textContent.replace(/\s+/g, " ").trim();
      return { el: el, v: v, yer: yer, t: t, k: katla(t) };
    });
  }
  function parcacik(d, terim) {
    var i = d.k.indexOf(terim);
    if (i < 0) i = 0;
    var bas = Math.max(0, i - 50), son = Math.min(d.t.length, i + terim.length + 110);
    return (bas ? "…" : "") + kacis(d.t.slice(bas, i)) + "<mark>" + kacis(d.t.slice(i, i + terim.length)) + "</mark>" +
      kacis(d.t.slice(i + terim.length, son)) + (son < d.t.length ? "…" : "");
  }
  function ara() {
    var q = araK.value.trim();
    if (q.length < 2) { araS.hidden = true; return; }
    if (!dizin) dizinKur();
    var terimler = katla(q).split(/\s+/).filter(Boolean), sonuc = [];
    for (var i = 0; i < dizin.length && sonuc.length < 40; i++) {
      var d = dizin[i];
      if (terimler.every(function (t) { return d.k.indexOf(t) >= 0; })) sonuc.push(i);
    }
    araS.innerHTML = sonuc.length ? sonuc.map(function (i) {
      return '<button type="button" data-i="' + i + '"><span class="yer">' + kacis(dizin[i].yer) + "</span>" + parcacik(dizin[i], terimler[0]) + "</button>";
    }).join("") + (sonuc.length === 40 ? '<p class="bos">İlk 40 sonuç gösteriliyor; aramayı daraltın.</p>' : "")
      : '<p class="bos">“' + kacis(q) + "” için sonuç yok.</p>";
    araS.hidden = false;
  }
  if (araK) {
    var zam = null;
    araK.addEventListener("input", function () { clearTimeout(zam); zam = setTimeout(ara, 120); });
    araK.addEventListener("focus", function () { if (araK.value.trim().length >= 2) ara(); });
    araK.addEventListener("keydown", function (e) {
      if (e.key === "Escape") { araS.hidden = true; araK.blur(); }
      else if (e.key === "ArrowDown" || e.key === "Enter") { var b = $("button", araS); if (b && !araS.hidden) { e.preventDefault(); if (e.key === "Enter") b.click(); else b.focus(); } }
    });
    araS.addEventListener("keydown", function (e) {
      var bs = $$("button", araS), i = bs.indexOf(document.activeElement);
      if (e.key === "ArrowDown" && i < bs.length - 1) { e.preventDefault(); bs[i + 1].focus(); }
      else if (e.key === "ArrowUp") { e.preventDefault(); if (i > 0) bs[i - 1].focus(); else araK.focus(); }
      else if (e.key === "Escape") { araS.hidden = true; araK.focus(); }
    });
    araS.addEventListener("click", function (e) {
      var b = e.target.closest("button[data-i]");
      if (!b) return;
      var d = dizin[+b.dataset.i];
      araS.hidden = true;
      git(d.v, d.el);
    });
  }

  document.addEventListener("keydown", function (e) {
    if (e.key === "Escape") { atifKapat(); menuKapat(); }
    if (e.key === "/" && !/^(INPUT|TEXTAREA|SELECT)$/.test(document.activeElement.tagName) && araK) { e.preventDefault(); araK.focus(); }
  });

  /* ---------- Simülasyonlar ---------- */
  function rastgele(tohum) {
    return function () {
      tohum |= 0; tohum = (tohum + 0x6D2B79F5) | 0;
      var t = Math.imul(tohum ^ (tohum >>> 15), 1 | tohum);
      t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
      return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
    };
  }
  function normal(rng) { var u = 1 - rng(), v = rng(); return Math.sqrt(-2 * Math.log(u)) * Math.cos(2 * Math.PI * v); }
  var simSayac = 0;
  function kaydirici(id, etiketMetni, min, max, adim, deger, birim) {
    return '<div class="sim-kontrol"><label for="' + id + '">' + etiketMetni + '</label><input type="range" id="' + id + '" min="' + min +
      '" max="' + max + '" step="' + adim + '" value="' + deger + '"><output for="' + id + '" class="sim-deger">' + deger + (birim || "") + "</output></div>";
  }

  var SIMLER = {
    esik: function (alan) {
      var id = "sim" + (++simSayac), rng = rastgele(11), noktalar = [];
      while (noktalar.length < 160) {
        var p = Math.round(46 + 15 * normal(rng));
        if (p >= 3 && p <= 97) noktalar.push({ p: p, y: rng() });
      }
      var kisiler = [{ ad: "Ali", p: 68 }, { ad: "Ayşe", p: 71 }, { ad: "Zeynep", p: 96 }];
      var N = noktalar.length + kisiler.length;
      alan.innerHTML = kaydirici(id, "Kesme puanı", 40, 90, 1, 70) +
        '<div class="sim-svg-kap"><svg class="sim-svg" viewBox="0 0 640 200" role="img" aria-label="Belirti şiddeti dağılımı ve kesme puanı"><g></g></svg></div>' +
        '<p class="sim-sonuc" aria-live="polite"></p>';
      var r = $("input", alan), o = $("output", alan), g = $("svg g", alan), sonuc = $(".sim-sonuc", alan);
      function x(p) { return 20 + p * 6; }
      function kat(p, e) { return p >= e ? "hasta" : "sağlıklı"; }
      function ciz() {
        var e = +r.value;
        o.textContent = e;
        var h = '<rect x="' + x(e) + '" y="14" width="' + (x(100) - x(e)) + '" height="142" class="sim-bolge"/>' +
          '<text x="' + (x(e) + 6) + '" y="28" class="sim-yazi sim-yazi-koyu">“Hasta” kategorisi</text>' +
          '<text x="' + (x(e) - 6) + '" y="28" class="sim-yazi sim-yazi-koyu" text-anchor="end">“Sağlıklı” kategorisi</text>' +
          '<line x1="20" y1="156" x2="620" y2="156" class="sim-eksen"/>';
        for (var t = 0; t <= 100; t += 10) {
          h += '<line x1="' + x(t) + '" y1="156" x2="' + x(t) + '" y2="161" class="sim-eksen"/><text x="' + x(t) + '" y="175" class="sim-yazi" text-anchor="middle">' + t + "</text>";
        }
        h += '<text x="320" y="194" class="sim-yazi" text-anchor="middle">Belirti şiddeti (sürekli bir boyut)</text>';
        noktalar.forEach(function (n) { h += '<circle cx="' + x(n.p) + '" cy="' + (40 + n.y * 78) + '" r="3.6" class="' + (n.p >= e ? "sim-a" : "sim-b") + '"/>'; });
        kisiler.forEach(function (k, i) {
          var cx = x(k.p), cy = 136, anchor = i === 0 ? "end" : i === 1 ? "start" : "middle", tx = i === 0 ? cx - 8 : i === 1 ? cx + 8 : cx;
          h += '<circle cx="' + cx + '" cy="' + cy + '" r="7" class="sim-kisi ' + (k.p >= e ? "sim-a" : "sim-b") + '"/>' +
            '<text x="' + tx + '" y="' + (i === 2 ? cy - 12 : cy + 4) + '" class="sim-yazi sim-yazi-koyu" text-anchor="' + anchor + '">' + k.ad + " " + k.p + "</text>";
        });
        h += '<line x1="' + x(e) + '" y1="14" x2="' + x(e) + '" y2="156" class="sim-esik"/>';
        g.innerHTML = h;
        var hasta = noktalar.filter(function (n) { return n.p >= e; }).length + kisiler.filter(function (k) { return k.p >= e; }).length;
        var ali = kat(68, e), ayse = kat(71, e), zey = kat(96, e);
        var yorum = ali !== ayse ? "Ali ile Ayşe arasında yalnızca 3 puan var, ama ayrı kategorilerdeler. " : "Ali ile Ayşe aynı kategoride. ";
        yorum += ayse === zey ? "Ayşe ile Zeynep arasındaki 25 puan ise aynı etiketin altında kayboluyor." : "Ayşe ile Zeynep ayrı kategorilerde.";
        sonuc.innerHTML = "<strong>Tanı alan: " + hasta + " / " + N + " (%" + sayi(100 * hasta / N, 1) + ").</strong> Ali: " + ali +
          " · Ayşe: " + ayse + " · Zeynep: " + zey + ". " + yorum;
      }
      r.addEventListener("input", ciz);
      ciz();
    },

    kisasa: function (alan) {
      var id = "sim" + (++simSayac), tohum = 3;
      var ODEME = [[1, 5], [0, 3]]; // ODEME[benim][onun]: 1 = işbirliği, 0 = ihanet
      var STR = [
        { ad: "Hep işbirliği", h: function () { return 1; } },
        { ad: "Hep ihanet", h: function () { return 0; } },
        { ad: "Kısasa kısas", h: function (b, o) { return o.length ? o[o.length - 1] : 1; } },
        { ad: "Cömert kısasa kısas", h: function (b, o, r) { return !o.length || o[o.length - 1] ? 1 : (r() < 1 / 3 ? 1 : 0); } },
        { ad: "Kindar (bir ihanette küser)", h: function (b, o) { return o.indexOf(0) >= 0 ? 0 : 1; } },
        { ad: "Rastgele", h: function (b, o, r) { return r() < 0.5 ? 1 : 0; } }
      ];
      alan.innerHTML = kaydirici(id, "Sinyal hatası (hamlenin yanlış gitme olasılığı)", 0, 10, 1, 0, "%") +
        '<p class="sim-dugmeler"><button type="button" class="dugme dugme-ikincil sim-yeniden">Turnuvayı yeniden oynat</button></p>' +
        '<ol class="sim-bar-liste" aria-live="polite"></ol><p class="sim-not">Puanlar: ikisi de işbirliği yaparsa 3–3, ikisi de ihanet ederse ' +
        "1–1; biri ihanet eder öteki işbirliği yaparsa 5–0. Her eşleşme 200 tur, turnuva 10 kez oynanır; tablo tur başına ortalama puanı gösterir.</p>";
      var r = $("input", alan), o = $("output", alan), liste = $(".sim-bar-liste", alan);
      function mac(a, b, hata, rng) {
        var ha = [], hb = [], pa = 0, pb = 0;
        for (var t = 0; t < 200; t++) {
          var ma = a.h(ha, hb, rng), mb = b.h(hb, ha, rng);
          if (rng() < hata) ma = 1 - ma;
          if (rng() < hata) mb = 1 - mb;
          ha.push(ma); hb.push(mb);
          pa += ODEME[ma][mb]; pb += ODEME[mb][ma];
        }
        return [pa / 200, pb / 200];
      }
      function oyna() {
        var hata = +r.value / 100, rng = rastgele(tohum), top = STR.map(function () { return 0; }), say_ = STR.map(function () { return 0; });
        o.textContent = r.value + "%";
        for (var tekrar = 0; tekrar < 10; tekrar++) {
          for (var i = 0; i < STR.length; i++) {
            for (var j = i; j < STR.length; j++) {
              var s = mac(STR[i], STR[j], hata, rng);
              top[i] += s[0]; say_[i]++;
              top[j] += s[1]; say_[j]++;
            }
          }
        }
        var sonuc = STR.map(function (st, i) { return { ad: st.ad, p: top[i] / say_[i] }; }).sort(function (a, b) { return b.p - a.p; });
        liste.innerHTML = sonuc.map(function (s, i) {
          return '<li><span class="sim-bar-ad">' + (i + 1) + ". " + s.ad + '</span><span class="sim-bar"><span style="width:' + (100 * s.p / 5) +
            '%"></span></span><span class="sim-bar-deger">' + sayi(s.p, 2) + "</span></li>";
        }).join("");
      }
      r.addEventListener("input", oyna);
      $(".sim-yeniden", alan).addEventListener("click", function () { tohum = Math.floor(Math.random() * 1e9); oyna(); });
      oyna();
    },

    kalitsallik: function (alan) {
      var id = "sim" + (++simSayac), rng = rastgele(5), N = 240, G = [], M = [], K = [];
      for (var i = 0; i < N; i++) { G.push(4 * normal(rng)); M.push(1.5 * normal(rng)); K.push(rng() < 0.5 ? 1 : 0); }
      var mod = "tek";
      alan.innerHTML = '<div class="sim-secim" role="group" aria-label="Ekim düzeni">' +
        '<button type="button" data-mod="tek" aria-pressed="true">Tek tip toprak</button>' +
        '<button type="button" data-mod="karisik" aria-pressed="false">Karışık toprak</button>' +
        '<button type="button" data-mod="iki" aria-pressed="false">İki ayrı tarla</button></div>' +
        kaydirici(id, "İyi ve kötü toprak arasındaki fark", 0, 20, 1, 10, " cm") +
        '<div class="sim-svg-kap"><svg class="sim-svg" viewBox="0 0 640 170" role="img" aria-label="Bitki boylarının dağılımı"><g></g></svg></div>' +
        '<p class="sim-sonuc" aria-live="polite"></p>';
      var r = $("input", alan), o = $("output", alan), g = $("svg g", alan), sonuc = $(".sim-sonuc", alan);
      function x(b) { return 20 + (b - 15) * 12; }
      function ort(a) { return a.reduce(function (s, v) { return s + v; }, 0) / a.length; }
      function vary(a) { var m = ort(a); return a.reduce(function (s, v) { return s + (v - m) * (v - m); }, 0) / a.length; }
      function ciz() {
        var d = +r.value;
        o.textContent = d + " cm";
        r.disabled = mod === "tek";
        var boy = [], toprak = [];
        for (var i = 0; i < N; i++) {
          var iyi = mod === "tek" ? 1 : mod === "karisik" ? K[i] : (i < N / 2 ? 1 : 0);
          var e = mod === "tek" ? 0 : (iyi ? d / 2 : -d / 2);
          toprak.push(iyi);
          boy.push(40 + G[i] + M[i] + e);
        }
        var h = '<line x1="20" y1="140" x2="620" y2="140" class="sim-eksen"/>';
        for (var t = 15; t <= 65; t += 5) h += '<line x1="' + x(t) + '" y1="140" x2="' + x(t) + '" y2="145" class="sim-eksen"/><text x="' + x(t) + '" y="158" class="sim-yazi" text-anchor="middle">' + t + "</text>";
        h += '<text x="620" y="168" class="sim-yazi" text-anchor="end">Boy (cm)</text>';
        var r2 = rastgele(9);
        boy.forEach(function (b, i) {
          var yy = mod === "iki" ? (toprak[i] ? 30 + r2() * 35 : 80 + r2() * 35) : 30 + r2() * 90;
          h += '<circle cx="' + x(Math.max(15, Math.min(65, b))) + '" cy="' + yy + '" r="3.4" class="' + (toprak[i] ? "sim-iyi" : "sim-kotu") + '"/>';
        });
        if (mod === "iki") h += '<text x="24" y="24" class="sim-yazi sim-yazi-koyu">İyi toprak</text><text x="24" y="76" class="sim-yazi sim-yazi-koyu">Kötü toprak</text>';
        g.innerHTML = h;
        var vG = vary(G);
        if (mod === "iki") {
          var a = [], b = [], ga = [], gb = [];
          boy.forEach(function (v, i) { if (toprak[i]) { a.push(v); ga.push(G[i]); } else { b.push(v); gb.push(G[i]); } });
          var hA = vary(ga) / vary(a), hB = vary(gb) / vary(b);
          sonuc.innerHTML = "<strong>Her tarlanın içinde kalıtsallık ≈ %" + sayi(100 * (hA + hB) / 2) + ".</strong> Ama iki tarla arasındaki " +
            sayi(ort(a) - ort(b), 1) + " cm’lik ortalama farkın tamamı topraktan: tohumlar aynı karışımdan. Grup içi kalıtsallık, gruplar arası farkı açıklamaz.";
        } else {
          var hh = vG / vary(boy);
          sonuc.innerHTML = "<strong>Kalıtsallık ≈ %" + sayi(100 * hh) + ".</strong> " + (mod === "tek"
            ? "Bütün bitkiler aynı toprakta: boy farklarının çoğu genlerden."
            : "Genler hiç değişmedi; değişen yalnızca toprak. Toprak farkı büyüdükçe boy farklarının daha büyük bir bölümü topraktan geliyor.");
        }
      }
      $$("button[data-mod]", alan).forEach(function (b) {
        b.addEventListener("click", function () {
          mod = b.dataset.mod;
          $$("button[data-mod]", alan).forEach(function (x) { x.setAttribute("aria-pressed", x === b ? "true" : "false"); });
          ciz();
        });
      });
      r.addEventListener("input", ciz);
      ciz();
    },

    hamilton: function (alan) {
      var id = "sim" + (++simSayac);
      var AKRABA = [["Tek yumurta ikizi", 1], ["Kardeş, anne–baba ya da çocuk", 0.5],
        ["Anne bir ya da baba bir kardeş, yeğen, büyükanne–büyükbaba ya da torun", 0.25], ["Birinci dereceden kuzen", 0.125], ["Akraba olmayan biri", 0]];
      alan.innerHTML = '<div class="sim-kontrol"><label for="' + id + 'a">Kime yardım ediliyor?</label><select id="' + id + 'a">' +
        AKRABA.map(function (a, i) { return '<option value="' + i + '"' + (i === 1 ? " selected" : "") + ">" + a[0] + " (r = " + sayi(a[1], a[1] === 0.125 ? 3 : a[1] === 0.25 ? 2 : 1).replace(",0", "") + ")</option>"; }).join("") +
        "</select></div>" + kaydirici(id + "b", "Yardım alanın kazancı (B)", 0, 10, 0.5, 6) + kaydirici(id + "c", "Yardım edenin bedeli (C)", 0, 10, 0.5, 2) +
        '<div class="sim-karsilastir"><div><span>r × B</span><span class="sim-bar"><span class="rb"></span></span><b class="rb-d"></b></div>' +
        '<div><span>C</span><span class="sim-bar sim-bar-c"><span class="c"></span></span><b class="c-d"></b></div></div>' +
        '<p class="sim-sonuc" aria-live="polite"></p>';
      var sec = $("select", alan), rB = $("#" + id + "b"), rC = $("#" + id + "c"), sonuc = $(".sim-sonuc", alan);
      function ciz() {
        var a = AKRABA[+sec.value], rr = a[1], B = +rB.value, C = +rC.value, rb = rr * B;
        $("#" + id + "b + output").textContent = sayi(B, 1);
        $("#" + id + "c + output").textContent = sayi(C, 1);
        $(".rb", alan).style.width = (10 * rb) + "%";
        $(".c", alan).style.width = (10 * C) + "%";
        $(".rb-d", alan).textContent = sayi(rb, 2);
        $(".c-d", alan).textContent = sayi(C, 2);
        var m;
        if (rr === 0) m = "<strong>r = 0: akraba seçilimi bu yardımı açıklayamaz.</strong> Akraba olmayana yardımın evrimsel açıklaması karşılıklılıktır (Oturum 1, kısasa kısas).";
        else if (rb > C) m = "<strong>r × B > C: seçilim bu yardımı destekler.</strong> Yardım edenin genleri, ortak gen payı üzerinden kârlı çıkar.";
        else m = "<strong>r × B ≤ C: seçilim bu yardımı desteklemez.</strong> Bu yakınlıkta yardımın kârlı olması için kazanç, bedelin " + sayi(1 / rr, 0) + " katından büyük olmalı.";
        sonuc.innerHTML = m;
      }
      [sec, rB, rC].forEach(function (el) { el.addEventListener("input", ciz); el.addEventListener("change", ciz); });
      ciz();
    },

    dopamin: function (alan) {
      var id = "sim" + (++simSayac);
      alan.innerHTML = kaydirici(id, "Ödülün gelme olasılığı", 0, 100, 5, 50, "%") +
        '<div class="sim-svg-kap"><svg class="sim-svg" viewBox="0 0 640 230" role="img" aria-label="Dopamin yanıtlarının ödül olasılığına göre değişimi"><g></g></svg></div>' +
        '<p class="sim-sonuc" aria-live="polite"></p><p class="sim-not">Şematik çizim: eğrilerin biçimi örüntüyü gösterir, ölçülmüş değerleri değil.</p>';
      var r = $("input", alan), o = $("output", alan), g = $("svg g", alan), sonuc = $(".sim-sonuc", alan);
      function x(p) { return 60 + p * 540; }
      function y(v) { return 190 - v * 160; }
      var yolA = "", yolB = "";
      for (var i = 0; i <= 100; i++) {
        var p = i / 100;
        yolA += (i ? "L" : "M") + x(p).toFixed(1) + " " + y(p).toFixed(1);
        yolB += (i ? "L" : "M") + x(p).toFixed(1) + " " + y(4 * p * (1 - p)).toFixed(1);
      }
      function ciz() {
        var p = +r.value / 100, a = p, b = 4 * p * (1 - p);
        o.textContent = r.value + "%";
        var h = '<line x1="60" y1="190" x2="600" y2="190" class="sim-eksen"/><line x1="60" y1="30" x2="60" y2="190" class="sim-eksen"/>';
        [0, 25, 50, 75, 100].forEach(function (t) { h += '<text x="' + x(t / 100) + '" y="208" class="sim-yazi" text-anchor="middle">%' + t + "</text>"; });
        h += '<text x="330" y="226" class="sim-yazi" text-anchor="middle">Ödülün gelme olasılığı</text>' +
          '<text x="52" y="34" class="sim-yazi" text-anchor="end">yüksek</text><text x="52" y="190" class="sim-yazi" text-anchor="end">düşük</text>' +
          '<path d="' + yolA + '" class="sim-egri-a"/><path d="' + yolB + '" class="sim-egri-b"/>' +
          '<line x1="' + x(p) + '" y1="30" x2="' + x(p) + '" y2="190" class="sim-esik sim-esik-ince"/>' +
          '<circle cx="' + x(p) + '" cy="' + y(a) + '" r="6" class="sim-nokta-a"/><circle cx="' + x(p) + '" cy="' + y(b) + '" r="6" class="sim-nokta-b"/>' +
          '<text x="596" y="' + (y(1) - 8) + '" class="sim-yazi sim-yazi-a" text-anchor="end">İpucuna anlık yanıt</text>' +
          '<text x="' + x(0.5) + '" y="' + (y(1) - 8) + '" class="sim-yazi sim-yazi-b" text-anchor="middle">Bekleme sırasında süregen etkinlik</text>';
        g.innerHTML = h;
        var m;
        if (p === 0.5) m = "Belirsizlik en yüksek: bekleme sırasındaki süregen etkinlik zirvede. “Belki” en güçlü çekimdir; bildirimin ve kumar makinesinin sırrı da bu.";
        else if (p === 1) m = "Ödül kesin: ipucuna anlık yanıt en yüksek, ama beklemede belirsizlik kalmadığı için süregen etkinlik düşük.";
        else if (p === 0) m = "Ödül hiç gelmeyecek: iki yanıt da düşük.";
        else m = "İpucuna anlık yanıt olasılıkla artar; bekleme sırasındaki süregen etkinlik ise belirsizlikle artar ve %50’de zirve yapar.";
        sonuc.textContent = m;
      }
      r.addEventListener("input", ciz);
      ciz();
    }
  };
  $$(".sim[data-sim]").forEach(function (s) {
    var f = SIMLER[s.dataset.sim], alan = $(".sim-alan", s);
    if (f && alan) { try { f(alan); } catch (e) { alan.textContent = "Etkinlik yüklenemedi."; } }
  });

  /* Kayıtlı durumu geri yükle */
  Object.keys(durum.sina).forEach(function (vid) {
    var v = document.getElementById("v-" + vid);
    if (!v) return;
    $$(".sina-madde", v).forEach(function (m) { var y = durum.sina[vid][m.dataset.no]; if (y) sinaUygula(m, y); });
  });
  Object.keys(durum.test).forEach(function (vid) {
    var v = document.getElementById("v-" + vid);
    if (!v) return;
    $$(".adim-test .test-madde", v).forEach(function (m) { var y = durum.test[vid][m.dataset.no]; if (y !== undefined && y !== null) testUygula(m, +y); });
  });
  gorunumler.forEach(function (v) {
    var vid = v.dataset.view, b = $(".okundu", v);
    if (b) b.setAttribute("aria-pressed", durum.okundu[vid] ? "true" : "false");
    skorYaz(vid);
  });

  rota();
})();
