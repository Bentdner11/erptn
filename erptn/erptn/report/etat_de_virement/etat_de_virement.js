// Copyright (c) 2022, amf and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Etat de virement"] = {
	"filters": [
		{
			"fieldname": "company",
			"label": __("Nom de la societe"),
			"fieldtype": "Link",
			"options": "Company",
		},
		{


			"fieldname": "posting_date",
			"label": __("jour comptable"),
			"fieldtype": "Date",
			"width": "60px"
		},
		{
			"fieldname": "start_date",
			"label": __("periode de paie a partir de"),
			"fieldtype": "Date",
			"width":"60px"
		},
		{
			"fieldname": "end_date",
			"label": __("Jusqua"),
			"fieldtype": "Date"
		},
		{
			"fieldname": "department",
			"label": __("Département"),
			"fieldtype": "Link",
			"options": "Department"

		},
		{
			"fieldname": "branch",
			"label": __("Branche"),
			"fieldtype": "Link",
			"options": "Branch"
		},
		{
			"fieldname": "bank_name",
			"label":__("Nom de banque"),
			"fieldtype":"Link",
			"options":"Bank"
		}
		]
};

