/** @odoo-module **/
import { ListRenderer } from "@web/views/list/list_renderer";
import { patch } from "@web/core/utils/patch";

patch(ListRenderer.prototype, {
    setup() {
        super.setup(...arguments);
    },

    onCellKeydownEditMode(hotkey, cell, group, record) {
        const row = cell.parentElement;
        const { list } = this.props;
        const recordIndex = list.records.indexOf(record);
        const rowCount = list.records.length;

        switch (hotkey) {
            case "arrowup": {
                if (recordIndex === 0) {
                    const lastRowIndex = rowCount - 1;
                    row.parentElement.children[lastRowIndex].cells[cell.cellIndex].click();
                } else {
                    const preRow = row.previousElementSibling;
                    preRow && preRow.cells[cell.cellIndex].click();
                }
                break;
            }

            case "arrowdown": {
                if (recordIndex === rowCount - 1) {
                    row.parentElement.children[0].cells[cell.cellIndex].click();
                } else {
                    const nextRow = row.nextElementSibling;
                    nextRow && nextRow.cells[cell.cellIndex].click();
                }
                break;
            }
        }

        return super.onCellKeydownEditMode(...arguments);
    }
});
