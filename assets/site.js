// The Ethics of a Birmingham Healthy Life: small page behaviours. The site works without this file.

// The contents menu on narrow screens
(function () {
  var bar = document.querySelector('.sidebar');
  var btn = document.querySelector('.menu-toggle');
  if (!bar || !btn) return;
  btn.addEventListener('click', function () {
    var open = bar.classList.toggle('open');
    btn.setAttribute('aria-expanded', open ? 'true' : 'false');
  });
})();

// Live embeds (Tableau) load only when asked, so the page stays light
document.querySelectorAll('[data-embed]').forEach(function (button) {
  button.addEventListener('click', function () {
    var frame = button.closest('.frame');
    var iframe = document.createElement('iframe');
    iframe.src = button.getAttribute('data-embed');
    iframe.title = button.getAttribute('data-title') || 'Embedded dashboard';
    iframe.loading = 'lazy';
    iframe.allowFullscreen = true;
    frame.innerHTML = '';
    frame.appendChild(iframe);
  });
});
