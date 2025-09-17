odoo.define('whatsapp_shopping_bot.cart', function (require) {
    'use strict';

    var publicWidget = require('web.public.widget');
    var core = require('web.core');

    publicWidget.registry.WhatsappCart = publicWidget.Widget.extend({
        selector: '.a-clickpublic',
        events: {
            'click': '_onClickWhatsappPurchase',
        },
        _onClickWhatsappPurchase: function (ev) {
            ev.preventDefault();
            var saleOrderId = this.$el.data('sale_order_id');
            this.$('#AddressModal').modal('show');
            this.$('#AddressModal form input[name="sale_order_id"]').val(saleOrderId);
        },
    });

    return publicWidget.registry.WhatsappCart;
});