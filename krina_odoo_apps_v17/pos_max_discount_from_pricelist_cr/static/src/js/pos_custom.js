
///** @odoo-module */

import { Order, Orderline, Product} from "@point_of_sale/app/store/models";
import { ProductScreen } from "@point_of_sale/app/screens/product_screen/product_screen";
import { patch } from "@web/core/utils/patch";
const { DateTime } = luxon;
import { registry } from "@web/core/registry";
import { Component, markup, onMounted, xml } from "@odoo/owl";

patch(Orderline.prototype, {

        setup() {
            super.setup(...arguments);

            this.pricelist_id = this.pricelist_id || false;
            this.pricelist_label = this.pricelist_label || false;
            this.pricelist_discount_label = this.pricelist_discount_label || false;
       },

    //@override
     init_from_JSON(json){
            super.init_from_JSON(...arguments);
            this.pricelist_id  = json.pricelist_id;
            this.pricelist_label = json.pricelist_label;
            this.pricelist_discount_label = json.pricelist_discount_label;

     },

     //@override
     export_as_JSON(){
            const json = super.export_as_JSON(...arguments);
            if(json){
                json.pricelist_id  = this.pricelist_id;
                json.pricelist_label = this.pricelist_label;
                json.pricelist_discount_label = this.pricelist_discount_label;
                return json;
            }
     },


     getDisplayData() {
        return {
            ...super.getDisplayData(),
            productName: this.get_full_product_name(),
            price:
                this.get_discount_str() === "100"
                    ? "free"
                    : this.env.utils.formatCurrency(this.get_display_price()),
            qty: this.get_quantity_str(),
            unit: this.get_unit().name,
            unitPrice: this.env.utils.formatCurrency(this.get_unit_display_price()),
            oldUnitPrice: this.env.utils.formatCurrency(this.get_old_unit_display_price()),
            discount: this.get_discount_str(),
            customerNote: this.get_customer_note(),
            internalNote: this.getNote(),
            comboParent: this.comboParent?.get_full_product_name(),
            pack_lot_lines: this.get_lot_lines(),
            price_without_discount: this.env.utils.formatCurrency(
                this.getUnitDisplayPriceBeforeDiscount()
            ),
            attributes: this.attribute_value_ids
                ? this.findAttribute(this.attribute_value_ids)
                : [],
            pricelist_label: this.pricelist_label,
            pricelist_discount_label:this.pricelist_discount_label,
        };
    },

     get_pricelist_label(){
        return this.pricelist_label;
     },

     set_pricelist_label(name){
        this.pricelist_label = name;
     },

     get_pricelist_id(){
        return this.pricelist_id;
     },

     set_pricelist_id(id){
        this.pricelist_id = id;
     },

     get_pricelist_discount_label(){
         return this.pricelist_discount_label;
     },

     set_pricelist_discount_label(name){
        this.pricelist_discount_label = name;
     }
});

patch(Order.prototype, {
    setup() {
        super.setup(...arguments);
    },
    select_orderline(orderline) {
        super.select_orderline(...arguments);
        this.get_pricelist_label(orderline);
    },



    get_pricelist_label(lines){
        var line = lines;
          if (line){
            var quantity = line.quantity;
            var price_extra = line.price_extra;

            var self = this;
            var date = DateTime.now().startOf("day");
            var price = line.product.lst_price;
            var product_id = line.product.id

            var default_price = line.product.lst_price;
            if (price_extra){
                default_price += price_extra;
            }

            if (self.pos.config.use_pricelist){
                var pricelist_price_dict = {}
                var element=Array.from(self.pos.pricelists)
                element.forEach((pricelists) =>{

                    var items=pricelists.items
                    var pricelist_items = items.filter((item)=> {
                        return (! item.product_tmpl_id || item.product_tmpl_id[0] === line.product.product_tmpl_id) &&
                               (! item.product_id || item.product_id[0] === line.product.id) &&
                               (! item.categ_id || _.contains(category_ids, item.categ_id[0])) &&
                               (! item.date_start || moment(item.date_start).isSameOrBefore(date)) &&
                               (! item.date_end || moment(item.date_end).isSameOrAfter(date));
                    });
                    var pricelist_rule_items = {}

                   pricelist_items.find((rule) => {
                        var temp_price = default_price

                        if (rule.min_quantity && quantity < rule.min_quantity) {
                            pricelist_rule_items[rule.id] = temp_price
                            return false;
                        }
                        if (rule.base === 'pricelist') {
                            temp_price = self.get_price(rule.base_pricelist, quantity);
                            pricelist_rule_items[rule.id] = temp_price
                        } else if (rule.base === 'standard_price') {
                            temp_price = self.standard_price;
                            pricelist_rule_items[rule.id] = temp_price
                        }


                        if (rule.compute_price === 'fixed')
                        {
                            temp_price = rule.fixed_price;
                            pricelist_rule_items[rule.id] = temp_price
                            return true;
                        }
                        else if (rule.compute_price === 'percentage')
                        {
                            temp_price = temp_price - (temp_price * (rule.percent_price / 100));
                            pricelist_rule_items[rule.id] = temp_price
                            return true;
                        }
                        else
                        {
                            var price_limit = price;
                            temp_price = temp_price - (temp_price * (rule.price_discount / 100));

                            if (rule.price_round) {
                                temp_price = round_pr(temp_price, rule.price_round);
                            }
                            if (rule.price_surcharge) {
                                temp_price += rule.price_surcharge;
                            }

                            if (rule.price_min_margin) {
                                temp_price = Math.max(temp_price, price_limit + rule.price_min_margin);
                            }
                            if (rule.price_max_margin) {
                                temp_price = Math.min(temp_price, price_limit + rule.price_max_margin);
                            }

                            pricelist_rule_items[rule.id] = temp_price
                            return true;
                        }
                        pricelist_rule_items[rule.id] = temp_price
                        return false;
                   })
                    var minKey = Object.keys(pricelist_rule_items)[0]
                    pricelist_price_dict[pricelists.id] = pricelist_rule_items[minKey]

                });
//                var minpriceKey = Object.keys(pricelist_price_dict)[0]
                Object.keys(pricelist_price_dict).forEach((maxpricelist) =>{
                    var minpriceKey = maxpricelist
                    if(price == pricelist_price_dict[minpriceKey]  ) {
                        line.set_pricelist_discount_label(false);
                        line.set_pricelist_label(false);
                        line.set_pricelist_id(false);

                    }
                else if(price < pricelist_price_dict[minpriceKey] || price > pricelist_price_dict[minpriceKey] ){

                    var name = false;
                    var policy = false;
                    self.pos.pricelists.forEach((pricelists)=> {
                        if (pricelists.id === parseInt(minpriceKey)  ){

                            name = pricelists.name
                            policy = pricelists.discount_policy
                        }

                    });

                    line.set_pricelist_discount_label(policy);
                    line.set_pricelist_label(name);
                    line.set_pricelist_id(minpriceKey);

                }
            })
                }

            }
         return true
    }

});

patch(Product.prototype,{
    setup(){
        super.setup(...arguments);
    },

    get_price(pricelist, quantity, price_extra){
        var self = this;
        var date = DateTime.now().startOf("day");
        var price = super.get_price(...arguments);
        var default_price = self.lst_price;
        if (price_extra){
            default_price += price_extra;
        }
        if (self.pos.config.use_pricelist){
	    		var pricelist_price_dict = {}

	    		self.pos.pricelists.forEach(function (pricelists) {
	    			var pricelist_items = pricelists.items.filter(function (item) {
			            return (! item.product_tmpl_id || item.product_tmpl_id[0] === self.product_tmpl_id) &&
			                   (! item.product_id || item.product_id[0] === self.id) &&
			                   (! item.categ_id || category_ids.contains(item.categ_id[0])) &&
			                   (! item.date_start || moment(item.date_start).isSameOrBefore(date)) &&
			                   (! item.date_end || moment(item.date_end).isSameOrAfter(date));
			        });
			        var pricelist_rule_items = {}

			       pricelist_items.find(function (rule) {
			       		var temp_price = default_price
			            if (rule.min_quantity && quantity < rule.min_quantity) {
			            	pricelist_rule_items[rule.id] = temp_price
			                return false;
			            }

			            if (rule.base === 'pricelist') {
			                temp_price = self.get_price(rule.base_pricelist, quantity);
			                pricelist_rule_items[rule.id] = temp_price
			            } else if (rule.base === 'standard_price') {

			                temp_price = self.standard_price;
			                pricelist_rule_items[rule.id] = temp_price
			            }

			            if (rule.compute_price === 'fixed') {
			                temp_price = rule.fixed_price;
			                pricelist_rule_items[rule.id] = temp_price
			                return true;
			            } else if (rule.compute_price === 'percentage') {
			                temp_price = temp_price - (temp_price * (rule.percent_price / 100));
			                pricelist_rule_items[rule.id] = temp_price
			                return true;
			            } else {
			                var price_limit = price;
			                temp_price = temp_price - (temp_price * (rule.price_discount / 100));
			                if (rule.price_round) {
			                    temp_price = round_pr(temp_price, rule.price_round);
			                }
			                if (rule.price_surcharge) {
			                    temp_price += rule.price_surcharge;
			                }
			                if (rule.price_min_margin) {
			                    temp_price = Math.max(temp_price, price_limit + rule.price_min_margin);
			                }
			                if (rule.price_max_margin) {
			                    temp_price = Math.min(temp_price, price_limit + rule.price_max_margin);
			                }
			                pricelist_rule_items[rule.id] = temp_price
			                return true;
			            }
			            pricelist_rule_items[rule.id] = temp_price
			            return false;
			        });

			        var minKey = Object.keys(pricelist_rule_items)
					pricelist_price_dict[pricelists.id] = pricelist_rule_items[minKey]
	    		});
	    		var minpriceKey = Object.keys(pricelist_price_dict)[0]
	    		if(price > pricelist_price_dict[minpriceKey]) {
	    			price = pricelist_price_dict[minpriceKey]
	    		}
	    		self.pos.get_order().get_pricelist_label(self.pos.get_order().get_selected_orderline())
	    	}
        return price;
	}
})

patch(ProductScreen.prototype, {
    setup() {
        super.setup(...arguments);
    },

    onMounted() {
//        this.pos.get_order().pricelist['display_name'];
//        this.pos.selectedOrder.pricelist['display_name'];

    }
});








