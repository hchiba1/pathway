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
      td.textContent = binding[variable].value;
      tr.appendChild(td);
    });
    tbody.appendChild(tr);
  });
  table.appendChild(tbody);
}
