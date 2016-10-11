
var nodes, links;

function escapeHtml(unsafe) {return (!isNaN(unsafe))? unsafe: unsafe.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;").replace(/'/g, "&#039;");}

function ce(key){return document.createElement(key);}

function display_list(table_id, triples){
    document.getElementById(table_id).style.display='inline-block'
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

function getNode(uri){
    for (var i in nodes) {
        if (nodes[i].uri==uri) {
            return nodes[i];
        }
    }
    return false;
}

String.prototype.replaceAll = function(search, replacement) {
    var target = this;
    return target.replace(new RegExp(search, 'g'), replacement);
};

var id = 0;

function makeNode(uri,type){

    var stroke;
    switch (type){
        /* visualization properties for different elements go here */
        case 'person': stroke='blue';break;
        case 'bill': stroke='red';break;
        default:break;
    }

    var n = {id:id++,uri:uri,type:type,stroke:stroke};
    nodes.push(n);

    return n;
}

function getOrMake(uri,type){
    // if a node with this uri exists, return it.

    var n = getNode(uri);
    if (n == false) {

        return makeNode(uri,type);
    }
    else return n;
}

function addToVisualization(triple){

    var subject = getOrMake(triple[0],'person'), object = getOrMake(triple[2],'bill');
    links.push(
        {
            source:subject,
            target:object,
            text:triple[1]
        }
    )
}

function display_network(triples){

    // (re)set visualizer state
    reset();

    // add each triple to the visualization
    for (var t in triples) addToVisualization(triples[t]);

    // initiate visualization
    start()
}












