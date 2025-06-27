/** @odoo-module */

import { OrderWidget } from "@point_of_sale/app/generic_components/order_widget/order_widget";
import { patch } from "@web/core/utils/patch";

// Patch the OrderSummary to add custom properties
patch(OrderWidget.prototype, {
    get ItemCount(){
       return this.props.lines.length
    },
     get total(){
        return this.props.total
    },
    get TotalQuantity(){
        var totalQuantity = 0;
        this.props.lines.forEach(line => totalQuantity += Number(line.get_currency_exchange.slice(0, -1)));
        totalQuantity = totalQuantity.toFixed(4);
        let currencySymbol = this.props?.lines[0]?.get_currency_exchange?.slice(-1)
        if (totalQuantity == 'NaN'){
            return this.props.total
        }
        return totalQuantity + currencySymbol
    }
});