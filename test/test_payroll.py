import pytest
import datetime

# This hack to be able to import pacman
import sys, os
myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath+ '/../')

import payroll

def test_add_salaried_employee():
    
    empid = 1
    
    t = payroll.Add_Salaried_Employee(empid, "Bob", "Home", 1000.00)
    t.execute()
    
    e = payroll.db.get_employee(empid)
    
    assert e.name == "Bob"
    
    assert e.classification.name == "Salaried"
    
    assert e.classification.salary == 1000.00
    
    assert e.schedule.name == "Monthly"
    
    assert e.payment_method.name == "Hold"
    
def test_add_hourly_employee():
    
    empid = 2
    
    t = payroll.Add_Hourly_Employee(empid, "John", "Home", 45.00)
    t.execute()
    
    e = payroll.db.get_employee(empid)
    
    assert e.name == "John"
    
    assert e.classification.name == "Hourly"
    
    assert e.classification.rate == 45.00
    
    assert e.schedule.name == "Weekly"
    
    assert e.payment_method.name == "Hold"
    
def test_add_commissioned_employee():
    
    empid = 3
    
    t = payroll.Add_Commissioned_Employee(empid, "Mike", "Home", 1100, 0.10)
    t.execute()
    
    e = payroll.db.get_employee(empid)
    
    assert e.name == "Mike"
    
    assert e.classification.name == "Commissioned"
    
    assert e.classification.salary == 1100
    
    assert e.classification.commission_rate == 0.10
    
    assert e.schedule.name == "Biweekly"
    
    assert e.payment_method.name == "Hold"   
    
def test_delete_employee():
    
    empid = 1
    
    t = payroll.Add_Commissioned_Employee(empid, "Mike", "Home", 1100, 0.10)
    t.execute()
    
    # Check that the employee was actually created
    e = payroll.db.get_employee(empid)
    assert e
    
    dt = payroll.Delete_Employee_Transaction(empid)
    dt.execute()

    with pytest.raises(KeyError):
        payroll.db.get_employee(empid)    
        
def test_timecard_transaction():
    
    empid = 1
    
    t = payroll.Add_Hourly_Employee(empid, "John", "Home", 45.00)
    t.execute()
   
    tct = payroll.Timecard_Transaction(datetime.date(2014, 9, 26), 8.0, empid)
    tct.execute()

    e = payroll.db.get_employee(empid)
    assert e

    assert e.classification.name == "Hourly"

    tc = e.classification.get_timecard(datetime.date(2014, 9, 26))

    assert tc.hours == 8.0       
    
    