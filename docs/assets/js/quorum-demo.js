(() => {
  const card = document.querySelector('#quorum-demo .quorum-card');
  const keys = [...card.querySelectorAll('.quorum-key')];
  const map = card.querySelector('.quorum-map');
  const lock = card.querySelector('.quorum-lock');
  const sign = document.getElementById('quorum-sign');
  const recover = document.getElementById('quorum-recover');
  const presets = [
    {button: document.getElementById('quorum-cap-sign'), keyCount: 2, hasMap: false},
    {button: document.getElementById('quorum-cap-watch'), keyCount: 0, hasMap: true},
    {button: document.getElementById('quorum-cap-full'), keyCount: 2, hasMap: true}
  ];
  const selected = button => button.getAttribute('aria-pressed') === 'true';
  function capability(name, ready, label) {
    const indicator = document.getElementById('quorum-cap-' + name);
    indicator.dataset.ready = String(ready);
    indicator.querySelector('span').textContent = label;
  }
  function render() {
    const count = keys.filter(selected).length;
    const hasMap = selected(map);
    for (const preset of presets) {
      preset.button.setAttribute('aria-pressed', String(count === preset.keyCount && hasMap === preset.hasMap));
    }
    const canSign = count >= 2;
    const canRebuild = count === 3;
    const canWatch = hasMap || canRebuild;
    const canRecover = canSign && canWatch;
    capability('sign', canSign, canSign ? 'Threshold met' : 'Needs two keys');
    capability('watch', canWatch, hasMap ? 'Available via map' : canRebuild ? 'Available after rebuild' : 'Needs wallet map');
    capability('full', canRecover, canRebuild ? 'Rebuild from three seeds' : canRecover ? 'Two keys + map' : 'Needs more backups');
    lock.classList.toggle('open', canSign);
    lock.querySelector('.quorum-lock-body').textContent = canSign ? 'Open' : 'Locked';
    sign.textContent = canSign ? 'Open · Two keys can sign a correctly prepared transaction.' : count === 1 ? 'Locked · One more key is needed.' : 'Locked · Choose two keys.';
    if (count === 3) {
      recover.textContent = 'No saved descriptor file needed. All three original seeds can rebuild the wallet using its original settings.';
    } else if (count === 2) {
      recover.textContent = hasMap ? 'Ready to recover. The saved map supplies the third signer’s public key.' : 'Signing only. Add the wallet map or the third seed for full recovery.';
    } else if (hasMap) {
      recover.textContent = 'Watch-only. The map can recreate wallet addresses and track balances. Spending requires two signing keys.';
    } else {
      recover.textContent = 'Select keys or add the wallet map.';
    }
  }
  function setSetup(keyCount, hasMap) {
    keys.forEach((key, index) => key.setAttribute('aria-pressed', String(index < keyCount)));
    map.setAttribute('aria-pressed', String(hasMap));
    render();
  }
  function reset() {
    setSetup(0, false);
  }
  for (const preset of presets) {
    preset.button.addEventListener('click', () => {
      if (selected(preset.button)) {
        reset();
      } else {
        setSetup(preset.keyCount, preset.hasMap);
      }
    });
  }
  for (const button of [...keys, map]) {
    button.addEventListener('click', () => {
      button.setAttribute('aria-pressed', String(!selected(button)));
      render();
    });
  }
  card.querySelector('.quorum-reset').addEventListener('click', reset);
  document.addEventListener('click', event => {
    if (!card.contains(event.target)) reset();
  });
})();
