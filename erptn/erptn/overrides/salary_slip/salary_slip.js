frappe.ui.form.on('Salary Slip', {
	rounding_type : function(frm){
		frm.refresh_field("rounded_total");}
	table_primes_excep : function(frm){
		frm.refresh_field("valeur_de_prime");}








































})

/*	employee:function(frm) {
		frm.doc.tax_salary = 0 ;
		frm.doc.tot_deduct = 0 ;
		frappe.call({
                method: "frappe.client.get",
		async:false,
                args: {
                    doctype: "Employee",
                    name: frm.doc.employee,
                },
                callback(r) {
                    if(r.message) {
                        var empl = r.message;
                        frm.set_value("deduct_impot",empl.deduct_impot);
                        frm.set_value("n_p_c",empl.n_p_c);
			deduct=empl.deduct_impot;
			console.log("la dedcution est "+deduct);
			npc=empl.n_p_c ;
                    }}
               });
	       frm.refresh_field("deduct_impot");
	       frm.refresh_field("n_p_c");
	           console.log(frm.doc.deductions);
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
	console.log("la deduction totale est"+frm.doc.total_deduct);
	console.log("la dedcution est "+deduct);
        frm.doc.tax_salary =frm.doc.social_salary - frm.doc.tot_deduct;
	css = frm.doc.tax_salary*0.01/12;
	console.log("le css ="+css);
	if (frm.doc.tax_salary<5000){
		tax=0;
	}
	else if (frm.doc.tax_salary>5000 && frm.doc.tax_salary<20000){
		tax=(frm.doc.tax_salary-5000)*0.26;
		//console.log(tax);
	}
	else if (frm.doc.tax_salary>20000 && frm.doc.tax_salary<30000){
		tax=(frm.doc.tax_salary-20000)*0.28+3900;
	}
	else if (frm.doc.tax_salary>30000 && frm.doc.tax_salary<50000){
		tax=(frm.doc.tax_salary-30000)*0.32+3900+2800;
	}
	else {(tax=frm.doc.tax_salar-50000)*0.35+3900+2800+6400;}
	irpp=tax/12;
	console.log("irpp"+irpp);
	frm.doc.net_salary=((frm.doc.social_salary/12)-irpp-css);

    	}
*/
