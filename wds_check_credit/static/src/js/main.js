openerp.wds_check_credit = function(instance){
    var QWeb = instance.web.qweb,
    _t = instance.web._t;
    var module = instance.point_of_sale;

    var _initialize_ = module.PosModel.prototype.initialize;
    module.PosModel.prototype.initialize = function(session, attributes){
        self = this;
        for (var i = 0 ; i < this.models.length; i++){
            if (this.models[i].model == 'res.partner'){
                this.models[i].fields.push('credit_limit');
            }
        }
        return _initialize_.call(this, session, attributes);
    }

    module.PaymentScreenWidget.include({
        validate_order: function(options, callback) {
            if(callback)
              return this._super(options);
            var self = this;
            options = options || {};

            var currentOrder = this.pos.get('selectedOrder');

            partner = false;
            if (currentOrder.get_client())
              partner = currentOrder.get_client();

            if (partner){
                var posOrderModel = new instance.web.Model('pos.order');
                posOrderModel.call('check_credit_from_ui',[partner.id, currentOrder.getTotalTaxIncluded()]).then(function(result){
                  if (typeof result != 'object'){
                      return self.validate_order(options,true);
                  }else{
                      credit = self.format_currency(result[1]);
                      credit_limit = self.format_currency(partner.credit_limit);
                      self.pos_widget.screen_selector.show_popup('error',{
                          comment: _t('The ongoing credit('+credit+') and the amount of the order exceeds the credit limit('+credit_limit+') for that customer.')
                      });
                  }
                })
            }else{
                return this._super(options);
            }
        }
    });

};
