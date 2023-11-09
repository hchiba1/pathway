$(function () { // When DOM is ready
  $.get('./tsv/pathway.sorted', (res) => {
    setupAutocomplete(res.trim().split('\n'));
  });
  $('#tags').focus();

  function setupAutocomplete(candidates) {
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
          document.getElementById('resultsTable').innerHTML = 'Searching ...';
          let name = ui.item.label;
          fetchDatabySPARQL(name).then(data => {
            renderTable(data);
          }).catch(error => {
            console.error('Error fetching data:', error);
            document.getElementById('resultsTable').innerHTML = 'Error fetching data.';
          });
        }
      }
    });
  }
});

function escapeRegExp(string) {
  return string.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'); // $& means the whole matched string
}

function renderTable(data) {
  const table = document.getElementById('resultsTable');
  table.innerHTML = '';

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
