(() => {
  const path = location.pathname === '/open/' ? '/open/' : '/';
  const destination = 'https://owouwuiwi.github.io' + path + location.search + location.hash;
  document.getElementById('destination').href = destination;
  location.replace(destination);
})();
