const block = document.querySelector('.t-stagger');
if (block && !window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
  const lines = block.querySelectorAll('[data-reveal]');
  lines.forEach((line, index) => {
    line.classList.add('t-stagger-line');
    if (index > 0) line.classList.add('t-stagger-line--2');
  });
  function showText() {
    block.classList.remove('is-hiding');
    block.classList.remove('is-shown');
    void block.offsetHeight;
    block.classList.add('is-shown');
  }
  showText();
  block.addEventListener('transitionend', () => {
    lines.forEach(line => { line.style.willChange = 'auto'; });
  }, { once: true });
}

// This is a site illustration, not the app's algorithm or a device screenshot.
const hours = ['midnight', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'ten', 'eleven'];
const amounts = {5: 'five', 10: 'ten', 20: 'twenty', 25: 'twenty-five'};
function phraseFor(minutes) {
  const hour = Math.floor(minutes / 60) % 24;
  const minute = minutes % 60;
  const current = hour === 12 ? 'noon' : hours[hour % 12];
  const nextHour = (hour + 1) % 24;
  const next = nextHour === 12 ? 'noon' : hours[nextHour % 12];
  if (minute >= 55) return 'almost ' + next + '.';
  const rounded = Math.round(minute / 5) * 5;
  if (rounded === 0) return 'about ' + current + '.';
  if (rounded === 15) return 'quarter past ' + current + '.';
  if (rounded === 30) return 'half past ' + current + '.';
  if (rounded === 45) return 'quarter to ' + next + '.';
  if (rounded < 30) return amounts[rounded] + ' past ' + current + '.';
  return amounts[60 - rounded] + ' to ' + next + '.';
}
const time = document.getElementById('demo-time');
const exact = document.getElementById('demo-exact');
const phrase = document.getElementById('approximate-time');
const presets = document.querySelectorAll('[data-minute]');
function showTime(minutes) {
  const bounded = Math.max(0, Math.min(1439, Math.round(minutes)));
  const clock = String(Math.floor(bounded / 60)).padStart(2, '0') + ':' + String(bounded % 60).padStart(2, '0');
  const wording = phraseFor(bounded);
  time.value = String(bounded);
  time.setAttribute('aria-valuetext', clock + ' — ' + wording);
  exact.value = clock;
  if (phrase.textContent !== wording) phrase.textContent = wording;
  presets.forEach(button => button.setAttribute('aria-pressed', String(Number(button.dataset.minute) === bounded)));
}
if (time && exact && phrase) {
  time.addEventListener('input', () => showTime(Number(time.value)));
  presets.forEach(button => button.addEventListener('click', () => showTime(Number(button.dataset.minute))));
  document.getElementById('demo-now').addEventListener('click', () => {
    const now = new Date();
    showTime(now.getHours() * 60 + now.getMinutes());
  });
  showTime(Number(time.value));
}
