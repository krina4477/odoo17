/** @odoo-module */
import { Orderline } from "@point_of_sale/app/store/models";
import { patch } from "@web/core/utils/patch";

patch(Orderline.prototype, {
    async setup() {
        super.setup(...arguments);

        this.list_of_product = []  
                
        if(this.quantityStr){
            this.addedClasses
        }
    },

    async autoOrderline(){

        var check = await this.pos.env.services.rpc("/rpc_service",data)


        const order = this.pos.get_order();
        const orderlines = order.get_orderlines();
        var order_lines_list = [];
        var data = order_lines_list;

        for(var i = 0; i < orderlines.length; i++){
            order_lines_list.push({'product_id': orderlines[i].product.id,
                                'qty': parseFloat(orderlines[i].quantity).toFixed(1) })
        }

        const ld = []

        
        for(let i = 0 ; i < orderlines.length; i++){
            ld.push(data[i])
        }


        const fetch_combo_deal = await this.pos.env.services.rpc("/rpc_service",{ld})

        const orm = this.pos.env.services.orm

        const combo_deal = orm.searchRead("product.product", [], ['is_combo_deal', 'combo_products']).then(result => {

            for(let i = 0; i < result.length; i++){

                if(fetch_combo_deal === result[i]['id']){

                    var product  = this.pos.db.get_product_by_id(result[i]['id'])
                    if(product){

                        for(var j = 0; j < order.orderlines.length; j++){
                            if(order.orderlines[j].product.is_combo_deal === false){
                            this.list_of_product.push(order.orderlines[j])
                            }
                        }

                        for(var j = 0; j < this.list_of_product.length; j++){
                            order.removeOrderline(this.list_of_product[j]);
                        }
                        
                       order.add_product(product, {quantity:1.0});
                        for(var j = 0; j < orderlines.length; j++){
                            if(orderlines[j].product.is_combo_deal === true){
                              orderlines[j].set_quantity(1.0);
                            }
                        }
                    }
                }
            }

        })
    },


    get_combo_product(){
        return this.product.combo_products
    },

    totalProductDisplay() {
        return this.product.combo_products
    },

    get_quantity_str() {
        this.autoOrderline()
        return this.quantityStr;
    },

    getDisplayData() {
        return {
            productName: this.get_full_product_name(),
            price: this.env.utils.formatCurrency(this.get_display_price()),
            qty: this.get_quantity_str(),
            unit: this.get_unit().name,
            unitPrice: this.env.utils.formatCurrency(this.get_unit_display_price()),
            oldUnitPrice: this.env.utils.formatCurrency(this.get_old_unit_display_price()),
            discount: this.get_discount_str(),
            customerNote: this.get_customer_note(),
            internalNote: this.getNote(),
            comboParent: this.comboParent?.get_full_product_name(),
            pack_lot_lines: this.get_lot_lines(),
            totalProduct: this.totalProductDisplay()
        };
    },


    get addedClasses() {
        this.autoOrderline()
    },
    
});

export class CustomOrderline extends Orderline {

static defaultProps = {
    totalProduct: String,
};

}