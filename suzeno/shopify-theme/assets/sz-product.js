/* Suzeno product landing: gallery, per-item color/size picks, bundles, add-ons, add to cart. */
(function () {
  function init(root) {
    var SZ = window.SZ, esc = SZ.esc, money = SZ.money;
    var section = root.closest('.shopify-section') || document;
    var product = JSON.parse(section.querySelector('[data-product-json]').textContent);
    var cfg = JSON.parse(section.querySelector('[data-config-json]').textContent);
    var tiers = cfg.tiers.filter(function (t) { return t.qty > 0; });
    if (!tiers.length) tiers = [{ qty: 1, off: 0, label: '1 item', badge: '' }];
    var swatch = {};
    (cfg.swatches || '').split(/\n/).forEach(function (l) { var i = l.lastIndexOf(':'); if (i > 0) swatch[l.slice(0, i).trim().toLowerCase()] = l.slice(i + 1).trim(); });
    var options = product.options || [];
    var single = product.variants.length === 1 && options.length <= 1 && product.variants[0].title === 'Default Title';
    var isColor = function (name) { return /colou?r|style|pattern/i.test(name); };
    var start = (product.variants.find(function (v) { return v.available; }) || product.variants[0]);

    /* ---- gallery ---- */
    var slides = root.querySelector('[data-slides]'), thumbs = [].slice.call(root.querySelectorAll('.thumb'));
    var count = slides.children.length, cur = 0;
    function go(i) {
      cur = (i + count) % count;
      slides.style.transform = 'translateX(-' + (cur * 100) + '%)';
      thumbs.forEach(function (t, k) { t.setAttribute('aria-current', k === cur); });
    }
    root.querySelector('[data-prev]').addEventListener('click', function () { go(cur - 1); });
    root.querySelector('[data-next]').addEventListener('click', function () { go(cur + 1); });
    thumbs.forEach(function (t) { t.addEventListener('click', function () { go(+t.dataset.i); }); });
    var sx = null, stage = root.querySelector('.stage');
    stage.addEventListener('touchstart', function (e) { sx = e.touches[0].clientX; }, { passive: true });
    stage.addEventListener('touchend', function (e) { if (sx === null) return; var d = e.changedTouches[0].clientX - sx; if (Math.abs(d) > 40) go(cur + (d < 0 ? 1 : -1)); sx = null; });
    function showVariantImage(v) {
      if (!v || !v.featured_media) return;
      var el = slides.querySelector('[data-media-id="' + v.featured_media.id + '"]');
      if (el) go([].indexOf.call(slides.children, el));
    }
    go(0);

    /* ---- picks ---- */
    var state = {
      tier: Math.min(Math.max(cfg.defaultTier, 0), tiers.length - 1),
      picks: tiers.map(function (t) { return Array.from({ length: t.qty }, function () { return start.options.slice(); }); }),
      addons: {}
    };
    function variantFor(opts) {
      return product.variants.find(function (v) { return v.options.every(function (o, i) { return o === opts[i]; }); });
    }
    function optionValues(i) { var o = options[i]; return (o && o.values) || []; }
    function optionName(i) { var o = options[i]; return typeof o === 'string' ? o : (o && o.name) || ''; }
    // product | json gives options as names; values come from variants
    function valuesFor(i) {
      var seen = []; product.variants.forEach(function (v) { if (seen.indexOf(v.options[i]) < 0) seen.push(v.options[i]); }); return seen;
    }

    var box = root.querySelector('[data-bundles]');
    function render() {
      box.innerHTML = tiers.map(function (t, ti) {
        var on = ti === state.tier;
        var vs = state.picks[ti].map(variantFor);
        var base = vs.reduce(function (s, v) { return s + (v ? v.price : start.price); }, 0);
        var total = base - t.off * t.qty;
        var full = vs.reduce(function (s, v) { v = v || start; return s + Math.max(v.compare_at_price || 0, v.price); }, 0);
        var save = full - total;
        var pct = full > 0 ? Math.round(save / full * 100) : 0;
        var picks = single ? '' : state.picks[ti].map(function (pk, k) {
          var rows = pk.map(function (val, oi) {
            var name = optionName(oi), vals = valuesFor(oi);
            if (isColor(name)) {
              return '<div class="swatches">' + vals.map(function (cv) {
                var c = swatch[cv.toLowerCase()] || '#ccc';
                return '<button type="button" class="swatch" style="--sw:' + esc(c) + '" data-t="' + ti + '" data-k="' + k + '" data-o="' + oi + '" data-v="' + esc(cv) + '" aria-pressed="' + (cv === val) + '" aria-label="' + esc(cv) + '" title="' + esc(cv) + '"></button>';
              }).join('') + '</div>';
            }
            return '<div class="sizes">' + vals.map(function (sv) {
              var test = pk.slice(); test[oi] = sv; var tv = variantFor(test);
              return '<button type="button" class="size" data-t="' + ti + '" data-k="' + k + '" data-o="' + oi + '" data-v="' + esc(sv) + '" aria-pressed="' + (sv === val) + '"' + (tv && !tv.available ? ' style="opacity:.4;text-decoration:line-through"' : '') + '>' + esc(sv) + '</button>';
            }).join('') + '</div>';
          }).join('');
          var label = (t.qty > 1 ? 'Item ' + (k + 1) : 'Your pick') + ': <span class="pick-color">' + esc(pk.join(' / ')) + '</span>';
          return '<div class="pick"><label>' + label + '</label>' + rows + '</div>';
        }).join('');
        var addons = (cfg.addons || []).filter(function (a) { return a.available; }).map(function (a) {
          return '<label class="addon"><input type="checkbox" data-addon="' + a.id + '"' + (state.addons[a.id] ? ' checked' : '') + '><span class="ico">' + esc(a.icon || '+') + '</span><span>' + esc(a.title) + '</span><b>+' + money(a.price) + '</b></label>';
        }).join('');
        return '<div class="bundle' + (on ? ' on' : '') + '" role="radio" aria-checked="' + on + '" tabindex="0" data-tier="' + ti + '">' +
          (t.badge ? '<div class="tag' + (/best/i.test(t.badge) ? ' best' : '') + '">' + esc(t.badge) + '</div>' : '') +
          '<div class="b-top"><span class="radio"></span><div><div class="b-name">' + esc(t.label) + '</div>' +
          (save > 0 ? '<div class="b-save">You save <strong>' + money(save) + '</strong></div><span class="chip-save">Save ' + pct + '%</span>' : '') +
          '</div><div class="b-price">' + money(total) + (full > total ? '<s>' + money(full) + '</s>' : '') + '</div></div>' +
          '<div class="b-body">' + picks + (addons ? '<div class="addons">' + addons + '</div>' : '') + '</div>' +
          (cfg.gift ? '<div class="gift"><span>🎁 ' + esc(cfg.gift) + '</span><em>FREE</em></div>' : '') +
          '</div>';
      }).join('');
      var t = tiers[state.tier];
      var vs = state.picks[state.tier].map(variantFor);
      var sum = vs.reduce(function (s, v) { return s + (v ? v.price : start.price); }, 0) - t.off * t.qty;
      (cfg.addons || []).forEach(function (a) { if (state.addons[a.id]) sum += a.price; });
      var sub = root.querySelector('[data-add-sub]');
      if (sub) sub.textContent = money(sum) + ' · ' + t.qty + ' item' + (t.qty > 1 ? 's' : '');
    }
    box.addEventListener('click', function (e) {
      var b = e.target.closest('[data-o]');
      if (b) {
        var pk = state.picks[+b.dataset.t][+b.dataset.k]; pk[+b.dataset.o] = b.dataset.v;
        if (isColor(optionName(+b.dataset.o))) showVariantImage(variantFor(pk) || product.variants.find(function (v) { return v.options[+b.dataset.o] === b.dataset.v; }));
        render(); return;
      }
      if (e.target.closest('.addon')) return;
      var card = e.target.closest('[data-tier]');
      if (card && +card.dataset.tier !== state.tier) { state.tier = +card.dataset.tier; render(); }
    });
    box.addEventListener('change', function (e) { var id = e.target.dataset.addon; if (!id) return; state.addons[id] = e.target.checked; render(); });
    box.addEventListener('keydown', function (e) {
      var card = e.target.closest('[data-tier]');
      if (card && e.target === card && (e.key === 'Enter' || e.key === ' ')) { e.preventDefault(); state.tier = +card.dataset.tier; render(); }
    });
    render();

    /* ---- add to cart ---- */
    var err = root.querySelector('[data-err]'), btn = root.querySelector('[data-add]');
    function add() {
      err.hidden = true;
      var counts = {};
      var bad = state.picks[state.tier].some(function (pk) {
        var v = variantFor(pk);
        if (!v || !v.available) return true;
        counts[v.id] = (counts[v.id] || 0) + 1; return false;
      });
      if (bad) { err.textContent = 'One of your picks is sold out. Please choose another color or size.'; err.hidden = false; return; }
      var items = Object.keys(counts).map(function (id) { return { id: Number(id), quantity: counts[id] }; });
      (cfg.addons || []).forEach(function (a) { if (state.addons[a.id]) items.push({ id: a.id, quantity: 1 }); });
      btn.disabled = true;
      SZ.addItems(items).catch(function (x) { err.textContent = x.message; err.hidden = false; }).finally(function () { btn.disabled = false; });
    }
    btn.addEventListener('click', add);
    var sticky = section.querySelector('[data-sticky-add]');
    if (sticky) sticky.addEventListener('click', function () { root.querySelector('.info').scrollIntoView({ behavior: 'smooth' }); setTimeout(add, 350); });
  }
  function boot() { document.querySelectorAll('[data-sz-product]').forEach(function (r) { if (!r.dataset.ready) { r.dataset.ready = 1; init(r); } }); }
  // run after every deferred script (including suzeno.js) has loaded
  if (document.readyState === 'complete') boot(); else document.addEventListener('DOMContentLoaded', boot);
  document.addEventListener('shopify:section:load', boot);
})();
