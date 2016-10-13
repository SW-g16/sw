

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

String.prototype.replaceAll = function(search, replacement) {
    var target = this;
    return target.replace(new RegExp(search, 'g'), replacement);
};








