""" Package payroll into a single namespace """

from payroll.payroll_database_implementation import Payroll_Database
from payroll.transaction_implementation import * 
	
# Initialize the global payroll database variable
DATABASE = Payroll_Database()