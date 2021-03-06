import pytest
import datetime

import payroll

def test_add_salaried_employee():
    
    empid = 1
    
    t = payroll.Add_Salaried_Employee(empid, "Bob", "Home", 1000.00)
    t.execute()
    
    e = payroll.DATABASE.get_employee(empid)
    
    assert e.name == "Bob"
    
    assert e.classification.name == "Salaried"
    
    assert e.classification.salary == 1000.00
    
    assert e.schedule.name == "Monthly"
    
    assert e.payment_method.name == "Hold"
    
def test_add_hourly_employee():
    
    empid = 2
    
    t = payroll.Add_Hourly_Employee(empid, "John", "Home", 45.00)
    t.execute()
    
    e = payroll.DATABASE.get_employee(empid)
    
    assert e.name == "John"
    
    assert e.classification.name == "Hourly"
    
    assert e.classification.rate == 45.00
    
    assert e.schedule.name == "Weekly"
    
    assert e.payment_method.name == "Hold"
    
def test_add_commissioned_employee():
    
    empid = 3
    
    t = payroll.Add_Commissioned_Employee(empid, "Mike", "Home", 1100, 0.10)
    t.execute()
    
    e = payroll.DATABASE.get_employee(empid)
    
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
    e = payroll.DATABASE.get_employee(empid)
    assert e
    
    dt = payroll.Delete_Employee_Transaction(empid)
    dt.execute()

    with pytest.raises(KeyError):
        payroll.DATABASE.get_employee(empid)    
        
def test_timecard_transaction():
    
    empid = 1
    
    t = payroll.Add_Hourly_Employee(empid, "John", "Home", 45.00)
    t.execute()
   
    tct = payroll.Timecard_Transaction(datetime.date(2014, 9, 26), 8.0, empid)
    tct.execute()

    e = payroll.DATABASE.get_employee(empid)
    assert e

    assert e.classification.name == "Hourly"

    tc = e.classification.get_timecard(datetime.date(2014, 9, 26))

    assert tc.hours == 8.0       
    
def test_sales_transaction():
    
    empid = 1
    
    t = payroll.Add_Commissioned_Employee(empid, "John", "Home", 1100, 0.10)
    t.execute()
   
    tct = payroll.Sales_Transaction(datetime.date(2014, 9, 26), 25000, empid)
    tct.execute()

    e = payroll.DATABASE.get_employee(empid)
    assert e

    assert e.classification.name == "Commissioned"

    tc = e.classification.get_sales(datetime.date(2014, 9, 26))

    assert tc.amount == 25000   
    
def test_paying_single_salaried_employees():
    
    empid = 1
    
    t = payroll.Add_Salaried_Employee(empid, "Bob", "Home", 1000.00)
    t.execute()
    
    paydate = datetime.date(2014, 9, 30)
    
    pt = payroll.Payday_Transaction(paydate)
    pt.execute()
    
    pc = pt.get_paycheck(empid)
    
    assert pc.paydate == paydate
    
    assert pc.gross_pay == 1000.00
    
    assert pc.get_field("Disposition") == "Hold"
    
    assert pc.deductions == 0
    
    assert pc.net_pay == 1000.00

def validate_hourly_paycheck(pt, empid, paydate, pay):
    """ Helper function to validate paychecks """
    
    pc = pt.get_paycheck(empid)
    
    assert pc.paydate == paydate
    
    assert pc.gross_pay == pay
    
    assert pc.deductions == 0
    
    assert pc.get_field("Disposition") == "Hold"
    
    assert pc.net_pay == pay
    
def test_pay_single_hourly_emp_no_timecards():
    
    empid = 1
    
    t = payroll.Add_Hourly_Employee(empid, "John", "Home", 45.00)
    t.execute()
    
    paydate = datetime.date(2014, 9, 26) # Friday

    pt = payroll.Payday_Transaction(paydate)
    pt.execute()
    
    validate_hourly_paycheck(pt, empid, paydate, 0.00)

def test_pay_single_hourly_emp_one_timecard():
    
    empid = 1
    
    t = payroll.Add_Hourly_Employee(empid, "John", "Home", 45.00)
    t.execute()

    
    paydate = datetime.date(2014, 9, 26) # Friday
    
    tc = payroll.Timecard_Transaction(paydate, 2.0, empid)
    tc.execute()

    pt = payroll.Payday_Transaction(paydate)
    pt.execute()
    
    validate_hourly_paycheck(pt, empid, paydate, 90.00)    
    
def test_pay_single_hourly_emp_one_timecard_overtime():
    
    empid = 1
    
    t = payroll.Add_Hourly_Employee(empid, "John", "Home", 45.00)
    t.execute()

    
    paydate = datetime.date(2014, 9, 26) # Friday
    
    tc = payroll.Timecard_Transaction(paydate, 9.0, empid)
    tc.execute()

    pt = payroll.Payday_Transaction(paydate)
    pt.execute()
    
    validate_hourly_paycheck(pt, empid, paydate, (8 + 1.5) * 45.00)       
    