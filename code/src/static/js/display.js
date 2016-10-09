
function escapeHtml(unsafe) {

    if (isNaN(unsafe))
        return unsafe
            .replace(/&/g, "&amp;")
            .replace(/</g, "&lt;")
            .replace(/>/g, "&gt;")
            .replace(/"/g, "&quot;")
            .replace(/'/g, "&#039;");
    else return unsafe;
}

function ce(key){
    return document.createElement(key);
}

function lol(string){
    var arr = string.substring(0,string.length-2).split(' '), result = arr.splice(0,2);
    result.push(arr.join(' '));
    return result;
}

function parse_triples(server_response){
    var d = $('<div/>').html(server_response).text().split('\n');
    var triples = [];
    for (var i in d){
        if (d[i].length>1) {
            triples.push(lol(d[i]));
        }
    }

    var votes = {};

    for (var i=0;i<triples.length;i++){
        if (triples[i][0][0]=='_'){

            // this is an object with a voter, vote, and stance connected to it.
            // we shorten the data by saying {voter stance bill}
            // instead of {obj hasvoter voter, obj hasbill bill, obj hasstance stance}

            // we use the bnode id as an index
            var index = triples[i][0];

            if (votes[index]==null) votes[index] = [null,null,null];

            if (triples[i][1]=='<http://www.'+WEBSITE+'/'+DB_NAME+'/stance>'){
                votes[index][1] = parseInt(triples[i][2]);
            }

            else if (triples[i][1]=='<http://www.'+WEBSITE+'/'+DB_NAME+'/voter>'){
                var parts = triples[i][2].split('/');
                votes[index][0] = 'a' + parts[parts.length-1].split('>')[0];
            }

            else if (triples[i][1]=='<http://www.'+WEBSITE+'/'+DB_NAME+'/bill>') {
                var parts = triples[i][2].split('=');
                votes[index][2] = 'b'+parts[parts.length-1].split('>')[0];
            }
        }
    }
    return votes;
}

function display_list(table_id, triples){
    for (var r in triples){
        var tr = ce('tr');
        for (var c in triples[r]){
            var td = ce('td');
            td.className = 'col-sm-4';
            td.innerHTML = escapeHtml(triples[r][c]);
            tr.appendChild(td);
        }
        document.getElementById(table_id).appendChild(tr);
    }
}


function findOrMake(id,type){
    // if a node with this id exists, return it
    // if it doesn't, indicate a new node
    for (var i in nodes) if (nodes[i].id==id) return nodes[i];
    return {id:id,type:type};
}

function add_predicate(predicate){
    var subject = findOrMake(predicate[0],'person'), object = findOrMake(predicate[2],'bill');
    nodes.push(subject,object);
    links.push({source:subject,target:object,text:predicate[1]})
}

function display_network(triples){
    reset();
    for (var t in triples) add_predicate(triples[t]);
    start()
}











