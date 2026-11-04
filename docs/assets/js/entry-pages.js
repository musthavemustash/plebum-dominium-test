/* Local glossary filtering; definitions remain readable without JavaScript. */
(function () {
  'use strict';
  var filter = document.getElementById('term-filter');
  if (filter) {
    document.querySelector('.glossary-search').hidden = false;
    var terms = Array.from(document.querySelectorAll('.entry-glossary .term'));
    filter.addEventListener('input', function () {
      var query = filter.value.toLocaleLowerCase().trim(), shown = 0;
      terms.forEach(function (term) {
        term.hidden = term.textContent.toLocaleLowerCase().indexOf(query) < 0;
        if (!term.hidden) shown++;
      });
      document.getElementById('term-count').textContent = shown ? shown + ' of ' + terms.length + ' terms shown.' : 'No matching terms. Try a shorter word or clear the search.';
    });
  }
})();
