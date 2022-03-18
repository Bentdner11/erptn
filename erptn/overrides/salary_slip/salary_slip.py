from erpnext.payroll.doctype.salary_slip.salary_slip import SalarySlip

import frappe
from frappe.utils import flt
from erpnext.utilities.transaction_base import TransactionBase
from frappe.model.document import Document
class CustomSalarySlip(SalarySlip):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

	def validate(self):
		super(CustomSalarySlip, self).validate()
		self.salary_imp = self.salary_imp - self.gross_pay
	def my_custom_code(self):
		pass
#		self.salary_imp =self.gross_pay -
		#for d in self._salary_structure_doc.get("deductions"):
		#	if d.salary_component_abbr == "CS":
		#		self.salary_imp = flt(self.gross_pay) - flt(d.amount)
