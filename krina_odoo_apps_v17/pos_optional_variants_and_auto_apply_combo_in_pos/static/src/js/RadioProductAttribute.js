/** @odoo-module **/

import { ProductConfiguratorPopup } from "@point_of_sale/app/store/product_configurator_popup/product_configurator_popup";
import { patch } from "@web/core/utils/patch";

patch(ProductConfiguratorPopup.prototype, {

    getPayload() {
        const attribute_custom_values = [];
        let attribute_value_ids = [];
        var price_extra = 0.0;
        const quantity = this.state.quantity;

        this.env.attribute_components.forEach((attribute_component) => {
            var attribute_name = attribute_component.attribute.name;
            var radioValue = $("input[name='"+attribute_name.toString()+"']:checked").val();
            if (radioValue !== 'no'){
                const { valueIds, extra, custom_value } = attribute_component.getValue();
                attribute_value_ids.push(valueIds);

                if (custom_value) {
                    // for custom values, it will never be a multiple attribute
                    attribute_custom_values[valueIds[0]] = custom_value;
                }

                price_extra += extra;
            }
        });

        attribute_value_ids = attribute_value_ids.flat();
        return {
            attribute_value_ids,
            attribute_custom_values,
            price_extra,
            quantity,
        };
    }

})