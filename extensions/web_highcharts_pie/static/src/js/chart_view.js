odoo.define('web_highcharts_pie.PieChartView', function (require) {
"use strict";

var core = require('web.core');
var View = require('web.View');
var _lt = core._lt;

var PieChartView = View.extend({
    template: "ChartPieView",
    //className: 'o_chart_pie',
    display_name: _lt('ChartPie'),
    view_type: "chart-pie",
    icon: 'fa-pie-chart',
    //require_fields: true,
    init: function () {
        this._super.apply(this, arguments);
    },
    willStart: function () {
        var self = this;
    },
    render_buttons: function ($node) {

    },
    do_show: function () {
        this.do_push_state({});
        return this._super();
    },
    do_search: function (domain, context, group_by) {

    },
    get_context: function () {

    },
    destroy: function () {
        return this._super.apply(this, arguments);
    },
});

core.view_registry.add('chart-pie', PieChartView);
return PieChartView;
});