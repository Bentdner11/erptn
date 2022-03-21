frappe.ui.form.on('Salary Slip', {
	employee:function(frm) {
	            console.log(frm.doc.deductions);
	for(var i=0;i<cur_frm.doc.deductions.length;i++){
	    if (frm.doc.deductions[i].abbr == "CS" || frm.doc.deductions[i].abbr == "cnss"){

	         frm.doc.salary_imp = frm.doc.gross_pay - parseFloat(frm.doc.deductions[i].amount);
	    }
	    if (frm.doc.salary_imp > 0){
	        frm.doc.salary_imp_year = frm.doc.salary_imp * 12;
	    }
    }
    refresh_field("salary_imp");
    refresh_field("salary_imp_year");
    }
})
