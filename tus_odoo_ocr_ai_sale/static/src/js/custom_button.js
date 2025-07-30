/** @odoo-module */
import { ListController } from "@web/views/list/list_controller";
import { registry } from '@web/core/registry';
import { listView } from '@web/views/list/list_view';
import { useService } from "@web/core/utils/hooks";
import { FileUploadListController } from "@account/views/file_upload_list/file_upload_list_controller";
import { patch } from "@web/core/utils/patch";


patch(FileUploadListController.prototype, {
      setup() {
       super.setup();
       this.orm = useService('orm');
       this.actionService = useService('action');
       this.notification = useService('notification');
   },

   async onClickOCRSale() {
       const active_model = this.props.resModel;

       try {
           const result = await this.orm.call(
               'sale.order',
               'check_active_boolean_sale',
               [active_model]
           );

           if (result.active) {
               await this.actionService.doAction({
                  type: 'ir.actions.act_window',
                  res_model: 'import.via.ocr',
                  name: 'Import From OCR',
                  view_mode: 'form',
                  views: [[false, 'form']],
                  target: 'new',
                  context: {
                      'active_model': active_model,
                      'record_id': result.record_id,
                  },
               });
           } else {
               this.notification.add(('We are unable to find any configuration for ' + active_model), {
                   type: 'danger',
               });
           }
       } catch (error) {
           console.error('Error during RPC call:', error);
           this.notification.add('Error during RPC call: ' + error.message, {
               type: 'danger',
           });
       }
   }

});
export class SaleListController extends ListController {
   setup() {
       super.setup();
       this.orm = useService('orm');
       this.actionService = useService('action');
       this.notification = useService('notification');
   }

   async onClickOCRSale() {
       const active_model = this.props.resModel;

       try {
           const result = await this.orm.call(
               'sale.order',
               'check_active_boolean_sale',
               [active_model]
           );

           if (result.active) {
               await this.actionService.doAction({
                  type: 'ir.actions.act_window',
                  res_model: 'import.via.ocr',
                  name: 'Import From OCR',
                  view_mode: 'form',
                  views: [[false, 'form']],
                  target: 'new',
                  context: {
                      'active_model': active_model,
                      'record_id': result.record_id,
                  },
               });
           } else {
               this.notification.add(('We are unable to find any configuration for ' + active_model), {
                   type: 'danger',
               });
           }
       } catch (error) {
           console.error('Error during RPC call:', error);
           this.notification.add('Error during RPC call: ' + error.message, {
               type: 'danger',
           });
       }
   }
}

registry.category("views").add("ocr_button_sale", {
   ...listView,
   Controller: SaleListController,
   buttonTemplate: "button_sale.ListView.Buttons",
});
