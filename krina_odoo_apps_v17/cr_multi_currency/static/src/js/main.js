/** @odoo-module */
/* Copyright (c) 2016-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>) */
/* See LICENSE file for full copyright and licensing details. */
/* License URL : <https://store.webkul.com/license.html/> */
import { PosStore } from "@point_of_sale/app/store/pos_store";
import { Order,Orderline } from "@point_of_sale/app/store/models";
import { patch } from "@web/core/utils/patch";
import { Payment } from "@point_of_sale/app/store/models";
import { formatFloat, roundDecimals as round_di } from "@web/core/utils/numbers";
import { ProductCard } from "@point_of_sale/app/generic_components/product_card/product_card";
import FeedbackPopup from "@cr_multi_currency/js/MultiCurrencyPopup"
import  { onMounted, useRef, useState } from "@odoo/owl";
import { useBus } from "@web/core/utils/hooks";
import { usePos } from "@point_of_sale/app/store/pos_hook";
import { PaymentScreenStatus } from "@point_of_sale/app/screens/payment_screen/payment_status/payment_status";


patch(PosStore.prototype, {
    async _processData(loadedData) {
        await super._processData(...arguments);
       var self = this;
       this.current_currency = this.current_currency || ''
       const savedCashier = this._getConnectedCashier();
        const currencies = await self.orm.silent.call(
           'res.currency',
           'get_currency',
            [this.config.multi_currency_ids]
        )
        if (currencies) {
            self.currencies = false
            if (self.config.enable_multi_currency && self.config.multi_currency_ids) {
                self.currencies = []
                self.currency_by_id = {}
                currencies.forEach(function (currencie) {
                    if (self.config.multi_currency_ids.includes(currencie.id)) {
                        if (self.config.currency_id[0] != currencie.id) {
                            self.currencies.push(currencie)
                            self.currency_by_id[currencie.id] = currencie
                        }
                    }
                    if (self.config.currency_id[0] == currencie.id) {
                        self.currencies.push(currencie)
                        self.currency_by_id[currencie.id] = currencie
                    }
                    if (currencie.rate == 1) {
                        self.base_currency = currencie
                    }
                });
            }
        }
    },
     async addProductToCurrentOrder(product, options = {}) {
        var currency_order = this.get_order().use_multi_currency
        this.get_order().use_multi_currency = currency_order
        if (Number.isInteger(product)) {
            product = this.db.get_product_by_id(product);
        }
        this.get_order() || this.add_new_order();

        options = { ...(await product.getAddProductOptions()), ...options };

        if (!Object.keys(options).length) {
            return;
        }

        // Add the product after having the extra information.
        await this.addProductFromUi(product, options);
        this.numberBuffer.reset();
    },
    formating(amount, currency_id) {
        if (currency_id) {
          var currency = this.currency_by_id[currency_id];
        }
        else {
          var currency = this.currency;
        }
        if (currency.position === 'after') {
          return amount + ' ' + (currency.symbol || '');
        } else {
          return (currency.symbol || '') + ' ' + amount;
        }
      },
      format_currency_n_symbol(amount, precisson) {
        if (typeof amount === 'number') {
          var decimals = 4;
          amount = round_di(amount, decimals)
          amount = formatFloat(round_di(amount, decimals), {
            digits: [69, decimals],
          });
        }
        return amount;
  
      },
      test(){
        console.log
      }
});


patch(Order.prototype, {
    setup(options) {
        super.setup(...arguments);
        var self = this;
        self.use_multi_currency = self.use_multi_currency || false;
        self.multi_payment_lines = self.multi_payment_lines || {};
        self.is_multi_currency_payment = self.is_multi_currency_payment || false;
    },
    init_from_JSON(json) {
        var self = this;
        super.init_from_JSON(...arguments);
        this.use_multi_currency = json.use_multi_currency || false;
        this.other_currency_amount = json.other_currency_amount || false;
        this.multi_payment_lines = json.multi_payment_lines || {};
        this.is_multi_currency_payment = json.is_multi_currency_payment || false;
        this.reprint = json.reprint || false;

    },
    export_as_JSON() {
        var self = this;
        var loaded = super.export_as_JSON();
        if (self.use_multi_currency)
            loaded.use_multi_currency = self.use_multi_currency;
            loaded.reprint = self.reprint;
        loaded.multi_payment_lines = self.multi_payment_lines;
        loaded.is_multi_currency_payment = self.is_multi_currency_payment;
        return loaded
    },
    export_for_printing() {
        var self = this;
        var receipt = super.export_for_printing();
        receipt.multi_payment_lines = self.get_paymentlines();
        // if (receipt.multi_payment_lines.length) {
        //     receipt.multi_payment_lines.forEach(function (line) {
        //         if (line.is_multi_currency_payment) {
        //             line.other_currency_amount=formatFloat(round_di(line.other_currency_amount, 4), { digits: [69, 4] });
        //         }
        //     });
        // }
        if(self.reprint){
            receipt.is_multi_currency_payment = self.is_multi_currency_payment;
            receipt.multi_payment_lines = self.multi_payment_lines;
            receipt.multi_payment_lines.forEach(function(line){
                if(line.is_change){
                    receipt.is_other_currency_change = true
                    receipt.change_other_currency_id = line.other_currency_id
                    receipt.change_other_currency_amount = line.other_currency_amount
                }
            })
        }
        receipt.is_multi_currency_payment = self.is_multi_currency_payment;
        return receipt;
    },
    get_other_currency_amount(line) {
        var self = this;
        if (line && line.currency_id) {
            var amt = (self.pos.currency_by_id[line.currency_id].rate * line.otc_amount) / self.pos.currency.rate
            line.other_currency_amount = (self.pos.currency_by_id[line.currency_id].rate * line.get_amount()) / self.pos.currency.rate;
            var res = formatFloat(round_di(amt, 4), { digits: [69, 4] });
            return res;
        }
        else {
            line.other_currency_amount = 0.0;
            return 0.0;
        }
    },
    get_change_mc(change, paymentline) {
        if (this.use_multi_currency && paymentline && paymentline.other_currency_id) {
            var amt = (this.pos.currency_by_id[paymentline.currency_id].rate * change) / this.pos.currency.rate
            amt = parseFloat(round_di(amt, 4));
            return amt
        } else {
            return Math.max(0, change);
        }
    }
});

patch(Orderline.prototype, {
    setup(options) {
        super.setup(...arguments);
        var self = this;
        this.get_currency_exchange = ""
        self.use_multi_currency = self.use_multi_currency || false;
    },
    init_from_JSON(json) {
        var self = this;
        super.init_from_JSON(...arguments);
        this.use_multi_currency = json.use_multi_currency || false;

    },
    export_as_JSON() {
        var self = this;
        var loaded = super.export_as_JSON();
        if (self.use_multi_currency)
            loaded.use_multi_currency = self.use_multi_currency;
        return loaded
    },
    export_for_printing() {
        var self = this;
        var receipt = super.export_for_printing();
        receipt.use_multi_currency = self.use_multi_currency;
        // if (receipt.multi_payment_lines.length) {
        //     receipt.multi_payment_lines.forEach(function (line) {
        //         if (line.is_multi_currency_payment) {
        //             line.other_currency_amount=formatFloat(round_di(line.other_currency_amount, 4), { digits: [69, 4] });
        //         }
        //     });
        // }
        return receipt;
    },
      get get_set_currency_exchange(){
        return this.get_currency_exchange;
    },


    set_currency_exchange(data){
        this.get_currency_exchange = data
    },

    getDisplayData() {
        let result = super.getDisplayData();
        var amountInUSD = parseFloat(result.price.replace(/[^0-9.]/g, '')); // Amount in USD for the specific order line
        var curr = Number(this.use_multi_currency) || this.order.use_multi_currency
        var exchangeRate = this.pos.currency_by_id[curr]?.rate;  // Fetch the rate for selected currency

//         this.props?.lines[0]?.get_currency_exchange?.slice(-1)
        console.log("this.pos",this.pos.currency.id)
        var convertedAmount = this.convertCurrency(amountInUSD, exchangeRate);
        convertedAmount = convertedAmount.toFixed(4);
        this.set_currency_exchange(convertedAmount + this.pos.currency_by_id[curr]?.symbol);
        result['get_currency_exchange'] = this.get_set_currency_exchange
        return result
    },
     convertCurrency(amount, exchangeRate) {
            return amount * exchangeRate;
     },
    get_other_currency_amount(line) {
        var self = this;
        if (line && line.currency_id) {
            var amt = (self.pos.currency_by_id[line.currency_id].rate * line.otc_amount) / self.pos.currency.rate
            line.other_currency_amount = (self.pos.currency_by_id[line.currency_id].rate * line.get_amount()) / self.pos.currency.rate;
            var res = formatFloat(round_di(amt, 4), { digits: [69, 4] });
            return res;
        }
        else {
            line.other_currency_amount = 0.0;
            return 0.0;
        }
    },
    get_change_mc(change, paymentline) {
        if (this.use_multi_currency && paymentline && paymentline.other_currency_id) {
            var amt = (this.pos.currency_by_id[paymentline.currency_id].rate * change) / this.pos.currency.rate
            amt = parseFloat(round_di(amt, 4));
            return amt
        } else {
            return Math.max(0, change);
        }
    }
});
patch(ProductCard.prototype, {
    setup() {
        super.setup();
        this.pos = usePos();
        useBus(this.env.bus, 'validate-order', (ev) => this.validate_order(ev.detail.currencyId));
        this.state = useState({
            exchange_currency: {},
        });
    },
    get getWkFormattedUnitPrice() {
        const feedbackPopupInstance = FeedbackPopup;
        let product_price = this.props.price
        let price = product_price.replace(/[^0-9.]/g, '');
        var amountInUSD = price; // Amount in USD for the specific order line
        var exchangeRate = this.pos.currency_by_id[126].rate;
        const formattedUnitPrice = this.env.services.pos.formating(price,this.pos.xxx);
        return amountInUSD * exchangeRate
    },

    validate_order(currencyId){
        var productId = this.props.productId
        let product_price = this.props.price
        let price = product_price.replace(/[^0-9.]/g, '');
        var exchangeRate = this.pos.currency_by_id[currencyId].rate;
        var final_price = price * exchangeRate
        const formattedUnitPrice = this.env.services.pos.formating(final_price.toFixed(4),currencyId);
        this.state.exchange_currency[productId] = formattedUnitPrice
    },
});


patch(Payment.prototype, {
    setup() {
        super.setup(...arguments);
        var self = this;
        // self.other_currency_id = false
        // self.other_currency_rate = false
        // self.other_currency_amount = 0.0
        // self.otc_amount = 0.0
        self.currency_id = self.currency_id || false;
        self.other_currency_id = self.currency_id || false;
        self.other_currency_rate = self.other_currency_rate || false;
        self.other_currency_amount = self.other_currency_amount || 0.0;
        self.is_multi_currency_payment = self.is_multi_currency_payment || false;
        self.otc_amount = self.otc_amount || 0;
    },
    init_from_JSON(json) {
        var self = this;
        super.init_from_JSON(...arguments);
        self.currency_id = json.currency_id || false;
        self.other_currency_id = self.currency_id || false;
        self.other_currency_rate = json.other_currency_rate || false;
        self.other_currency_amount = self.other_currency_amount || 0.0;
        self.is_multi_currency_payment = json.is_multi_currency_payment || false;
        self.otc_amount = json.otc_amount || 0.0;
    },
    export_as_JSON() {
        var self = this;
        var loaded = super.export_as_JSON();
        if (self.currency_id) {
            loaded.currency_id = self.currency_id;
        }
        if (self.other_currency_id) {
            loaded.other_currency_id = self.currency_id;
        }
        if (self.other_currency_rate) {
            loaded.other_currency_rate = self.other_currency_rate;
        }
        if (self.other_currency_amount) {
            loaded.other_currency_amount = self.other_currency_amount;
        }
        if (self.is_multi_currency_payment) {
            loaded.is_multi_currency_payment = self.is_multi_currency_payment
        }
        if (self.otc_amount) {
            loaded.otc_amount = self.otc_amount
        }
        return loaded;
    }
});
