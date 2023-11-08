$(function () { // When DOM is ready
  let candidates = [];
  $.get('./tsv/pathway.sorted', (res) => {
    candidates = res.trim().split('\n')
  });
  $('#tags').focus();
  $('#tags').autocomplete({
    source: (request, response) => {
      response(
        $.grep(candidates, (value) => {
          let regexp = new RegExp('\\b' + escapeRegExp(request.term), 'i');
          return value.match(regexp);
        })
      );
    },
    autoFocus: true,
    delay: 100,
    minLength: 2,
    select: (e, ui) => {
      if (ui.item) {
        let name = ui.item.label;
        name = name.replace(/ \(.+\)$/, '');
        fetchDatabySPARQL(name).then(data => {
          renderTable(data);
        });
      }
    }
  });
});

function escapeRegExp(string) {
  return string.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'); // $& means the whole matched string
}

function renderTable(data) {
  const table = document.getElementById('resultsTable');

  const thead = document.createElement('thead');
  const headerRow = document.createElement('tr');
  data.head.vars.forEach(variable => {
    const th = document.createElement('th');
    th.textContent = variable;
    headerRow.appendChild(th);
  });
  thead.appendChild(headerRow);
  table.appendChild(thead);

  const tbody = document.createElement('tbody');
  data.results.bindings.forEach(binding => {
    const tr = document.createElement('tr');
    data.head.vars.forEach(variable => {
      const td = document.createElement('td');
      const value = binding[variable].value;
      if (value.match(/^http/)) {
        let link = document.createElement('a');
        link.href = value;
        link.textContent = value.replace(/.*\//, '');
        td.appendChild(link);
      } else {
        td.textContent = value;
      }
      tr.appendChild(td);
    });
    tbody.appendChild(tr);
  });
  table.appendChild(tbody);
}
