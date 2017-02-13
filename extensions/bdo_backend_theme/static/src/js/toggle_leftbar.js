odoo.define('toggle_leftbar', function(require) {
    'use strict';
    var Widget = require('web.Widget');

    var AppDrawer = Widget.extend({
        template: "webclient_bootstrap",
        init: function(parent) {
            this._super(parent);
            alert("x");
        },
    });



    return {
        'AppDrawer': AppDrawer,

    };

});