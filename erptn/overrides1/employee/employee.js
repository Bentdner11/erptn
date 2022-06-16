/*frappe.ui.form.on('Employee', {
    validate: function(frm){
        var regex = /[^0-9]/g;
	var sum = 0;
	var chef = 0;
	frm.doc.deduction_impot = 0;
        if (frm.doc.cnss_id && regex.test(frm.doc.cnss_id) === true){
                msgprint(__("CNSS Identifier: Only numbers are allowed."));
                validated = false;
		return false;
        }
	if (frm.doc.cin && regex.test(frm.doc.cin) === true){
                msgprint(__("National ID: Only numbers are allowed."));
                validated = false;
		return false;
        }
	if (frm.doc.cin && frm.doc.cin.length != 8){
		msgprint(__("National ID: National ID must contain 8 numbers."));
                validated = false;
                return false;
	}
	if (frm.doc.cnss_id && frm.doc.cnss_id.length != 10){
              	msgprint(__("CNSS Identifier: CNSS Identifier must contain 10 numbers."));
                validated = false;
                return false;
        }
	if (frm.doc.n_e_c && frm.doc.n_e_c > frm.doc.max_enfants){
                msgprint(__(" Veuillez resaisir le nombre des enfants pris-en charge"));
                validated = false;
                return false;
        }
});
/*
	if (frm.doc.n_e_h && frm.doc.n_e_h > frm.doc.max_enfants){
                msgprint(__("Veuillez resaisir le nombre des enfants infirmes pris-en charge"));
                validated = false;
                return false;
        }
	if (frm.doc.n_e_b && frm.doc.n_e_b > frm.doc.max_enfants){
                msgprint(__("Veuillez resaisir le nombre des enfants boursiers pris-en charge "));
                validated = false;
                return false;
        }
	if (frm.doc.n_p_c && frm.doc.n_p_c > max_parents){
                msgprint(__("Veillez resaisir le nombre des parents pris-en charge "));
                validated = false;
                return false;
	}
	sum = sum + frm.doc.n_e_b + frm.doc.n_e_h + frm.doc.n_e_c ;
	if ( sum > frm.doc.max_enfants) {
		msgprint(__("veuillez resaire les donnees des enfants vous depassez les chiffres acceptable "));
		validated = false;
        	 return false;
   	}
	if ( frm.doc.epargne_banque > frm.doc.max_banque ){
		frm.doc.epargne_banque=frm.doc.max_banque;
	}
	if ( frm.doc.epargne_poste >frm.doc.max_poste){
		frm.doc.epargne_poste=frm.doc.max_poste;
	}
	if ( frm.doc.Emprunt_obligatoire > frm.doc.max_obligatoire) {
		frm.doc.Emprunt_obligatoire = frm.doc.max_obligatoire;
	}
	if (frm.doc.c_d_f =="Oui"){
		chef=frm.doc.deduct_chef;}
	if (frm.doc.c_d_f == "Non"){
		        frm.doc.deduction_impot = frm.doc.deduction_impot + frm.doc.epargne_banque + frm.doc.epargne_poste + frm.doc.Emprunt_obligatoire + frm.doc.n_e_c * 0 + frm.doc.n_e_b * 0 + frm.doc.n_e_h * 0 + chef + frm.doc.autre + frm.doc.habitation;

	}
	if (frm.doc.c_d_f =="Oui"){
			frm.doc.deduction_impot = frm.doc.deduction_impot + frm.doc.epargne_banque + frm.doc.epargne_poste + frm.doc.Emprunt_obligatoire + frm.doc.n_e_c * frm.doc.deduct_enfant + frm.doc.n_e_b * frm.doc.deduct_non_bour + frm.doc.n_e_h * frm.doc.deduct_infirm + chef + frm.doc.autre + frm.doc.habitation;
}
    }
});
*/
