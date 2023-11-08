async function fetchDatabySPARQL(name) {
  const endpointUrl = 'https://sparql.uniprot.org';
  const sparqlQuery = `
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX up: <http://purl.uniprot.org/core/>

SELECT DISTINCT ?uniprot ?mnemonic ?protein_label ?taxid ?organism_name
WHERE {
  ?pathway a up:Pathway ;
           rdfs:label "${name}" .
  ?uniprot a up:Protein ;
           up:mnemonic ?mnemonic ;
           rdfs:label ?protein_label ;
           up:organism ?taxid ;
           up:annotation [
             a up:Pathway_Annotation ;
             rdfs:seeAlso ?pathway
           ] .
  ?taxid up:scientificName ?organism_name .
}
ORDER BY ?cientificName ?mnemonic
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
