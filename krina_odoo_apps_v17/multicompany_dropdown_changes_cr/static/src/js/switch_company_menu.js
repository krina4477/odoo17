/** @odoo-module **/
import { SwitchCompanyMenu } from "@web/webclient/switch_company_menu/switch_company_menu";
import { patch } from "@web/core/utils/patch";
import { useService } from "@web/core/utils/hooks"

patch(SwitchCompanyMenu.prototype, {

    setup() {

        super.setup(...arguments);

        this.company = useService("company");

        this.allCompanyIds = Object.values(this.company.allowedCompanies).map(
            (company) => company.id
        );

        this.isAllCompaniesSelected = this.allCompanyIds.every((elem) =>
            this.companySelector.selectedCompaniesIds.includes(elem)
        );
    },

    search_company() {
        
        let searchVal = document.querySelector('.company_search_bar2').value.toUpperCase();
        let elements = document.querySelectorAll('div.o_menu_systray > div.o-dropdown.dropdown.o-dropdown--no-caret.o_switch_company_menu.show > div > span');

        elements.forEach(function(settingView) {
            if (settingView.innerText.toUpperCase().indexOf(searchVal) > -1) {
                settingView.style.display = 'block';
            } else {
                settingView.style.display = 'none';
            }
        });

    },

    
    select_all_company() {

        if (this.isAllCompaniesSelected) {
            this.isAllCompaniesSelected = true;
            this.companySelector.selectedCompaniesIds.length = this.company.currentCompany.id
            this.company.setCompanies(this.company.currentCompany.id,false)
            
        } else {
            this.isAllCompaniesSelected = false;
            this.companySelector.selectedCompaniesIds.length = 0;
            this.companySelector.selectedCompaniesIds.push(...this.allCompanyIds);
            this.company.setCompanies(this.companySelector.selectedCompaniesIds,false);
        }
    },
});