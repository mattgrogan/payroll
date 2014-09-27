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