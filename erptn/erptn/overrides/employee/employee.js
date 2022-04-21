frappe.ui.form.on('Employee', {
    setup: function(frm){
		add_fetch("company", "working_months_in_the_company", "working_months");
	},
    validate: function(frm){
        var regex = /[^0-9]/g;
	var sum = 0;
	var chef = 0;
	frm.doc.deduct_impot = 0;
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
	if (frm.doc.n_e_c && frm.doc.n_e_c > 4){
                msgprint(__("le nombre des enfants pris-en charge doit etre au plus 4"));
                validated = false;
                return false;
        }
	if (frm.doc.n_e_h && frm.doc.n_e_h > 4){
                msgprint(__("le nombre des enfants infirmes pris-en charge doit etre au plus 4 "));
                validated = false;
                return false;
        }
	if (frm.doc.n_e_b && frm.doc.n_e_b > 4){
                msgprint(__("le nombre des enfants boursiers pris-en charge doit etre au plus 4 "));
                validated = false;
                return false;
        }
	if (frm.doc.n_p_c && frm.doc.n_p_c > 2){
                msgprint(__("le nombre des parents pris-en charge doit etre au plus 2"));
                validated = false;
                return false;
	}
	sum = sum + frm.doc.n_e_b + frm.doc.n_e_h + frm.doc.n_e_c ;
	if ( sum > 4 ) {
		msgprint(__("veuillez resaire les donnees des enfants vous depassez les chiffres acceptable "));
		validated = false;
        	 return false;
   	}
	if ( frm.doc.epargne_banque > 3000 ){
		frm.doc.epargne_banque=3000;
	}
	if ( frm.doc.epargne_poste > 3000 ){
		frm.doc.epargne_poste=3000;
	}
	if ( frm.doc.Emprunt_obligatoire > 5000) {
		frm.doc.Emprunt_obligatoire = 5000;
	}
	if (frm.doc.c_d_f =="Oui"){
		chef=300;}
	frm.doc.deduct_impot = frm.doc.deduct_impot + frm.doc.epargne_banque + frm.doc.epargne_poste + frm.doc.Emprunt_obligatoire + frm.doc.n_e_c * 100 + frm.doc.n_e_b * 1000 + frm.doc.n_e_h * 2000 + chef + frm.doc.autre + frm.doc.habitation;

    }
});
