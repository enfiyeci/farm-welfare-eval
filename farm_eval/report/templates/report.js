document.querySelectorAll('[data-node-filter]').forEach(function(input) {
  input.addEventListener('input', function() {
    var query = input.value.toLowerCase();
    document.querySelectorAll('[data-node-card]').forEach(function(card) {
      card.hidden = !card.dataset.search.includes(query);
    });
  });
});
document.querySelectorAll('[data-expand]').forEach(function(button) {
  button.addEventListener('click', function() {
    var open = button.dataset.expand === 'all';
    document.querySelectorAll('[data-node-card]').forEach(function(card) { card.open = open; });
  });
});
document.querySelectorAll('th button[data-sort]').forEach(function(button) {
  button.addEventListener('click', function() {
    var table = button.closest('table'), body = table.querySelector('tbody');
    var index = Array.from(button.closest('tr').children).indexOf(button.parentElement);
    var rows = Array.from(body.rows), direction = button.dataset.direction === 'up' ? -1 : 1;
    rows.sort(function(a, b) {
      var av = a.cells[index].dataset.value || a.cells[index].textContent;
      var bv = b.cells[index].dataset.value || b.cells[index].textContent;
      var an = Number(av), bn = Number(bv);
      return ((!Number.isNaN(an) && !Number.isNaN(bn)) ? an - bn : av.localeCompare(bv)) * direction;
    });
    rows.forEach(function(row) { body.appendChild(row); });
    button.dataset.direction = direction === 1 ? 'up' : 'down';
  });
});
