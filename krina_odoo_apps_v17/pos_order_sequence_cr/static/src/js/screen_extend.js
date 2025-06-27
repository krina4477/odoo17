/** @odoo-module */

import { jsonrpc } from "@web/core/network/rpc_service";
import { Order } from "@point_of_sale/app/store/models";
import { patch } from "@web/core/utils/patch";
import { ReceiptScreen } from "@point_of_sale/app/screens/receipt_screen/receipt_screen";

patch(ReceiptScreen.prototype, {
    setup() {
        super.setup(...arguments);
        this.get_sale_sequence_number()
    },

    async get_sale_sequence_number(){
       const seq = await jsonrpc('/new_seq',{
                kwargs: {'old_name':this.currentOrder.name},
    }).then((res) => {
                this.currentOrder.name = res
         })
   }
})
