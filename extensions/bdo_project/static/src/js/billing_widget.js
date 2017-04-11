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
        this.domain = this.domain.concat([['service_id.name','=',self.measure]]);
        self.data = [];
        return this.model
                    .query()
					.filter(this.domain)
                    .all()
                    .then(function(records) {
                        _.each(records, function (record) {
                            self.data.push({
				                partner_id: record.partner_id,
				                year_invoice: record.year_invoice,
								jan : self.convert_month_name(record.jan),
								jan_paid : record.jan_paid,
								jan_aging : self.convert_class_attribute(record.jan_aging),
								feb : self.convert_month_name(record.feb),
								feb_paid : record.feb_paid,
								feb_aging : self.convert_class_attribute(record.feb_aging),
								mar : self.convert_month_name(record.mar),
								mar_paid : record.mar_paid,
								mar_aging : self.convert_class_attribute(record.mar_aging),
								apr : self.convert_month_name(record.apr),
								apr_paid : record.apr_paid,
								apr_aging : self.convert_class_attribute(record.apr_aging),
								may : self.convert_month_name(record.may),
								may_paid : record.may_paid,
								may_aging : self.convert_class_attribute(record.may_aging),
								jun : self.convert_month_name(record.jun),
								jun_paid : record.jun_paid,
								jun_aging : self.convert_class_attribute(record.jun_aging),
								jul : self.convert_month_name(record.jul),
								jul_paid : record.jul_paid,
								jul_aging : self.convert_class_attribute(record.jul_aging),
								aug : self.convert_month_name(record.aug),
								aug_paid : record.aug_paid,
								aug_aging : self.convert_class_attribute(record.aug_aging),
								sept : self.convert_month_name(record.sept),
								sept_paid : record.sept_paid,
								sept_aging : self.convert_class_attribute(record.sept_aging),
								oct : self.convert_month_name(record.oct),
								oct_paid : record.oct_paid,
								oct_aging : self.convert_class_attribute(record.oct_aging),
								nov : self.convert_month_name(record.nov),
								nov_paid : record.nov_paid,
								nov_aging : self.convert_class_attribute(record.nov_aging),
								dec : self.convert_month_name(record.dec),
								dec_paid : record.dec_paid,
								dec_aging : self.convert_class_attribute(record.dec_aging)

				            });
				             //console.log('Year :' + record.year_invoice + ' partner : ' + record.partner_id);
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
	convert_class_attribute: function(aging) {
		var result;
		if(aging >= 1 && aging <= 30) {
			result = 'on_before_30';
		}else if(aging >= 31 && aging <= 60) {
			result = 'on_before_60';
		}else if(aging >= 61 && aging <= 90) {
			result = 'on_before_90';
		}else if(aging >= 91 && aging <= 120) {
			result = 'on_before_120';
		}else if(aging >= 121) {
			result = 'on_after_120';
		}  else {
			result = '';
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
