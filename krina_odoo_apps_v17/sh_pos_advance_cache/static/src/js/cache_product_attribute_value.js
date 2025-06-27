odoo.define("sh_pos_advance_cache.cache_product_attribute_value", function (require) {
    "use strict";

    var indexedDB = require('sh_pos_advance_cache.indexedDB');
    const { PosGlobalState } = require('point_of_sale.models');
    const Registries = require('point_of_sale.Registries');
    const rpc = require("web.rpc");

    const shPosProductAttributeValueModel = (PosGlobalState) => class shPosProductAttributeValueModel extends PosGlobalState {

        async _processData(loadedData) {
            const productAttributeValueModel = 'product.template.attribute.value'
            const session_id = odoo.pos_session_id
            const dynamic_key = `${session_id}_${productAttributeValueModel}`;
            if (localStorage.getItem(dynamic_key) === 'loaded') {
                // Remove deleted products from indexed db
                await rpc.query({
                    model: 'product.attribute.value.update',
                    method: 'search_read',
                    args: [[]],
                }).then(async function (result) {
                    if (result) {
                        for (var i = 0; i < result.length; i++) {
                            await indexedDB.get_by_id('product.template.attribute.value', parseInt(result[i]['delete_ids'])).then(function (cache_product_attribute_value) {
                                indexedDB.delete_item('product.template.attribute.value', parseInt(result[i]['delete_ids']))
                            });
                        }
                    }
                });
                //
                var all_products_attribute_value = []
                await indexedDB.get_all('product.template.attribute.value').then(function (cache_product_attribute_value) {
                    all_products_attribute_value = cache_product_attribute_value
                });
                loadedData['product.template.attribute.value'] = all_products_attribute_value
                var product_temlate_attribute_by_id = {};
                $.each(all_products_attribute_value,function(index,value){
                    product_temlate_attribute_by_id[value['id']] = value
                });
                loadedData['product_temlate_attribute_by_id'] = product_temlate_attribute_by_id
                var attributes_by_ptal_id = {};
                $.each(all_products_attribute_value,function(index,value){
                    var attribute_line_id = value['attribute_line_id']
                    var data1 = {}
                    var data = {
                        'id': value['product_attribute_value_id'],
                        'name': value['name'],
                        'is_custom': value['is_custom'],
                        'html_color':value['html_color'],
                        'price_extra': value['price_extra']
                    }
                    if (value['attribute_line_id'] in attributes_by_ptal_id) {
                        attributes_by_ptal_id[value['attribute_line_id']][attribute_line_id]['values'].push(data)
                    }
                    else {
                        // var attribute_line_id = value['attribute_line_id'];
                        var data2 = {
                            'id': value['attribute_line_id'],
                            'name': value['display_name'].split(":")[0],
                            'display_type': value['display_type'],
                            'values': [data],
                        }
                        var data1 = {}
                        data1[attribute_line_id] = data2
                        attributes_by_ptal_id[value['attribute_line_id']] = data1
                    }
                });
                loadedData['attributes_by_ptal_id'] = attributes_by_ptal_id
            } else {
                var all_products_attribute_value = []
                await this.env.services.rpc({
                    model: 'pos.session',
                    method: 'sh_load_model',
                    args: [odoo.pos_session_id, productAttributeValueModel],
                }).then(function (result) {
                    if (result) {
                        all_products_attribute_value = result
                        indexedDB.save_data('product.template.attribute.value', all_products_attribute_value)
                    }
                });

                loadedData['product.template.attribute.value'] = all_products_attribute_value
                var product_temlate_attribute_by_id = {};
                $.each(all_products_attribute_value,function(index,value){
                    product_temlate_attribute_by_id[value['id']] = value
                });
                loadedData['product_temlate_attribute_by_id'] = product_temlate_attribute_by_id
                var attributes_by_ptal_id = {};
                $.each(all_products_attribute_value,function(index,value){
                    var attribute_line_id = value['attribute_line_id']
                    var data1 = {}
                    var data = {
                        'id': value['product_attribute_value_id'],
                        'name': value['name'],
                        'is_custom': value['is_custom'],
                        'html_color':value['html_color'],
                        'price_extra': value['price_extra']
                    }
                    if (value['attribute_line_id'] in attributes_by_ptal_id) {
                        attributes_by_ptal_id[value['attribute_line_id']][attribute_line_id]['values'].push(data)
                    }
                    else {
                        // var attribute_line_id = value['attribute_line_id'];
                        var data2 = {
                            'id': value['attribute_line_id'],
                            'name': value['display_name'].split(":")[0],
                            'display_type': value['display_type'],
                            'values': [data],
                        }
                        var data1 = {}
                        data1[attribute_line_id] = data2
                        attributes_by_ptal_id[value['attribute_line_id']] = data1
                    }
                });
                loadedData['attributes_by_ptal_id'] = attributes_by_ptal_id
                localStorage.setItem(dynamic_key, 'loaded')
            }
            await super._processData(...arguments);
        }
    }
    Registries.Model.extend(PosGlobalState, shPosProductAttributeValueModel);

});
