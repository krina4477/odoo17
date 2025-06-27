/** @odoo-module **/
// Customer feedback button fn
import { _t } from "@web/core/l10n/translation";
import { ProductScreen } from "@point_of_sale/app/screens/product_screen/product_screen";
import { useService } from "@web/core/utils/hooks";
import { Component } from "@odoo/owl";
import { onMounted } from "@odoo/owl";
import FeedbackPopup from "@cr_multi_currency/js/MultiCurrencyPopup"
import { formatFloat } from "@web/views/fields/formatters";
import {roundDecimals as round_di } from "@web/core/utils/numbers";
import { ProductCard } from "@point_of_sale/app/generic_components/product_card/product_card";

export class MultiCurrency extends Component {
    static template = "point_of_sale.MultiCurrency";
    setup() {
        const pos = useService("pos");
        if (!pos) {
            console.error("POS service not available");
            return;
        }
        this.pos=pos
         this.partner = pos.get_order().get_partner();
         this.selectedOrderline = pos.get_order().get_selected_orderline();

        const { popup } = this.env.services;
        this.popup = popup;

        onMounted(() => {
            const starValue = pos.selectedOrder && pos.selectedOrder.customer_feedback;
            if (starValue) {
                this.setStarRating(starValue);
            }
        });
    }
//    get selected_currency() {
//        return this.props
//    }

    setStarRating(starValue) {
        let newStarValue = starValue || 0;
        const starPercentage = (parseInt(newStarValue) / 5) * 100;
        const starPercentageRounded = `${(Math.round(starPercentage / 10) * 10)}%`;
        document.querySelector(`.stars-inner`).style.width = starPercentageRounded;
    }

    async onClick() {
        const { confirmed, payload: inputFeedback } = await this.popup.add(
            FeedbackPopup
        );

        if (confirmed) {
            var currency_id = $('.wk-selected-currency').val();
            this.env.bus.trigger("validate-order", {currencyId: currency_id});
            var order = this.pos.get_order();
            this.pos.current_currency = currency_id
            order.get_orderlines().use_multi_currency = currency_id
            order.use_multi_currency = currency_id
            order.get_orderlines().forEach(function (orderline) {
                var amountInUSD = orderline.price; // Amount in USD for the specific order line
                var exchangeRate = this.pos.currency_by_id[currency_id].rate;  // Fetch the rate for selected currency
                var convertedAmount = convertCurrency(amountInUSD, exchangeRate);
                convertedAmount = convertedAmount.toFixed(2);
                orderline.set_currency_exchange(convertedAmount + this.pos.currency_by_id[currency_id].symbol);
                orderline.use_multi_currency = currency_id;
            }, this);
        }

        function convertCurrency(amount, exchangeRate) {
            return amount * exchangeRate;
        }
    }
}
ProductScreen.addControlButton({
    component: MultiCurrency,
});
