import pytest

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
    
    assert e.salary == 1000.00
    
    assert e.payment_schedule.name == "Monthly"
    
    assert e.payment_method.name == "Hold"
    
