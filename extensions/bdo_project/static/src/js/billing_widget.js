odoo.define('bdo_project.BillingWidget', function (require) {
"use strict";

var core = require('web.core');
var Widget = require('web.Widget');
var Model = require('web.DataModel');
var QWeb = core.qweb;
var _t = core._t;

return Widget.extend({
	className: "o_billing",
	init: function (parent, model, options) {
        this._super(parent);
        this.measure = options.measure || "";
        this.domain = options.domain || [];
        this.groupbys = options.groupbys || [];
        this.context = options.context;
        this.fields = options.fields;
        this.model = new Model(model, {group_by_no_leaf: true});
    },
    start: function () {
		return this.load_data().then(this.proxy('_display'));
    },
    load_data:function () {
        var self = this;
        self.data = [];
        return this.model
                    .query()
                    .all()
                    .then(function(records) {
                        _.each(records, function (record) {
                            self.data.push({
				                partner_id: record.partner_id
				            });
				             console.log('Partner :' + record.partner_id);
				         });
                    });
    },
    update_data: function (domain, groupbys) {
        this.domain = domain;
        this.groupbys = groupbys;
        return this.load_data().then(this.proxy('_display'));
    },
    _display:function () {
        if (this.to_remove) {
            nv.utils.offWindowResize(this.to_remove);
        }

        this.$el.empty();
        if (!this.data.length) {
            this.$el.append(QWeb.render('BillingView.error', {
                title: _t("No data to display"),
                description: _t("No data available for this chart. " +
                    "Try to add some records, or make sure that " +
                    "there is no active filter in the search bar."),
            }));
        } else {
            var disp = this['display_billing']();
            if (disp) {
                disp.tooltip.chartContainer(this.$el[0]);
            }
        }
    },
    display_billing: function () {
        //var self = this;
        //var data = self.data;
        this.$el.empty();
        this.$el.append(QWeb.render('BillingView',{rows:this.data}));
    },
	destroy: function () {
        nv.utils.offWindowResize(this.to_remove);
        return this._super();
    }
});
});
