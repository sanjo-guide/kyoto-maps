/* Tango & Tajima guide — renders the EN/JA guide from window.GUIDE (js/data.js). Copied from shikoku/js/app.js, plus model plans (G.plans). */
(function () {
  "use strict";
  const G = window.GUIDE;
  const UI = {
    title: { en: "My Tango & Tajima Picks", ja: "丹後・但馬のおすすめ" },
    madeby: { en: "Made by Toshi", ja: "Toshiが作成しました" },
    home: { en: "← All maps", ja: "← マップ一覧" },
   howto_h: { en: "How to use this page", ja: "このページの使い方" },
    howto_1: { en: "Use the buttons at the top to switch between “Toyooka” and “Day trips”. Example itineraries are in “Model plans”.", ja: "上のボタンで「豊岡」と「丹後・竹田」を切り替えられます。回り方の例は「モデルプラン」にあります。" },
    howto_2: { en: "Swipe or tap the arrows to see more photos. The numbers match the numbers on the map.", ja: "写真は左右に送って見られます。番号は、地図の番号と同じです。" },
    howto_3: { en: "Tap a place’s “Google Maps” button to open it in Google Maps. “← All maps” at the top takes you back to the list.", ja: "各スポットの「Googleマップ」ボタンで、Googleマップに場所を開けます。一覧に戻るときは、いちばん上の「← マップ一覧」を。" },
    home_full: { en: "Back to all maps", ja: "マップ一覧へ戻る" },
    subtitle: { en: "A day trip to Amanohashidate and Ine, or a few nights based in Toyooka.", ja: "京都から日帰りで天橋立・伊根へ。泊まるなら、豊岡を拠点に城崎温泉・竹野・舞鶴・竹田城跡へ。" },
    nav_city: { en: "Toyooka", ja: "豊岡" }, nav_food: { en: "Food", ja: "食べる" }, nav_trips: { en: "Day trips", ja: "丹後・竹田" }, nav_map: { en: "Map", ja: "地図" },
    jump_city: { en: "Toyooka, Kinosaki, Izushi & Takeno", ja: "豊岡・城崎・出石・竹野" }, jump_food: { en: "place to stay", ja: "拠点の宿" }, jump_trips: { en: "areas further afield", ja: "天橋立・伊根・舞鶴・竹田のエリア" },
    group: { en: "AREA", ja: "エリア" },
    map_h: { en: "Where everything is", ja: "おすすめの場所の地図" },
    tab_city: { en: "Toyooka, Kinosaki & Izushi", ja: "豊岡・城崎・出石・竹野" }, tab_trips: { en: "Amanohashidate, Ine, Maizuru & Takeda", ja: "天橋立・伊根・舞鶴・竹田" },
    map_note: { en: "Tap a number to jump to that place. Pinch or use + / − to zoom. For directions, use each place’s “Google Maps” button.", ja: "番号をタップすると、その場所の紹介へ移動します。拡大・縮小は2本指か「＋／−」ボタンで。道順は各スポットの「Googleマップ」ボタンで確認してください。" },
    map_fb: { en: "The map images could not load, so a simple map is shown instead.", ja: "地図の画像を読み込めなかったため、簡易な地図を表示しています。" },
    show_all: { en: "Show all", ja: "全体を表示" },
    city_h: { en: "Around Toyooka", ja: "豊岡と、そのまわり" }, city_sub: { en: "The old market, Kinosaki Onsen, Genbudo, Izushi and the sea at Takeno", ja: "公設市場・城崎温泉・玄武洞・出石・竹野の海" },
    food_h: { en: "Where to stay", ja: "拠点にするならここ" }, food_sub: { en: "If you’re staying a night or more, base yourself here.", ja: "1泊以上するなら、豊岡のこのゲストハウスがおすすめです。" },
    trips_h: { en: "Amanohashidate, Ine, Maizuru and Takeda", ja: "天橋立・伊根・舞鶴・竹田城跡" },
    trips_sub: { en: "Day trips from Toyooka, or from Kyoto.", ja: "豊岡から、または京都から日帰りで。" },
    cr_h: { en: "Photo credits", ja: "写真のクレジット" },
    cr_toshi: { en: "Photos without a credit were taken by Toshi.", ja: "クレジットのない写真は、Toshiが撮影したものです。" },
    cr_map: { en: "Map: OpenFreeMap / © OpenMapTiles / © OpenStreetMap contributors. Outlines in the simple map (shown only if the map images cannot load): Global Map Japan (GSI), via dataofjapan/land.", ja: "地図：OpenFreeMap / © OpenMapTiles / © OpenStreetMap contributors。簡易地図（地図の画像を読み込めないときだけ表示）の輪郭：地球地図日本（国土地理院）をもとに作成（dataofjapan/land）。" },
    disclaimer: { en: "Opening hours, prices and booking rules can change. Please check the official information before you go.", ja: "営業時間・料金・予約方法は変わることがあります。お出かけ前に公式の情報をご確認ください。" },
    to_top: { en: "Back to top ↑", ja: "ページの先頭へ ↑" },
    gmap: { en: "Google Maps", ja: "Googleマップ" },
    map_mini: { en: "Map", ja: "地図" },
    photo_of: { en: "Photo", ja: "写真" },
    prev: { en: "Previous photo", ja: "前の写真" }, next: { en: "Next photo", ja: "次の写真" },
    base: { en: "Hostel Act (base)", ja: "Hostel Act（拠点）" },
    plans_h: { en: "Model plans", ja: "モデルプラン" }, plans_sub: { en: "A day trip from Kyoto, or 1–3 nights based at Hostel Act in Toyooka.", ja: "京都から日帰り、または豊岡のHostel Actを拠点に1〜3泊。" }, plan_links: { en: "See also:", ja: "あわせて見る：" },
    sea: { en: "SEA OF JAPAN", ja: "日 本 海" }, bay: { en: "WAKASA BAY", ja: "若狭湾" },
    note_h: { en: "Note:", ja: "メモ：" },
    visits: { en: "Times I've been", ja: "行った回数" },
    scale: { en: "2 km", ja: "2 km" }, scale_r: { en: "20 km", ja: "20 km" },
    via: { en: "via Wikimedia Commons", ja: "Wikimedia Commons" },
  };

  const state = { lang: "en", map: "city" };
  try {
    const s = localStorage.getItem("kyoto-maps-lang");
    if (s === "en" || s === "ja") state.lang = s;
    else if ((navigator.language || "").toLowerCase().startsWith("ja")) state.lang = "ja";
  } catch (e) { if ((navigator.language || "").toLowerCase().startsWith("ja")) state.lang = "ja"; }

  const L = () => state.lang;
  const t = (k) => (UI[k] ? UI[k][L()] : k);
  const tr = (o) => (o ? (typeof o === "string" ? o : (o[L()] != null ? o[L()] : o.en)) : "");
  const esc = (s) => String(s == null ? "" : s).replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
  const other = () => (L() === "en" ? "ja" : "en");

  const ICON = {
    pin: '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 21s-7-6.2-7-11.5A7 7 0 0 1 19 9.5C19 14.8 12 21 12 21z"/><circle cx="12" cy="9.5" r="2.5"/></svg>',
    ext: '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M14 4h6v6M20 4l-9 9M18 14v5a1 1 0 0 1-1 1H5a1 1 0 0 1-1-1V7a1 1 0 0 1 1-1h5"/></svg>',
    train: '<svg viewBox="0 0 24 24" aria-hidden="true"><rect x="5" y="3" width="14" height="14" rx="3"/><path d="M5 11h14M9 21l-2-4M15 21l2-4M8.5 14h.01M15.5 14h.01"/></svg>',
    left: '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M15 5l-7 7 7 7"/></svg>',
    right: '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M9 5l7 7-7 7"/></svg>',
    again: '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M20 11a8 8 0 1 0-2.3 5.7M20 4v7h-7"/></svg>',
  };

  const LIC = { "CC0": "https://creativecommons.org/publicdomain/zero/1.0/", "Public domain": "https://creativecommons.org/publicdomain/mark/1.0/" };
  const licUrl = (l) => LIC[l] || ("https://creativecommons.org/licenses/" + (/SA/.test(l) ? "by-sa/" : "by/") + ((l.match(/[\d.]+$/) || ["4.0"])[0]) + "/");

  /* ---------- cards ---------- */
  function slides(s) {
    const n = s.photos.length;
    return s.photos.map((p, i) => {
      const tall = p.h > p.w;
      const cap = p.cap ? `<span class="cap">${esc(tr(p.cap))}</span>` : "";
      const cr = p.credit ? `<span class="credit">${esc(t("photo_of"))}: <a href="${esc(p.credit.page)}" target="_blank" rel="noopener">${esc(p.credit.author)}</a> / ${esc(p.credit.license)}</span>` : "";
      const alt = (tr(p.cap) || tr(s)) + ` (${i + 1}/${n})`;
      return `<figure class="slide${tall ? " tall" : ""}">${tall ? `<img class="bgblur" src="img/${esc(p.f)}" alt="" aria-hidden="true" loading="lazy">` : ""}<img src="img/${esc(p.f)}" alt="${esc(alt)}" width="${p.w}" height="${p.h}" loading="${i === 0 ? "eager" : "lazy"}" decoding="async">${cap}${cr}</figure>`;
    }).join("");
  }
  function carousel(s) {
    const many = s.photos.length > 1;
    return `<div class="car"><div class="track" tabindex="0" aria-label="${esc(tr(s))}">${slides(s)}</div>` +
      (many ? `<button type="button" class="cbtn prev" aria-label="${esc(t("prev"))}" disabled>${ICON.left}</button><button type="button" class="cbtn next" aria-label="${esc(t("next"))}">${ICON.right}</button><span class="count">1 / ${s.photos.length}</span>` : "") + `</div>`;
  }
  const mapBtn = (url) => `<a class="btn pri" href="${esc(url)}" target="_blank" rel="noopener">${ICON.pin}${esc(t("gmap"))}</a>`;
  function subBlock(sb) {
    const extra = (sb.extra || []).map((x) => ` <a class="mini" href="${esc(x.map)}" target="_blank" rel="noopener">${esc(tr(x))} · ${esc(t("map_mini"))}</a>`).join("");
    const m = sb.map ? ` <a class="mini" href="${esc(sb.map)}" target="_blank" rel="noopener">${esc(t("map_mini"))}</a>` : "";
    return `<div class="sub"><h4><span class="dot"></span><span>${esc(tr(sb))}</span>${m}${extra}</h4><p>${esc(tr(sb.t))}</p></div>`;
  }
  function groupHead(s) {
    const body = (s.body && s.body[L()]) || [];
    return `<div class="ghead" id="${esc(s.id)}"><p class="gkick">${esc(t("group"))}</p><h3>${esc(tr(s))}</h3>
      ${s.time ? `<p class="time">${ICON.train}<span>${esc(tr(s.time))}</span></p>` : ""}${body.map((p) => `<p>${esc(p)}</p>`).join("")}</div>`;
  }
  function card(s, kind) {
    if (s.kind === "group") return groupHead(s);
    const body = (s.body && s.body[L()]) || [];
    const time = (s.time ? `<p class="time">${ICON.train}<span>${esc(tr(s.time))}</span></p>` : "") +
      (s.visits ? `<p class="time visits">${ICON.again}<span>${esc(tr(s.visits))}</span></p>` : "");
    const subs = s.subs ? `<div class="subs">${s.subs.map(subBlock).join("")}</div>` : "";
    const note = s.note ? `<p class="note"><b>${esc(t("note_h"))}</b> ${esc(tr(s.note))}</p>` : "";
    const acts = [];
    if (s.map) acts.push(mapBtn(s.map));
    (s.extra_map || []).forEach((x) => acts.push(`<a class="btn" href="${esc(x.map)}" target="_blank" rel="noopener">${ICON.pin}${esc(tr(x))}</a>`));
    (s.links || []).forEach((x) => acts.push(`<a class="btn" href="${esc(x.url)}" target="_blank" rel="noopener">${ICON.ext}${esc(tr(x))}</a>`));
    return `<article class="card ${kind}" id="${esc(s.id)}">${carousel(s)}<div class="body">
      <div class="titlerow"><span class="num">${esc(s.no)}</span><div><h3>${esc(tr(s))}</h3><p class="alt" lang="${other()}">${esc(s[other()])}</p></div></div>
      ${time}${body.length ? `<div class="txt">${body.map((p) => `<p>${esc(p)}</p>`).join("")}</div>` : ""}${subs}${note}
      ${acts.length ? `<div class="acts">${acts.join("")}</div>` : ""}</div></article>`;
  }

  function wireCarousels(root) {
    root.querySelectorAll(".car").forEach((car) => {
      const track = car.querySelector(".track");
      const prev = car.querySelector(".prev"), next = car.querySelector(".next"), count = car.querySelector(".count");
      if (!prev) return;
      const n = track.children.length;
      const idx = () => Math.round(track.scrollLeft / Math.max(1, track.clientWidth));
      const upd = () => { const i = idx(); count.textContent = `${i + 1} / ${n}`; prev.disabled = i <= 0; next.disabled = i >= n - 1; };
      const go = (d) => track.scrollTo({ left: (idx() + d) * track.clientWidth, behavior: "smooth" });
      prev.addEventListener("click", () => go(-1));
      next.addEventListener("click", () => go(1));
      track.addEventListener("scroll", () => { window.requestAnimationFrame(upd); }, { passive: true });
      track.addEventListener("keydown", (e) => { if (e.key === "ArrowRight") { e.preventDefault(); go(1); } if (e.key === "ArrowLeft") { e.preventDefault(); go(-1); } });
    });
  }

  /* ---------- maps ---------- */
  const CITY_BOX = { lon0: 134.70, lon1: 134.92, lat0: 35.44, lat1: 35.67, W: 600 };   // 出石（南）まで入る範囲
  CITY_BOX.c = Math.cos(((CITY_BOX.lat0 + CITY_BOX.lat1) / 2) * Math.PI / 180);
  CITY_BOX.k = CITY_BOX.W / ((CITY_BOX.lon1 - CITY_BOX.lon0) * CITY_BOX.c);
  CITY_BOX.H = Math.round((CITY_BOX.lat1 - CITY_BOX.lat0) * CITY_BOX.k);
  const cp = (lat, lon) => [(lon - CITY_BOX.lon0) * CITY_BOX.c * CITY_BOX.k, (CITY_BOX.lat1 - lat) * CITY_BOX.k];
  const HOME = [35.54360, 134.81892];   // Hostel Act（拠点）
  const BASE = HOME;
  const R = G.region;
  const rp = (lat, lon) => [(lon - R.lon0) * R.c * R.k, (R.lat1 - lat) * R.k];
  const LAB = { izushi: [-18, 5, "end"] };   // label side per place id in the simple (fallback) city map: [dx, dy, anchor]

  const f1 = (n) => n.toFixed(1);
  function marker(x, y, label, cls, id, r) {
    return `<g class="mk ${cls}" tabindex="0" role="button" data-go="${esc(id)}" aria-label="${esc(label)}"><circle cx="${f1(x)}" cy="${f1(y)}" r="${r || 14}"/><text x="${f1(x)}" y="${f1(y + 5.5)}">${esc(label.split(" ")[0])}</text></g>`;
  }
  function lab(x, y, dx, dy, anchor, text, cls) {
    return `<text class="m-lab${cls ? " " + cls : ""}" x="${f1(x + dx)}" y="${f1(y + dy)}" text-anchor="${anchor}">${esc(text)}</text>`;
  }
  function citySVG() {
    const { W, H } = CITY_BOX;
    let s = `<svg viewBox="0 0 ${W} ${H}" role="img" aria-label="${esc(t("tab_city"))}"><rect class="m-bg" width="${W}" height="${H}" rx="3"/>`;
    for (let lon = 134.70; lon < CITY_BOX.lon1; lon += 0.02) { const [x] = cp(CITY_BOX.lat0, lon); s += `<line class="m-grid" x1="${f1(x)}" y1="0" x2="${f1(x)}" y2="${H}"/>`; }
    for (let lat = 35.44; lat < CITY_BOX.lat1; lat += 0.02) { const [, y] = cp(lat, CITY_BOX.lon0); s += `<line class="m-grid" x1="0" y1="${f1(y)}" x2="${W}" y2="${f1(y)}"/>`; }
    G.refs.forEach((r) => {
      const [x, y] = cp(r.lat, r.lon);
      if (r.kind === "park") s += `<circle class="m-park" cx="${f1(x)}" cy="${f1(y)}" r="16"/><text class="m-ref" x="${f1(x)}" y="${f1(y + 4)}" text-anchor="middle">${esc(tr(r))}</text>`;
      else s += `<text class="m-ref" x="${f1(x)}" y="${f1(y + 32)}" text-anchor="middle">${esc(tr(r))}</text>`;
    });
    G.city.forEach((p) => { const [x, y] = cp(p.lat, p.lon); const l = LAB[p.id] || [18, 5, "start"]; s += lab(x, y, l[0], l[1], l[2], tr(p.short)); });
    G.food.forEach((p) => {
      if (p.pins) p.pins.forEach((q) => { const [x, y] = cp(q.lat, q.lon); s += lab(x, y, q.dx || 18, q.dy || 5, q.anchor || "start", tr(q)); });
      else { const [x, y] = cp(p.lat, p.lon); const l = LAB[p.id] || [18, 5, "start"]; s += lab(x, y, l[0], l[1], l[2], tr(p.short)); }
    });
    G.city.forEach((p) => { const [x, y] = cp(p.lat, p.lon); s += marker(x, y, String(p.no) + " " + tr(p), "city", p.id); });
    G.food.forEach((p) => {
      const pts = p.pins || [{ lat: p.lat, lon: p.lon }];
      pts.forEach((q) => { const [x, y] = cp(q.lat, q.lon); s += marker(x, y, String(p.no) + " " + tr(p), "food", p.id); });
    });
    // north arrow + scale bar (1 km)
    const px500 = 2.0 / 111.0 * CITY_BOX.k;
    s += `<g transform="translate(${W - 34},30)"><path d="M0,-16 L7,6 L0,1 L-7,6 Z" fill="currentColor" class="m-ref"/><text class="m-small" x="0" y="22" text-anchor="middle">N</text></g>`;
    s += `<line class="m-scale" x1="20" y1="${H - 22}" x2="${f1(20 + px500)}" y2="${H - 22}"/><line class="m-scale" x1="20" y1="${H - 27}" x2="20" y2="${H - 17}"/><line class="m-scale" x1="${f1(20 + px500)}" y1="${H - 27}" x2="${f1(20 + px500)}" y2="${H - 17}"/><text class="m-small" x="${f1(20 + px500 / 2)}" y="${H - 30}" text-anchor="middle">${esc(t("scale"))}</text>`;
    return s + `</svg>`;
  }
  function regionSVG() {
    const W = R.W, H = R.H;
    let s = `<svg viewBox="0 0 ${W} ${H}" role="img" aria-label="${esc(t("tab_trips"))}"><rect class="m-sea" width="${W}" height="${H}" rx="3"/>`;
    R.prefs.forEach((p) => { s += `<path class="m-land${[26, 28].includes(p.id) ? " home" : ""}" d="${p.d}"/>`; });
    const PL = [
      [35.33, 135.20, { en: "KYOTO", ja: "京都府" }], [35.40, 134.68, { en: "HYOGO", ja: "兵庫県" }],
      [35.50, 135.45, { en: "FUKUI", ja: "福井県" }],
    ];
    PL.forEach(([la, lo, n]) => { const [x, y] = rp(la, lo); s += `<text class="m-plab" x="${f1(x)}" y="${f1(y)}" text-anchor="middle">${esc(tr(n))}</text>`; });
    { const [x, y] = rp(35.72, 134.95); s += `<text class="m-sealab" x="${f1(x)}" y="${f1(y)}" text-anchor="middle">${esc(t("sea"))}</text>`; }
    { const [x, y] = rp(35.62, 135.42); s += `<text class="m-sealab" x="${f1(x)}" y="${f1(y)}" text-anchor="middle" style="font-size:11px;letter-spacing:.12em">${esc(t("bay"))}</text>`; }
    // labels first, markers on top
    const DX = { start: 14, end: -14, middle: 0 };
    G.trips.forEach((p) => (p.pins || []).forEach((q) => { const [x, y] = rp(q.lat, q.lon); const an = q.anchor || "start"; s += lab(x, y, q.dx != null ? q.dx : DX[an], q.dy != null ? q.dy : (an === "middle" ? -16 : 4), an, tr(q), "sm"); }));
    const [bx, by] = rp(BASE[0], BASE[1]);
    s += `<path class="m-base" transform="translate(${f1(bx)},${f1(by)})" d="M0,-13 L3.8,-4 L13,-4 L5.6,1.8 L8.3,11 L0,5.5 L-8.3,11 L-5.6,1.8 L-13,-4 L-3.8,-4 Z"/>`;
    s += `<text class="m-baselab" x="${f1(bx + 16)}" y="${f1(by + 5)}">${esc(t("base"))}</text>`;
    G.trips.forEach((p) => (p.pins || []).forEach((q) => { const [x, y] = rp(q.lat, q.lon); s += marker(x, y, String(p.no) + " " + tr(q), "trip", p.id, 12); }));
    const px20 = 20 / 111.0 * R.k;
    s += `<g transform="translate(${W - 30},30)"><path d="M0,-16 L7,6 L0,1 L-7,6 Z" fill="currentColor" class="m-ref"/><text class="m-small" x="0" y="22" text-anchor="middle">N</text></g>`;
    s += `<line class="m-scale" x1="${W - 20 - px20}" y1="${H - 22}" x2="${W - 20}" y2="${H - 22}"/><line class="m-scale" x1="${f1(W - 20 - px20)}" y1="${H - 27}" x2="${f1(W - 20 - px20)}" y2="${H - 17}"/><line class="m-scale" x1="${W - 20}" y1="${H - 27}" x2="${W - 20}" y2="${H - 17}"/><text class="m-small" x="${f1(W - 20 - px20 / 2)}" y="${H - 30}" text-anchor="middle">${esc(t("scale_r"))}</text>`;
    return s + `</svg>`;
  }
  function renderMap(refit) {
    document.querySelectorAll(".tabs button").forEach((b) => b.setAttribute("aria-selected", String(b.dataset.map === state.map)));
    const tab = state.map === "city" ? "tab-city" : "tab-trips";
    if (mapFailed || !lmap) {
      const box = document.getElementById("svgmap");
      box.innerHTML = state.map === "city" ? citySVG() : regionSVG();
      box.setAttribute("aria-labelledby", tab);
      return;
    }
    document.getElementById("lmap").setAttribute("aria-labelledby", tab);
    if (layer) lmap.removeLayer(layer);
    layer = buildLayer(state.map).addTo(lmap);
    const fb = document.getElementById("lfit"); if (fb) fb.textContent = t("show_all");
    if (tlView !== state.map) useTiles(state.map);   // also fits the view
    else if (refit) fitCurrent();
    labelsByZoom();
  }
  function goTo(id) {
    const el = document.getElementById(id); if (!el) return;
    el.scrollIntoView({ behavior: "smooth", block: "start" });
    el.classList.add("flash"); setTimeout(() => el.classList.remove("flash"), 1600);
  }


  /* ---------- real map (Leaflet + 全マップ共通の地図スタイル ../assets/basemap.js) ---------- */
  // 地図は Googleマップに近い見た目（町名やお店の名前は出さず、紹介する場所が目立つ）。
  // 読み込めないとき（WebGL が使えない端末など）は簡易な図（SVG）に切り替える。
  const DIR = { start: "right", end: "left", middle: "top" };
  const LBL_MIN = { city: 13, trips: 8 };   // hide name labels when zoomed out further than this
  const LF = window.L;
  let lmap = null, layer = null, base = null, gl = null, tlView = null, mapFailed = !LF || !window.KM_BASEMAP || !window.maplibregl;
  const VIEW = { city: { minZoom: 11, maxZoom: 18 }, trips: { minZoom: 7, maxZoom: 16 } };
  function useTiles(which) {
    const v = VIEW[which];
    // set the zoom limits directly (setMinZoom/setMaxZoom start an animation that would undo the fit below)
    lmap.options.minZoom = v.minZoom; lmap.options.maxZoom = v.maxZoom; lmap.fire("zoomlevelschange");
    tlView = which;
    fitCurrent();
  }
  const allBounds = {};
  function mkIcon(text, cls, size) {
    return LF.divIcon({ className: "lmk " + cls, html: `<span>${esc(text)}</span>`, iconSize: [size, size], iconAnchor: [size / 2, size / 2] });
  }
  function addPin(group, lat, lon, num, label, cls, id, dir, size, minor) {
    const m = LF.marker([lat, lon], { icon: mkIcon(num, cls, size), title: num + " " + label, riseOnHover: true, keyboard: true });
    const OFF = { left: [-12, 0], top: [0, -12], bottom: [0, 12], right: [12, 0] };
    m.bindTooltip(esc(label), { permanent: true, direction: dir || "right", offset: OFF[dir || "right"], className: "ltip ltip-" + cls + (minor ? " minor" : ""), opacity: 1 });
    if (id) m.on("click", () => goTo(id));
    m.addTo(group);
    return [lat, lon];
  }
  function buildLayer(which) {
    const g = LF.layerGroup(); const pts = [];
    if (which === "city") {
      G.city.forEach((p) => { const l = LAB[p.id] || [0, 0, "start"]; pts.push(addPin(g, p.lat, p.lon, String(p.no), tr(p.short), "city", p.id, DIR[l[2]], 28)); });
      G.food.forEach((p) => {
        (p.pins || [{ lat: p.lat, lon: p.lon, en: p.short.en, ja: p.short.ja }]).forEach((q) => {
          const l = LAB[p.id] || [0, 0, "start"];
          pts.push(addPin(g, q.lat, q.lon, String(p.no), tr(q), "food", p.id, q.ldir || (p.pins ? "right" : DIR[l[2]]), 28));
        });
      });
    } else {
      G.trips.forEach((p) => (p.pins || []).forEach((q) => { pts.push(addPin(g, q.lat, q.lon, String(p.no), tr(q), "trip", p.id, q.ldir || DIR[q.anchor || "start"], 26, q.minor)); }));
      // 拠点（Hostel Act）は日帰り先の地図にも★で出す
      const base = LF.marker(HOME, { icon: LF.divIcon({ className: "lmk base", html: "<span>★</span>", iconSize: [26, 26], iconAnchor: [13, 13] }), keyboard: false });
      base.bindTooltip(esc(t("base")), { permanent: true, direction: "right", offset: [12, 0], className: "ltip ltip-base", opacity: 1 });
      base.addTo(g); pts.push(HOME);
    }
    allBounds[which] = LF.latLngBounds(pts);
    return g;
  }
  function labelsByZoom() {
    if (!lmap) return;
    document.getElementById("lmap").classList.toggle("nolabels", lmap.getZoom() < LBL_MIN[state.map]);
    // 宮島・尾道のように近くに何か所もあるところは、引いた表示ではおもな名前だけ出す
    document.getElementById("lmap").classList.toggle("nominor", state.map === "trips" && lmap.getZoom() < 11);
  }
  function fitCurrent() {
    if (!lmap || !allBounds[state.map]) return;
    lmap.fitBounds(allBounds[state.map], { padding: [26, 26], maxZoom: state.map === "city" ? 15 : 10, animate: false });
  }
  let fbShown = false;
  function useFallback() {
    if (fbShown) return;
    fbShown = true; mapFailed = true;
    if (lmap) { lmap.remove(); lmap = null; }
    document.getElementById("lmap").hidden = true;
    document.getElementById("svgmap").hidden = false;
    document.getElementById("map-fb").hidden = false;
    renderMap();
  }
  function initMap() {
    if (mapFailed) { useFallback(); return; }
    const touch = window.matchMedia("(pointer: coarse)").matches;
    lmap = LF.map("lmap", { scrollWheelZoom: false, dragging: !touch, tap: true, zoomSnap: 0.5 });
    const Fit = LF.Control.extend({ options: { position: "topleft" }, onAdd: function () {
      const b = LF.DomUtil.create("button", "lfit"); b.type = "button"; b.id = "lfit"; b.textContent = t("show_all");
      LF.DomEvent.disableClickPropagation(b); b.addEventListener("click", fitCurrent); return b; } });
    lmap.addControl(new Fit());
    lmap.on("zoomend", labelsByZoom);
    try {
      lmap.setView([34.3935, 132.4600], 14, { animate: false });   // 地図を重ねる前に仮の位置が必要（あとで全体表示に合わせる）
      const dark = window.matchMedia("(prefers-color-scheme: dark)").matches;
      base = window.KM_BASEMAP.addTo(lmap, { lang: L(), dark: dark, worker: "../vendor/maplibre/maplibre-gl-csp-worker.js" });
      if (!base) throw new Error("basemap");
      gl = base.getMaplibreMap();
      gl.on("style.load", () => window.KM_BASEMAP.setLang(gl, L()));
    } catch (err) { useFallback(); }
  }

  /* ---------- page ---------- */
  function render() {
    document.documentElement.lang = L();
    document.title = L() === "ja" ? "丹後・但馬のおすすめ｜天橋立・伊根・舞鶴・城崎温泉・豊岡" : "My Tango & Tajima Picks｜Amanohashidate, Ine, Maizuru, Kinosaki and Toyooka";
    const cnt = (a) => a.filter((s) => s.kind !== "group").length;
    document.getElementById("n-city").textContent = cnt(G.city);
    document.getElementById("n-food").textContent = cnt(G.food);
    document.getElementById("n-trips").textContent = G.trips.filter((s) => s.kind === "group").length;
    document.querySelectorAll("[data-t]").forEach((el) => { el.textContent = t(el.dataset.t); });
    document.querySelectorAll(".lang button").forEach((b) => b.setAttribute("aria-pressed", String(b.dataset.lang === L())));
    document.getElementById("intro").innerHTML = G.intro[L()].map((p, i, a) => `<p${i === a.length - 1 ? ' class="em"' : ""}>${esc(p)}</p>`).join("");
    document.getElementById("outro").innerHTML = G.outro[L()].map((p) => `<p>${esc(p)}</p>`).join("");
    document.getElementById("grid-city").innerHTML = G.city.map((s) => card(s, "city")).join("");
    document.getElementById("grid-food").innerHTML = G.food.map((s) => card(s, "food")).join("");
    document.getElementById("grid-trips").innerHTML = G.trips.map((s) => card(s, "trip")).join("");
    // モデルプラン（日帰り・1泊・2泊・3泊）
    document.getElementById("plans-list").innerHTML = (G.plans || []).map((p) => `<article class="plan" id="${esc(p.id)}">
      <h3>${esc(tr(p.title))}</h3>${p.sub ? `<p class="plan-sub">${esc(tr(p.sub))}</p>` : ""}
      <ol>${p.days.map((d) => `<li><b>${esc(tr(d.label))}</b><span>${esc(tr(d.text))}</span></li>`).join("")}</ol>
      ${p.note ? `<p class="note">${esc(tr(p.note))}</p>` : ""}
      ${(p.links || []).length ? `<div class="acts">${p.links.map((x) => `<a class="btn" href="${esc(x.url)}">${ICON.ext}${esc(tr(x))}</a>`).join("")}</div>` : ""}
    </article>`).join("");
    wireCarousels(document);
    renderMap();
    if (gl) window.KM_BASEMAP.setLang(gl, L());   // 地図の文字も EN / 日本語 に合わせる
    const cr = [];
    [G.city, G.food, G.trips].forEach((grp) => grp.forEach((s) => (s.photos || []).forEach((p) => {
      if (p.credit) cr.push(`<li>${esc(tr(p.cap) || tr(s))}: <a href="${esc(p.credit.page)}" target="_blank" rel="noopener">${esc(p.credit.author)}</a>, <a href="${licUrl(p.credit.license)}" target="_blank" rel="noopener">${esc(p.credit.license)}</a>, ${esc(t("via"))}${L() === "ja" ? "（縮小）" : " (resized)"}</li>`);
    })));
    document.getElementById("credits").innerHTML = cr.join("");
  }

  document.querySelector(".lang").addEventListener("click", (e) => {
    const b = e.target.closest("button[data-lang]"); if (!b || b.dataset.lang === L()) return;
    const y = window.scrollY;
    state.lang = b.dataset.lang;
    try { localStorage.setItem("kyoto-maps-lang", state.lang); } catch (err) { /* private mode */ }
    render();
    window.scrollTo(0, y);
  });
  document.querySelector(".tabs").addEventListener("click", (e) => {
    const b = e.target.closest("button[data-map]"); if (!b) return;
    setView(b.dataset.map);
  });
  // 「豊岡・城崎・竹野」「天橋立・伊根・舞鶴・竹田」を別のタブにする（上のバー・数字のタイル・地図の上のタブ、どれからでも切り替え）
  const TRIP_IDS = new Set(G.trips.map((s) => s.id).concat(["trips"]));
  function viewOf(hash) { return TRIP_IDS.has((hash || "").replace(/^#/, "")) ? "trips" : "city"; }
  function setView(v, scrollTo) {
    state.view = v; state.map = v;
    document.querySelector("main").dataset.view = v;
    document.querySelectorAll("[data-view-tab]").forEach((a) => {
      if (a.dataset.viewTab === v) a.setAttribute("aria-current", "true"); else a.removeAttribute("aria-current");
    });
    renderMap(true);
    history.replaceState(null, "", "#" + (v === "trips" ? "trips" : "city"));
    if (scrollTo) document.getElementById(scrollTo).scrollIntoView({ block: "start" });
  }
  document.addEventListener("click", (e) => {
    const a = e.target.closest("a[data-view-tab]"); if (!a) return;
    e.preventDefault();
    setView(a.dataset.viewTab, "map");
  });
  const svgBox = document.getElementById("svgmap");
  svgBox.addEventListener("click", (e) => { const g = e.target.closest("[data-go]"); if (g) goTo(g.dataset.go); });
  svgBox.addEventListener("keydown", (e) => { const g = e.target.closest("[data-go]"); if (g && (e.key === "Enter" || e.key === " ")) { e.preventDefault(); goTo(g.dataset.go); } });

  initMap();
  render();
  const startHash = location.hash;
  setView(viewOf(startHash));
  labelsByZoom();
  // 直接リンク（例 #yamanaka）のときは、そのカードまで移動する
  const target = startHash && document.getElementById(startHash.slice(1));
  if (target && !["city", "trips", "map", "top"].includes(startHash.slice(1))) {
    history.replaceState(null, "", startHash);
    setTimeout(() => target.scrollIntoView({ block: "start" }), 50);
  }
})();
