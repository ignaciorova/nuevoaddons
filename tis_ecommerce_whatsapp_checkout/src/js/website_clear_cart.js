/** @odoo-module **/
import publicWidget from "@web/legacy/js/public/public_widget";
import { browser } from "@web/core/browser/browser";
import { rpc } from "@web/core/network/rpc";

publicWidget.registry.websiteSaleDelivery = publicWidget.Widget.extend({
  selector: '.oe_website_sale',

  events: {
    'click .whatsapp_checkout': '_onWhatsappCheckoutClick',
  },

  async _onWhatsappCheckoutClick() {
    setTimeout(() => {
      this._postClearActions();
    }, 5000);
  },

  _postClearActions() {
    rpc("/shop/cart/clear");
    window.location = "/shop";
  },
});