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

      // Run a function after 5 seconds
      setTimeout(() => {
        this._postClearActions();
      }, 5000);


  },
  _postClearActions() {
    // Your code here for actions to perform after 5 seconds
    // clear cart and redirect to shop
     rpc("/shop/cart/clear");
     window.location = "/shop"
  },

});

