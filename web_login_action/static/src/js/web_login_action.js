openerp.web_login_action = function(instance) {

	var QWeb = instance.web.qweb,
	    _t = instance.web._t,
	    _lt = instance.web._lt;
	
	instance.web.WebClient.include({
		bind_hashchange: function() {
		    var self = this;
		    var res = 0;
		    $(window).bind('hashchange', this.on_hashchange);
		
		    var state = $.bbq.getState(true);
		    if (_.isEmpty(state) || state.action == "login") {
		        self.menu.is_bound.done(function() {
		            new instance.web.Model("res.users").call("read", [self.session.uid, ["action_id","action_id_init"]]).done(function(data) {
		                if(data.action_id_init) {
		                    self.action_manager.do_action(data.action_id_init[0]);
		                    self.menu.open_action(data.action_id_init[0]);
		                    res = new instance.web.Model('res.users').call('clear_init_action', [self.session.uid]);
		                } else {
			                if(data.action_id) {
			                    self.action_manager.do_action(data.action_id[0]);
			                    self.menu.open_action(data.action_id[0]);
			                } else {
			                    var first_menu_id = self.menu.$el.find("a:first").data("menu");
			                    if(first_menu_id) {
			                        self.menu.menu_click(first_menu_id);
			                    }                    
			                }
		                }
		            });
		        });
		    } else {
		        $(window).trigger('hashchange');
		    }
		}
	});
	
};