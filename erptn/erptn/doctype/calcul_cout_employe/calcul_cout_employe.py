# Copyright (c) 2022, amf and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class Calculcoutemploye(Document):
	pass
@frappe.whitelist()
def calcule(emp,salary_slip):
	salary=frappe.db.get_value('Salary Slip',salary_slip,['gross_pay'])
	worker=frappe.db.get_value('Employee',emp,['regime_cnss'])
	cnss,patron,accident,tauxfp,tauxfoprolos=frappe.db.get_value('Regime CNSS',worker,['cnss_employe','cnss_patron','acc_travail','tfp','foprolos'])
	retenue_cnss=salary*cnss*0.01
	retenue_patronale=salary*patron*0.01
	accident_travail=salary*accident*0.01
	retenue_tfp=salary*tauxfp*0.01
	retenue_foprolos=salary*tauxfoprolos*0.01
	total_cotisation=retenue_foprolos+retenue_tfp+accident_travail+retenue_patronale+retenue_cnss
	return {"total_cotisation":total_cotisation,"retenue_foprolos":retenue_foprolos,"retenue_tfp":retenue_tfp,"accident_travail":accident_travail,"retenue_patronale":retenue_patronale,"retenue_cnss":retenue_cnss}
	#return total_cotisation, retenue_foprolos, retenue_tfp, accident_travail, retenue_patronale, retenue_cnss
