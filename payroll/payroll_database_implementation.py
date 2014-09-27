class Payroll_Database(object):
    """ Payroll database """
	
    _instance = None
	
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Payroll_Database, cls).__new__(
                cls, *args, **kwargs)
        return cls._instance

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

