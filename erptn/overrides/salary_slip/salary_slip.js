frappe.ui.form.on('Salary Slip', {
	employee:function(frm) {
		var parent = 0 ;
		var cot_pro = 0 ;
		var deduct=0;
		var npc=0;
//		frm.doc.tax_salary = 0 ;
//		frm.doc.tot_deduct = 0 ;
		frappe.call({
                method: "frappe.client.get",
                args: {
                    doctype: "Employee",
                    name: frm.doc.employee,
                },
                callback(r) {
                    if(r.message) {
                        var empl = r.message;
                        frm.set_value("deduct_impot",empl.deduct_impot || 0);
                        frm.set_value("n_p_c",empl.n_p_c || 0);
			deduct=empl.deduct_impot;
			npc=empl.n_p_c || 0;
                    }}
               });
	       frm.refresh_field("deduct_impot");
	       frm.refresh_field("n_p_c");
	           // console.log(frm.doc.deductions);
	for(var i=0;i<cur_frm.doc.deductions.length;i++){
	    if (frm.doc.deductions[i].abbr == "CS" || frm.doc.deductions[i].abbr == "cnss"){

	         frm.doc.social_salary = (frm.doc.gross_pay - parseFloat(frm.doc.deductions[i].amount))*12;
	    }
	    }
	cot_pro = frm.doc.social_salary * 0.1 ;
	if ( cot_pro > 2000 ){
	cot_pro = 2000;
	}
	parent = frm.doc.social_salary * 0.05;
	if (parent < 450) {
	parent = npc * parent ;}
	else {
	parent = 450 * npc;}
	frm.doc.tot_deduct += deduct + parent + cot_pro;
        frm.doc.tax_salary =frm.doc.social_salary - frm.doc.tot_deduct;
    	}

 })
