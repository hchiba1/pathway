async function fetchDatabySPARQL(name) {
  const endpointUrl = 'https://rdfportal.org/sib/sparql';
  const sparqlQuery = `
PREFIX up: <http://purl.uniprot.org/core/>

SELECT ?pathway
FROM <http://sparql.uniprot.org/pathways>
WHERE {
  ?pathway a up:Pathway ;
           rdfs:label "${name}" .
}
`;

  const response = await fetch(endpointUrl, {
    method: 'POST',
    headers: {
      'Accept': 'application/sparql-results+json',
      'Content-Type': 'application/x-www-form-urlencoded'
    },
    body: `query=${encodeURIComponent(sparqlQuery)}`
  });

  return await response.json();
}

$(function () {
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
        console.log(name);
        fetchDatabySPARQL(name).then(data => {
          renderTable(data);
        });
      }
    }
  });
});

function init() {
  $.get('./tsv/pathway.sorted', (res) => {
    candidates = res.trim().split('\n')
  });
  $('#tags').focus();
}

function escapeRegExp(string) {
  return string.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'); // $& means the whole matched string
}
