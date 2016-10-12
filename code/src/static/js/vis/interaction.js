
function click_node(d){
    if (d.type!='person'&&d.type!='bill') {
        console.log('weird node',d);
        return false;
    }
    var uri_parts = d.uri.split('/'),
        govtrack_link = 'https://www.govtrack.us/api/v2/' + d.type + '/' + uri_parts[uri_parts.length-1];
    window.open(govtrack_link,'_blank');
}

function mouseover_node(d) {
    d3.select(this).append('text').classed('info', true).attr('x', 20).attr('y', 10).text(d.id);

}

function mouseout_node(d) {
    d3.select(this).select('text.info').remove();
}