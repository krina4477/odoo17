/** @odoo-module */
import { Orderline } from "@point_of_sale/app/store/models";
import { patch } from "@web/core/utils/patch";


patch(Orderline.prototype, {
    async setup() {
        super.setup(...arguments);
        this.combo_deals_id = [];
    },


    set_order_suggestion(combo_deals_id){
        this.suggestion = combo_deals_id
        },
        export_as_JSON() {
        const json = super.export_as_JSON(...arguments)
        json.combo_deals_id = this.combo_deals_id ;
        return json;
        },

        init_from_JSON(json) {
        super.init_from_JSON(...arguments);
         this.combo_deals_id = json.combo_deals_id;
         },


         can_be_merged_with(orderline) {
      
            const order = this.pos.get_order();
            const orderlines = order.orderlines;
            for(let j = 0; j < orderlines.length; j++){
                if(orderlines[j].product.is_combo_deal === true){
                    this.combo_deals_id.push(orderlines[j].product.id)
                    }
            }
                return super.can_be_merged_with(...arguments);
            }

})