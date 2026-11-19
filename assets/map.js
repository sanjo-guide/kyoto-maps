(function () {
  "use strict";

  const UI = {
    ja: {
      mapsBtn: "Googleマップで開く",
      time: "おすすめ時間",
      hours: "営業時間",
      photos: (n) => `写真 ${n}枚（横にスワイプ）`,
      more: "続きを読む",
      less: "閉じる",
      mapLabel: "ルートの地図",
      loadError: "データを読み込めませんでした。",
      rights: "© Piece Hostel Sanjo　写真・文章の無断転載はご遠慮ください（クレジット表記のある写真は各ライセンスに従います）。",
      access: "アクセス",
      photo: "写真",
      base: "起点",
    },
    en: {
      mapsBtn: "Open in Google Maps",
      time: "Suggested time",
      hours: "Hours",
      photos: (n) => `${n} photos (swipe)`,
      more: "Read more",
      less: "Show less",
      mapLabel: "Route map",
      loadError: "Could not load the map data.",
      rights: "© Piece Hostel Sanjo. Please do not reuse photos or text without permission (credited photos follow their own licenses).",
      access: "Access",
      photo: "Photo",
      base: "Base",
    },
  };

  const body = document.body;
  const routeId = body.dataset.route;
  const root = body.dataset.root || ""; // サイトのトップへの相対パス（例 "../"）
  const asset = (p) => (/^https?:\/\//.test(p) ? p : root + p);
  let lang = pickLang();
  let route = null;
  let map = null;
  const markers = [];

  function pickLang() {
    const q = new URLSearchParams(location.search).get("lang");
    if (q === "ja" || q === "en") return q;
    try {
      const saved = localStorage.getItem("lang");
      if (saved === "ja" || saved === "en") return saved;
    } catch (e) {}
    return (navigator.language || "").toLowerCase().startsWith("ja") ? "ja" : "en";
  }

  function el(tag, attrs, children) {
    const n = document.createElement(tag);
    for (const [k, v] of Object.entries(attrs || {})) {
      if (v == null || v === false) continue;
      if (k === "text") n.textContent = v;
      else if (k === "class") n.className = v;
      else n.setAttribute(k, v === true ? "" : v);
    }
    for (const c of [].concat(children || [])) if (c) n.append(c);
    return n;
  }

  // 改行を保ったまま段落にする（HTMLとしては解釈しない）
  function paragraphs(text) {
    return (text || "").split(/\n{2,}/).map((block) => {
      const p = el("p");
      block.split("\n").forEach((line, i) => {
        if (i) p.append(el("br"));
        p.append(document.createTextNode(line));
      });
      return p;
    });
  }

  function t(obj) {
    if (!obj) return "";
    return obj[lang] || obj.ja || obj.en || "";
  }

  function other(obj) {
    if (!obj) return "";
    const o = obj[lang === "ja" ? "en" : "ja"];
    return o && o !== t(obj) ? o : "";
  }

  function numBadge(spot) {
    return el("span", { class: "num", style: `background:${spot.color}`, "aria-hidden": "true", text: String(spot.no) });
  }

  // ---------- 地図 ----------
  function buildMap() {
    map = L.map("map", { scrollWheelZoom: false, tap: true });
    L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
      maxZoom: 19,
      attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
    }).addTo(map);

    const latlngs = route.spots.map((s) => [s.lat, s.lng]);
    // おすすめ集のように順番に巡らないページは "line": false で線を引かない
    if (route.line !== false) {
      L.polyline(latlngs, { color: "#2f6b3a", weight: 3, opacity: 0.55, dashArray: "6 8" }).addTo(map);
    }
    // 起点（例: 金沢駅）。番号なしの印で表示する
    if (route.base) {
      const b = route.base;
      const bm = L.marker([b.lat, b.lng], {
        icon: L.divIcon({ className: "pin base", html: '<span class="num">🚉</span>', iconSize: [30, 30], iconAnchor: [15, 15] }),
        title: t(b.name),
      }).addTo(map);
      bm.bindPopup(() => `${UI[lang].base}: ${t(b.name)}`);
      latlngs.push([b.lat, b.lng]);
    }

    route.spots.forEach((spot, i) => {
      const icon = L.divIcon({
        className: "pin",
        html: `<span class="num" style="background:${spot.color}">${spot.no}</span>`,
        iconSize: [30, 30],
        iconAnchor: [15, 15],
      });
      const m = L.marker([spot.lat, spot.lng], { icon, title: `${spot.no}. ${t(spot.name)}`, riseOnHover: true }).addTo(map);
      m.on("click", () => openSpot(i, { scroll: true, fly: false }));
      markers.push(m);
    });

    map.fitBounds(L.latLngBounds(latlngs), { padding: [24, 24] });
  }

  function setActiveMarker(i) {
    markers.forEach((m, j) => {
      const node = m.getElement();
      if (node) node.classList.toggle("active", i === j);
      m.setZIndexOffset(i === j ? 1000 : 0);
    });
  }

  // ---------- 一覧 ----------
  function renderHeader() {
    document.documentElement.lang = lang;
    document.getElementById("route-title").textContent = t(route.title);
    document.getElementById("map").setAttribute("aria-label", UI[lang].mapLabel);
    document.querySelectorAll(".lang button").forEach((b) => b.setAttribute("aria-pressed", String(b.dataset.lang === lang)));

    // 1番（ホステル）の説明を、ルート全体の紹介として上に出す
    const intro = document.getElementById("route-intro");
    const introText = t(route.summary) || t(route.spots[0] && route.spots[0].description);
    intro.textContent = introText;
    intro.classList.add("collapsed");
    const old = document.querySelector(".more-btn");
    if (old) old.remove();
    if (introText) {
      const btn = el("button", { type: "button", class: "more-btn", text: UI[lang].more, "aria-expanded": "false" });
      btn.addEventListener("click", () => {
        const open = intro.classList.toggle("collapsed") === false;
        btn.textContent = open ? UI[lang].less : UI[lang].more;
        btn.setAttribute("aria-expanded", String(open));
      });
      intro.after(btn);
    }

    // 関連ページ（例: 金沢市内 ⇔ 金沢から日帰り）へのリンク
    const oldRel = document.querySelector(".related");
    if (oldRel) oldRel.remove();
    if (route.related && route.related.length) {
      const rel = el("div", { class: "related" }, route.related.map((r) =>
        el("a", { href: root + r.href, text: "➜ " + t(r.label) })
      ));
      (document.querySelector(".more-btn") || intro).after(rel);
    }

    // route.source.note は管理用メモなので表示しない。ゲスト向けの注意書きは route.notice
    document.getElementById("source-note").textContent = t(route.notice);
    document.getElementById("rights").textContent = UI[lang].rights;
    // 作成者はページ下部に小さく出すだけにする（route.author があるページのみ）
    let author = document.getElementById("author");
    if (route.author) {
      if (!author) {
        author = el("p", { id: "author" });
        document.getElementById("rights").before(author);
      }
      author.textContent = t(route.author);
    } else if (author) author.remove();
  }

  function renderList() {
    const list = document.getElementById("spots");
    list.replaceChildren();
    route.spots.forEach((spot, i) => {
      const bodyId = `spot-body-${spot.no}`;
      const first = spot.photos[0];
      const toggle = el("button", { type: "button", class: "spot-toggle", "aria-expanded": "false", "aria-controls": bodyId }, [
        first ? el("img", { class: "thumb", src: asset(first.thumb || first.src), alt: "", loading: "lazy", decoding: "async" }) : null,
        el("span", { class: "spot-main" }, [
          el("span", { class: "spot-name" }, [numBadge(spot), el("span", { text: t(spot.name) })]),
          other(spot.name) ? el("span", { class: "spot-sub", text: other(spot.name) }) : null,
          t(spot.time) ? el("span", { class: "spot-time", text: `🕘 ${t(spot.time)}` }) : null,
        ]),
        el("span", { class: "chev", "aria-hidden": "true", text: "▾" }),
      ]);
      toggle.addEventListener("click", () => {
        const isOpen = toggle.getAttribute("aria-expanded") === "true";
        if (isOpen) closeSpot(i);
        else openSpot(i, { scroll: false, fly: true });
      });
      const li = el("li", { class: "spot", id: `spot-${spot.no}` }, [toggle, el("div", { class: "spot-body", id: bodyId, hidden: true })]);
      list.append(li);
    });
  }

  function fillBody(i) {
    const spot = route.spots[i];
    const box = document.getElementById(`spot-body-${spot.no}`);
    if (box.dataset.lang === lang) return;
    box.dataset.lang = lang;
    box.replaceChildren();

    if (spot.photos.length) {
      box.append(
        el("div", { class: "photos" }, spot.photos.map((p, k) => {
          // caption（{ja, en}）があれば写真の下に小さく出す（例: 「志摩の離れの茶室」）
          const cap = p.caption ? t(p.caption) : "";
          return el("figure", {}, [
            el("img", { src: asset(p.src), alt: cap || p.alt || `${t(spot.name)} ${k + 1}`, loading: "lazy", decoding: "async" }),
            cap ? el("figcaption", { text: cap }) : null,
          ]);
        }))
      );
      if (spot.photos.length > 1) box.append(el("p", { class: "photo-count", text: UI[lang].photos(spot.photos.length) }));
      // 他の人が撮った写真（CC ライセンス等）はクレジットを必ず表示する
      const credited = spot.photos.map((p, k) => [p, k]).filter(([p]) => p.credit);
      if (credited.length) {
        box.append(el("ul", { class: "photo-credits" }, credited.map(([p, k]) => {
          const c = p.credit;
          return el("li", {}, [
            document.createTextNode(`${UI[lang].photo} ${k + 1}: `),
            c.url ? el("a", { href: c.url, target: "_blank", rel: "noopener", text: c.author || c.url }) : document.createTextNode(c.author || ""),
            c.license ? document.createTextNode(" / ") : null,
            c.license && c.license_url ? el("a", { href: c.license_url, target: "_blank", rel: "noopener", text: c.license }) : (c.license ? document.createTextNode(c.license) : null),
          ]);
        })));
      }
    }

    const facts = [];
    if (t(spot.access)) facts.push([UI[lang].access, t(spot.access)]);
    if (t(spot.time)) facts.push([UI[lang].time, t(spot.time)]);
    if (t(spot.hours)) facts.push([UI[lang].hours, t(spot.hours)]);
    if (facts.length) {
      box.append(el("dl", { class: "facts" }, facts.map(([k, v]) => el("div", {}, [el("dt", { text: k }), el("dd", { text: v })]))));
    }

    // 見出し（例「一乗寺駅から鞍馬方面へ」）は日本語のみなので、日本語表示のときだけ出す
    // 見出しが {ja, en} のときは両言語で出す
    const heading = spot.heading && typeof spot.heading === "object" ? t(spot.heading) : (lang === "ja" ? spot.heading : null);
    if (heading) box.append(el("h3", { class: "spot-heading", text: heading }));
    box.append(el("div", { class: "desc" }, paragraphs(t(spot.description))));

    // スポットの中の「立ち寄り先」（例: ひがし茶屋街の中の 志摩）
    if (spot.subs && spot.subs.length) {
      box.append(el("div", { class: "subs" }, spot.subs.map((sub) =>
        el("section", { class: "sub" }, [
          el("h3", { text: t(sub.name) }),
          other(sub.name) ? el("p", { class: "sub-alt", text: other(sub.name) }) : null,
          ...paragraphs(t(sub.text)),
          sub.url ? el("a", { class: "sub-link", href: sub.url, target: "_blank", rel: "noopener", text: "📍 " + UI[lang].mapsBtn }) : null,
        ])
      )));
    }

    if (spot.links.length) {
      box.append(
        el("div", { class: "links" }, spot.links.map((l, k) => {
          const isMaps = /maps\.app\.goo\.gl|google\.[^/]+\/maps/.test(l.url);
          const label = isMaps && /^googlemaps$/i.test(l.label) ? UI[lang].mapsBtn : l.label;
          return el("a", { href: l.url, target: "_blank", rel: "noopener", class: k === 0 && isMaps ? "primary" : null, text: (isMaps ? "📍 " : "🔗 ") + label });
        }))
      );
    }
  }

  function openSpot(i, opts) {
    route.spots.forEach((_, j) => { if (j !== i) closeSpot(j); });
    const spot = route.spots[i];
    const li = document.getElementById(`spot-${spot.no}`);
    const toggle = li.querySelector(".spot-toggle");
    fillBody(i);
    li.querySelector(".spot-body").hidden = false;
    toggle.setAttribute("aria-expanded", "true");
    li.classList.add("active");
    setActiveMarker(i);
    if (opts.fly === "instant") map.setView([spot.lat, spot.lng], 15, { animate: false });
    else if (opts.fly) map.flyTo([spot.lat, spot.lng], Math.max(map.getZoom(), 15), { duration: 0.6 });
    else map.panTo([spot.lat, spot.lng]);
    if (opts.scroll || opts.fly) requestAnimationFrame(() => li.scrollIntoView({ behavior: "smooth", block: "start" }));
    history.replaceState(null, "", `#${spot.no}`);
  }

  function closeSpot(i) {
    const spot = route.spots[i];
    const li = document.getElementById(`spot-${spot.no}`);
    if (!li) return;
    li.querySelector(".spot-body").hidden = true;
    li.querySelector(".spot-toggle").setAttribute("aria-expanded", "false");
    li.classList.remove("active");
  }

  function setLang(next) {
    lang = next;
    try { localStorage.setItem("lang", lang); } catch (e) {}
    const openIdx = route.spots.findIndex((s) => document.getElementById(`spot-${s.no}`).classList.contains("active"));
    renderHeader();
    renderList();
    markers.forEach((m, i) => m.getElement() && m.getElement().setAttribute("title", `${route.spots[i].no}. ${t(route.spots[i].name)}`));
    if (openIdx >= 0) openSpot(openIdx, { scroll: false, fly: false });
  }

  document.querySelectorAll(".lang button").forEach((b) => b.addEventListener("click", () => setLang(b.dataset.lang)));

  fetch(`${root}data/routes/${routeId}.json`)
    .then((r) => { if (!r.ok) throw new Error(r.status); return r.json(); })
    .then((data) => {
      route = data;
      document.title = `${t(route.title)} | Piece Hostel Sanjo`;
      renderHeader();
      renderList();
      buildMap();
      const n = parseInt(location.hash.slice(1), 10);
      const idx = route.spots.findIndex((s) => s.no === n);
      if (idx >= 0) {
        openSpot(idx, { scroll: false, fly: "instant" });
        // ページを開いた直後はブラウザがスクロール位置を戻すことがあるので、少し待ってから移動する
        setTimeout(() => document.getElementById(`spot-${route.spots[idx].no}`).scrollIntoView({ block: "start" }), 300);
      }
    })
    .catch(() => { document.getElementById("route-title").textContent = UI[lang].loadError; });
})();
