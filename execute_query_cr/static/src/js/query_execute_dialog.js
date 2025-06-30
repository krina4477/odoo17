import { _t } from "@web/core/l10n/translation";
import { registry } from "@web/core/registry";
import { Dialog } from "@web/core/dialog/dialog";
import { rpc } from "@web/core/network/rpc";
import { Component, useState, markRaw, useRef } from "@odoo/owl";


export class QueryExecuteDialog extends Component {
    static template = "execute_query_cr.DebugMenu.ExecuteQuery";

    static components = { Dialog };

    setup(){
        this.errorInfo = useState({info : ""})
        let records = markRaw({ header: "" , rows:""});
        this.successInfo = useState({info : "", records:records})
        let code = markRaw({ value: "" });
        this.state = useState({code : code, offset:0, totalPage : 0})
        this.rootRef = useRef("rootRef");
    }

    offsetNext(){
        this.state.offset = parseInt(this.state.offset) + 1;
        const offset_input = this.rootRef.el.querySelector("#offset_input")
        offset_input.value = this.state.offset + 1
        this.createTable();
    }

    offsetPrevious(){
        this.state.offset = parseInt(this.state.offset) - 1;
        const offset_input = this.rootRef.el.querySelector("#offset_input");
        offset_input.value = this.state.offset + 1;
        this.createTable();
    }

    setOffset(e){
        if(e.key == 'Enter' && Number(e.target.value) > 0 && Number(e.target.value) <= this.state.totalPage){
            this.state.offset = e.target.value - 1;
            this.createTable();
        }
    }


    createTable(){

            let header = this.successInfo.records.header;
            let rows = this.successInfo.records.rows;
            if(header && rows){

                const container = this.rootRef.el.querySelector("#table-container");

                const table = document.createElement("table");
                table.classList.add("table", "table-striped", "table-bordered", "table-hover", "table-responsive"); 

                const thead = document.createElement("thead");
                const headerRow = document.createElement("tr");
                
                header.forEach(colName => {
                const th = document.createElement("th");
                th.textContent = colName;
                headerRow.appendChild(th);
                });
                thead.appendChild(headerRow);
                table.appendChild(thead);

                const tbody = document.createElement("tbody");

                for(let i = this.state.offset * 20; i < (20 + (this.state.offset * 20)); i++){
                    const tr = document.createElement("tr");
                    if(rows.length - 1 < i){
                        break
                    }
                    rows[i].forEach(cellData => {
                        const td = document.createElement("td");
                        td.textContent = cellData;
                        tr.appendChild(td);
                    });
                    tbody.appendChild(tr);
                }


                table.appendChild(tbody);

                const tfoot = document.createElement("tfoot");
                const footerRow = document.createElement("tr");
                const footerCell = document.createElement("td");
                footerCell.colSpan = header.length;
                footerCell.style.paddingLeft = 0;
                footerCell.textContent = `Total rows: ${rows.length}`;
                footerRow.appendChild(footerCell);
                tfoot.appendChild(footerRow);
                table.appendChild(tfoot);

                if(container){
                    container.innerHTML = ""
                    container.appendChild(table);
                }
            }
    }

    async executeQuery(){

        this.rootRef.el.querySelector('.dialog').classList.add("d-none")
        this.rootRef.el.querySelector('.loading').classList.remove("d-none")
        let result = await rpc("/execute_query", { 
            code: this.state.code.value ,
        });
    
        const container = this.rootRef.el.querySelector("#table-container");
        if(container){
            container.innerHTML = ""
        }
        this.successInfo.info = ""
        this.errorInfo.info = ""
        this.successInfo.records.rows = ""
        this.successInfo.records.header = ""
        this.state.totalPage = 0

        if (result.error){
            this.errorInfo.info = `Error while executing SQL code: ${result.error.toString()}`;
        }else if(result.success_returnred){
            this.state.offset = 0
            this.successInfo.records.header = Object.keys(result.success_returnred[0]);
            this.successInfo.records.rows = result.success_returnred.map(obj => Object.values(obj))
            this.state.totalPage = Math.ceil(this.successInfo.records.rows.length / 20)
            this.createTable()
        }else if(result.success_affected){
            this.successInfo.info = `Rows affected by query: ${result.success_affected.toString()}`;
        }else if(result.message){
            this.successInfo.info = `Message: ${result.message}`;
        } 
        this.rootRef.el.querySelector('.dialog').classList.remove("d-none")
        this.rootRef.el.querySelector('.loading').classList.add("d-none")
        
        
    
    }
}

registry.category("dialogs").add("QueryExecuteDialog", QueryExecuteDialog);