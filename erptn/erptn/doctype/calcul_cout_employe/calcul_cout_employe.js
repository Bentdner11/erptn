// Copyright (c) 2022, amf and contributors
// For license information, please see license.txt

frappe.ui.form.on('Calcul cout employe', {
	select_employee: function(frm){
		frm.set_query('select_slip', () => {
                                return {
                                        filters: {
                                                employee: frm.doc.select_employee
                                        }
                                                        };
                                        });
					},
	select_slip: function(frm) {
		frappe.call({
		method: "erptn.erptn.doctype.calcul_cout_employe.calcul_cout_employe.calcule",
		async:false,
		args: {
			emp :cur_frm.doc.select_employee,
			salary_slip: cur_frm.doc.select_slip,
		},
		callback(r) {
                    if(r.message) {
                        console.log(r.message);
			cur_frm.set_value("retenue_cnss",r.message.retenue_cnss,0);
			cur_frm.set_value("retenue_patronale",r.message.retenue_patronale,0);
			cur_frm.set_value("accident_travail",r.message.accident_travail,0);
			cur_frm.set_value("retenue_tfp",r.message.retenue_tfp,0);
			cur_frm.set_value("retenue_foprolos",r.message.retenue_foprolos,0);
			cur_frm.set_value("total_cotisation",r.message.total_cotisation,0);
                                }}
                                });
	}
});
