odoo.define('web_highcharts_pie.PieChartWidget', function (require) {
"use strict";

var Widget = require('web.Widget');
var Model = require('web.DataModel');

return Widget.extend({
    className: "o_graph_svg_container",
    init: function (parent, model, options) {
        this._super(parent);
        this.context = options.context;
        this.fields = options.fields;
        this.model = new Model(model, {group_by_no_leaf: true});
        this.domain = options.domain || [];
        this.groupbys = options.groupbys || [];
        this.mode = options.mode || "pie";
        this.measure = options.measure || "__count__";
    },
    start: function () {
        return this.load_data().then(this.proxy('display_graph'));
    },
    update_data: function (domain, groupbys) {
        this.domain = domain;
        this.groupbys = groupbys;
        return this.load_data().then(this.proxy('display_graph'));
    },
    load_data: function () {
        var fields = this.groupbys.slice(0);
        fields = fields.concat(this.measure.slice(0));
        console.log("Fields Slice : " + fields);

        return this.model
                    .query(fields)
                    .filter(this.domain)
                    .context(this.context)
                    .lazy(false)
                    .group_by(this.groupbys.slice(0,2))
                    .then(this.proxy('prepare_data'));
    },
    prepare_data: function () {
        var raw_data = arguments[0],
            is_count = this.measure === '__count__';
        var data_pt, j, values, value;
        this.data = [];
        var measure;
        var x,y;

        for (var i = 0; i < raw_data.length; i++) {
            data_pt = raw_data[i].attributes;
            for(var j = 0; j < this.measure.slice(0).length; j++) {
				x = j + 0;
				y = j + 1;
                measure = this.measure.slice(x ,y);
                this.data.push({
                    name: this.fields[measure].string,
                    y: data_pt.aggregates[measure],
                });
            }
        }

    },
    display_graph: function () {
        this.$el.empty();
        var chart = this['display_' + this.mode]();
        if(chart){
            chart.tooltip.chartContainer(this.$el[0]);
        }
    },
    display_pie: function () {
        var chart = new Highcharts.Chart({
            chart: {
                renderTo: $('.o_graph_svg_container')[0],
                type: 'pie',
                options3d: {
                        enabled: true,
                        alpha: 45,
                        beta: 0
                }
            },
            title: {
                text: '2017'
            },
            plotOptions: {
                allowPointSelect: true,
	            cursor: 'pointer',
	            depth: 35,
                pie: {
                    dataLabels: {
                        enabled: true,
                        format: '<b>{point.name}</b>: {point.percentage:.1f} %',
                    },
                    //size: '75%'
                }
            },

		    series: [{
		        name: 'Brands',
		        colorByPoint: true,
		        data: this.data,
		    }],

        });
    },
    destroy: function () {
        nv.utils.offWindowResize(this.to_remove);
        return this._super();
    }

});

});

