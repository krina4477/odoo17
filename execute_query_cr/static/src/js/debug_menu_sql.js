import { _t } from "@web/core/l10n/translation";
import { registry } from "@web/core/registry";
import { QueryExecuteDialog } from "./query_execute_dialog"

function executeQuery({ env }) {

    return {
        type: "item",
        description: _t("Execute Query"),
        callback: () => {

            env.services.dialog.add(QueryExecuteDialog, {
                title: _t("Execute Query"),
                multiSelect: false,
                cancel: () => resolve.bind(null, false),
            },
            );
        },
        sequence: 541,
    };
}

registry
    .category("debug")
    .category("default").add("executeQuery", executeQuery);
