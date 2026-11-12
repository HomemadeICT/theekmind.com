(function () {
  var root = document.documentElement;

  function store(k, v) {
    try { if (v === undefined) return localStorage.getItem(k); localStorage.setItem(k, v); } catch (e) {}
    return null;
  }
  function isDark() {
    return root.getAttribute('data-theme') === 'dark';
  }

  var themeBtn = document.getElementById('theme');
  if (themeBtn) {
    var sync = function () { themeBtn.setAttribute('aria-checked', isDark() ? 'true' : 'false'); };
    sync();
    themeBtn.addEventListener('click', function () {
      var next = isDark() ? 'light' : 'dark';
      root.setAttribute('data-theme', next);
      store('tm-theme', next);
      sync();
    });
  }

  var menu = document.getElementById('menu'), nav = document.getElementById('nav');
  if (menu && nav) {
    menu.addEventListener('click', function () {
      var open = nav.classList.toggle('open');
      menu.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
  }

  var reveals = document.querySelectorAll('.reveal');
  if ('IntersectionObserver' in window && !matchMedia('(prefers-reduced-motion: reduce)').matches) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); } });
    }, { threshold: 0.08 });
    reveals.forEach(function (el) { io.observe(el); });
  } else {
    reveals.forEach(function (el) { el.classList.add('in'); });
  }

  var filters = document.getElementById('filters');
  if (filters) {
    filters.hidden = false;
    var cards = document.querySelectorAll('.pcard[data-cats]');
    filters.addEventListener('click', function (ev) {
      var b = ev.target.closest('button');
      if (!b) return;
      var f = b.getAttribute('data-filter');
      filters.querySelectorAll('button').forEach(function (x) { x.setAttribute('aria-pressed', x === b ? 'true' : 'false'); });
      cards.forEach(function (c) {
        c.hidden = !(f === 'all' || c.getAttribute('data-cats').split(' ').indexOf(f) > -1);
      });
    });
  }

  var box = document.getElementById('latest-posts');
  if (box) {
    window.__tmPosts = function (data) {
      var entries = (data && data.feed && data.feed.entry) || [];
      if (!entries.length) return;
      box.textContent = '';
      entries.forEach(function (e) {
        var href = '';
        (e.link || []).forEach(function (l) { if (l.rel === 'alternate') href = l.href; });
        if (!/^https:\/\/blogs\.theekmind\.com\//.test(href)) return;
        var a = document.createElement('a');
        a.className = 'post'; a.href = href;
        var meta = document.createElement('span');
        meta.className = 'meta';
        var d = new Date(e.published.$t);
        var cat = (e.category && e.category[0] && e.category[0].term) || 'Article';
        meta.textContent = cat + ' · ' + d.toLocaleDateString('en-GB', { day: 'numeric', month: 'short', year: 'numeric' });
        var h = document.createElement('h3');
        h.textContent = e.title.$t;
        var more = document.createElement('span');
        more.textContent = 'Read article →';
        more.style.cssText = 'color:var(--link);font-weight:600;margin-top:auto';
        a.appendChild(meta); a.appendChild(h); a.appendChild(more);
        box.appendChild(a);
      });
    };
    var s = document.createElement('script');
    s.src = 'https://blogs.theekmind.com/feeds/posts/default?alt=json-in-script&max-results=3&callback=__tmPosts';
    s.async = true;
    document.head.appendChild(s);
  }
})();
