// Copyright (c) 2016, amf and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Custom Salary Slip report"] = {
	"filters": [
		{
			"fieldname": "company",
			"label": __("Company"),
			"fieldtype": "Link",
			"options": "Company",
			"reqd":1
		}
		{


			"fieldname": "posting_date",
			"label": __("Posting date"),
			"fieldtype": "Date",
			"options": "Company"
}

	]
};
