from erpnext.payroll.doctype.salary_slip.salary_slip import SalarySlip

import frappe
from frappe.utils import (
	add_days,
	cint,
	cstr,
	date_diff,
	flt,
	formatdate,
	get_first_day,
	getdate,
	money_in_words,
	rounded,
)
from erpnext.utilities.transaction_base import TransactionBase
from frappe.model.document import Document
class CustomSalarySlip(SalarySlip):
#	def __init__(self, *args, **kwargs):
#		super().__init__(*args, **kwargs)

	def calculate_net_pay(self):
		super(CustomSalarySlip,self).calculate_net_pay()
		cnss,cot_pro,parent,pour_parent,plaf_parent,plaf_pro=frappe.db.get_value('taxes et cotisation',self.taxes_et_cotisations,['pourc_cnss','pourc_pro','max_parents','pourcent_parent','plafond_parent','plafond_pro'])
		cot_cnss=self.gross_pay*cnss*0.01
		self.social_salary=(self.gross_pay - cot_cnss)*12	#salaire annuel social
		parents=frappe.db.get_value('Employee',self.employee,['n_p_c'])




		frais_cot_pro=self.social_salary*cot_pro*0.01	#calcul frais cotisation pro a partir du salaire annuel social
		if (frais_cot_pro>plaf_pro):
			frais_cot_pro=plaf_pro


		frais_parent=self.social_salary*pour_parent*0.01	#calcul frais parent a partir du salaire annuel social
		if (frais_parent>plaf_parent):
			frais_parent=plaf_parent
		total_parent=parents*frais_parent
		print("frais des parents "+str(total_parent))



		deduction=0
		deduction +=frais_cot_pro+total_parent 		#la deduction contient seulement la deduction des frais pro et celle des parents pris en charge
		print("deduction pro"+str(deduction))
		print(cot_pro)


		deduction_chef,enfant1,enfant2,enfant3,enfant4,infirme,nonbour=frappe.db.get_value('taxes et cotisation',self.taxes_et_cotisations,['deduct_chef','deduct_enfant1','deduct_enfant2','deduct_enfant3','deduct_enfant4','deduct_infirm','deduct_non_bour'])
		chef,nb_enfant,nb_infirme,nb_nonbour=frappe.db.get_value('Employee',self.employee,['c_d_f','n_e_c','n_e_h','n_e_b'])
		total_deduct_chef=0
		deduct_enfant=0
		if (chef=="Oui"):
			if (nb_enfant==4):
				deduct_enfant += enfant1 + enfant2 + enfant3 + float(enfant4)
			if (nb_enfant==3):
				deduct_enfant += enfant1 + enfant2 + enfant3
			if (nb_enfant==2):
				deduct_enfant += enfant1 + enfant2
			if (nb_enfant==1):
				deduct_enfant += enfant1
			total_deduct_chef += deduction_chef + deduct_enfant + nb_infirme*infirme + nb_nonbour*nonbour		#consideration du cas chef famille ou non + calculs necessaire
		else :
			total_deduct_chef = 0
		deduction += total_deduct_chef




		bank,post,obliga,habit,aut=frappe.db.get_value('Employee',self.employee,['interet_compte_epargne_banque_consideration','interet_compte_epargne_poste_consideration','interet_emprunt_obligatoire_considearation','habitation','autre'])
		deduction += float(bank) + float(post) +float(obliga) + aut + habit		#la suite des autres deduction
		print("les deduction"+str(deduction))
		self.les_deductions=deduction



		self.tax_salary =self.social_salary - deduction				#salaire annuel imposable


		css=frappe.db.get_value('taxes et cotisation',self.taxes_et_cotisations,['pourc_css'])
		deduct_css=self.tax_salary*css*0.01/12				#calcul css
		print("css:"+str(deduct_css))




#		we need to fix code bellow taken snippets from payroll
		#tax_slab = frappe.db.get_value("Salary Structure Assignment",
		#	{"employee": self.employee, "salary_structure": self.salary_structure, "docstatus": 1}, ["income_tax_slab"]) # this is importing income tax slab from the proper doctype
		tax_slab = self.get_custom_tax()
		tax = 0
#		print(tax_slab.slabs)
		irpp_tax=self.custom_calculate_tax_by_tax_slab(self.tax_salary,tax_slab)
		print(irpp_tax)
		irpp=irpp_tax/12
#		for slab in tax_slab.slabs:                             #calcul irpp en utilisant le salaire imposable en utilsant le tableau de irpp
#			while (self.tax_salary >=0):
#				if (self.tax_salary > slab.from_amount and self.tax_salary < slab.to_amount):
#					tax += self.tax_salary * slab.percent_deduction*0.01
#				if (self.tax_salary>slab.to_amount):
#					tax +=(slab.to_amount - slab.from_amount)* slab.percent_deduction*0.01
#					self.tax_salary=self.tax_salary - slab.to_amount
#		irpp=tax/12
# calcul de net pay
		self.net_pay=(self.social_salary/12)-irpp-deduct_css
		self.valeur_irpp=irpp
		self.valeur_css=deduct_css
		self.cotisation_sociale=cot_cnss
	def get_custom_tax(self):
		income_tax_slab, ss_assignment_name = frappe.db.get_value("Salary Structure Assignment",
			{"employee": self.employee, "salary_structure": self.salary_structure, "docstatus": 1}, ["income_tax_slab", 'name'])

		if not income_tax_slab:
			frappe.throw(_("Income Tax Slab not set in Salary Structure Assignment: {0}").format(ss_assignment_name))

		income_tax_slab_doc = frappe.get_doc("Income Tax Slab", income_tax_slab)
		if income_tax_slab_doc.disabled:
			frappe.throw(_("Income Tax Slab: {0} is disabled").format(income_tax_slab))

#		if getdate(income_tax_slab_doc.effective_from) > getdate(payroll_period.start_date):
#			frappe.throw(_("Income Tax Slab must be effective on or before Payroll Period Start Date: {0}")
#				.format(payroll_period.start_date))

		return income_tax_slab_doc


	def custom_calculate_tax_by_tax_slab(self, annual_taxable_earning, tax_slab):
		data = self.get_data_for_eval()
		data={}
		data.update({"annual_taxable_earning": annual_taxable_earning})
		tax_amount = 0
		print("tax_salary:"+str(annual_taxable_earning))
		for slab in tax_slab.slabs:
#			cond = cstr(slab.condition).strip()
#			if cond and not self.eval_tax_slab_condition(cond, data):
#				continue
			if not slab.to_amount and annual_taxable_earning >= slab.from_amount:
				tax_amount += (annual_taxable_earning - slab.from_amount + 1) * slab.percent_deduction *.01
				continue
			if annual_taxable_earning >= slab.from_amount and annual_taxable_earning < slab.to_amount:
				tax_amount += (annual_taxable_earning - slab.from_amount + 1) * slab.percent_deduction *.01
			elif annual_taxable_earning >= slab.from_amount and annual_taxable_earning >= slab.to_amount:
				tax_amount += (slab.to_amount - slab.from_amount + 1) * slab.percent_deduction * .01
			print("tax_amount:"+str(tax_amount))


		return tax_amount





































#	@frappe.whitelist()
#	def get_emp_and_working_day_details(self):
#		a= super(CustomSalarySlip,self).get_emp_and_working_day_details()
#		cnss=self.get_cnss()
#		self.social_salary = (self.gross_pay - cnss)*12
#		print(self.social_salary)
		#a= super(CustomSalarySlip,self).get_emp_and_working_day_details()
#		print("hello from override"*12)
#		return a
#	def get_cnss(self):
#		pass
#		self.salary_imp =self.gross_pay -
#		cnss=0
#		for d in self.deductions:
#			print(d.amount)
#			if d.salary_component == "cotisation sociale":
#				cnss = flt(d.amount)
#		return cnss

#	def get_employee_field(self,emp_name):
#		dicz= frappe.get_all("Employee",fields=["gender"],filters={"name": emp_name},order_by= "idx")[0]
#		return list
# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt
