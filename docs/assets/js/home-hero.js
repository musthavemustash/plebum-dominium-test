// Homepage hero definitions. No storage, network calls, or wallet data.
(() => {
      const root = document.getElementById('plebum-home-hero');
      if (!root) return;
      const tiles = [...root.querySelectorAll('[data-pd-topic]')];
      const hero = root.querySelector('.pd-hero');
      const shelf = root.querySelector('.pd-shelf');
      const popup = root.querySelector('.pd-popout');
      const leader = root.querySelector('.pd-leader');
      const line = leader.querySelector('polyline');
      const dot = leader.querySelector('circle');
      const heading = root.querySelector('.pd-pop-title');
      const description = root.querySelector('.pd-pop-text');
      const index = root.querySelector('.pd-pop-index');
      const closeButton = root.querySelector('.pd-pop-close');
      const announcement = root.querySelector('[data-pd-announcement]');
      const topics = {
        bitcoin: { title: 'Bitcoin', text: 'Digital money you can hold and send yourself, without a bank holding it for you.' },
        dice: { title: 'Dice', text: 'Dice rolls provide randomness—the starting point for creating your wallet’s secret keys.' },
        home: { title: 'At home', text: 'Build and practice your self-custody setup at home, with an offline computer.' },
        metal: { title: 'On metal', text: 'Durable metal backups are geographically separated to protect your recovery information from a single point of failure.' }
      };
      let pinned = null, hovered = null, focused = null, displayed = null;
      let leaveTimer = null, lastTrigger = null, suppressFocus = false;
      const clamp = (value, low, high) => Math.max(low, Math.min(high, value));
      const cancelLeave = () => { clearTimeout(leaveTimer); leaveTimer = null; };
      function positionPopup() {
        if (!displayed || popup.hidden) return;
        const tile = tiles.find(item => item.dataset.pdTopic === displayed);
        const bounds = hero.getBoundingClientRect();
        const target = tile.getBoundingClientRect();
        const width = hero.clientWidth, height = hero.clientHeight;
        const x = target.left - bounds.left - hero.clientLeft + target.width / 2;
        const y = target.top - bounds.top - hero.clientTop + 3;
        const left = clamp(x - popup.offsetWidth / 2, 12, width - popup.offsetWidth - 12);
        const top = Math.max(12, y - 35 - popup.offsetHeight);
        popup.style.left = left + 'px';
        popup.style.top = top + 'px';
        const bottom = top + popup.offsetHeight;
        const startX = clamp(x + (x < width / 2 ? 23 : -23), left + 18, left + popup.offsetWidth - 18);
        leader.setAttribute('viewBox', '0 0 ' + width + ' ' + height);
        line.setAttribute('points', startX + ',' + bottom + ' ' + startX + ',' + (bottom + 7) + ' ' + x + ',' + (y - 10) + ' ' + x + ',' + y);
        dot.setAttribute('cx', x);
        dot.setAttribute('cy', y);
      }
      function render(announce = false) {
        const key = hovered || focused || pinned;
        displayed = key;
        tiles.forEach(tile => {
          const active = tile.dataset.pdTopic === key;
          tile.dataset.active = String(active);
          tile.setAttribute('aria-expanded', String(active));
          tile.querySelector('.pd-item-hint').textContent = active ? '−' : '+';
        });
        popup.hidden = !key;
        leader.toggleAttribute('hidden', !key);
        if (key) {
          lastTrigger = tiles.find(tile => tile.dataset.pdTopic === key);
          index.textContent = String(tiles.indexOf(lastTrigger) + 1).padStart(2, '0');
          heading.textContent = topics[key].title;
          description.textContent = topics[key].text;
          positionPopup();
        }
        if (announce) announcement.textContent = key ? topics[key].title + '. ' + topics[key].text : 'Definition closed.';
      }
      function closeDefinition(restoreFocus = false) {
        cancelLeave();
        pinned = hovered = focused = null;
        render();
        announcement.textContent = '';
        if (restoreFocus && lastTrigger) {
          suppressFocus = true;
          lastTrigger.focus({preventScroll:true});
          suppressFocus = false;
        }
      }
      function scheduleLeave() {
        cancelLeave();
        leaveTimer = setTimeout(() => { hovered = null; render(); }, 180);
      }
      tiles.forEach(tile => {
        const key = tile.dataset.pdTopic;
        tile.addEventListener('pointerenter', event => {
          if (event.pointerType === 'touch') return;
          cancelLeave(); hovered = key; render();
        });
        tile.addEventListener('focus', () => {
          if (suppressFocus || !tile.matches(':focus-visible')) return;
          cancelLeave(); focused = key; hovered = null; render(true);
        });
        tile.addEventListener('blur', event => {
          if (popup.contains(event.relatedTarget)) return;
          focused = null; render();
        });
        tile.addEventListener('click', () => {
          cancelLeave(); pinned = pinned === key ? null : key;
          hovered = focused = null; render(true);
        });
      });
      shelf.addEventListener('pointerleave', event => {
        if (event.pointerType !== 'touch') scheduleLeave();
      });
      popup.addEventListener('pointerenter', cancelLeave);
      popup.addEventListener('pointerleave', event => {
        if (event.pointerType !== 'touch') scheduleLeave();
      });
      popup.addEventListener('focusout', event => {
        if (!popup.contains(event.relatedTarget)) { focused = null; render(); }
      });
      closeButton.addEventListener('click', () => closeDefinition(true));
      document.addEventListener('pointerdown', event => {
        if (shelf.contains(event.target) || popup.contains(event.target)) return;
        closeDefinition();
      });
      root.addEventListener('keydown', event => {
        if (event.key === 'Escape') {
          closeDefinition(popup.contains(document.activeElement));
          event.preventDefault();
        }
      });
      new ResizeObserver(positionPopup).observe(hero);
      render();

    })();
