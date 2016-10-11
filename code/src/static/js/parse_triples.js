
function parse_line(line){
    line = line.replaceAll('<','').replaceAll('>','');
    while (line[line.length-1]==' '||line[line.length-1]=='.') line = line.substr(0,line.length-1);
    var arr = line.trim().split(' ');
    arr[2]=parseInt(arr[2]);
    return arr;
}

function parse_triples(server_response) {

    // todo make more efficient


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

    /*
     var voter_str = GT_NS+':person/';

     function pass_filter(line){

     // this is a patch that should be une

     if (line.length < 5) return false;

     //if (line.indexOf('Thing') != -1) return false;
     if (line.indexOf(' a ') != -1) return false;
     if (line.indexOf(voter_str)==-1) return false;

     return true;
     }

     for (var i in d) {
     if (pass_filter(d[i])) {
     var l = parse_line(d[i])
     triples.push(l);
     }
     }

     return triples;
}*/