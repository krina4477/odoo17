/* @odoo-module */

import VariantMixin from "@website_sale_stock/js/variant_mixin";
import "@website_sale/js/website_sale";
import { renderToElement } from "@web/core/utils/render";
import { renderToFragment } from "@web/core/utils/render";


const oldChangeCombinationStock = VariantMixin._onChangeCombinationStock;

VariantMixin._onChangeCombinationStock = function (ev, $parent, combination) {    
    oldChangeCombinationStock.apply(this, arguments);
    $('.oe_website_sale')
        .find('.container availability_message')
        .remove();

    $('.availability_message_undefined').addClass('d-none')

    if ($('.oe_website_sale').find('.availability_message').length < 1)
    $('div.availability_messages').append(renderToFragment(
        'website_product_stock_notify_cr.product_availability',
        combination
    ));

};