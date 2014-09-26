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
## Employee Classifications
#############################

class Hourly_Classification(object):
    """ Classification for hourly employees """
    
    def __init__(self, rate):
        """ Initialize the classification """
        
        self.name = "Hourly"
        self.rate = rate
        
class Salaried_Classification(object):
    """ Classification for salaried employees """
    
    def __init__(self, salary):
        """ Initialize the classification """
        
        self.name = "Salaried"
        self.salary = salary

#############################
## Payment Schedules
#############################

class Weekly_Schedule(object):
    """ Payment schedule """

    def __init__(self):
        """ Initialize the schedule """
        
        self.name= "Weekly"
        
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

class Add_Hourly_Employee(Add_Employee_Transaction):
    """ Add a hourly employee """
    
    def __init__(self, empid, name, address, rate):
        """ Initialize the transaction """
     
        super(Add_Hourly_Employee, self).__init__(empid, name, address)
        
        self.classification = Hourly_Classification(rate)
        
        self.schedule = Weekly_Schedule()
        
        self.payment_method = Hold_Method()
        