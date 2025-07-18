odoo.define("sh_pos_advance_cache.cache_customer", function (require) {
    "use strict";

    var indexedDB = require('sh_pos_advance_cache.indexedDB');
    const { PosGlobalState } = require('point_of_sale.models');
    const Registries = require('point_of_sale.Registries');
    const rpc = require("web.rpc");

    const shPosCustomerModel = (PosGlobalState) => class shPosCustomerModel extends PosGlobalState {
        async _processData(loadedData) {
            const customerModel = 'res.partner'
            const session_id = odoo.pos_session_id
            const dynamic_key = `${session_id}_${customerModel}`;
            if (localStorage.getItem(dynamic_key) === 'loaded') {
                // Remove deleted partners from indexed db
                await rpc.query({
                    model: 'customer.update',
                    method: 'search_read',
                    args: [[]],
                }).then(async function (result) {
                    if (result) {
                        for (var i = 0; i < result.length; i++) {
                            await indexedDB.get_by_id('res.partner', parseInt(result[i]['delete_ids'])).then(function (cache_partner) {
                                indexedDB.delete_item('res.partner', parseInt(result[i]['delete_ids']))
                            });
                        }
                    }
                });
                var all_partners = []
                await indexedDB.get_all('res.partner').then(function (cache_partners) {
                    all_partners = cache_partners
                });
                loadedData['res.partner'] = all_partners
            } else {
                var all_partners = []
                await this.env.services.rpc({
                    model: 'pos.session',
                    method: 'sh_load_model',
                    args: [odoo.pos_session_id, customerModel],
                }).then(function (result) {
                    if (result) {
                        all_partners = result
                        indexedDB.save_data('res.partner', all_partners)
                    }
                });
                loadedData['res.partner'] = all_partners
                localStorage.setItem(dynamic_key, 'loaded')
            }
            await super._processData(...arguments);
        }
    }
    Registries.Model.extend(PosGlobalState, shPosCustomerModel);


});
