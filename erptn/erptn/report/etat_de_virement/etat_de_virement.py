# Copyright (c) 2013, amf and contributors
# For license information, please see license.txt

import frappe
from frappe import _

def execute(filters=None):
	if not filters:
		return get_columns(),get_data(None)
	columns = get_columns()
	data=get_data(filters)
	#columns, data = [], []
	return columns, data


def get_data(filters):
	data = []
	if len(frappe.db.sql(""" select code , employee_name , net_pay , bank_account_no , bank_name from `tabSalary Slip` """)) > 0:
		if filters :
			my_company= filters.company
			jour_comptable= filters.posting_date
			deJour=filters.start_date
			auJour=filters.end_date
			department=filters.department
			branch=filters.branch
			banque=filters.bank_name
		else:
			data=frappe.db.sql(""" select code , employee_name , net_pay , bank_account_no , bank_name from `tabSalary Slip` limit 10 """,as_dict=True)
			return data
		data=frappe.db.sql(""" select code , employee_name , net_pay , bank_account_no , bank_name from `tabSalary Slip` where company = %s or bank_name = %s or branch = %s or department = %s or end_date = %s or start_date = %s or posting_date= %s """,(filters.company,filters.bank_name,filters.branch,filters.department,filters.end_date,filters.start_date,filters.posting_date),as_dict=True)
		return data
	return data
def get_columns():
	return [
		{
			"fieldname":"code",
			"label": _("Code"),
			"fieldtype": "Data",
			"width": 100
		},
		{
			"fieldname": "employee_name",
			"label": _("Nom et Prenom"),
			"fieldtype": "Link",
			"options": "Employee",
			"width": 200
		},
		{
			"fieldname": "net_pay",
			"label": _("Montant"),
			"fieldtype": "Link",
			"options": "Currency",
			"width": 100
		},
		{
			"fieldname":"bank_account_no",
			"label": _("RIB"),
			"fieldtype": "Data",
			"width": 200
		},
		{
			"fieldname":"bank_name",
			"label": _("Banque"),
			"fieldtype": "Data",
			"hidden":0,
			"width": 100
		}



	]
