odoo.define('bdo_project.BillingWidget', function (require) {
"use strict";
var Widget = require('web.Widget');
var Model = require('web.DataModel');

return Widget.extend({
	init: function (parent, model, options) {
        this._super(parent);
    },
	destroy: function () {
        nv.utils.offWindowResize(this.to_remove);
        return this._super();
    }
});
});
