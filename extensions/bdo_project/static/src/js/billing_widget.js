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
        this.measure = options.measure || 'Payroll';
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
					.filter([['service_id.name','=',self.measure]])
                    .all()
                    .then(function(records) {
                        _.each(records, function (record) {
                            self.data.push({
				                partner_id: record.partner_id,
								jan : self.convert_month_name(record.jan),
								jan_paid : record.jan_paid,
								feb : self.convert_month_name(record.feb),
								feb_paid : record.feb_paid,
								mar : self.convert_month_name(record.mar),
								mar_paid : record.mar_paid,
								apr : self.convert_month_name(record.apr),
								apr_paid : record.apr_paid,
								may : self.convert_month_name(record.may),
								may_paid : record.may_paid,
								jun : self.convert_month_name(record.jun),
								jun_paid : record.jun_paid,
								jul : self.convert_month_name(record.jul),
								jul_paid : record.jul_paid,
								aug : self.convert_month_name(record.aug),
								aug_paid : record.aug_paid,
								sept : self.convert_month_name(record.sept),
								sept_paid : record.sept_paid,
								oct : self.convert_month_name(record.oct),
								oct_paid : record.oct_paid,
								nov : self.convert_month_name(record.nov),
								nov_paid : record.nov_paid,
								dec : self.convert_month_name(record.dec),
								dec_paid : record.dec_paid
				            });
				             console.log('Partner :' + self.convert_month_name(record.oct));
				         });
                    });
    },
	convert_month_name: function(month) {
		var result;
		switch(month) {
			case 1 :
				result = 'Jan';
				break;
			case 2 :
				result = 'Feb';
				break;	
			case 3 :
				result = 'Mar';
				break;			
			case 4 :
				result = 'Apr';
				break;	
			case 5 :
				result = 'May';
				break;
			case 6 :
				result = 'Jun';
				break;
			case 7 :
				result = 'Jul';
				break;
			case 8 :
				result = 'Aug';
				break;
			case 9 :
				result = 'Sept';
				break;
			case 10 :
				result = 'Oct';
				break;
			case 11 :
				result = 'Nov';
				break;
			case 12 :
				result = 'Dec';
				break;
			default : 
				result = '';
				break;
		}
		return result;	
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
        this.$el.empty();
        this.$el.append(QWeb.render('BillingView',{rows:this.data}));
    },
	set_measure: function (measure) {
        this.measure = measure;
        return this.load_data().then(this.proxy('_display'));
    },
	destroy: function () {
        nv.utils.offWindowResize(this.to_remove);
        return this._super();
    }
});
});
