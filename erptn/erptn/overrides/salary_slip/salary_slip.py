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

	#if (self.prime_exp):
	#	self.gross_pay+=self.valeur_de_prime
#importation de nombre de jours travaillee (regime 26 et 22 jours sinon calcul normal de erpnext)
	#regime_jour=frappe.db.get_value('Company',self.company,['default_holiday_list'])
	#if (regime_jour=='Régime 22 jours'):
	#	self.total_working_days=22
	#if (regime_jour=='Régime 26 Jours'):
	#	self.total_working_days=26


	def calculate_net_pay(self):
		super(CustomSalarySlip,self).calculate_net_pay()
		if (self.prime_exp):
			self.gross_pay+=self.valeur_de_prime
#importation de nombre de jours travaillee (regime 26 et 22 jours sinon calcul normal de erpnext)
		regime_jour=frappe.db.get_value('Company',self.company,['default_holiday_list'])
		if (regime_jour=='Régime 22 jours'):
			self.total_working_days=22
		if (regime_jour=='Régime 26 Jours'):
			self.total_working_days=26

 #import de type de contrat et la situation du contrat ( impos et cotis )
		contrat=frappe.db.get_value('Employee',self.employee,['contract_type'])
		print("ici cest le contrat"+str(contrat))
		state_cotis, state_impos = frappe.db.get_value('Type de contrat',contrat,['cotisable','imposable'])
		print("ici si cest cotisable"+str(state_cotis))
		print("ici si cest imposable"+str(state_impos))

#calcul cnss si le contrat et cotisable et import de sa valeur
		if (state_cotis):
			type_cnss=frappe.db.get_value('Type de contrat',contrat,['select_cnss'])
			cnss=frappe.db.get_value('Regime CNSS',type_cnss,['cnss_employe'])
		else:
			cnss=0
			type_cnss="non cotisable"
		print("valeur de taux cnss "+str(cnss))
		print("type de cnss"+str(type_cnss))

#traitement de cas ou le salaire du regime dignité dépasse le plafond
		if (type_cnss=="Régime dignité"):
			salaire_plafond=frappe.db.get_value('Regime CNSS',type_cnss,['plaf'])
			print("le plafond"+str(salaire_plafond))
			if (self.gross_pay>salaire_plafond):
				self.gross_pay=self.gross_pay-salaire_plafond
				print("le salaire condideree si on depeasse le plafond"+str(self.gross_pay))
				contrat="Permanent"
				type_cnss=frappe.db.get_value('Type de contrat',contrat,['select_cnss'])
				cnss=frappe.db.get_value('Regime CNSS',type_cnss,['cnss_employe'])
				state_impos=1
				state_cotis=1





#import de nombre de mois travaileees

		cot_pro,parent,pour_parent,plaf_parent,plaf_pro=frappe.db.get_value('taxes et cotisation',self.loi_de_finance,['pourc_pro','max_parents','pourcent_parent','plafond_parent','plafond_pro'])
		cot_cnss=self.gross_pay*cnss*0.01
		num_months=frappe.db.get_value('Employee',self.employee,['working_months'])
		print("mois travailleees"+str(num_months))
#salaire annuel social

		self.social_salary=(self.gross_pay - cot_cnss)*num_months
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


		deduction_chef,enfant1,enfant2,enfant3,enfant4,infirme,nonbour=frappe.db.get_value('taxes et cotisation',self.loi_de_finance,['deduct_chef','deduct_enfant1','deduct_enfant2','deduct_enfant3','deduct_enfant4','deduct_infirm','deduct_non_bour'])
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




		bank,post,obliga,habit,aut=frappe.db.get_value('Employee',self.employee,['consideration_b','consideration_p','interet_emprunt_obligatoire_considearation','habitation','autre'])
		deduction += float(bank) + float(post) +float(obliga) + aut + habit		#la suite des autres deduction
		print("les deduction"+str(deduction))
		self.les_deductions=deduction



		self.tax_salary =self.social_salary - deduction				#salaire annuel imposable



#condition si il est imposable irpp + css

		if (state_impos):

			tax_slab = self.get_custom_tax()
			tax = 0
			irpp_tax=self.custom_calculate_tax_by_tax_slab(self.tax_salary,tax_slab)
			print(irpp_tax)
			irpp=irpp_tax/num_months
			#calcul css
			css=frappe.db.get_value('taxes et cotisation',self.loi_de_finance,['pourc_css'])
			deduct_css=self.tax_salary*css*0.01/num_months
			print("css:"+str(deduct_css))

		else:
			irpp=0
			css=0
		print("la mensuelle de irpp"+str(irpp))
#		for slab in tax_slab.slabs:                             #calcul irpp en utilisant le salaire imposable en utilsant le tableau de irpp
#			while (self.tax_salary >=0):
#				if (self.tax_salary > slab.from_amount and self.tax_salary < slab.to_amount):
#					tax += self.tax_salary * slab.percent_deduction*0.01
#				if (self.tax_salary>slab.to_amount):
#					tax +=(slab.to_amount - slab.from_amount)* slab.percent_deduction*0.01
#					self.tax_salary=self.tax_salary - slab.to_amount
#		irpp=tax/num_months
# calcul de net pay
		self.net_pay=(self.social_salary/num_months)-irpp-deduct_css
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
#		self.social_salary = (self.gross_pay - cnss)*num_months
#		print(self.social_salary)
		#a= super(CustomSalarySlip,self).get_emp_and_working_day_details()
#		print("hello from override"*num_months)
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
