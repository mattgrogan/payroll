from payroll.abstract_transactions import Add_Employee_Transaction
from payroll.payroll_implementation import (
    Hourly_Classification, Salaried_Classification, Commissioned_Classification,
	Weekly_Schedule, Biweekly_Schedule, Monthly_Schedule, Hold_Method, Timecard,
	Sales)

from __init__ import DATABASE

class Add_Salaried_Employee(Add_Employee_Transaction):
    """ Add a salaried employee """

    def __init__(self, empid, name, address, salary):
        """ Initialize the transaction """

        super(Add_Salaried_Employee, self).__init__(empid, name, address)

        self.classification = Salaried_Classification(salary)

        self.schedule = Monthly_Schedule()

        self.payment_method = Hold_Method()

class Add_Commissioned_Employee(Add_Employee_Transaction):
    """ Add a commissioned employee """

    def __init__(self, empid, name, address, salary, commission_rate):
        """ Initialize the transaction """

        super(Add_Commissioned_Employee, self).__init__(empid, name, address)

        self.classification = Commissioned_Classification(salary, commission_rate)

        self.schedule = Biweekly_Schedule()

        self.payment_method = Hold_Method()

class Add_Hourly_Employee(Add_Employee_Transaction):
    """ Add a hourly employee """

    def __init__(self, empid, name, address, rate):
        """ Initialize the transaction """

        super(Add_Hourly_Employee, self).__init__(empid, name, address)

        self.classification = Hourly_Classification(rate)

        self.schedule = Weekly_Schedule()

        self.payment_method = Hold_Method()

class Delete_Employee_Transaction(object):
    """ Delete an employee """

    def __init__(self, empid):
        """ Initialize the transaction """

        self.empid = empid

    def execute(self):
        """ Execute the trnsaction """

        DATABASE.delete_employee(self.empid)

class Timecard_Transaction(object):
    """ Timecard Transaction """

    def __init__(self, date, hours, empid):
        """ Initialize the timecard transaction """

        self.date = date
        self.hours = hours
        self.empid = empid

    def execute(self):
        """ Execute the transaction """

        e = DATABASE.get_employee(self.empid)

        # Timecards can only be posted to hourly employees
        if e.classification.name == "Hourly":
            tc = Timecard(self.date, self.hours)
            e.classification.add_timecard(self.date, tc)
        else:
            raise Exception("Tried to add timecard to non-hourly employee")

class Sales_Transaction(object):
    """ Sales Transaction for commissioned employees """

    def __init__(self, date, hours, empid):
        """ Initialize the sales transaction """

        self.date = date
        self.amount = hours
        self.empid = empid

    def execute(self):
        """ Execute the transaction """

        e = DATABASE.get_employee(self.empid)

        # Sales can only be posted to commissioned employees
        if e.classification.name == "Commissioned":
            tc = Sales(self.date, self.amount)
            e.classification.add_sales(self.date, tc)
        else:
            raise Exception("Tried to add sales to non-commissioned employee")

class Payday_Transaction(object):
    """ The payday transaction """

    def __init__(self, paydate):
        """ Initialize the transaction """

        self.paydate = paydate
        self.paychecks = {}

    def execute(self):
        """ Execute the transaction """

        empids = DATABASE.get_all_empids()

        for empid in empids:

            e = DATABASE.get_employee(empid)

            if e.is_pay_date(self.paydate):
                pc = e.payday(self.paydate)
                self.paychecks[empid] = pc

    def get_paycheck(self, empid):
        """ Return the paycheck for emplid """

        return self.paychecks[empid]
