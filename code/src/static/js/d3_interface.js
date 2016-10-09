
var link, node, svg, force, nodes, links, width=1500, height=1500;

function reset() {

    if (svg != undefined) svg[0][0].parentNode.removeChild(svg[0][0]);;

    nodes = [], links = [];

    force = d3.layout.force()
        .nodes(nodes)
        .links(links)
        .size([width,height])

        .linkDistance([500])
        .linkStrength(1)

        .charge([0])
        .friction(0)
        .gravity(0.005)
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
        .attr('class', 'node');

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
            'stroke-width':'5px',
            'stroke':function(d){switch (d.text){case -1:return 'red';case 0:return "grey"; case 1:return 'green'}},
            'id':function(d,i) {return 'edgepath'+i}
        });

    link.exit().remove();

    node = node.data(force.nodes(), function(d) {return d.id;});

    node.enter()
        .append("g")
        .append("circle")
        .attr("class", function(d) {return "node " + d.id;})
        .attr("r", 8);

    node.append("text")
        .attr("dx", 12)
        .attr("dy", ".35em")
        .text(function(d) {return d.id});

    node.exit().remove();

    force.start();
}

function tick() {

    node.attr("transform", function(d) {return 'translate(' + [d.x, d.y] + ')';});

    link.attr("x1", function(d) {return d.source.x;})
        .attr("y1", function(d) {return d.source.y;})
        .attr("x2", function(d) {return d.target.x;})
        .attr("y2", function(d) {return d.target.y;});
}
