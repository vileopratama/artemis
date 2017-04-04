odoo.define('bdo_project.BillingWidget', function (require) {
"use strict";
var Widget = require('web.Widget');
var Model = require('web.DataModel');

return Widget.extend({
	className: "o_billing",
	init: function (parent, model, options) {
        this._super(parent);
        this.measure = options.measure || "";
        this.domain = options.domain || [];
        this.groupbys = options.groupbys || [];
        this.context = options.context;
        this.fields = options.fields;
    },
    start: function () {
		return this.load_data().then(this.proxy('_display'));
    },
    load_data:function () {
        return this.model
                    .filter(this.domain)
                    .context(this.context)
                    .lazy(false)
                    .group_by(this.groupbys.slice(0,2))
                    .then(this.proxy('prepare_data'));
    },
    prepare_data: function () {
        var raw_data = arguments[0],data_pt,partner_id;
        for (var i = 0; i < raw_data.length; i++) {
            data_pt = raw_data[i].attributes;
            partner_id = data_pt.aggregates['partner_id'];
            this.data.push({
                partner_id: partner_id,
            });
        }
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
		var data = this.data;
		var contents = this.$el[0].querySelector('.line');
		contents.innerHTML = "";
		for(var i = 0, len = Math.min(data.length,1000); i < len; i++) {
			var row = data[i];
			var line_html = QWeb.render('Line',{widget: this, row:row});
			var line = document.createElement('tbody');
			line.innerHTML = line_html;
			line = line.childNodes[1];
			contents.appendChild(line);
		}

    },
	destroy: function () {
        nv.utils.offWindowResize(this.to_remove);
        return this._super();
    }
});
});
