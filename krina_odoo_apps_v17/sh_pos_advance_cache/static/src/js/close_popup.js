odoo.define("sh_pos_advance_cache.close_popup", function(require) {
    "use strict";

    var framework = require("web.framework");
    const ClosePosPopup = require("point_of_sale.ClosePosPopup");
    const Registries = require("point_of_sale.Registries");
    const {identifyError} = require("point_of_sale.utils");
    const {ConnectionLostError,ConnectionAbortedError} = require("@web/core/network/rpc_service");
    const {useState} = owl;
    var indexedDB = window.indexedDB || window.mozIndexedDB || window.webkitIndexedDB || window.msIndexedDB || window.shimIndexedDB;
    if (!indexedDB) {
        window.alert("Your browser doesn't support a stable version of IndexedDB.")
    }

    const SHClosePosPopup = (ClosePosPopup) =>
        class extends ClosePosPopup {
            close_session_delete_cache() {
                const deleteRequest = indexedDB.deleteDatabase(odoo.pos_session_id);
                deleteRequest.onsuccess = function() {
                    var session_id = odoo.pos_session_id
                    localStorage.removeItem(`${session_id}_${'product.product'}`);
                    localStorage.removeItem(`${session_id}_${'res.partner'}`);
                    localStorage.removeItem(`${session_id}_${'product.template.attribute.value'}`);
                    localStorage.removeItem(`${session_id}_${'product.template.attribute.line'}`);
                    localStorage.removeItem(`${session_id}_${'res.country'}`);
                    localStorage.removeItem(`${session_id}_${'res.country.state'}`);
                    localStorage.removeItem(`${session_id}_${'pre.define.note'}`);
                    localStorage.removeItem(`${session_id}_${'uom.uom'}`);
                    console.log("Database deleted successfully");
                };
                deleteRequest.onerror = function(event) {
                    console.error("Error deleting database:", event.target.errorCode);
                };
            }
            closePos() {
                this.close_session_delete_cache()
                super.closePos();
            }
            async closeSession() {
                this.close_session_delete_cache()
                await super.closeSession();
            }
        };
    Registries.Component.extend(ClosePosPopup, SHClosePosPopup);
});