# Copyright (c) 2022, amf and contributors
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
	if len(frappe.db.sql(""" select employee , net_pay from `tabSalary Slip` """)) > 0:
		if filters :
			my_company= filters.company
		else:
			data=frappe.db.sql(""" select employee , net_pay from `tabSalary Slip` limit 10 """,as_dict=True)
			return data
		data=frappe.db.sql(""" select employee , net_pay from `tabSalary Slip` where company = '{0}' """.format(str(my_company)),as_dict=True)
		return data
	return data
def get_columns():
	return [
		{
			"fieldname": "employee",
			"label": _("Employee"),
			"fieldtype": "Link",
			"options": "Employee",
			"width": 300
		},
		{
			"fieldname": "net_pay",
			"label": _("Net a payer"),
			"fieldtype": "Link",
			"options": "Currency",
			"width": 300
		}

	]
