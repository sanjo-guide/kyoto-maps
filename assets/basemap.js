/* 全マップ共通の地図スタイル（Googleマップ / Appleマップに近い見た目）
   - データ: OpenFreeMap（OpenStreetMap）のベクター地図。MapLibre で描き、Leaflet の上に重ねる
   - 色: 地面は明るいグレー、公園・森は薄い緑、水は水色、道は白、高速道路は黄色
   - 文字: 市町村・駅・川・公園・大きな道の名前だけ。町名やお店の名前は出さない（紹介したい場所を目立たせるため）
   使い方:
     var layer = KM_BASEMAP.addTo(leafletMap, { lang: 'ja', dark: false, worker: '../vendor/maplibre/maplibre-gl-csp-worker.js' });
     KM_BASEMAP.setLang(layer.getMaplibreMap(), 'en');
*/
(function () {
  'use strict';

  var ATTR = '<a href="https://openfreemap.org" target="_blank" rel="noopener">OpenFreeMap</a> ' +
    '<a href="https://www.openmaptiles.org/" target="_blank" rel="noopener">&copy; OpenMapTiles</a> ' +
    'Data from <a href="https://www.openstreetmap.org/copyright" target="_blank" rel="noopener">OpenStreetMap</a>';

  var LIGHT = {
    land: '#F4F3F0', park: '#CDEAC4', wood: '#D7EACB', grass: '#DCEDD2', water: '#A9D3F2', waterLine: '#9CCBEE',
    building: '#E8E6E1', buildingLine: '#DCD9D3',
    road: '#FFFFFF', roadCase: '#DEDBD5', major: '#FFFFFF', majorCase: '#D3CFC8',
    trunk: '#FFF0B8', trunkCase: '#E8CF86', motorway: '#FBD77A', motorwayCase: '#E2B04B',
    path: '#FFFFFF', rail: '#A9ACB0', boundary: '#B9B4C4',
    text: '#5F6368', textStrong: '#3C4043', halo: '#FFFFFF', waterText: '#3E7DB8', parkText: '#3C7A4A',
    station: '#FFFFFF', stationLine: '#6E7377'
  };
  var DARK = {
    land: '#1F2124', park: '#22332A', wood: '#233128', grass: '#24342A', water: '#17283A', waterLine: '#1B3045',
    building: '#2A2D31', buildingLine: '#33363B',
    road: '#3A3D42', roadCase: '#2A2D31', major: '#4A4E54', majorCase: '#2A2D31',
    trunk: '#5A5446', trunkCase: '#3A362C', motorway: '#6B5A35', motorwayCase: '#3D3324',
    path: '#3A3D42', rail: '#5D6166', boundary: '#55525E',
    text: '#A9ADB3', textStrong: '#D7DADF', halo: '#1F2124', waterText: '#7FA8CF', parkText: '#8DBB98',
    station: '#2A2D31', stationLine: '#A9ADB3'
  };

  function nameExpr(lang) {
    return lang === 'ja'
      ? ['coalesce', ['get', 'name:ja'], ['get', 'name']]
      : ['coalesce', ['get', 'name:en'], ['get', 'name:ja-Latn'], ['get', 'name:latin'], ['get', 'name']];
  }
  function z(stops) { return ['interpolate', ['exponential', 1.5], ['zoom']].concat(stops); }
  var NOT_TUNNEL = ['!=', ['get', 'brunnel'], 'tunnel'];
  function cls(list) { return ['match', ['get', 'class'], list, true, false]; }
  var LINE = { 'line-cap': 'round', 'line-join': 'round' };

  function style(opt) {
    opt = opt || {};
    var c = opt.dark ? DARK : LIGHT;
    var nm = nameExpr(opt.lang || 'ja');
    var font = ['Noto Sans Regular'], bold = ['Noto Sans Bold'], ital = ['Noto Sans Italic'];
    var label = function (extra) {
      var l = { 'text-field': nm, 'text-font': font, 'text-size': 12, 'text-max-width': 8 };
      for (var k in extra) l[k] = extra[k];
      return l;
    };
    var paintText = function (color, w) { return { 'text-color': color, 'text-halo-color': c.halo, 'text-halo-width': w || 1.4 }; };

    function road(id, classes, minz, color, casing, w) {
      return [
        { id: id + '_case', type: 'line', source: 'omt', 'source-layer': 'transportation', minzoom: minz,
          filter: ['all', NOT_TUNNEL, cls(classes)], layout: LINE,
          paint: { 'line-color': casing, 'line-width': z(w.map(function (s, i) { return i % 2 ? s + 1.6 : s; })) } },
        { id: id, type: 'line', source: 'omt', 'source-layer': 'transportation', minzoom: minz,
          filter: ['all', NOT_TUNNEL, cls(classes)], layout: LINE,
          paint: { 'line-color': color, 'line-width': z(w) } }
      ];
    }

    var layers = [
      { id: 'land', type: 'background', paint: { 'background-color': c.land } },
      { id: 'wood', type: 'fill', source: 'omt', 'source-layer': 'landcover', filter: cls(['wood', 'forest']), paint: { 'fill-color': c.wood } },
      { id: 'grass', type: 'fill', source: 'omt', 'source-layer': 'landcover', filter: cls(['grass', 'farmland', 'wetland']), paint: { 'fill-color': c.grass, 'fill-opacity': 0.7 } },
      { id: 'park', type: 'fill', source: 'omt', 'source-layer': 'park', paint: { 'fill-color': c.park } },
      { id: 'landuse-green', type: 'fill', source: 'omt', 'source-layer': 'landuse', filter: cls(['cemetery', 'pitch', 'stadium', 'zoo', 'theme_park']), paint: { 'fill-color': c.grass, 'fill-opacity': 0.6 } },
      { id: 'water', type: 'fill', source: 'omt', 'source-layer': 'water', filter: NOT_TUNNEL, paint: { 'fill-color': c.water } },
      { id: 'river', type: 'line', source: 'omt', 'source-layer': 'waterway', minzoom: 9, filter: ['all', NOT_TUNNEL, cls(['river'])], layout: LINE,
        paint: { 'line-color': c.waterLine, 'line-width': z([9, 0.8, 14, 2.5, 18, 6]) } },
      { id: 'stream', type: 'line', source: 'omt', 'source-layer': 'waterway', minzoom: 14, filter: ['all', NOT_TUNNEL, cls(['stream', 'canal'])], layout: LINE,
        paint: { 'line-color': c.waterLine, 'line-width': z([14, 0.8, 18, 2.5]) } },
      { id: 'building', type: 'fill', source: 'omt', 'source-layer': 'building', minzoom: 15,
        paint: { 'fill-color': c.building, 'fill-outline-color': c.buildingLine, 'fill-opacity': z([15, 0.5, 16.5, 1]) } },
      { id: 'boundary', type: 'line', source: 'omt', 'source-layer': 'boundary', maxzoom: 12,
        filter: ['all', ['==', ['get', 'admin_level'], 4], ['!=', ['get', 'maritime'], 1]],
        paint: { 'line-color': c.boundary, 'line-width': 1, 'line-dasharray': [3, 2] } },
      { id: 'path', type: 'line', source: 'omt', 'source-layer': 'transportation', minzoom: 15,
        filter: ['all', NOT_TUNNEL, cls(['path'])], layout: LINE,
        paint: { 'line-color': c.path, 'line-width': z([15, 1, 18, 2.5]), 'line-dasharray': [1, 1.5] } }
    ];
    layers = layers.concat(
      road('road-minor', ['minor', 'service'], 13, c.road, c.roadCase, [13, 0.6, 16, 4, 18, 11]),
      road('road-mid', ['secondary', 'tertiary'], 10, c.major, c.majorCase, [10, 0.6, 14, 3, 18, 16]),
      road('road-primary', ['primary'], 8, c.major, c.majorCase, [8, 0.6, 14, 4, 18, 20]),
      road('road-trunk', ['trunk'], 7, c.trunk, c.trunkCase, [7, 0.8, 14, 4.5, 18, 22]),
      road('road-motorway', ['motorway'], 5, c.motorway, c.motorwayCase, [5, 0.8, 14, 5, 18, 24])
    );
    layers.push(
      { id: 'rail', type: 'line', source: 'omt', 'source-layer': 'transportation', minzoom: 9,
        filter: ['all', NOT_TUNNEL, cls(['rail', 'transit'])],
        paint: { 'line-color': c.rail, 'line-width': z([9, 0.8, 14, 1.8, 18, 3]) } },

      // ---- 文字 ----
      { id: 'label-river', type: 'symbol', source: 'omt', 'source-layer': 'waterway', minzoom: 12, filter: cls(['river']),
        layout: label({ 'symbol-placement': 'line', 'text-font': ital, 'text-size': 12, 'symbol-spacing': 400 }), paint: paintText(c.waterText) },
      { id: 'label-sea', type: 'symbol', source: 'omt', 'source-layer': 'water_name', minzoom: 5,
        filter: cls(['ocean', 'sea', 'bay', 'strait']),
        layout: label({ 'text-font': ital, 'text-size': z([5, 11, 10, 14]) }), paint: paintText(c.waterText) },
      // 池・堀などの小さな水面の名前は、かなり拡大したときだけ
      { id: 'label-water', type: 'symbol', source: 'omt', 'source-layer': 'water_name', minzoom: 16,
        filter: ['!', cls(['ocean', 'sea', 'bay', 'strait'])],
        layout: label({ 'text-font': ital, 'text-size': 12 }), paint: paintText(c.waterText) },
      { id: 'label-road', type: 'symbol', source: 'omt', 'source-layer': 'transportation_name', minzoom: 15,
        filter: cls(['primary', 'secondary', 'trunk']),
        layout: label({ 'symbol-placement': 'line', 'text-size': 11.5, 'symbol-spacing': 350 }), paint: paintText(c.text, 1.6) },
      { id: 'label-park', type: 'symbol', source: 'omt', 'source-layer': 'poi', minzoom: 16,
        filter: cls(['park', 'garden']),
        layout: label({ 'text-size': 11.5, 'text-max-width': 7 }), paint: paintText(c.parkText) },
      { id: 'station-dot', type: 'circle', source: 'omt', 'source-layer': 'poi', minzoom: 12,
        filter: ['all', cls(['rail', 'railway']), ['match', ['get', 'subclass'], ['station', 'halt'], true, false]],
        paint: { 'circle-radius': z([12, 2.5, 16, 4.5]), 'circle-color': c.station, 'circle-stroke-color': c.stationLine, 'circle-stroke-width': 1.5 } },
      { id: 'label-station', type: 'symbol', source: 'omt', 'source-layer': 'poi', minzoom: 13,
        filter: ['all', cls(['rail', 'railway']), ['match', ['get', 'subclass'], ['station', 'halt'], true, false]],
        layout: label({ 'text-size': 11.5, 'text-anchor': 'top', 'text-offset': [0, 0.7], 'text-font': bold }), paint: paintText(c.textStrong, 1.6) },
      { id: 'label-village', type: 'symbol', source: 'omt', 'source-layer': 'place', minzoom: 11, maxzoom: 15,
        filter: cls(['village']), layout: label({ 'text-size': 11.5 }), paint: paintText(c.text) },
      { id: 'label-town', type: 'symbol', source: 'omt', 'source-layer': 'place', minzoom: 8, maxzoom: 14,
        filter: cls(['town']), layout: label({ 'text-size': z([8, 11, 13, 14]) }), paint: paintText(c.textStrong) },
      { id: 'label-city', type: 'symbol', source: 'omt', 'source-layer': 'place', minzoom: 5, maxzoom: 13,
        filter: cls(['city']), layout: label({ 'text-size': z([5, 12, 12, 17]), 'text-font': bold }), paint: paintText(c.textStrong, 1.8) }
    );
    layers.forEach(function (l) { if (l.layout && l.layout['text-field']) (l.metadata = l.metadata || {})['phs:name'] = true; });

    return {
      version: 8,
      sources: { omt: { type: 'vector', url: 'https://tiles.openfreemap.org/planet' } },
      glyphs: 'https://tiles.openfreemap.org/fonts/{fontstack}/{range}.pbf',
      layers: layers
    };
  }

  function setLang(gl, lang) {
    if (!gl || !gl.getStyle || !gl.isStyleLoaded()) return;
    gl.getStyle().layers.forEach(function (l) {
      if (l.metadata && l.metadata['phs:name']) gl.setLayoutProperty(l.id, 'text-field', nameExpr(lang));
    });
  }

  function addTo(map, opt) {
    opt = opt || {};
    if (!window.maplibregl || !window.L || !L.maplibreGL) return null;
    if (opt.worker) maplibregl.setWorkerUrl(opt.worker);
    return L.maplibreGL({
      style: style(opt),
      maxZoom: opt.maxZoom || 19,
      attributionControl: { customAttribution: ATTR }
    }).addTo(map);
  }

  window.KM_BASEMAP = { style: style, setLang: setLang, addTo: addTo, attribution: ATTR };
})();
