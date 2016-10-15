

var g = {
    next_new_id:0, // node-id used by d3
    nodes:[],
    links:[]
};

function getNode(uri){
    for (var i in g.nodes) {
        if (g.nodes[i].uri==uri) {
            return g.nodes[i];
        }
    }
    return false;
}

function makeNode(uri,type){
    var stroke;
    switch (type){
        /* visualization properties for different elements go here */
        case 'person': stroke='blue';break;
        case 'bill': stroke='red';break;
        default:break;
    }
    var n = {id:g.next_new_id++,uri:uri,type:type,stroke:stroke};
    g.nodes.push(n);
    return n;
}

function getOrMake(uri,type){
    var n = getNode(uri);
    if (n == false) return makeNode(uri,type);
    else return n;
}

function addToVisualization(triple){
    var subject = getOrMake(triple[0],'person'), object = getOrMake(triple[2],'bill');
    g.links.push({source:subject,target:object,text:triple[1]})
}

function display_network(triples){
    // (re)set visualizer state
    d3Network.reset();
    // add each triple to the visualization
    for (var t in triples) addToVisualization(triples[t]);
    // initiate visualization
    d3Network.start()
}