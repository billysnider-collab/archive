/* Shared Archive chrome — injects a consistent "back to index" button
   on every entry page. Does nothing on the index itself. */
(function () {
  var p = location.pathname;
  var isIndex = /(^|\/)index\.html?$/.test(p) || /\/archive\/?$/.test(p);
  if (isIndex) return;

  function add() {
    if (document.getElementById('archive-back') || !document.body) return;
    var a = document.createElement('a');
    a.id = 'archive-back';
    a.href = 'index.html';
    a.textContent = '\u2190 Archive';
    a.setAttribute('aria-label', 'Back to Archive index');
    document.body.appendChild(a);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', add);
  } else {
    add();
  }
})();
