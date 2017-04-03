odoo.define('bdo_project.BillingView', function (require) {
"use strict";
var View = require('web.View');
var core = require('web.core');
var Model = require('web.DataModel');
var Widget = require('bdo_project.BillingWidget');
var QWeb = core.qweb;
var _lt = core._lt;

var BillingView = View.extend({
	template: "BillingView",
	display_name: _lt('Billing'),
	view_type: "billing",
	icon: 'fa-list',
	init: function () {
		this._super.apply(this, arguments);
		this.service = [];
		this.load_service();
	},
	willStart: function () {
		var fields_def = 'id,name';
		return $.when(this._super(), fields_def);
	},
	render_buttons: function ($node) {
		self = this;
		var measures=[];
		console.log('measures length :' + self.service.length);
		if ($node) {
			//this.node = [];
			console.log('a node: ' + $node);
			var service = new Model('bdo.project.service');
			service.query().all().then(function (records)  {
				//var measures = [];
				_.each(records, function (record) {
                    console.log('service :' + record.name);
                    measures.push({id:record.id,name:record.name});
                });
				//console.log('button node: ' + $node);
			});

			console.log('button node: ' + measures.length);
			this.$buttons = $(QWeb.render('BillingView.buttons', {measures:measures}));
			this.$buttons.appendTo($node);

			//var measures = self.service;
			//var context = {measures:measures};
			//this.$buttons = $(QWeb.render('BillingView.buttons', context));
			//this.$measure_list = this.$buttons.find('.o_graph_measures_list');
			//this.update_measure();
            //this.$buttons.find('button').tooltip();
            //this.$buttons.click(this.on_button_click.bind(this));
            //this.$buttons.find('.o_graph_button[data-mode="' + this.widget.mode + '"]').addClass('active');
			//this.$buttons.appendTo($node);
		}
	},
	prepare_data:function ($node){
		this.$buttons = $(QWeb.render('BillingView.buttons', {measures:measures}));
		this.$buttons.appendTo($node);
	},
	do_show: function () {
        this.do_push_state({});
        return this._super();
    },
    do_search: function (domain, context, group_by) {
        console.log('servicex : ' + this.service.length);
		var contents = this.$el[0].querySelector('.line');
		contents.innerHTML = "";

		//QWeb.render('line',{widget:this, line:this.service});
    },
    destroy: function () {
        return this._super.apply(this, arguments);
    },
    load_service: function () {
        var self = this;
        var measures = [];
        var success;
        var def  = new $.Deferred();
        var fields = ['name'];
        var service = new Model('bdo.project.service');
		self.service.push({id:1,name:'Service'});

		this.alive(service.query().all()).then(function (records) {
            // would break if executed after the widget is destroyed, wrapping
            // rpc in alive() prevents execution
            _.each(records, function (record) {
                console.log('service :' + record.name);
                self.service.push({id:record.id,name:record.name});
                //self.$el.append(self.format(record));
            });
		});

		/*var service = new Model('bdo.project.service').query(fields).all();
		service.then(function(services) {
			var service;
			for(var i = 0, len = services.length; i < len; i++) {
				service = services[i];
				self.service.push({id:service.id,name:service.name});
				console.log('service :' + service.name);
			}
		});*/
		//console.log('success total log : ' + service.length);

		//var models = new Model();

		/*new Model('bdo.project.service')
                    .query(fields)
                    //.filter(this.domain)
                    //.context(this.context)
                    //.lazy(false)
                    //.group_by(this.groupbys.slice(0,2))
                    .all({'timeout':3000, 'shadow': true})
                    .then(function(services) {
                        //self.prepare_service(services);
	                    var service;
						//var measures = [];
						for(var i = 0, len = services.length; i < len; i++) {
						    service = services[i];
						    console.log('service :' + service.name);
						    success = self.service.push({id:service.id,name:service.name});
						    if(success) { console.log('success log : ' + self.service.length);}
						    def.resolve();
						}
                     },function(err,event){ event.preventDefault(); def.reject(); }
                    );
		*/
        //console.log('success total log' + self.service.length);
        //return def;
    },
});

core.view_registry.add('billing', BillingView);
return BillingView;
});