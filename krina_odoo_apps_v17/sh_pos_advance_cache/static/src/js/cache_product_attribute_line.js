odoo.define("sh_pos_advance_cache.cache_product_attribute_line", function (require) {
    "use strict";

    var indexedDB = require('sh_pos_advance_cache.indexedDB');
    const { PosGlobalState } = require('point_of_sale.models');
    const Registries = require('point_of_sale.Registries');
    const rpc = require("web.rpc");

    const shPosProductAttributeLineModel = (PosGlobalState) => class shPosProductAttributeLineModel extends PosGlobalState {

        async _processData(loadedData) {
            const ProductAttributeLineModel = 'product.template.attribute.line'
            const session_id = odoo.pos_session_id
            const dynamic_key = `${session_id}_${ProductAttributeLineModel}`;
            if (localStorage.getItem(dynamic_key) === 'loaded') {
                // Remove deleted products from indexed db
                await rpc.query({
                    model: 'product.template.attribute.line.update',
                    method: 'search_read',
                    args: [[]],
                }).then(async function (result) {
                    if (result) {
                        for (var i = 0; i < result.length; i++) {
                            await indexedDB.get_by_id('product.template.attribute.line', parseInt(result[i]['delete_ids'])).then(function (cache_attribute_product_line) {
                                indexedDB.delete_item('product.template.attribute.line', parseInt(result[i]['delete_ids']))
                            });
                        }
                    }
                });
                //
                var all_products_attribute_line = []
                await indexedDB.get_all('product.template.attribute.line').then(function (cache_attribute_product_line) {
                    all_products_attribute_line = cache_attribute_product_line
                });
                loadedData['product.template.attribute.line'] = all_products_attribute_line
                var product_temlate_attribute_line_by_id = {};
                $.each(all_products_attribute_line,function(index,value){
                    product_temlate_attribute_line_by_id[value['id']] = value
                });
                loadedData['product_temlate_attribute_line_by_id'] = product_temlate_attribute_line_by_id
            } else {
                var all_products_attribute_line = []
                await this.env.services.rpc({
                    model: 'pos.session',
                    method: 'sh_load_model',
                    args: [odoo.pos_session_id, ProductAttributeLineModel],
                }).then(function (result) {
                    if (result) {
                        all_products_attribute_line = result
                        indexedDB.save_data('product.template.attribute.line', all_products_attribute_line)
                    }
                });

                loadedData['product.template.attribute.line'] = all_products_attribute_line
                var product_temlate_attribute_line_by_id = {};
                $.each(all_products_attribute_line,function(index,value){
                    product_temlate_attribute_line_by_id[value['id']] = value
                });
                loadedData['product_temlate_attribute_line_by_id'] = product_temlate_attribute_line_by_id
                localStorage.setItem(dynamic_key, 'loaded')
            }
            await super._processData(...arguments);
        }
    }
    Registries.Model.extend(PosGlobalState, shPosProductAttributeLineModel);

});
