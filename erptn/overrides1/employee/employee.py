from erpnext.hr.doctype.employee.employee import Employee



import frappe
from frappe import _

class CustomEmployee(Employee):
	def validate(self):
		super(CustomEmployee,self).validate()
		self.get_value()
	def get_value(self):
		enfant,parent,banque,poste,obligatoire= frappe.db.get_value('taxes et cotisation',self.taxes_et_cotisations,['max_enfants','max_parents','max_banque','max_poste','max_obligatoire'])
		if (self.n_e_c+self.n_e_h+self.n_e_b > enfant):
			frappe.throw(_("Veilllez resaisir les bons nombres des enfants"))
		if (self.n_p_c > parent):
			frappe.throw(_("Veuillez resaisir le bon nombre des parents pris en charge"))
		if (self.epargne_banque>banque):
			self.consideration_b=banque
		else:
			self.consideration_b=self.epargne_banque
		if (self.epargne_poste>poste):
			self.consideration_p=poste
		else:
			self.consideration_p=self.epargne_poste
		if (self.interetobligatoir>obligatoire):
			self.interet_emprunt_obligatoire_considearation=obligatoire
		else:
			self.interet_emprunt_obligatoire_considearation=self.interetobligatoir
		regime=frappe.db.get_value('Type de contrat',self.contract_type,['select_cnss'])
		self.regime_cnss=regime


