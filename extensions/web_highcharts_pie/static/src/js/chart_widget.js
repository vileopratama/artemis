odoo.define('web_highcharts_pie.PieChartWidget', function (require) {
"use strict";

var Widget = require('web.Widget');
var Model = require('web.DataModel');

return Widget.extend({
    className: "o_graph_svg_container",
    init: function (parent, model, options) {
        this._super(parent);
        this.context = options.context;
        this.model = new Model(model, {group_by_no_leaf: true});
        this.domain = options.domain || [];
        this.groupbys = options.groupbys || [];
        this.mode = options.mode || "pie";
        this.measure = options.measure || "__count__";
    },
    start: function () {
        console.log('on start');
        return this.load_data().then(this.proxy('display_graph'));
    },
    load_data: function () {
        var fields = this.groupbys.slice(0);
        if (this.measure !== '__count__'.slice(0))
            fields = fields.concat(this.measure);
        console.log("Fields Slice " + fields);
        return this.model
                    .query(fields)
                    .filter(this.domain)
                    .context(this.context)
                    .lazy(false)
                    .group_by(this.groupbys.slice(0,2))
                    .then(this.proxy('prepare_data'));

    },
    prepare_data: function () {

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
            xAxis: {
                categories: ['Target', 'Amount']
            },

            plotOptions: {
                pie: {
                    dataLabels: {
                        enabled: true,
                        format: '<b>{point.name}</b>: {point.percentage:.1f} %',
                    },
                    //size: '75%'
                }
            },

            series: [{
                name: 'Browser share Month 2017',
                data: [200000, 300000],
                title: {
                    align: 'left',
                    text: '<b>Pie 1</b><br>Subtext',
                    verticalAlign: 'top',
                    y: -40
                },
                //center: ['20%', '50%']
            }]

        });
    },
    destroy: function () {
        nv.utils.offWindowResize(this.to_remove);
        return this._super();
    }

});

});

