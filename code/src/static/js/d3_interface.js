/*
* Visualization
*
* This is where we define our visualization(s).
*
* todo decide on things to visualize
* */


var link,
    node,
    svg,
    force,
    width=2500,
    height=2500;

function reset() {

    if (svg != undefined) svg[0][0].parentNode.removeChild(svg[0][0]);;

    nodes = [], links = [];

    force = d3.layout.force()
        .nodes(nodes)
        .links(links)
        .size([width,height])
        .linkStrength(0)
        .linkDistance(50)
        .charge(-1)
        .friction(0.1)
        .gravity(0)
        .on('tick',tick);

    svg = d3.select("body").append("svg")
        .attr("width", width)
        .attr("height", height);

    svg.append('defs').append('marker')
        .attr({
            'id': 'arrowhead',
            'viewBox': '-0 -5 10 10',
            'refX': 25,
            'refY': 0,
            //'markerUnits':'strokeWidth',
            'orient': 'auto',
            'markerWidth': 10,
            'markerHeight': 10,
            'xoverflow': 'visible'
        })
        .append('svg:path')
        .attr('d', 'M 0,-5 L 10 ,0 L 0,5')
        .attr('fill', '#ccc')
        .attr('stroke', '#ccc');


    node = svg.selectAll('.node')
        .data(nodes)
        .enter()
        .append('g')
        .attr('class', 'node')
        .attr('stroke',function(d){return d.stroke})
        .attr('fill',function(d){return d.stroke});

    link = svg.selectAll("line")
        .data(links)
        .enter()
        .append("line")
        .attr("id", function(d, i) {return 'edge' + i})
        .style("stroke","#ccc")

}

function start() {

    link = link.data(force.links(), function(d) {return d.source.id + "-" + d.target.id;});

    link.enter().insert("line", ".node")
        .attr("class", "link")

        .attr({
            'd': function(d) {return 'M '+d.source.x+' '+d.source.y+' L '+ d.target.x +' '+d.target.y},
            'class':'link',
            'stroke-width':'1px',
            'stroke':function(d){switch (d.text){case -1:return 'red';case 0:return "grey"; case 1:return 'green'}},
            'id':function(d,i) {return 'edgepath'+i}
        });

    link.exit().remove();

    node = node.data(force.nodes(), function(d) {return d.id;});

    node.enter()
        .append("g")
        .on("click",function(d){
            var l;
            var type_key = d.type

            switch (d.type){
                case 'person':
                    l = 'https://www.govtrack.us/api/v2/person/' + d.uri.split('/')[d.uri.split('/').length-1];
                    break;
                case 'bill':
                    l = 'https://www.govtrack.us/api/v2/bill/' + d.uri.split('/')[d.uri.split('/').length-1];
                    break;
            }
            window.open(l,'_blank');
        })
        .on("mouseover", function(d) {
            var g = d3.select(this);
            var info = g.append('text')
                .classed('info', true)
                .attr('x', 20)
                .attr('y', 10)
                .text(d.id);
        })
        .on("mouseout", function() {
            // Remove the info text on mouse out.
            d3.select(this).select('text.info').remove();
        })
        .append("circle")
        .attr("class", function(d) {return "node " + d.id;})
        .attr("r", 2)
        .attr('stroke',function(d){return d.stroke})
        .attr('fill',function(d){return d.stroke});

    node.exit().remove();

    force.start();
}

function tick() {

    node.attr("transform", function(d) {return 'translate(' + [d.x,d.y] + ')';});

    link.attr("x1", function(d) {return d.source.x;})
        .attr("y1", function(d) {return d.source.y;})
        .attr("x2", function(d) {return d.target.x;})
        .attr("y2", function(d) {return d.target.y;});
}
