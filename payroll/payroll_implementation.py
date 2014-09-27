import datetime
import calendar

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
        
        total_pay = 0
        
        for key in self.timecards:
            if key > paycheck.start_date and key <= paycheck.paydate:
                tc = self.timecards[key]
                total_pay += self.calculate_pay_for_timecard(tc)
                
        return total_pay
        
    def calculate_pay_for_timecard(self, tc):
        """ Calculate pay including overtime for a single timecard """
        
        hours = tc.hours
        ot = max(0, hours - 8.0)
        reg_hours = hours - ot
        
        return reg_hours * self.rate + ot * self.rate * 1.5

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

class Hold_Method(object):
    """ Hold paycheck """

    def __init__(self):
        """ Initialize the hold method """

        self.name = "Hold"

    def get_fields(self):
        """ Add the fields """

        fields = {"Disposition": "Hold"}

        return fields
