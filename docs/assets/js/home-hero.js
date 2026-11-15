// Homepage hero introduction and definitions. No storage, network calls, or wallet data.
(() => {
  const root = document.getElementById('plebum-home-hero');
  if (!root) return;
  const tiles = [...root.querySelectorAll('[data-pd-topic]')];
  const hero = root.querySelector('.pd-hero');
  const shelf = root.querySelector('.pd-shelf');
  const intro = root.querySelector('.pd-introduction');
  const popup = root.querySelector('#pd-leader-definition');
  const leader = root.querySelector('.pd-leader');
  const line = leader.querySelector('polyline');
  const dot = leader.querySelector('circle');
  const heading = popup.querySelector('.pd-pop-title');
  const description = popup.querySelector('.pd-pop-text');
  const index = popup.querySelector('.pd-pop-index');
  const closeButton = popup.querySelector('.pd-pop-close');
  const announcement = root.querySelector('[data-pd-announcement]');
  const topics = {
  "bitcoin": {
    "title": "Bitcoin",
    "text": "Bitcoin is digital money you can hold and send without a bank holding it for you. In self-custody, you control the keys that authorize spending. This guide helps you understand those keys, check your setup, and practice recovery so you can take responsibility for your own Bitcoin."
  },
  "dice": {
    "title": "Dice",
    "text": "Dice rolls provide randomness you can create and record yourself. You turn those rolls into wallet seed words with offline software, then check the result. The guide walks you through the rolling, recording, and verification. Dice supply the randomness; careful software checks and recovery practice still matter."
  },
  "home": {
    "title": "At home",
    "text": "Build your self-custody setup at home, at your own pace. Use an offline computer for the steps that handle secret information, and practice spending and recovery with test funds. You can download the complete interactive guide, so the instructions and included tools are available while you work offline."
  },
  "metal": {
    "title": "On metal",
    "text": "Metal backups preserve the information you need to recover your wallet if a device is lost or stops working. Practice recovery first, then make and check your metal backups. Store them separately so one incident cannot destroy every copy. A hardware signer is optional after those backups are complete and checked."
  }
};
  let selected = null;
  let lastTrigger = null;
  const clamp = (value, low, high) => Math.max(low, Math.min(high, value));

  function positionLeader() {
    if (!selected || popup.hidden) return;
    const tile = tiles.find(item => item.dataset.pdTopic === selected);
    const bounds = hero.getBoundingClientRect();
    const target = tile.getBoundingClientRect();
    const card = popup.getBoundingClientRect();
    const width = hero.clientWidth, height = hero.clientHeight;
    const x = target.left - bounds.left - hero.clientLeft + target.width / 2;
    const y = target.bottom - bounds.top - hero.clientTop;
    const top = card.top - bounds.top - hero.clientTop;
    const portX = clamp(x, card.left - bounds.left - hero.clientLeft + 24, card.right - bounds.left - hero.clientLeft - 24);
    // Run outside the caption text before landing at the definition's top edge.
    const railX = x < width / 2 ? 15 : width - 15;
    leader.setAttribute('viewBox', '0 0 ' + width + ' ' + height);
    line.setAttribute('points', [x+','+y, x+','+(y+7), railX+','+(y+7), railX+','+(top-12), portX+','+(top-12), portX+','+top].join(' '));
    dot.setAttribute('cx', x);
    dot.setAttribute('cy', y);
  }

  function render(announce = false) {
    tiles.forEach(tile => {
      const active = tile.dataset.pdTopic === selected;
      tile.dataset.active = String(active);
      tile.setAttribute('aria-expanded', String(active));
      tile.querySelector('.pd-item-hint').textContent = active ? '−' : '+';
    });
    popup.hidden = !selected;
    leader.toggleAttribute('hidden', !selected);
    intro.classList.toggle('is-hidden', !!selected);
    intro.toggleAttribute('inert', !!selected);
    intro.setAttribute('aria-hidden', String(!!selected));
    if (selected) {
      lastTrigger = tiles.find(tile => tile.dataset.pdTopic === selected);
      index.textContent = String(tiles.indexOf(lastTrigger) + 1).padStart(2, '0');
      heading.textContent = topics[selected].title;
      description.textContent = topics[selected].text;
      positionLeader();
    }
    if (announce) announcement.textContent = selected ? topics[selected].title + '. ' + topics[selected].text : 'Introduction restored.';
  }

  function closeDefinition(restoreFocus = false) {
    selected = null;
    render();
    announcement.textContent = '';
    if (restoreFocus && lastTrigger) lastTrigger.focus({preventScroll:true});
  }

  const discoveryTile = tiles.find(tile => tile.dataset.pdTopic === 'bitcoin');
  let discoveryObserver = null, discoveryUsed = false;
  function stopDiscovery() {
    discoveryUsed = true;
    if (discoveryObserver) discoveryObserver.disconnect();
    discoveryTile.classList.remove('pd-discover', 'pd-discover-pulse');
  }
  tiles.forEach(tile => {
    tile.addEventListener('click', () => {
      stopDiscovery();
      selected = selected === tile.dataset.pdTopic ? null : tile.dataset.pdTopic;
      render(true);
    });
  });
  closeButton.addEventListener('click', () => closeDefinition(true));
  document.addEventListener('pointerdown', event => {
    if (!shelf.contains(event.target) && !popup.contains(event.target)) closeDefinition();
  });
  root.addEventListener('keydown', event => {
    if (event.key === 'Escape' && selected) {
      closeDefinition(popup.contains(document.activeElement));
      event.preventDefault();
    }
  });
  if ('ResizeObserver' in window) new ResizeObserver(positionLeader).observe(hero);
  window.addEventListener('resize', positionLeader);
  render();

  // Keep the existing discovery glow until a hero tile is activated.
  for (const eventName of ['animationend', 'animationcancel']) {
    discoveryTile.addEventListener(eventName, event => {
      if (event.animationName === 'pd-discover-glow') discoveryTile.classList.remove('pd-discover-pulse');
    });
  }
  if ('IntersectionObserver' in window) {
    discoveryObserver = new IntersectionObserver(entries => {
      if (!entries.some(entry => entry.isIntersecting && entry.intersectionRatio >= 0.5)) return;
      discoveryObserver.disconnect();
      if (discoveryUsed) return;
      discoveryUsed = true;
      discoveryTile.classList.add('pd-discover');
      if (!matchMedia('(prefers-reduced-motion: reduce)').matches && document.documentElement.dataset.motion !== 'off') {
        discoveryTile.classList.add('pd-discover-pulse');
      }
    }, { threshold: 0.5 });
    discoveryObserver.observe(discoveryTile);
  }
})();
