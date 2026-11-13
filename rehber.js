/* Davranışın Biyolojisi — görünümler, kendini sına, şekil kutusu, atıf penceresi, arama */
(function () {
  "use strict";
  var kok = document.documentElement;
  kok.classList.add("js");

  var ANAHTAR = "davranisin-biyolojisi:v1";
  var durum = oku();
  durum.sina = durum.sina || {};
  durum.okundu = durum.okundu || {};
  function oku() { try { return JSON.parse(localStorage.getItem(ANAHTAR) || "{}") || {}; } catch (e) { return {}; } }
  function yaz() { try { localStorage.setItem(ANAHTAR, JSON.stringify(durum)); } catch (e) { /* özel pencere */ } }

  function $(s, r) { return (r || document).querySelector(s); }
  function $$(s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); }
  function kacis(s) { return String(s).replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; }); }
  function parla(el) { el.classList.remove("parla"); void el.offsetWidth; el.classList.add("parla"); }
  function katla(s) { return s.toLocaleLowerCase("tr").replace(/ı/g, "i").normalize("NFD").replace(/[̀-ͯ]/g, ""); }

  var gorunumler = $$(".view");
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
    var vid = v.dataset.view;
    if (location.hash !== adres(v)) history.pushState(null, "", adres(v));
    goster(vid, null, false);
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

  /* Kendini sına */
  function sinaUygula(m, yanit) {
    var bildi = yanit === m.dataset.dogru;
    m.classList.add("cevaplandi");
    m.classList.toggle("bildi", bildi);
    m.classList.toggle("bilemedi", !bildi);
    $$("button[data-yanit]", m).forEach(function (b) {
      b.setAttribute("aria-pressed", b.dataset.yanit === yanit ? "true" : "false");
      b.disabled = true;
    });
    var ac = $(".sina-aciklama", m);
    if (!ac) return;
    var et = $(".sonuc-etiket", ac);
    if (!et) { et = document.createElement("span"); et.className = "sonuc-etiket"; ac.insertBefore(et, ac.firstChild); }
    et.textContent = bildi ? "✓ Bildiniz" : "✗ Bu sefer olmadı";
  }
  function sinaTemizle(m) {
    m.classList.remove("cevaplandi", "bildi", "bilemedi");
    $$("button[data-yanit]", m).forEach(function (b) { b.removeAttribute("aria-pressed"); b.disabled = false; });
    var et = $(".sonuc-etiket", m);
    if (et) et.remove();
  }
  function sayac(vid) {
    var v = document.getElementById("v-" + vid);
    var maddeler = v ? $$(".sina-madde", v) : [];
    var cev = durum.sina[vid] || {}, n = 0, d = 0;
    maddeler.forEach(function (m) { var y = cev[m.dataset.no]; if (y) { n++; if (y === m.dataset.dogru) d++; } });
    return { toplam: maddeler.length, n: n, d: d };
  }
  function skorGuncelle(vid) {
    var s = sayac(vid);
    var sk = $('[data-skor="' + vid + '"]');
    if (sk) sk.textContent = s.n ? (s.d + " / " + s.toplam + " doğru" + (s.n < s.toplam ? " · " + (s.toplam - s.n) + " ifade kaldı" : "")) : "";
    var sf = $('[data-sifirla="' + vid + '"]');
    if (sf) sf.hidden = !s.n;
    durumGuncelle(vid);
  }
  function durumGuncelle(vid) {
    var s = sayac(vid), p = [];
    if (durum.okundu[vid]) p.push("✓ Okundu");
    if (s.n) p.push("Test " + s.d + "/" + s.toplam);
    var kart = $('[data-durum="' + vid + '"]');
    if (kart) kart.textContent = p.join(" · ");
    var nav = $('[data-durum-nav="' + vid + '"]');
    if (nav) nav.textContent = durum.okundu[vid] ? "✓" : "";
    var oturumlar = gorunumler.filter(function (v) { return v.classList.contains("oturum"); });
    var ok = oturumlar.filter(function (v) { return durum.okundu[v.dataset.view]; }).length;
    var il = $("[data-ilerleme]");
    if (il) il.textContent = ok ? ok + " / " + oturumlar.length + " oturum okundu" : "";
  }

  /* Karışık test */
  var kAlan = $(".karisik-alan"), kBasla = $(".karisik-basla");
  var kListe = [], kSira = 0, kDogru = 0;
  function karistir(a) {
    for (var i = a.length - 1; i > 0; i--) { var j = Math.floor(Math.random() * (i + 1)); var t = a[i]; a[i] = a[j]; a[j] = t; }
    return a;
  }
  function kGoster() {
    if (kSira >= kListe.length) {
      var oran = kDogru / kListe.length;
      kAlan.innerHTML = '<p class="karisik-son">' + kDogru + " / " + kListe.length + " doğru</p><p>" +
        (oran >= 0.85 ? "Çok iyi. Kova yok, merdiven var." : oran >= 0.6 ? "İyi. Yanlış yaptığınız ifadelerin oturumlarına dönmek iyi olur."
          : "Oturumların “Beş ana fikir” bölümleriyle başlamak iyi bir tekrar olur.") + "</p>";
      kBasla.hidden = false;
      kBasla.textContent = "Yeniden başlat";
      kBasla.focus();
      return;
    }
    var asil = kListe[kSira], m = asil.cloneNode(true);
    sinaTemizle(m);
    m.removeAttribute("data-ara");
    var kaynak = asil.closest(".view");
    kAlan.innerHTML = '<p class="karisik-ilerleme">İfade ' + (kSira + 1) + " / " + kListe.length + " · " +
      '<a href="' + adres(kaynak) + '">' + kacis(baslik(kaynak)) + "</a></p>";
    var ol = document.createElement("ol");
    ol.className = "sina sina-tek";
    ol.appendChild(m);
    kAlan.appendChild(ol);
    var b = $("button[data-yanit]", m);
    if (b) b.focus();
  }
  if (kBasla) kBasla.addEventListener("click", function () {
    kListe = karistir($$(".view.oturum .sina-madde"));
    kSira = 0; kDogru = 0;
    kBasla.hidden = true;
    kGoster();
  });

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
    $(".isik-resim", isik).scrollTop = 0;
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
      var m = y.closest(".sina-madde");
      sinaUygula(m, y.dataset.yanit);
      if (m.closest(".karisik-alan")) {
        if (y.dataset.yanit === m.dataset.dogru) kDogru++;
        var sn = document.createElement("button");
        sn.type = "button";
        sn.className = "dugme karisik-sonraki";
        sn.textContent = kSira + 1 < kListe.length ? "Sonraki ifade →" : "Sonucu gör";
        kAlan.appendChild(sn);
        sn.focus();
        return;
      }
      var vid = m.closest(".view").dataset.view;
      (durum.sina[vid] = durum.sina[vid] || {})[m.dataset.no] = y.dataset.yanit;
      yaz();
      skorGuncelle(vid);
      return;
    }
    if (t.closest(".karisik-sonraki")) { kSira++; kGoster(); return; }
    var sf = t.closest(".sina-sifirla");
    if (sf) {
      var id = sf.dataset.sifirla;
      delete durum.sina[id];
      yaz();
      $$("#v-" + id + " .sina-madde").forEach(sinaTemizle);
      skorGuncelle(id);
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
    if (e.key === "/" && !/^(INPUT|TEXTAREA)$/.test(document.activeElement.tagName) && araK) { e.preventDefault(); araK.focus(); }
  });

  /* Kayıtlı durumu geri yükle */
  Object.keys(durum.sina).forEach(function (vid) {
    var v = document.getElementById("v-" + vid);
    if (!v) return;
    $$(".sina-madde", v).forEach(function (m) { var y = durum.sina[vid][m.dataset.no]; if (y) sinaUygula(m, y); });
  });
  gorunumler.forEach(function (v) {
    var vid = v.dataset.view, b = $(".okundu", v);
    if (b) b.setAttribute("aria-pressed", durum.okundu[vid] ? "true" : "false");
    skorGuncelle(vid);
  });

  rota();
})();
