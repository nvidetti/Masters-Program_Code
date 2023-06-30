USE
	ist722_nvidetti_stage
GO

--Stage Customers
IF EXISTS(SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA = 'dbo' AND TABLE_NAME = 'stgNorthwindCustomers')
BEGIN
	DROP TABLE dbo.stgNorthwindCustomers
END
SELECT
	CustomerID,
	CompanyName,
	ContactName,
	ContactTitle,
	Address,
	City,
	Region,
	PostalCode,
	Country
INTO
	dbo.stgNorthwindCustomers
FROM
	Northwind.dbo.Customers
GO
	
--Stage Employees
IF EXISTS(SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA = 'dbo' AND TABLE_NAME = 'stgNorthwindEmployees')
BEGIN
	DROP TABLE dbo.stgNorthwindEmployees
END
SELECT
	EmployeeID,
	FirstName,
	LastName,
	Title
INTO
	dbo.stgNorthwindEmployees
FROM
	Northwind.dbo.Employees
GO

--Stage Products
IF EXISTS(SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA = 'dbo' AND TABLE_NAME = 'stgNorthwindProducts')
BEGIN
	DROP TABLE stgNorthwindProducts
END
SELECT
	ProductID,
	ProductName,
	Discontinued,
	CompanyName,
	CategoryName
INTO
	dbo.stgNorthwindProducts
FROM
	Northwind.dbo.Products P
INNER JOIN
	Northwind.dbo.Suppliers S
		ON P.SupplierID = S.SupplierID
INNER JOIN
	Northwind.dbo.Categories C
		ON P.CategoryID = C.CategoryID
GO

--Stage Dates
IF EXISTS(SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA = 'dbo' AND TABLE_NAME = 'stgNorthwindDates')
BEGIN
	DROP TABLE stgNorthwindDates
END
SELECT
	*
INTO
	dbo.stgNorthwindDates
FROM
	ExternalSources2.dbo.date_dimension
WHERE
	YEAR BETWEEN 1996 AND 1998	
GO

--Stage Sales Fact
IF EXISTS(SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA = 'dbo' AND TABLE_NAME = 'stgNorthwindSales')
BEGIN
	DROP TABLE stgNorthwindSales
END
SELECT
	ProductID,
	D.OrderID,
	CustomerID,
	EmployeeID,
	OrderDate,
	ShippedDate,
	UnitPrice,
	Quantity,
	Discount
INTO
	dbo.stgNorthwindSales
FROM
	Northwind.dbo.[Order Details] D
INNER JOIN
	Northwind.dbo.Orders O
		ON D.OrderID = O.OrderId
GO