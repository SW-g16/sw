
function parse_triples(server_response) {

    // todo make more efficient

    console.log(server_response);

    var triples = [];
    // get in convenient format by running through jquery
    var d = $('<div/>').html(server_response.trim()).text().split(' ;\n');
    var n_persons = 0;
    var person = null, parts;
    for (var i in d) {
        parts = d[i].trim().split(' ');
        if (parts.length == 3) {
            person = parts.shift().replace("\"\n", '').replace('>','').replace('<','');
        } else if (parts.length==5){
            triples.push([person, parseInt(parts[1]), parts[0].replace('>','').replace('<','')]);
            person = parts[2].replace('>','').replace('<','');
            triples.push([person, parseInt(parts[4]), parts[3].replace('>','').replace('<','')]);
            continue;
        }
        triples.push([person, parseInt(parts.pop()), parts.pop().replace('>','').replace('<','')]);
    }
    return triples
}
