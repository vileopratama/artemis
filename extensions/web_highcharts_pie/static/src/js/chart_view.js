odoo.define('web_highcharts_pie.PieChartView', function (require) {
"use strict";

var core = require('web.core');
var data_manager = require('web.data_manager');
var PieChartWidget = require('web_highcharts_pie.PieChartWidget');
var View = require('web.View');
var _lt = core._lt;
var _t = core._t;
var QWeb = core.qweb;

var PieChartView = View.extend({
    className: 'o_chart_pie',
    display_name: _lt('ChartPie'),
    view_type: "chart-pie",
    icon: 'fa-pie-chart',
    require_fields: true,
    init: function () {
        this._super.apply(this, arguments);
        this.measures = [];
        this.measure = [];
        this.active_measure = [];
        this.initial_groupbys = [];
        this.widget = undefined;
    },
    willStart: function () {
        var self = this;
        var fields_def = data_manager.load_fields(this.dataset).then(this.prepare_fields.bind(this));
        this.fields_view.arch.children.forEach(function(field) {
			var name = field.attrs.name;
			if(field.attrs.interval) {
				name += ':' + field.attrs.interval;
			}
			//console.log('type :' + field.attrs.type + ' name:'+name);
			if (field.attrs.type === 'measure') {
                //self.active_measure = name;
                //self.active_measure = self.measures[name];
                self.active_measure.push(name);
            } else {
                self.initial_groupbys.push(name);
            }
        });
        return $.when(this._super(), fields_def);
    },
    render_buttons: function ($node) {
		var measure = [];
		if (this.widget) {
			//var data = this.widget.prepare_measure();
			//console.log("tahun" + data.length);
			//measure = this.widget.prepare_measure();
		}

		if ($node) {
            //var context = {measures: _.pairs(_.omit(this.measures, '__count__'))};
            var context = {measures:  _.pairs(_.omit(measure, '__count__'))};
            this.$buttons = $(QWeb.render('GraphView.buttons', context));
            //this.$measure_list = this.$buttons.find('.o_graph_measures_list');
            //this.update_measure();
            //this.$buttons.find('button').tooltip();
            //this.$buttons.click(this.on_button_click.bind(this));
            //this.$buttons.find('.o_graph_button[data-mode="' + this.widget.mode + '"]').addClass('active');
            this.$buttons.appendTo($node);
        }
    },
    do_show: function () {
        this.do_push_state({});
        return this._super();
    },
    prepare_fields: function (fields) {
        var self = this;
        this.fields = fields;
        _.each(fields, function (field, name) {
             if ((name !== 'id') && (field.store === true)) {
                if (field.type === 'integer' || field.type === 'float' || field.type === 'monetary') {
                    self.measures[name] = field;
                    console.log("self measure" + field.value);
                }
             }
        });
        this.measures.__count__ = {string: _t("Count"), type: "integer"};
    },
    do_search: function (domain, context, group_by) {
        this.initial_groupbys = context.graph_groupbys || (group_by.length ? group_by : this.initial_groupbys);
        if (!this.widget) {
            this.widget = new PieChartWidget(this, this.model, {
                groupbys: this.initial_groupbys,
                domain: domain,
                context: context,
                fields: this.fields,
                measure: context.graph_measure || this.active_measure,
            });
            this.widget.appendTo(this.$el);
        }else {
            var groupbys = group_by.length ? group_by : this.initial_groupbys.slice(0);
            this.widget.update_data(domain, groupbys);
        }
    },
    get_context: function () {
        return !this.widget ? {} : {
            graph_mode: this.widget.mode,
            graph_measure: this.widget.measure,
            graph_groupbys: this.widget.groupbys
        };
    },
    destroy: function () {
        return this._super.apply(this, arguments);
    },
});

core.view_registry.add('chart-pie', PieChartView);
return PieChartView;
});