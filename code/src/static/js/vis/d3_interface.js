/*
* Visualization
*
* This is where we define our visualization(s).
*
* todo decide on things to visualize
* */



var d3Network = {

    link:[],
    node:[],
    svg:null,
    force:null,

    reset: function() {

        if (this.svg != undefined) this.svg[0][0].parentNode.removeChild(this.svg[0][0]);

        g.nodes = [], g.links = [];

        this.force = d3.layout.force()
            .nodes(g.nodes)
            .links(g.links)
            .size([c.width,c.height])
            .linkStrength(c.linkStrength)
            .linkDistance(c.linkDistance)
            .charge(c.charge)
            .friction(c.friction)
            .gravity(c.gravity)
            .on('tick',this.tick);

        this.svg = d3.select("body").append("svg")
            .attr("width", c.width)
            .attr("height", c.height);

        this.node = this.svg.selectAll('.node')
            .data(g.nodes)
            .enter()
            .append('g')
            .attr('class', 'node')
            .attr('stroke',function(d){return d.stroke})
            .attr('fill',function(d){return d.stroke});

        this.link = this.svg.selectAll("line")
            .data(g.links)
            .enter()
            .append("line")
            .attr("id", function(d, i) {return 'edge' + i})
            .style("stroke","#ccc")

    },

    start : function() {

        this.link = this.link.data(this.force.links(), function(d) {return d.source.id + "-" + d.target.id;});

        this.link.enter().insert("line", ".node")
            .attr("class", "link")

            .attr({
                'd': function(d) {return 'M '+d.source.x+' '+d.source.y+' L '+ d.target.x +' '+d.target.y},
                'class':'link',
                'stroke-width':'1px',
                'stroke':function(d){switch (d.text){case -1:return 'red';case 0:return "grey"; case 1:return 'green'}},
                'id':function(d,i) {return 'edgepath'+i}
            });

        this.link.exit().remove();

        this.node = this.node.data(this.force.nodes(), function(d) {return d.id;});

        this.node.enter()
            .append("g")
            .on("click",click_node)
            .on("mouseover", mouseover_node)
            .on("mouseout", mouseout_node)
            .append("circle")
            .attr("r", 2)
            .attr('stroke',function(d){return d.stroke})
            .attr('fill',function(d){return d.stroke});

        this.node.exit().remove();

        this.force.start();
    },

    tick: function () {

        d3Network.node.attr("transform", function(d) {return 'translate(' + [d.x,d.y] + ')';});

        d3Network.link.attr("x1", function(d) {return d.source.x;})
            .attr("y1", function(d) {return d.source.y;})
            .attr("x2", function(d) {return d.target.x;})
            .attr("y2", function(d) {return d.target.y;});
    }
};

