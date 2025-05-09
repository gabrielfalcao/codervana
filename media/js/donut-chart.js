$(function(){
    var overall = { label: 'Overwall', values: [30, 10, 6, 30, 14, 10] },
    modules = { label: 'Modules',   values: [24,  7, 2, 18, 13, 36] },
    classes = { label: 'Classes',   values: [12,  4, 2, 10, 11, 61] },
    callables = { label: 'Functions',     values:  [12,  4, 2, 10, 21, 51]  },

    data = overall;

    var labels = ['A', 'B', 'C', 'D', 'E', 'F'];

    var COLORS = ['#8D50C5', '#C550B1', '#5089C5', '#66CC68', '#FF782D', '#FF1443'];

    var w = 270,                       // width and height, natch
    h = 270,
    r = Math.min(w, h) / 2,        // arc radius
    dur = 750,                     // duration, in milliseconds
    color = d3.scale.category10(),
    donut = d3.layout.pie().sort(null),
    arc = d3.svg.arc().innerRadius(r - 70).outerRadius(r - 20);

    // ---------------------------------------------------------------------
    var svg = d3.select(".svg-container").append("svg:svg")
        .attr("width", w).attr("height", h);

    var arc_grp = svg.append("svg:g")
        .attr("class", "arcGrp")
        .attr("transform", "translate(" + (w / 2) + "," + (h / 2) + ")");

    var label_group = svg.append("svg:g")
        .attr("class", "lblGroup")
        .attr("transform", "translate(" + (w / 2) + "," + (h / 2) + ")");

    // GROUP FOR CENTER TEXT
    var center_group = svg.append("svg:g")
        .attr("class", "ctrGroup")
        .attr("transform", "translate(" + (w / 2) + "," + (h / 2) + ")");

    // CENTER LABEL
    var pieLabel = center_group.append("svg:text")
        .attr("dy", ".35em").attr("class", "chartLabel")
        .attr("text-anchor", "middle")
        .text(data.label);

    // DRAW ARC PATHS
    var arcs = arc_grp.selectAll("path")
        .data(donut(data.values));
    arcs.enter().append("svg:path")
        .attr("stroke", "white")
        .attr("stroke-width", 0.5)
        .attr("fill", function(d, i) {return COLORS[i];})
        .attr("d", arc)
        .each(function(d) {this._current = d});

    // DRAW SLICE LABELS
    var sliceLabel = label_group.selectAll("text")
        .data(donut(data.values));
    sliceLabel.enter().append("svg:text")
        .attr("class", "arcLabel")
        .attr("transform", function(d) {return "translate(" + arc.centroid(d) + ")"; })
        .attr("text-anchor", "middle")
        .text(function(d, i) {return labels[i]; });

    // --------- "PAY NO ATTENTION TO THE MAN BEHIND THE CURTAIN" ---------

    // Store the currently-displayed angles in this._current.
    // Then, interpolate from this._current to the new angles.
    function arcTween(a) {
        var i = d3.interpolate(this._current, a);
        this._current = i(0);
        return function(t) {
            return arc(i(t));
        };
    }

    // update chart
    function updateChart(model) {
        data = eval(model); // which model?

        arcs.data(donut(data.values)); // recompute angles, rebind data
        arcs.transition().ease("elastic").duration(dur).attrTween("d", arcTween);

        sliceLabel.data(donut(data.values));
        sliceLabel.transition().ease("elastic").duration(dur)
            .attr("transform", function(d) {return "translate(" + arc.centroid(d) + ")"; })
            .style("fill-opacity", function(d) {return d.value==0 ? 1e-6 : 1;});

        pieLabel.text(data.label);
    }

    // click handler
    $(".donut-graph .labels a").click(function(e) {
        updateChart(this.href.slice(this.href.indexOf('#') + 1));
        return e.preventDefault();
    });
});