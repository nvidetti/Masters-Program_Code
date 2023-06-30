/*
Nick Videtti
NetID: nvidetti
IST 722 - Data Warehouse
Assignment 5: Implementing Dimensional Models
2/16/2023
*/

USE
	ist722_nvidetti_stage
GO

/*
Customers staged in part 2 as stgNorthwindCustomers
Employees staged in part 2 as stgNorthwindEmployees
Dates staged in part 2 as stgNorthwindDates
*/

--Stage Shippers
IF EXISTS(SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA = 'dbo' AND TABLE_NAME = 'stgNorthwindShippers')
BEGIN
	DROP TABLE stgNorthwindShippers
END
SELECT
	*
INTO
	dbo.stgNorthwindShippers
FROM
	Northwind.dbo.Shippers
GO

--Stage Order Fulfillment Fact
IF EXISTS(SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA = 'dbo' AND TABLE_NAME = 'stgNorthwindOrderFulfillment')
BEGIN
	DROP TABLE stgNorthwindOrderFulfillment
END
SELECT
	OrderID,
	CustomerID,
	EmployeeID,
	OrderDate,
	ShippedDate,
	RequiredDate,
	ShipVia,
	Freight
INTO
	dbo.stgNorthwindOrderFulfillment
FROM
	Northwind.dbo.Orders
GO