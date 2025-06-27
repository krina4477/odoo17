/** @odoo-module **/
//  Part of Odoo Module Developed by Candidroot Solutions Pvt. Ltd.
//  See LICENSE file for full copyright and licensing details.

import { KanbanRenderer } from "@web/views/kanban/kanban_renderer";
import { KanbanController } from "@web/views/kanban/kanban_controller";
import { kanbanView } from "@web/views/kanban/kanban_view";
import { registry } from '@web/core/registry';
import { useService } from "@web/core/utils/hooks";
import { ExportDataDialog } from "@web/views/view_dialogs/export_data_dialog";
import { deleteConfirmationMessage,ConfirmationDialog } from "@web/core/confirmation_dialog/confirmation_dialog";
import { ActionMenus } from "@web/search/action_menus/action_menus";
import { Layout } from "@web/search/layout";
import { KanbanCheckboxRenderer } from "./kanban_renderer";
import { unique } from "@web/core/utils/arrays";
import { patch } from "@web/core/utils/patch";
import { session } from "@web/session";
import { sprintf } from "@web/core/utils/strings";
import { _t } from "@web/core/l10n/translation";
import { useSetupView } from "@web/views/view_hook";
import { download } from "@web/core/network/download";
import { STATIC_ACTIONS_GROUP_NUMBER } from "@web/search/action_menus/action_menus";
import { omit } from "@web/core/utils/objects";
import { browser } from "@web/core/browser/browser";

patch(KanbanController.prototype,{
    setup() {
        super.setup();
        this.dialogService = useService("dialog");
        this.userService = useService("user");
        this.rpc = useService("rpc");
        this.notificationService = useService("notification");
        this.activeActions = this.props.archInfo.activeActions;
        this.fields = this.props.fields;
        this.archiveEnabled ="active" in this.props.fields
                ? !this.props.fields.active.readonly
                : "x_active" in this.props.fields
                ? !this.props.fields.x_active.readonly
                : false;
        this.optionalActiveFields = [];

    },
    onOptionalFieldsChanged(optionalActiveFields) {
        this.optionalActiveFields = optionalActiveFields;
        },

    nbTotal() {
        return unique(this.props.fields);
    },

    async getExportedFields(model, import_compat, parentParams) {
        return await this.rpc("/web/export/get_fields", {
            ...parentParams,
            model,
            import_compat,
        });
    },

    async onExportData() {
        const dialogProps = {
            context: this.props.context,
            defaultExportList: [this.nbTotal],
            download: this.downloadExport.bind(this),
            getExportedFields: this.getExportedFields.bind(this),
            root: this.model.root,
        };
        this.dialogService.add(ExportDataDialog, dialogProps);
    },

    async downloadExport(fields, import_compat, format) {
        var isDomainSelected = this.model.root.isDomainSelected;
        let ids = false;
        if (!this.isDomainSelected) {
            const resIds = this.model.root.records.map((datapoint) => datapoint.resId);
            ids = resIds.length > 0 && resIds;
        }
        const exportedFields = fields.map((field) => ({
            name: field.name || field.id,
            label: field.label || field.string,
            store: field.store,
            type: field.field_type || field.type,
        }));
        if (import_compat) {
            exportedFields.unshift({ name: "id", label: this.env._t("External ID") });
        }
        download({
            data: {
                data: JSON.stringify({
                    import_compat,
                    context: this.props.context,
                    domain: this.model.root.domain,
                    fields: exportedFields,
                    groupby: this.model.root.groupBy,
                    ids,
                    model: this.model.root.resModel,
                }),
            },
            url: `/web/export/${format}`,
        });
    },

    get className() {
        var checked = $('input[type=checkbox]:checked');
        const root = this.model.root;
        let body = deleteConfirmationMessage;
        const total = root.count;
        const list = this.model.root;
        var inputselected = Object.values(checked);
        var iter = 0;
        var recIds = [];
        var loopstop = inputselected.length - 2;
        if (checked.length > 0) {
            inputselected.forEach((select) => {
                if(iter < loopstop ){
                    list.records.forEach((record) => {
                        if(select.id == record.id){
                            recIds.push(record.resId);
                        }
                    });
                    iter += 1;
                }
            });
        }
        if (root.isDomainSelected || root.selection.length > 1) {
            body = _t("Are you sure you want to delete these records?");
        }
        return {
            title: _t("Bye-bye, record!"),
            body,
            confirmLabel: _t("Delete"),
            recIds: recIds,
            confirm: () => {
                const total = root.count;
                const list = this.model.root;
                var inputselected = Object.values(checked);
                var iter = 0;
                var recIds = [];
                var loopstop = inputselected.length - 2;
                if (checked.length > 0) {
                    inputselected.forEach((select) => {
                        if(iter < loopstop ){
                            list.records.forEach((record) => {
                                if(select.id == record.id){
                                    recIds.push(record.resId);
                                }
                            });
                            iter += 1;
                        }
                    });
                }
                const resIds =  this.model.orm.unlink(this.props.resModel, recIds, { context: this.props.context,});
            },
            cancel: () => {},
            cancelLabel: _t("No, keep it"),
        };
    },

    async onDeleteSelectedRecords() {
        var ConfirmationDialogBody = this.className
        var recIds = ConfirmationDialogBody['recIds']
        delete ConfirmationDialogBody['recIds']
        this.dialogService.add(ConfirmationDialog, ConfirmationDialogBody);
        return recIds
    },
    // async webSearchRead(){

    // }

    async toggleArchiveState(archive) {
        if (archive) {
            const checked = $('input[type=checkbox]:checked');
            const list = this.model.root;
            var promise = [];
            var inputselected = Object.values(checked);
            var iter = 0;
            var loopstop = inputselected.length - 2;
            if (checked.length > 0) {
                inputselected.forEach((select) => {
                    if(iter < loopstop ){
                        list.records.forEach((record) => {
                            if(select.id == record.id){
                                promise.push(record.archive(true));
                            }
                        });
                        iter += 1;
                    }
                }) 
            }
            return promise
        }
        const checked = $('input[type=checkbox]:checked');
        const list = this.model.root;
        var promise = [];
        var inputselected = Object.values(checked);
        var iter = 0;
        var loopstop = inputselected.length - 2;
        if (checked.length > 0) {
            inputselected.forEach((select) => {
                if(iter < loopstop ){
                    list.records.forEach((record) => {
                        if(select.id == record.id){
                            promise.push(record.unarchive(true));
                        }
                    });
                    iter += 1;
                }
            });
            
        }   
        return promise
    },
    get actionMenuItems() {
        const { actionMenus } = this.props.info;
        const staticActionItems = Object.entries(this.getStaticActionMenuItems())
            .filter(([key, item]) => item.isAvailable === undefined || item.isAvailable())
            .sort(([k1, item1], [k2, item2]) => (item1.sequence || 0) - (item2.sequence || 0))
            .map(([key, item]) =>
                Object.assign(
                    { key, groupNumber: STATIC_ACTIONS_GROUP_NUMBER },
                    omit(item, "isAvailable")
                )
            );

        return {
            action: [...staticActionItems, ...(actionMenus.action || [])],
            print: actionMenus.print,
        };
    },
    activeActions() {
        return this.props.activeActions || {};
    },
    async duplicateRecords() {
        const checked = $('input[type=checkbox]:checked');
        const list = this.model.root; 
        var promise;
        var inputselected = Object.values(checked);
        var iter = 0;
        var records = [];
        var loopstop = inputselected.length - 2;
        if (checked.length > 0) {
            inputselected.forEach((select) => {
                if(iter < loopstop ){
                    list.records.forEach((record) => {
                        if(select.id == record.id){
                            records.push(record)
                            this.model.orm.call(this.props.resModel, "copy", [record.resId], { context: this.props.context,}); 
                        }
                    });
                    iter += 1;
                }
            })  
            
        } 
        return records

    },
    getStaticActionMenuItems() {
        const list = this.model.root;
        const isM2MGrouped = list.groupBy.some((groupBy) => {
            const fieldName = groupBy.split(":")[0];
            return list.fields[fieldName].type === "many2many";
        });
        return {
            export: {
                isAvailable: () => this.isExportEnable,
                sequence: 10,
                icon: "fa fa-upload",
                description: _t("Export"),
                callback: () => this.onExportData(),
            },
            archive: {
                isAvailable: () => this.archiveEnabled && !isM2MGrouped,
                sequence: 20,
                icon: "oi oi-archive",
                description: _t("Archive"),
                callback: () => {
                    this.dialogService.add(ConfirmationDialog, {
                        body: _t("Are you sure that you want to archive all the selected records?"),
                        confirmLabel: _t("Archive"),
                        confirm: () => {
                            this.toggleArchiveState(true).then(function (records) {
                                var requiredSeconds = (records.length * 1000 ) / 10;
                                browser.setTimeout(function() {
                                        browser.location.reload();
                                }, requiredSeconds);
                            });
                        },
                        cancel: () => {},
                    });
                },
            },
            unarchive: {
                isAvailable: () => this.archiveEnabled && !isM2MGrouped,
                sequence: 30,
                icon: "oi oi-unarchive",
                description: _t("Unarchive"),
                callback: () => this.toggleArchiveState(false).then(function (records) {
                    var requiredSeconds = (records.length * 1000 ) / 10;
                    browser.setTimeout(function() {
                        browser.location.reload();
                    }, requiredSeconds);
                }),
            },
            duplicate: {
                isAvailable: () => this.activeActions.duplicate && !isM2MGrouped,
                sequence: 35,
                icon: "fa fa-clone",
                description: _t("Duplicate"),
                callback: () => this.duplicateRecords().then(function (records) {
                    var requiredSeconds = (records.length * 1000 ) / 10;
                    browser.setTimeout(function() {
                        browser.location.reload();
                    }, requiredSeconds);
                    }),
            },
            delete: {
                isAvailable: () => this.activeActions.delete && !isM2MGrouped,
                sequence: 40,
                icon: "fa fa-trash-o",
                description: _t("Delete"),
                callback: () => this.onDeleteSelectedRecords().then(function (records) {
                    var requiredSeconds = (records.length * 1000 ) / 2;
                    browser.setTimeout(function() {
                        browser.location.reload();
                    }, requiredSeconds);
                    }),
            },
        };
    },

    SelectRecord() {
        $('input.o_kanban_selector').prop('checked', true);
        var $inputs = $('input.o_kanban_selector');
        var allChecked = $inputs.length > 0;
        this.model.root.records.forEach((record) => {
            record.toggleSelection(true);
             $('.o_kanban_all_unselector').removeClass('d-none');
             $('.o_kanban_all_selector').addClass('d-none');
        });
    },

    UnSelectRecord() {
        $('input.o_kanban_selector').prop('checked', false);
        var $inputs = $('input.o_kanban_selector');
        var activeIds = this.model.root.records;
        this.model.root.records.forEach((record) => {
            record.toggleSelection(false);
            $('.o_kanban_all_selector').removeClass('d-none');
            $('.o_kanban_all_unselector').addClass('d-none');
        });
    },

});

patch(KanbanController,{ components: { ...KanbanController.components, ActionMenus,}});
