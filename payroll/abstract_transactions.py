from payroll.payroll_domain import Employee
from __init__ import DATABASE

class Add_Employee_Transaction(object):
    """ Add an employee """

    def __init__(self, empid, name, address):
        """ Initialize the transaction """

        self.empid = empid
        self.name = name
        self.address = address
        self.classification = None
        self.schedule = None
        self.payment_method= None

    def execute(self):
        """ Execute the transaction """

        emp = Employee(self.empid, self.name, self.address, self.classification)

        emp.classification = self.classification
        emp.schedule = self.schedule
        emp.payment_method = self.payment_method

        DATABASE.add_employee(self.empid, emp)