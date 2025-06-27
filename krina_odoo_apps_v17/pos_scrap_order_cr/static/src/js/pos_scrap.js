/** @odoo-module **/

import { patch } from "@web/core/utils/patch";
import { ProductScreen } from "@point_of_sale/app/screens/product_screen/product_screen";

patch(ProductScreen.prototype, {
    setup() {
        super.setup(...arguments);
        this.busService = this.env.services.bus_service;
        console.log('ddddddddddcccccccc', this);

        this.busService.subscribe("line_delete", (payload) => {
            console.log('dddddddddd', payload);
            this._handleLineDelete(payload);
        });
    },

    _handleLineDelete(payload) {
        console.log("Line delete payload received:", payload);

        if (!this.currentOrder) {
            console.warn("No current order found.");
            return;
        }

        console.log("----------this.currentOrder------------", this.currentOrder);

        const orderLines = this.currentOrder.get_orderlines();
        console.log("Order lines in the current order:", orderLines);

        let orderLineToDelete = orderLines.find((line) => line.id === payload.id);

        if (!orderLineToDelete) {
            orderLineToDelete = orderLines.find((line) => line.product.id === payload.product_id);
        }

        if (orderLineToDelete) {
            console.log("Order line to delete found:", orderLineToDelete);
            this.currentOrder.removeOrderline(orderLineToDelete);
        } else {
            console.warn("Order line not found for ID:", payload.id);
        }
    }
});
