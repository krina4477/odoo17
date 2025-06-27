odoo.define("sh_pos_advance_cache.cache_pre_define_note", function (require) {
    "use strict";

    var indexedDB = require('sh_pos_advance_cache.indexedDB');
    const { PosGlobalState } = require('point_of_sale.models');
    const Registries = require('point_of_sale.Registries');
    const rpc = require("web.rpc");

    const shPosPreDefineModel = (PosGlobalState) => class shPosPreDefineModel extends PosGlobalState {

        async _processData(loadedData) {
            const PreDefineModel = 'pre.define.note'
            const session_id = odoo.pos_session_id
            const dynamic_key = `${session_id}_${PreDefineModel}`;
            if (localStorage.getItem(dynamic_key) === 'loaded') {
                var pre_define = []
                await indexedDB.get_all('pre.define.note').then(function (cache_pre_define) {
                    pre_define = cache_pre_define
                });
                loadedData['pre.define.note'] = pre_define
                var pre_define_by_id = {};
                $.each(pre_define,function(index,value){
                    pre_define_by_id[value['id']] = value
                });
                loadedData['pre_defined_note_data_dict'] = pre_define_by_id
                var second_pre_define_by_id = {};
                $.each(pre_define,function(index,value){
                    second_pre_define_by_id[value['name']] = value
                });
                loadedData['all_note_names'] = second_pre_define_by_id
            } else {
                var pre_define = []
                await this.env.services.rpc({
                    model: 'pos.session',
                    method: 'sh_load_model',
                    args: [odoo.pos_session_id, PreDefineModel],
                }).then(function (result) {
                    if (result) {
                        pre_define = result
                        indexedDB.save_data('pre.define.note', pre_define)
                    }
                });

                loadedData['pre.define.note'] = pre_define
                var pre_define_by_id = {};
                $.each(pre_define,function(index,value){
                    pre_define_by_id[value['id']] = value
                });
                loadedData['pre_defined_note_data_dict'] = pre_define_by_id
                var second_pre_define_by_id = {};
                $.each(pre_define,function(index,value){
                    second_pre_define_by_id[value['name']] = value
                });
                loadedData['all_note_names'] = second_pre_define_by_id
                localStorage.setItem(dynamic_key, 'loaded')
            }
            await super._processData(...arguments);
        }
    }
    Registries.Model.extend(PosGlobalState, shPosPreDefineModel);

});
