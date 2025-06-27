/** @odoo-module **/
/**
 * Defines AbstractAwaitablePopup extending from AbstractAwaitablePopup
 */
import { AbstractAwaitablePopup } from "@point_of_sale/app/popup/abstract_awaitable_popup";
import { _lt } from '@web/core/l10n/translation';
import  { onMounted, useRef, useState } from "@odoo/owl";
import { usePos } from "@point_of_sale/app/store/pos_hook";
import { formatFloat } from "@web/views/fields/formatters";

import {roundDecimals as round_di } from "@web/core/utils/numbers";

export class MultiCurrencyPopup extends AbstractAwaitablePopup {
  amountCheck() {
    var currency_id = $('.wk-selected-currency').val()
    if (currency_id) {
      var currency = this.pos.currency_by_id[currency_id]
      if (currency) {
        $(".wk-exchange-rate").html(currency.rate)
        var rate = (currency.rate * 1) / this.pos.currency_by_id[this.pos.config.currency_id[0]].rate
        rate = formatFloat(round_di(rate, 5), { digits: [69, 5] })
        $(".wk-currency-amount").html(rate)
        $(".wk-currency-name").html(currency.name + "(" + currency.symbol + ")")
      }
    }
  }
  setup() {
    this.pos = usePos();
    super.setup();
    onMounted(this.onMounted);
  }
  onMounted() {
    var self = this;
    self.amountCheck();
  }
  selected_currency() {
    var self = this;
    self.amountCheck();
  }
  getPayload() {
    var currency_id = $('.wk-selected-currency').val();
    return currency_id;
  }
};
MultiCurrencyPopup.template = 'cr_multi_currency.MultiCurrencyPopup';
MultiCurrencyPopup.defaultProps = {
    confirmText: 'ADD',
    cancelText: 'Cancel',
    title: 'Select the Product',
    body: '',
    list: []
};
export default MultiCurrencyPopup;
