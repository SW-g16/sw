
function escapeHtml(unsafe) {
    return unsafe
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#039;");
}

function ce(key){
    return document.createElement(key);
}

function lol(string){
    var arr = string.split(' '), result = arr.splice(0,2);
    result.push(arr.join(' '));
    return result;
}

function display_stuff(table_id,d){

    var triples = [];
    for (var i in d){
        if (d[i].length>1) {

            triples.push(lol(d[i]));
        }
    }
    for (var r in triples){
        var tr = ce('tr');
        for (var c in triples[r]){
            var td = ce('td');
            td.className = 'col-sm-4';
            td.innerHTML = escapeHtml(triples[r][c]);
            tr.appendChild(td);
        }
        console.log(triples[r]);
        document.getElementById(table_id).appendChild(tr);
    }
}
