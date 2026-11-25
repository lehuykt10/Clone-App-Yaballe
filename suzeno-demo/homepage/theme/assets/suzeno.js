/* Suzeno theme: shared helpers, countdown, drawers, cart drawer. */
(function () {
  var SZ = window.SZ || (window.SZ = {});
  var $ = function (s, r) { return (r || document).querySelector(s); };
  SZ.$ = $;

  SZ.money = function (cents) {
    var fmt = SZ.moneyFormat || '${{amount}}';
    var n = (Number(cents) || 0) / 100;
    var two = n.toFixed(2);
    var withSep = function (str, thou, dec) {
      var parts = str.split('.');
      parts[0] = parts[0].replace(/\B(?=(\d{3})+(?!\d))/g, thou);
      return parts.join(dec);
    };
    return fmt.replace(/\{\{\s*(\w+)\s*\}\}/, function (_, k) {
      if (k === 'amount_no_decimals') return withSep(Math.round(n).toString(), ',', '.');
      if (k === 'amount_with_comma_separator') return withSep(two, '.', ',');
      if (k === 'amount_no_decimals_with_comma_separator') return withSep(Math.round(n).toString(), '.', ',');
      return withSep(two, ',', '.');
    });
  };
  SZ.esc = function (s) { return String(s == null ? '' : s).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); };

  var toastT;
  SZ.toast = function (msg) {
    var t = $('#toast'); if (!t) return;
    t.textContent = msg; t.classList.add('show');
    clearTimeout(toastT); toastT = setTimeout(function () { t.classList.remove('show'); }, 2200);
  };

  /* drawers */
  SZ.openDrawer = function (id) { var d = $(id); if (!d) return; d.classList.add('open'); d.setAttribute('aria-hidden', 'false'); };
  SZ.closeDrawer = function (d) { d.classList.remove('open'); d.setAttribute('aria-hidden', 'true'); };
  document.addEventListener('click', function (e) {
    var opener = e.target.closest('[data-open]');
    if (opener) { e.preventDefault(); SZ.openDrawer(opener.getAttribute('data-open')); if (opener.getAttribute('data-open') === '#cart') SZ.refreshCart(); return; }
    var d = e.target.closest('.drawer');
    if (d && e.target.closest('[data-close]')) SZ.closeDrawer(d);
  });
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape') document.querySelectorAll('.drawer.open').forEach(SZ.closeDrawer);
  });

  /* countdown to local midnight */
  function tick() {
    var now = new Date(), end = new Date(now); end.setHours(24, 0, 0, 0);
    var s = Math.max(0, Math.floor((end - now) / 1000));
    var h = String(Math.floor(s / 3600)).padStart(2, '0'), m = String(Math.floor(s % 3600 / 60)).padStart(2, '0'), sec = String(s % 60).padStart(2, '0');
    document.querySelectorAll('[data-cd-h]').forEach(function (el) { el.textContent = h; });
    document.querySelectorAll('[data-cd-m]').forEach(function (el) { el.textContent = m; });
    document.querySelectorAll('[data-cd-s]').forEach(function (el) { el.textContent = sec; });
    document.querySelectorAll('[data-cd-all]').forEach(function (el) { el.textContent = h + ':' + m + ':' + sec; });
  }
  tick(); setInterval(tick, 1000);

  /* cart drawer */
  SZ.renderCart = function (cart) {
    var badge = $('#cartCount');
    if (badge) { badge.hidden = !cart.item_count; badge.textContent = cart.item_count; }
    var lines = $('#cartLines'); if (!lines) return;
    if (!cart.items.length) {
      lines.innerHTML = '<p class="empty">Your cart is empty.</p>';
    } else {
      lines.innerHTML = cart.items.map(function (it) {
        var img = it.image ? it.image.replace(/(\.[a-z]+)(\?|$)/i, '_160x160$1$2') : '';
        var opts = (it.options_with_values || []).filter(function (o) { return o.value !== 'Default Title'; }).map(function (o) { return SZ.esc(o.value); }).join(' · ');
        return '<div class="line">' + (img ? '<img src="' + img + '" alt="">' : '<span></span>') +
          '<div><b>' + SZ.esc(it.product_title) + '</b><div class="meta">' + opts + '</div>' +
          '<div class="qty-pill"><button data-qty="' + it.key + '" data-to="' + (it.quantity - 1) + '" aria-label="Decrease">−</button><span>' + it.quantity + '</span><button data-qty="' + it.key + '" data-to="' + (it.quantity + 1) + '" aria-label="Increase">+</button></div></div>' +
          '<b>' + SZ.money(it.final_line_price) + '</b></div>';
      }).join('');
    }
    var total = $('#cartTotal'); if (total) total.textContent = SZ.money(cart.total_price);
  };
  SZ.refreshCart = function () {
    return fetch(SZ.routes.cart + '.js', { headers: { Accept: 'application/json' } }).then(function (r) { return r.json(); }).then(function (c) { SZ.renderCart(c); return c; });
  };
  document.addEventListener('click', function (e) {
    var b = e.target.closest('[data-qty]'); if (!b) return;
    fetch(SZ.routes.cartChange + '.js', { method: 'POST', headers: { 'Content-Type': 'application/json', Accept: 'application/json' }, body: JSON.stringify({ id: b.getAttribute('data-qty'), quantity: Number(b.getAttribute('data-to')) }) })
      .then(function (r) { return r.json(); }).then(SZ.renderCart);
  });
  SZ.addItems = function (items) {
    return fetch(SZ.routes.cartAdd + '.js', { method: 'POST', headers: { 'Content-Type': 'application/json', Accept: 'application/json' }, body: JSON.stringify({ items: items }) })
      .then(function (r) { return r.json().then(function (j) { if (!r.ok || j.status) throw new Error(j.description || j.message || 'Could not add to cart'); return j; }); })
      .then(function () { return SZ.refreshCart(); })
      .then(function () { SZ.openDrawer('#cart'); SZ.toast('Added to cart'); });
  };
  if (document.readyState !== 'loading') SZ.refreshCart(); else document.addEventListener('DOMContentLoaded', SZ.refreshCart);
})();
