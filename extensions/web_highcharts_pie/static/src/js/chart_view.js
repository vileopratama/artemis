odoo.define('web_highcharts_pie.PieChartView', function (require) {
"use strict";

var core = require('web.core');
var data_manager = require('web.data_manager');
var PieChartWidget = require('web_highcharts_pie.PieChartWidget');
var View = require('web.View');
var _lt = core._lt;
var _t = core._t;

var PieChartView = View.extend({
    //template: "ChartPieView",
    className: 'o_chart_pie',
    display_name: _lt('ChartPie'),
    view_type: "chart-pie",
    icon: 'fa-pie-chart',
    //require_fields: true,
    init: function () {
        this._super.apply(this, arguments);

         this.measures = [];
         this.widget = undefined;
    },
    willStart: function () {
        var self = this;
        var fields_def = data_manager.load_fields(this.dataset).then(this.prepare_fields.bind(this));
        return $.when(this._super(), fields_def);
    },
    render_buttons: function ($node) {

    },
    do_show: function () {
        this.do_push_state({});
        return this._super();
    },
    prepare_fields: function (fields) {
        var self = this;
        this.fields = fields;
        _.each(fields, function (field, name) {
            console.log('name =' + name);
            console.log('field = ' + field);
             if ((name !== 'id') && (field.store === true)) {
                if (field.type === 'integer' || field.type === 'float' || field.type === 'monetary') {
                    self.measures[name] = field;
                }
             }
        });
        this.measures.__count__ = {string: _t("Count"), type: "integer"};
    },
    do_search: function (domain, context, group_by) {
        if (!this.widget) {
            this.widget = new PieChartWidget(this, this.model, {

            });
            this.widget.appendTo(this.$el);
        }
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