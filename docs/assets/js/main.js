/* Plebum Dominium: progressive enhancement only. The guide reads fully with JS off. */
(function () {
  "use strict";

  /* --- mobile drawer --- */
  var btn = document.querySelector(".menu-btn");
  var scrim = document.querySelector(".scrim");
  var drawer = document.querySelector('.sidebar');
  var mobileNav = window.matchMedia('(max-width:760px)');
  function syncNavAccessibility() {
    if (drawer) drawer.inert = mobileNav.matches && !document.body.classList.contains('nav-open');
  }
  syncNavAccessibility();
  mobileNav.addEventListener('change', syncNavAccessibility);
  function closeNav() {
    document.body.classList.remove("nav-open");
    if (btn) btn.setAttribute("aria-expanded", "false");
    syncNavAccessibility();
  }
  if (btn) {
    btn.addEventListener("click", function () {
      var open = document.body.classList.toggle("nav-open");
      btn.setAttribute("aria-expanded", open ? "true" : "false");
      syncNavAccessibility();
      if (open && drawer) {
        var first = drawer.querySelector('button, a');
        if (first) first.focus();
      }
    });
  }
  if (scrim) scrim.addEventListener("click", closeNav);
  document.addEventListener("keydown", function (e) {
    if (e.key === "Escape" && document.body.classList.contains('nav-open')) {
      closeNav();
      if (btn) btn.focus();
    }
    if (e.key === 'Tab' && mobileNav.matches && drawer && document.body.classList.contains('nav-open')) {
      var items = Array.from(drawer.querySelectorAll('a[href], button:not([disabled])')).filter(function (el) { return el.getClientRects().length; });
      var first = items[0], last = items[items.length - 1];
      if (e.shiftKey && document.activeElement === first) { e.preventDefault(); last.focus(); }
      else if (!e.shiftKey && document.activeElement === last) { e.preventDefault(); first.focus(); }
    }
  });

  /* --- copy buttons on code blocks --- */
  document.querySelectorAll("pre").forEach(function (pre) {
    var b = document.createElement("button");
    b.className = "copy-btn";
    b.type = "button";
    b.textContent = "Copy";
    b.addEventListener("click", function () {
      var code = pre.querySelector("code");
      var text = code ? code.innerText : pre.innerText;
      navigator.clipboard.writeText(text).then(function () {
        b.textContent = "Copied";
        b.classList.add("copied");
        setTimeout(function () {
          b.textContent = "Copy";
          b.classList.remove("copied");
        }, 1600);
      });
    });
    pre.appendChild(b);
  });

  /* --- scrollspy for the "On this sheet" TOC --- */
  var tocLinks = Array.prototype.slice.call(document.querySelectorAll("[data-toc]"));
  if (tocLinks.length && "IntersectionObserver" in window) {
    var map = {};
    tocLinks.forEach(function (a) { map[a.getAttribute("data-toc")] = a; });
    var obs = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting) {
          tocLinks.forEach(function (a) { a.classList.remove("active"); });
          var a = map[en.target.id];
          if (a) a.classList.add("active");
        }
      });
    }, { rootMargin: "-20% 0px -70% 0px" });
    Object.keys(map).forEach(function (id) {
      var el = document.getElementById(id);
      if (el) obs.observe(el);
    });
  }

  /* --- sheet check-off, persisted on this device --- */
  var KEY = "plebum-dominium-done-" + (document.body.getAttribute("data-guide-path") || "reference");
  var done = {};
  try { done = JSON.parse(localStorage.getItem(KEY) || "{}"); } catch (e) { done = {}; }
  document.querySelectorAll(".sidebar a[data-sheet]").forEach(function (a) {
    var slug = a.getAttribute("data-sheet");
    if (done[slug]) a.parentElement.classList.add("done");
    // double-click a sidebar entry to toggle its checkmark
    a.addEventListener("dblclick", function (ev) {
      ev.preventDefault();
      var li = a.parentElement;
      var isDone = li.classList.toggle("done");
      if (isDone) done[slug] = true; else delete done[slug];
      try { localStorage.setItem(KEY, JSON.stringify(done)); } catch (e) {}
    });
  });
  // checking off happens on the sheet itself: mark current sheet done via footer button
  var here = document.querySelector('.sidebar a.active');
  if (here) {
    var slug = here.getAttribute("data-sheet");
    var row = document.querySelector(".prevnext-row");
    if (row && !done[slug]) {
      var b = document.createElement("button");
      b.className = "prevnext";
      b.type = "button";
      b.innerHTML = "<span>✓ Mark as read</span>";
      b.addEventListener("click", function () {
        done[slug] = true;
        try { localStorage.setItem(KEY, JSON.stringify(done)); } catch (e) {}
        here.parentElement.classList.add("done");
        b.innerHTML = "<span>✓ Marked as read</span>";
        b.disabled = true;
      });
      row.appendChild(b);
    }
  }
})();

/* ---------- theme: toggle + follow the OS when no saved choice ---------- */
(function () {
  var root = document.documentElement;
  function setTheme(t) {
    root.setAttribute("data-theme", t);
    try { localStorage.setItem("pd-theme", t); } catch (e) {}
  }
  var btn = document.getElementById("theme-btn");
  if (btn) {
    btn.addEventListener("click", function () {
      setTheme(root.getAttribute("data-theme") === "dark" ? "light" : "dark");
    });
  }
  try {
    var mq = window.matchMedia("(prefers-color-scheme: dark)");
    mq.addEventListener("change", function (e) {
      if (!localStorage.getItem("pd-theme")) setTheme(e.matches ? "dark" : "light");
    });
  } catch (e) {}
})();

/* ---------- reveal fallback (browsers without scroll timelines) ---------- */
(function () {
  if (window.CSS && CSS.supports && CSS.supports("animation-timeline: view()")) return;
  var els = document.querySelectorAll(".card, .you-need, .sheet-diagram, .callout, .keyring");
  els.forEach(function (el) { el.classList.add("reveal"); });
  if (!("IntersectionObserver" in window)) {
    els.forEach(function (el) { el.classList.add("in"); });
    return;
  }
  var io = new IntersectionObserver(function (entries) {
    entries.forEach(function (en) {
      if (en.isIntersecting) { en.target.classList.add("in"); io.unobserve(en.target); }
    });
  }, { threshold: 0.1 });
  els.forEach(function (el) { io.observe(el); });
})();

/* --- on-chain donate: copy address --- */
document.querySelectorAll(".btn-onchain").forEach(function (btn) {
  btn.addEventListener("click", function () {
    var addr = btn.getAttribute("data-copy");
    if (!addr || addr.indexOf("REPLACE_WITH") === 0) return;
    navigator.clipboard.writeText(addr).then(function () {
      var orig = btn.innerHTML;
      btn.classList.add("copied");
      btn.innerHTML = "\u2713 Address copied";
      setTimeout(function () {
        btn.classList.remove("copied");
        btn.innerHTML = orig;
      }, 2500);
    });
  });
});

/* --- first-visit "New to Bitcoin?" banner (homepage only) --- */
(function () {
  var banner = document.getElementById("newbie-banner");
  if (!banner) return;
  if (!document.body.classList.contains("home")) return;
  var seen = false;
  try { seen = localStorage.getItem("pd-newbie-seen") === "1"; } catch (e) {}
  if (seen) return;
  function dismiss() {
    try { localStorage.setItem("pd-newbie-seen", "1"); } catch (e) {}
    banner.hidden = true;
  }
  banner.querySelector(".newbie-close").addEventListener("click", dismiss);
  banner.querySelector(".newbie-go").addEventListener("click", dismiss);
  banner.hidden = false;
})();

/* first-visit splash: site name at the top, logo filling the screen, shown once */
(function () {
  var splash = document.getElementById("pd-splash");
  if (!splash) return;
  if (!document.body.classList.contains("home")) return;
  var seen = false;
  try { seen = localStorage.getItem("pd-splash-seen") === "1"; } catch (e) {}
  if (seen) return;
  try { localStorage.setItem("pd-splash-seen", "1"); } catch (e) {}
  if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) return;
  splash.hidden = false;
  document.body.classList.add("splash-lock");
  var done = false;
  function dismiss() {
    if (done) return;
    done = true;
    splash.classList.add("bye");
    document.body.classList.remove("splash-lock");
    document.removeEventListener("keydown", dismiss);
    setTimeout(function () { splash.hidden = true; }, 500);
  }
  setTimeout(dismiss, 2600);
  setTimeout(dismiss, 5000); /* hard stop: never trap a visitor */
  splash.addEventListener("click", dismiss);
  document.addEventListener("keydown", dismiss);
})();

/* Ticker price: existing mempool.space feed, refreshed once a minute.
   No request from local/offline guides. Hide failed or invalid quotes so a
   previously displayed price is never presented as a fresh result. */
(function () {
  var el = document.getElementById("ticker-price");
  if (!el || window.PD_OFFLINE_ROOT || !/^https?:$/.test(location.protocol)) return;
  function hide() { el.hidden = true; el.textContent = ""; }
  function load() {
    if (navigator.onLine === false) { hide(); return; }
    var controller = new AbortController();
    var timeout = setTimeout(function () { controller.abort(); }, 10000);
    return fetch("https://mempool.space/api/v1/prices", {
      signal: controller.signal, credentials: "omit", referrerPolicy: "no-referrer"
    })
      .then(function (r) {
        if (!r.ok) throw new Error("Price unavailable");
        return r.json();
      })
      .then(function (p) {
        if (!p || !Number.isFinite(p.USD) || p.USD <= 0) throw new Error("Invalid price");
        el.textContent = "BTC $" + p.USD.toLocaleString("en-US");
        el.title = "BTC / USD · mempool.space · updates every minute";
        el.hidden = false;
      })
      .catch(hide)
      .finally(function () { clearTimeout(timeout); });
  }
  load();
  setInterval(load, 60000);
  window.addEventListener("offline", hide);
  window.addEventListener("online", load);
})();

/* ---------- Ask the guide: header search over a build-time index ----------
   The index is a static JSON file on this same site, fetched once when the
   visitor first opens the search. Nothing typed is sent anywhere: matching
   happens in this script, and only a tap on an email link leaves the page. */
(function () {
  "use strict";
  var btn = document.getElementById("ask-btn");
  var backdrop = document.getElementById("ask-backdrop");
  var input = document.getElementById("ask-input");
  var results = document.getElementById("ask-results");
  if (!btn || !backdrop || !input || !results) return;

  var CONTACT = "Muststackmoresats@gmail.com";
  var SUBJECT = "Question about Plebum Dominium";
  var START = ["checklist", "verify", "airgap", "faq"];
  var index = null, indexFailed = false, loading = false;
  var selected = -1, lastFocus = null;

  function basePath() {
    var s = document.querySelector('script[src*="assets/js/main.js"]');
    if (s) {
      var src = s.getAttribute("src") || "";
      var i = src.indexOf("assets/js/main.js");
      if (i !== -1) return src.slice(0, i);
    }
    return "/";
  }

  function mailto(q) {
    return "mailto:" + CONTACT + "?subject=" + encodeURIComponent(SUBJECT) +
      "&body=" + encodeURIComponent("Question about Plebum Dominium:\n\n" + q);
  }

  function esc(s) {
    return s.replace(/&/g, "&amp;").replace(/</g, "&lt;")
      .replace(/>/g, "&gt;").replace(/"/g, "&quot;");
  }

  function words(q) {
    return q.toLowerCase().split(/\s+/).filter(function (w) { return w.length > 1; });
  }

  function highlight(text, ws) {
    var out = esc(text);
    ws.forEach(function (w) {
      var re = new RegExp("(" + w.replace(/[.*+?^${}()|[\]\\]/g, "\\$&") + ")", "gi");
      out = out.replace(re, '<mark class="ask-hit">$1</mark>');
    });
    return out;
  }

  function snippet(e, ws) {
    var text = e.text, lower = text.toLowerCase(), pos = -1;
    ws.forEach(function (w) {
      var p = lower.indexOf(w);
      if (p !== -1 && (pos === -1 || p < pos)) pos = p;
    });
    if (pos === -1) return highlight(text.slice(0, 140), ws);
    var start = Math.max(0, pos - 60), end = Math.min(text.length, pos + 90);
    var s = text.slice(start, end);
    if (start > 0) s = "…" + s;
    if (end < text.length) s = s + "…";
    return highlight(s, ws);
  }

  function search(q) {
    var ws = words(q), scored = [];
    index.forEach(function (e) {
      var title = e.title.toLowerCase(), body = e.text.toLowerCase(), score = 0;
      if (q.trim() === e.num) score += 200;
      ws.forEach(function (w) {
        if (title.indexOf(w) !== -1) score += 50;
        if (body.indexOf(w) !== -1) score += 10;
      });
      if (score > 0) scored.push({ e: e, score: score });
    });
    scored.sort(function (a, b) { return b.score - a.score; });
    return scored.slice(0, 6).map(function (s) { return s.e; });
  }

  function rowHTML(e, ws, withSnippet) {
    var snip = withSnippet ? '<span class="ask-snippet">' + snippet(e, ws) + "</span>" : "";
    return '<a class="ask-row" href="' + esc(e.url) + '"><span class="ask-num">' +
      esc(e.num) + '</span><span><span class="ask-row-title">' +
      highlight(e.title, ws) + "</span>" + snip + "</span></a>";
  }

  function findEntry(slug) {
    for (var i = 0; i < index.length; i++) if (index[i].slug === slug) return index[i];
    return null;
  }

  function renderStart() {
    var html = '<p class="ask-start-label">Start with</p>';
    START.forEach(function (slug) {
      var e = findEntry(slug);
      if (e) html += rowHTML(e, [], false);
    });
    results.innerHTML = html;
    selected = -1;
  }

  function renderResults(q) {
    var ws = words(q);
    if (!ws.length) { renderStart(); return; }
    var hits = search(q);
    if (!hits.length) {
      results.innerHTML = '<p class="ask-empty">Nothing in the guide matches \u2018' +
        esc(q) + '\u2019 yet.</p><p class="ask-action-row"><a href="' + mailto(q) +
        '">Email this question</a><a href="' + basePath() +
        '">Browse the full program</a></p>';
      selected = -1;
      return;
    }
    var html = hits.map(function (e) { return rowHTML(e, ws, true); }).join("");
    html += '<p class="ask-email-row">Not what you needed? <a href="' + mailto(q) +
      '">Email this question</a></p>';
    results.innerHTML = html;
    selected = -1;
  }

  function loadIndex() {
    if (loading) return;
    loading = true;
    var searchPath = document.body.getAttribute('data-guide-path');
    if (!searchPath) { try { searchPath = localStorage.getItem('pd-path') === 'one' ? 'one' : 'three'; } catch (e) { searchPath = 'three'; } }
    fetch(basePath() + 'paths/' + searchPath + '/search-index.json')
      .then(function (r) { return r.json(); })
      .then(function (data) {
        loading = false;
        index = data;
        if (input.value) renderResults(input.value); else renderStart();
      })
      .catch(function () {
        loading = false;
        indexFailed = true;
        results.innerHTML = '<p class="ask-empty">Search is not available right now.</p>';
      });
  }

  // Save each sibling's prior state, including an already inert navigation panel.
  var background = [];
  function isolateDialog() {
    var node = backdrop;
    while (node.parentElement && node !== document.body) {
      Array.from(node.parentElement.children).forEach(function (sibling) {
        if (sibling === node) return;
        background.push({ node: sibling, inert: sibling.inert });
        sibling.inert = true;
      });
      node = node.parentElement;
    }
  }
  function containTab(e) {
    var focusable = Array.from(backdrop.querySelectorAll(
      'a[href], button, input, textarea, select, [tabindex]'
    )).filter(function (node) {
      return !node.disabled && node.tabIndex >= 0 && !node.closest('[inert]') && node.getClientRects().length;
    });
    var first = focusable[0] || input;
    var last = focusable[focusable.length - 1] || input;
    var active = document.activeElement;
    if (focusable.indexOf(active) === -1 || (e.shiftKey ? active === first : active === last)) {
      e.preventDefault();
      (e.shiftKey ? last : first).focus();
    }
  }

  function open() {
    if (!backdrop.hidden) return;
    lastFocus = document.activeElement;
    backdrop.hidden = false;
    isolateDialog();
    input.focus();
    if (index) renderStart();
    else if (indexFailed) results.innerHTML = '<p class="ask-empty">Search is not available right now.</p>';
    else {
      results.innerHTML = '<p class="ask-empty">Loading the guide index…</p>';
      loadIndex();
    }
  }

  function close() {
    if (backdrop.hidden) return;
    backdrop.hidden = true;
    background.forEach(function (item) { item.node.inert = item.inert; });
    background = [];
    if (lastFocus && lastFocus.focus) lastFocus.focus();
  }

  btn.addEventListener("click", open);
  backdrop.addEventListener("click", function (e) { if (e.target === backdrop) close(); });
  input.addEventListener("input", function () { if (index) renderResults(input.value); });
  input.addEventListener("keydown", function (e) {
    var rows = results.querySelectorAll(".ask-row");
    if (e.key === "Escape") { close(); return; }
    if (e.key === "ArrowDown" && rows.length) {
      e.preventDefault();
      selected = Math.min(selected + 1, rows.length - 1);
    } else if (e.key === "ArrowUp" && rows.length) {
      e.preventDefault();
      selected = Math.max(selected - 1, 0);
    } else if (e.key === "Enter" && rows.length) {
      e.preventDefault();
      var r = rows[selected >= 0 ? selected : 0];
      if (r) window.location.href = r.getAttribute("href");
      return;
    } else return;
    rows.forEach(function (r, i) { r.classList.toggle("selected", i === selected); });
  });
  document.addEventListener("keydown", function (e) {
    if (e.key === "Escape" && !backdrop.hidden) { close(); return; }
    if (e.key === "Tab" && !backdrop.hidden) { containTab(e); return; }
    if (e.key !== "/") return;
    if (!backdrop.hidden) return;
    var t = document.activeElement;
    if (t && (t.tagName === "INPUT" || t.tagName === "TEXTAREA" || t.isContentEditable)) return;
    e.preventDefault();
    open();
  });
})();

/* --- online status dot: green on the live site, orange on a saved copy or with no network --- */
(function () {
  "use strict";
  var pill = document.getElementById("online-pill");
  if (!pill) return;
  var dot = document.getElementById("online-dot");
  var word = document.getElementById("online-word");
  function render() {
    var offline = (location.protocol === "file:") || !navigator.onLine;
    pill.hidden = false;
    dot.classList.toggle("offline", offline);
    word.textContent = offline ? "Offline" : "Online";
  }
  window.addEventListener("online", render);
  window.addEventListener("offline", render);
  render();
})();

/* --- hero keyring as quorum demo: the animation runs until a tap takes over --- */
(function () {
  "use strict";
  var ring = document.getElementById("keyring");
  if (!ring) return;
  var lock = document.getElementById("keyring-lock");
  var caption = document.getElementById("keyring-caption");
  var desc = document.getElementById("keyring-descriptor");
  var resetBtn = document.getElementById("keyring-reset");
  var keys = ring.querySelectorAll(".key");
  function selectedCount() {
    return ring.querySelectorAll(".key.sel").length;
  }
  function setSelected(key, selected) {
    key.classList.toggle("sel", selected);
    key.setAttribute("aria-pressed", String(selected));
  }
  function update() {
    var n = selectedCount();
    if (lock) lock.classList.toggle("open", n >= 2);
    if (resetBtn) resetBtn.hidden = n === 0;
    if (n === 0) {
      caption.innerHTML = "<strong>Vault locked.</strong> No keys selected.";
      desc.textContent = "Always preserve the verified wallet configuration.";
    } else if (n === 1) {
      caption.innerHTML = "<strong>Vault locked.</strong> One key alone cannot spend.";
      desc.textContent = "Choose a second key to meet the signing threshold.";
    } else if (n === 2) {
      caption.innerHTML = "<strong>Two keys can sign.</strong> Use the saved wallet map to recover.";
      desc.textContent = "If one seed plate is missing, the verified descriptor supplies that signer’s public key. Select the third key to see how recovery works without the saved file.";
    } else {
      caption.innerHTML = "<strong>No saved descriptor file needed.</strong> All three original seeds can rebuild this wallet.";
      desc.textContent = "The third seed lets you re-derive the last public key. Recreate the original 2-of-3 native SegWit setup using the guide’s derivation path, then verify a known receive address. Only two signatures are needed to spend.";
    }
  }
  function reset() {
    keys.forEach(function (key) { setSelected(key, false); });
    update();
  }
  keys.forEach(function (key) {
    key.addEventListener("click", function () {
      ring.classList.add("tapped");
      setSelected(key, !key.classList.contains("sel"));
      update();
    });
  });
  document.addEventListener("click", function (event) {
    if (selectedCount() && !ring.contains(event.target)) reset();
  });
  if (resetBtn) {
    resetBtn.addEventListener("click", function () {
      reset();
      keys[0].focus();
    });
  }
})();

/* ---------- motion: one toggle stops all motion, saved on this device ---------- */
(function () {
  var root = document.documentElement;
  var btn = document.getElementById("motion-btn");
  function applyMotion(m) {
    root.setAttribute("data-motion", m);
    if (btn) {
      btn.setAttribute("aria-pressed", m === "on" ? "true" : "false");
      btn.textContent = m === "on" ? "Motion on" : "Motion off";
    }
    var frames = document.querySelectorAll("iframe");
    for (var i = 0; i < frames.length; i++) {
      try { frames[i].contentWindow.postMessage({ type: "pd-motion", motion: m }, "*"); } catch (e) {}
    }
  }
  function setMotion(m) {
    try { localStorage.setItem("pd-motion", m); } catch (e) {}
    applyMotion(m);
  }
  if (btn) {
    btn.addEventListener("click", function () {
      setMotion(root.getAttribute("data-motion") === "off" ? "on" : "off");
    });
  }
  applyMotion(root.getAttribute("data-motion") || "on");
  try {
    var mq = window.matchMedia("(prefers-reduced-motion: reduce)");
    mq.addEventListener("change", function (e) {
      if (!localStorage.getItem("pd-motion")) applyMotion(e.matches ? "off" : "on");
    });
  } catch (e) {}
})();

/* ---------- independent, URL-addressable learning paths ---------- */
(function () {
  'use strict';
  var BASE = '/plebum-dominium-test/';
  var PATHS = {
    one: { label: 'One key + passphrase', steps: ['terms','threat-model','choose-path','checklist','airgap','verify','dice','single-sig','titanium','inheritance','faq','fire-card'] },
    three: { label: 'Three keys', steps: ['terms','threat-model','choose-path','checklist','airgap','verify','dice','sparrow','testnet','signing','titanium','encryption','inheritance','faq','briefing','fire-card'] }
  };
  var titles = {'choose-path':'Pick your path','threat-model':'Before you begin', terms:'Terms', checklist:'Checklist',verify:'Check the files',airgap:'Two boots',dice:'Make three keys','single-sig':'One key + passphrase',titanium:'Back up your keys and wallet map',inheritance:'If I am gone',faq:'If you get stuck','fire-card':'Recovery card',sparrow:'Build the 2-of-3',signing:'Practice spending and recovery',testnet:'Set up a test wallet',encryption:'Protect the wallet map',briefing:'Tough questions'};
  function link(path,slug) { return BASE+'paths/'+path+'/'+slug+'.html'; }
  var route = document.body.getAttribute('data-guide-path');
  var file = (location.pathname.split('/').pop() || '').replace(/\.html$/,'');
  var slug = document.body.getAttribute('data-guide-slug') || file.replace(/-(one|easy)$/,'');
  var saved = 'three';
  try { saved = localStorage.getItem('pd-path') === 'one' ? 'one' : 'three'; } catch(e) {}
  var path = route || (/-one$/.test(file) ? 'one' : saved);
  // Old bookmarks resolve to the matching route, never a hidden-content gate.
  if (!route && location.pathname.indexOf(BASE+'handouts/') === 0) {
    if (PATHS[path].steps.indexOf(slug) < 0) path = PATHS.one.steps.indexOf(slug) >= 0 ? 'one' : 'three';
    if (PATHS[path].steps.indexOf(slug) >= 0) {
      location.replace(link(path,slug)+location.search+location.hash);
      return;
    }
  }
  document.documentElement.setAttribute('data-path',path === 'one' ? 'one' : 'full');
  try { localStorage.setItem('pd-path',path === 'one' ? 'one' : 'full'); } catch(e) {}
  document.body.classList.remove('path-gated');
  document.querySelectorAll('#path-gate,#path-banner').forEach(function(el) { el.remove(); });
  var info=PATHS[path];
  var count=document.getElementById('path-count');
  if(count) count.textContent=info.label+' · '+info.steps.length+' steps';
  // Supporting pages offer the same complete sidebar; path pages already contain it statically.
  if (!route) {
    var list=document.querySelector('.sidebar ul');
    if(list) {
      list.textContent='';
      info.steps.forEach(function(s,i) {
        var li=document.createElement('li'), a=document.createElement('a');
        a.href=link(path,s);
        var n=document.createElement('span');n.className='sheet-num';n.textContent=String(i+1).padStart(2,'0');
        var t=document.createElement('span');t.className='sheet-title';t.textContent=path==='one'&&s==='dice'?'Make one key':path==='one'&&s==='titanium'?'Back up your key':titles[s];
        a.append(n,t);li.appendChild(a);list.appendChild(li);
      });
    }
    // Non-sequence handouts remain readable as optional references, with a route back.
    if(location.pathname.indexOf(BASE+'handouts/')===0) {
      document.querySelectorAll('.header-sheet,.kicker').forEach(function(el){el.textContent='Optional reference';});
      document.querySelectorAll('.step-banner,.prevnext-row').forEach(function(el){
        el.textContent='';var a=document.createElement('a');a.className='step-nav';a.href=link(path,'index');a.textContent='Return to '+info.label+' overview';el.appendChild(a);
      });
    }
  }
  function switchPath(value) {
    var target=value==='one'?'one':'three';
    var next=PATHS[target].steps.indexOf(slug)>=0?slug:'terms';
    location.href=link(target,next);
  }
  window.pdSetPath=switchPath;
  document.querySelectorAll('#sidebar-path button[data-path], .path-seg button[data-path]').forEach(function(b){
    b.setAttribute('aria-pressed',(b.getAttribute('data-path')==='one' ? 'one':'three')===path?'true':'false');
    b.addEventListener('click',function(){switchPath(b.getAttribute('data-path'));});
  });
  function showRisks(value) {
    document.querySelectorAll('.path-risks-switch button[data-path]').forEach(function(b){b.setAttribute('aria-pressed',b.getAttribute('data-path')===value?'true':'false');});
    ['one','full'].forEach(function(k){var sec=document.getElementById('risks-'+k);if(sec) sec.classList.toggle('path-hidden',k!==value);});
    var label=document.getElementById('path-risks-label');if(label)label.textContent=value==='one'?PATHS.one.label:PATHS.three.label;
  }
  showRisks(path==='one'?'one':'full');
  document.querySelectorAll('.path-risks-switch button[data-path]').forEach(function(b){b.addEventListener('click',function(){showRisks(b.getAttribute('data-path'));});});
  // Keep links from home, search results, and contextual references inside the active route
  // when that sheet exists there. Other references stay readable and are never gated.
  function routeLinks(root) {
    root.querySelectorAll('a[href]').forEach(function(a){
      var u=new URL(a.getAttribute('href'),location.href);
      if(u.origin!==location.origin || u.pathname.indexOf(BASE+'handouts/')!==0)return;
      var s=u.pathname.split('/').pop().replace(/\.html$/,'').replace(/-(one|easy)$/,'');
      if(info.steps.indexOf(s)>=0)a.setAttribute('href',link(path,s)+u.search+u.hash);
    });
  }
  routeLinks(document);
  // Reuse the sidebar's resolved route for the fixed mobile sheet strip.
  var mobilebar = document.querySelector('.mobilebar');
  var sheets = document.querySelectorAll('.sidebar ul a[href]');
  if (mobilebar && sheets.length) {
    var mobileNav = document.createElement('nav');
    mobileNav.className = 'mobilebar-track';
    mobileNav.setAttribute('aria-label', info.label + ' guide sheets');
    var currentSheet;
    sheets.forEach(function (sheet) {
      var number = sheet.querySelector('.sheet-num');
      var title = sheet.querySelector('.sheet-title');
      if (!title) return;
      var item = document.createElement('a');
      item.href = sheet.href;
      item.textContent = (number ? number.textContent + ' · ' : '') + title.textContent;
      if (item.pathname === location.pathname) {
        item.setAttribute('aria-current', 'page');
        currentSheet = item;
      }
      mobileNav.appendChild(item);
    });
    if (mobileNav.childElementCount) {
      var label = document.createElement('button');
      label.type = 'button';
      label.className = 'mobilebar-label';
      label.textContent = path === 'one' ? 'One key' : 'Three keys';
      label.setAttribute('aria-label', info.label + '. Switch to ' +
        (path === 'one' ? PATHS.three.label : PATHS.one.label));
      label.addEventListener('click', function () {
        switchPath(path === 'one' ? 'full' : 'one');
      });
      mobilebar.replaceChildren(label, mobileNav);
      mobilebar.removeAttribute('aria-label');
      mobilebar.classList.add('mobilebar-sheets');
      document.body.classList.add('has-mobile-sheets');
      if (currentSheet) {
        var mobileViewport = window.matchMedia('(max-width: 760px)');
        var showCurrentSheet = function () {
          if (mobileViewport.matches) {
            mobileNav.scrollLeft = currentSheet.getBoundingClientRect().left -
              mobileNav.getBoundingClientRect().left + mobileNav.scrollLeft - 8;
          }
        };
        showCurrentSheet();
        mobileViewport.addEventListener('change', showCurrentSheet);
      }
    }
  }
  var results=document.querySelector('#ask-results');
  if(results)new MutationObserver(function(){routeLinks(results);}).observe(results,{childList:true,subtree:true});
})();

/* --- Why section: tier view switcher (mobile, no sideways scroll; view only, never chooses the path) --- */
(function () {
  document.querySelectorAll('.tier-switch').forEach(function (sw) {
    var table = sw.parentElement.querySelector('.tier-chart');
    if (!table) return;
    sw.addEventListener('click', function (e) {
      var b = e.target.closest('button');
      if (!b) return;
      table.setAttribute('data-tier', b.getAttribute('data-tier'));
      sw.querySelectorAll('button').forEach(function (x) { x.classList.toggle('on', x === b); });
    });
  });
})();

/* Feedback is a link only: no Google scripts or background requests.
   Never attach feedback controls to offline custody tools. */
(function () {
  if (location.protocol !== 'https:' || location.hostname !== 'musthavemustash.github.io' ||
      location.pathname.indexOf('/plebum-dominium-test/') !== 0) return;
  var footer = document.querySelector('.site-footer');
  if (!footer || document.querySelector('[data-feedback-link]')) return;
  var note = document.createElement('p');
  var link = document.createElement('a');
  link.setAttribute('data-feedback-link', '');
  link.href = 'https://docs.google.com/forms/d/e/1FAIpQLSfOkY3FrZmZpIVro5oxWLy_YvU7U-1BOrL3KB9VCI3jXjad2Q/viewform';
  link.rel = 'noreferrer';
  link.textContent = 'Give feedback on this page (Google Form)';
  note.appendChild(link);
  note.appendChild(document.createTextNode(' — include this page’s link. Never submit wallet secrets.'));
  var checklist = document.createElement('a');
  checklist.href = '/plebum-dominium-test/test-the-site.html';
  checklist.textContent = 'Tester tasks and expected results';
  note.appendChild(document.createTextNode(' '));
  note.appendChild(checklist);
  footer.appendChild(note);
})();
