odoo.define("sh_pos_advance_cache.cache_res_country", function (require) {
    "use strict";

    var indexedDB = require('sh_pos_advance_cache.indexedDB');
    const { PosGlobalState } = require('point_of_sale.models');
    const Registries = require('point_of_sale.Registries');
    const rpc = require("web.rpc");

    const shPoscountryModel = (PosGlobalState) => class shPoscountryModel extends PosGlobalState {

        async _processData(loadedData) {
            const countryModel = 'res.country'
            const session_id = odoo.pos_session_id
            const dynamic_key = `${session_id}_${countryModel}`;
            if (localStorage.getItem(dynamic_key) === 'loaded') {
                var all_country = []
                await indexedDB.get_all('res.country').then(function (cache_country) {
                    all_country = cache_country
                });
                loadedData['res.country'] = all_country
            } else {
                var cache_country = []
                await this.env.services.rpc({
                    model: 'pos.session',
                    method: 'sh_load_model',
                    args: [odoo.pos_session_id, countryModel],
                }).then(function (result) {
                    if (result) {
                        cache_country = result
                        indexedDB.save_data('res.country', cache_country)
                    }
                });

                loadedData['res.country'] = cache_country
                localStorage.setItem(dynamic_key, 'loaded')
            }
            await super._processData(...arguments);
        }
    }
    Registries.Model.extend(PosGlobalState, shPoscountryModel);

});
