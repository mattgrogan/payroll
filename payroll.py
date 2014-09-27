# Payroll Application
# ===================

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
        
# Initialize the global payroll database variable
db = Payroll_Database()

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

#############################
## Classification Details 
#############################

class Timecard(object):
    """ Timecard for hourly employees """
    
    def __init__(self, date, hours):
        """ Initialize the timecard """
        
        self.date = date
        self.hours = hours
        
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
        
class Salaried_Classification(object):
    """ Classification for salaried employees """
    
    def __init__(self, salary):
        """ Initialize the classification """
        
        self.name = "Salaried"
        self.salary = salary

class Commissioned_Classification(object):
    """ Classification for salaried employees """
    
    def __init__(self, salary, commission_rate):
        """ Initialize the classification """
        
        self.name = "Commissioned"
        self.salary = salary
        self.commission_rate = commission_rate
        
#############################
## Payment Schedules
#############################

class Weekly_Schedule(object):
    """ Payment schedule """

    def __init__(self):
        """ Initialize the schedule """
        
        self.name= "Weekly"
 
class Biweekly_Schedule(object):
    """ Payment schedule """

    def __init__(self):
        """ Initialize the schedule """
        
        self.name= "Biweekly"
       
class Monthly_Schedule(object):
    """ Payment schedule """

    def __init__(self):
        """ Initialize the schedule """
        
        self.name= "Monthly"

#############################
## Payment Methods
#############################

class Hold_Method(object):
    """ Hold paycheck """

    def __init__(self):
        """ Initialize the hold method """
        
        self.name = "Hold"

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
## Timecard Transaction
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
            