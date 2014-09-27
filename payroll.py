# Payroll Application
# ===================

import calendar
import datetime

################
## Database
################

class Payroll_Database(object):
    """ Payroll database """

    def __init__(self):
        """ Initialize the database """

        # Employees dictionary indexed by empid
        self.employees = {}

    def get_employee(self, empid):
        """ Get a single employee """

        return self.employees[empid]

    def add_employee(self, empid, employee):
        """ Add an employee to the database """

        self.employees[empid] = employee

    def delete_employee(self, empid):
        """ Delete an employee from the database """

        del self.employees[empid]

    def get_all_empids(self):
        """ Return a list of all employee ids """

        return self.employees.keys()

# Initialize the global payroll database variable
db = Payroll_Database()

################
## Paycheck
################

class Paycheck(object):
    """ Paycheck """

    def __init__(self, paydate, start_date):
        """ Initialize the paycheck """

        self.paydate = paydate
        self.start_date = start_date
        self.gross_pay = None
        self.deductions = None
        self.fields = {}

    @property
    def net_pay(self):
        """ Get gross pay less deductions """
        return self.gross_pay - self.deductions

    def set_fields(self, fields):
        """ Set the paycheck fields """

        for key in fields:
            self.fields[key] = fields[key]

    def get_field(self, field):
        """ Get the value of a field """

        return self.fields[field]

################
## Employee
################

class Employee(object):
    """ Employee  """

    def __init__(self, empid, name, address, classification):
        """ Initialize the employee """

        self.empid = empid
        self.name = name
        self.address = address
        self.classification = classification
        self.schedule= None
        self.payment_method = None

    def is_pay_date(self, date):
        """ Is this a pay date? """

        # Delegate to the schedule
        return self.schedule.is_pay_date(date)

    def payday(self, date):
        """ Calculate the pay """
        pc = Paycheck(date, self.schedule.get_start_date(date))
        pc.gross_pay = self.classification.calculate_pay(pc)
        pc.deductions = 0 # Not implemented
        pc.set_fields(self.payment_method.get_fields())

        return pc

#############################
## Classification Details
#############################

class Timecard(object):
    """ Timecard for hourly employees """

    def __init__(self, date, hours):
        """ Initialize the timecard """

        self.date = date
        self.hours = hours

class Sales(object):
    """ Sales for commissioned employees """

    def __init__(self, date, amount):
        """ Initialize the sales """

        self.date = date
        self.amount = amount

#############################
## Employee Classifications
#############################

class Hourly_Classification(object):
    """ Classification for hourly employees """

    def __init__(self, rate):
        """ Initialize the classification """

        self.name = "Hourly"
        self.rate = rate
        self.timecards = {}

    def add_timecard(self, date, tc):
        """ Add a timecard """

        self.timecards[date] = tc

    def get_timecard(self, date):
        """ Get a timecard """

        return self.timecards[date]
        
    def calculate_pay(self, paycheck):
        """ Calculate the pay """
        
        total_hours = 0
        
        for key in self.timecards:
            if key > paycheck.start_date and key <= paycheck.paydate:
                total_hours += self.timecards[key].hours
                
        return total_hours * self.rate

class Salaried_Classification(object):
    """ Classification for salaried employees """

    def __init__(self, salary):
        """ Initialize the classification """

        self.name = "Salaried"
        self.salary = salary

    def calculate_pay(self, paycheck):
        """ Calculate the pay """

        return self.salary

class Commissioned_Classification(object):
    """ Classification for salaried employees """

    def __init__(self, salary, commission_rate):
        """ Initialize the classification """

        self.name = "Commissioned"
        self.salary = salary
        self.commission_rate = commission_rate
        self.sales = {}

    def add_sales(self, date, sale):
        """ Add a sale to the record """

        # Use a list to enable multiple sales on the same day
        if date in self.sales:
            # There's a sale on this date, let's append the new one to the list
            self.sales[date].append(sale)
        else:
            self.sales[date] = (sale) # Convert sale to a list

    def get_sales(self, date):
        """ Get the sales for this date """

        return self.sales[date]



#############################
## Payment Schedules
#############################

class Weekly_Schedule(object):
    """ Payment schedule """

    def __init__(self):
        """ Initialize the schedule """

        self.name= "Weekly"

    def is_pay_date(self, date):
        """ Is this a pay date? """

        return date.weekday() == 4 # Friday
        
    def get_start_date(self, date):
        """ Return the pay period start date """
        
        if self.is_pay_date(date):
            return date + datetime.timedelta(days = -7)

class Biweekly_Schedule(object):
    """ Payment schedule """

    def __init__(self):
        """ Initialize the schedule """

        self.name= "Biweekly"

    def is_pay_date(self, date):
        """ Is this a pay date? """

        return False # not implemented

class Monthly_Schedule(object):
    """ Payment schedule """

    def __init__(self):
        """ Initialize the schedule """

        self.name= "Monthly"

    def is_pay_date(self, date):
        """ Is this a pay date? """

        last_day = calendar.monthrange(date.year, date.month)[1]

        return date.day == last_day
        
    def get_start_date(self, date):
        """ Return the pay period start date """
        
        return datetime.date(date.year, date.month, 1)
        
#############################
## Payment Methods
#############################

class Hold_Method(object):
    """ Hold paycheck """

    def __init__(self):
        """ Initialize the hold method """

        self.name = "Hold"

    def get_fields(self):
        """ Add the fields """

        fields = {"Disposition": "Hold"}

        return fields

#############################
## Add Employeee Transactions
#############################

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

        db.add_employee(self.empid, emp)

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

#############################
## Delete Employeee Transaction
#############################

class Delete_Employee_Transaction(object):
    """ Delete an employee """

    def __init__(self, empid):
        """ Initialize the transaction """

        self.empid = empid

    def execute(self):
        """ Execute the trnsaction """

        db.delete_employee(self.empid)

#############################
## Timecard / Sales Transactions
#############################

class Timecard_Transaction(object):
    """ Timecard Transaction """

    def __init__(self, date, hours, empid):
        """ Initialize the timecard transaction """

        self.date = date
        self.hours = hours
        self.empid = empid

    def execute(self):
        """ Execute the transaction """

        e = db.get_employee(self.empid)

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

        e = db.get_employee(self.empid)

        # Sales can only be posted to commissioned employees
        if e.classification.name == "Commissioned":
            tc = Sales(self.date, self.amount)
            e.classification.add_sales(self.date, tc)
        else:
            raise Exception("Tried to add sales to non-commissioned employee")

#############################
## Payday Transaction
#############################

class Payday_Transaction(object):
    """ The payday transaction """

    def __init__(self, paydate):
        """ Initialize the transaction """

        self.paydate = paydate
        self.paychecks = {}

    def execute(self):
        """ Execute the transaction """

        empids = db.get_all_empids()

        for empid in empids:

            e = db.get_employee(empid)

            if e.is_pay_date(self.paydate):
                pc = e.payday(self.paydate)
                self.paychecks[empid] = pc

    def get_paycheck(self, empid):
        """ Return the paycheck for emplid """

        return self.paychecks[empid]

