Payroll Application
===================

Agile Software Development: Principles, Patterns, and Practices
Robert C. Marin

[![Build Status](https://travis-ci.org/mattgrogan/payroll.svg?branch=master)](https://travis-ci.org/mattgrogan/payroll)

# Use Cases

## Adding Employees

A new employee is added by the receipt of an `addemp` transaction. The transaction contains the employee's name, address, and assigned employee number. The transaction has three forms:

```
addemp <empid> "<name>" <"address"> H <hourly-rate>
addemp <empid> "<name>" <"address"> S <monthly-salary>
addemp <empid> "<name>" <"address"> C <monthly-salary> <commission-rate>
```

If the transaction structure is inappropriate, an error message is printed and no action is taken.

## Deleting an Employee

Employees are deleted when a  `delemp` transaction is received. The form of this transaction is as follows:

```
delemp <empid>
```

If the `<empid>` field is not  structured correctly or if it does not refer to a valid employee record, then the transaction is printed with an error message and no other action is taken.

## Post a Time Card

On receiving a `timecard` transaction, the system will create a time-card record and associate it with the appropriate employee record.

```
timecard <empid> <date> <hours>
```

If the selected employee is not hourly, the system will print an appropriate error message and take no further action.

If the transaction structure is inappropriate, an error message is printed and no action is taken.

## Posting a Sales Receipt

Upon receiving the `salesreceipt` transaction, the system will create a new sales-receipt record and associate it with the appropriate commissioned employee.

```
salesreceipt <empid> <date> <amount>
```

If the selected employee is not commissioned, the system will print an appropriate error message and take no further action.

If the transaction structure is inappropriate, an error message is printed and no action is taken.

## Posting a Union Service Charge

Upon receiving this transaction, the system will create a service-charge record and associate it with the appropriate union member.

```
servicecharge <memberid> <amount>
```

If the transaction is not well formed or if the `<memberid>` does not refer to an existing union member, then the transaction is printed with an appropriate error message.

## Changing Employee Details

Upon receiving the transaction, the system will alter one of the details of the appropriate employee record. There are several possible variations to this record:

```
chgemp <empid> name <name>                   
chgemp <empid> address <address>
chgemp <empid> hourly <hourlyrate>
chgemp <empid> salaried <salary>
chgemp <empid> commissioned <salary> <rate>
chgemp <empid> hold
chgemp <empid> direct <bank> <account>
chgemp <empid> mail <address>
chgemp <empid> member <memberid> dues <rate>
chgemp <empid> nomember
```

If the transaction is not well formed or if `<empid>` does not refer to an existing employee or if the `<memberid>` does not refer to an existing union member, then the transaction is printed with an appropriate error message.

## Run the Payroll for Today

Upon receiving the `payday` transaction, the system finds all those employees that should be paid on the specified date. The system then determines how much they are owed and pays them according ot their selected payment method.

```
payday <date>
```


