odoo.define("sh_pos_advance_cache.cache_uom", function (require) {
    "use strict";

    var indexedDB = require('sh_pos_advance_cache.indexedDB');
    const { PosGlobalState } = require('point_of_sale.models');
    const Registries = require('point_of_sale.Registries');
    const rpc = require("web.rpc");

    const shPosProductUomModel = (PosGlobalState) => class shPosProductUomModel extends PosGlobalState {

        async _processData(loadedData) {
            const productUomModel = 'uom.uom'
            const session_id = odoo.pos_session_id
            const dynamic_key = `${session_id}_${productUomModel}`;
            if (localStorage.getItem(dynamic_key) === 'loaded') {
                var all_products_uom = []
                await indexedDB.get_all('uom.uom').then(function (cache_products_uom) {
                    all_products_uom = cache_products_uom
                });
                loadedData['uom.uom'] = all_products_uom
                var units_by_id = {};
                $.each(all_products_uom,function(index,value){
                    units_by_id[value['id']] = value
                });
                loadedData['units_by_id'] = units_by_id
            } else {
                var all_products_uom = []
                await this.env.services.rpc({
                    model: 'pos.session',
                    method: 'sh_load_model',
                    args: [odoo.pos_session_id, productUomModel],
                }).then(function (result) {
                    if (result) {
                        all_products_uom = result
                        indexedDB.save_data('uom.uom', all_products_uom)
                    }
                });

                loadedData['uom.uom'] = all_products_uom
                var units_by_id = {};
                $.each(all_products_uom,function(index,value){
                    units_by_id[value['id']] = value
                });
                loadedData['units_by_id'] = units_by_id
                localStorage.setItem(dynamic_key, 'loaded')
            }
            await super._processData(...arguments);
        }
    }
    Registries.Model.extend(PosGlobalState, shPosProductUomModel);

});
