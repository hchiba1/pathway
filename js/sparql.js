async function fetchDatabySPARQL(name) {
  const endpointUrl = 'https://sparql.uniprot.org';
  const sparqlQuery = `
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX up: <http://purl.uniprot.org/core/>

SELECT DISTINCT ?taxid ?organism_name ?uniprot ?mnemonic ?protein_label
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
ORDER BY ?organism_name ?mnemonic
`;

  try {
    const response = await fetch(endpointUrl, {
      method: 'POST',
      headers: {
        'Accept': 'application/sparql-results+json',
        'Content-Type': 'application/x-www-form-urlencoded'
      },
      body: `query=${encodeURIComponent(sparqlQuery)}`
    });
    if (!response.ok) {
      // response.ok === true if the status code is 2xx
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    return await response.json();
  } catch (error) {
    console.error(`Could not fetch data: ${error}`);
  }
}
