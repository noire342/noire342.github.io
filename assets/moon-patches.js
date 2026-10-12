(() => {
  const button = document.querySelector('[data-copy-source]');
  const source = document.getElementById('moon-source-url');
  const status = document.querySelector('[data-copy-status]');
  if (button && source && status) {
    button.hidden = false;
    button.addEventListener('click', async () => {
      button.disabled = true;
      try {
        if (!navigator.clipboard?.writeText) throw new Error('Clipboard unavailable');
        await navigator.clipboard.writeText(source.textContent.trim());
        status.textContent = 'Copied. Paste in Morphe → Sources → + → Remote.';
      } catch {
        const range = document.createRange();
        range.selectNodeContents(source);
        const selection = window.getSelection();
        selection?.removeAllRanges();
        selection?.addRange(range);
        status.textContent = 'The address is selected. Copy it and paste it in Morphe.';
      } finally {
        button.disabled = false;
      }
    });
  }

  const preference = matchMedia('(prefers-reduced-motion: reduce)');
  if (preference.matches || !('IntersectionObserver' in window) || !Element.prototype.animate) return;
  const active = new Map();
  const observer = new IntersectionObserver(entries => {
    let stagger = 0;
    for (const entry of entries) {
      if (!entry.isIntersecting) continue;
      const element = entry.target;
      observer.unobserve(element);
      if (preference.matches || document.hidden || entry.boundingClientRect.top < 0 || element.contains(document.activeElement)) continue;
      const animation = element.animate([
        { opacity: 0, translate: '0 12px' }, { opacity: 1, translate: '0 0' },
      ], { duration: 500, delay: Math.min(stagger++ * 40, 200), easing: 'cubic-bezier(.22,1,.36,1)', fill: 'backwards' });
      active.set(element, animation);
      const clear = () => { if (active.get(element) === animation) active.delete(element); };
      animation.addEventListener('finish', clear, { once: true });
      animation.addEventListener('cancel', clear, { once: true });
    }
  }, { rootMargin: '0px 0px -24px 0px' });
  document.querySelectorAll('[data-reveal]').forEach(element => observer.observe(element));
  const settle = () => { for (const animation of active.values()) animation.cancel(); active.clear(); };
  preference.addEventListener('change', () => { if (preference.matches) { observer.disconnect(); settle(); } });
  document.addEventListener('visibilitychange', () => { if (document.hidden) settle(); });
  document.addEventListener('focusin', event => { for (const [element, animation] of active) { if (element.contains(event.target)) animation.cancel(); } });
})();
