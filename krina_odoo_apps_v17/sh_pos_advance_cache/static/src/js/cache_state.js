    odoo.define("sh_pos_advance_cache.cache_state", function (require) {
    "use strict";

    var indexedDB = require('sh_pos_advance_cache.indexedDB');
    const { PosGlobalState } = require('point_of_sale.models');
    const Registries = require('point_of_sale.Registries');
    const rpc = require("web.rpc");

    const shPosCountryStateModel = (PosGlobalState) => class shPosCountryStateModel extends PosGlobalState {

        async _processData(loadedData) {
            const StateModel = 'res.country.state'
            const session_id = odoo.pos_session_id
            const dynamic_key = `${session_id}_${StateModel}`;
            if (localStorage.getItem(dynamic_key) === 'loaded') {
                var all_state = []
                await indexedDB.get_all('res.country.state').then(function (cache_all_state) {
                    all_state = cache_all_state
                });
                loadedData['res.country.state'] = all_state
            } else {
                var all_state = []
                await this.env.services.rpc({
                    model: 'pos.session',
                    method: 'sh_load_model',
                    args: [odoo.pos_session_id, StateModel],
                }).then(function (result) {
                    if (result) {
                        all_state = result
                        indexedDB.save_data('res.country.state', all_state)
                    }
                });

                loadedData['res.country.state'] = all_state
                localStorage.setItem(dynamic_key, 'loaded')
            }
            await super._processData(...arguments);
        }
    }
    Registries.Model.extend(PosGlobalState, shPosCountryStateModel);

});
