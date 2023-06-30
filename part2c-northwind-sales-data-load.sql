USE
	ist722_nvidetti_dw
GO

--Load DimEmployee
INSERT INTO mynorth.DimEmployee
	(EmployeeID, EmployeeName, EmployeeTitle)
SELECT
	EmployeeID,
	FirstName + ' ' + LastName EmployeeName,
	Title
FROM
	ist722_nvidetti_stage.dbo.stgNorthwindEmployees

--Load DimCustomer
INSERT INTO mynorth.DimCustomer
	(CustomerID, CompanyName, ContactName, ContactTitle,
	CustomerCountry, CustomerRegion, CustomerCity, CustomerPostalCode)
SELECT
	CustomerID,
	CompanyName,
	ContactName,
	ContactTitle,
	Country,
	CASE
		WHEN Region IS NULL
			THEN 'N/A'
		ELSE Region
	END Region,
	City,
	CASE
		WHEN PostalCode IS NULL
			THEN 'N/A'
		ELSE PostalCode
	END PostalCode
FROM
	ist722_nvidetti_stage.dbo.stgNorthwindCustomers

--Load DimProduct
INSERT INTO mynorth.DimProduct
	(ProductID, ProductName, Discontinued, SupplierName, CategoryName)
SELECT
	ProductID,
	ProductName,
	CASE Discontinued
		WHEN 0 THEN 'N'
		WHEN 1 THEN 'Y'
	END Discontinued,
	CompanyName,
	CategoryName
FROM
	ist722_nvidetti_stage.dbo.stgNorthwindProducts

--Load DimDate
INSERT INTO mynorth.DimDate
	(DateKey, Date, FullDateUSA, DayOfWeek, DayName, 
	DayOfMonth, DayOfYear, WeekOfYear, MonthName, MonthOfYear,
	Quarter, QuarterName, Year, IsWeekday)
SELECT
	DateKey,
	Date,
	FullDateUSA,
	DayOfWeekUSA,
	DayName,
	DayOfMonth,
	DayOfYear,
	WeekOfYear,
	MonthName,
	Month,
	Quarter,
	QuarterName,
	Year,
	IsWeekday
FROM
	ist722_nvidetti_stage.dbo.stgNorthwindDates

--Load FactSales
INSERT INTO mynorth.FactSales
	(ProductKey, CustomerKey, EmployeeKey, OrderDateKey,
	ShippedDateKey, OrderID, Quantity, ExtendedPriceAmount,
	DiscountAmount, SoldAmount)
SELECT
	P.ProductKey,
	C.CustomerKey,
	E.EmployeeKey,
	ExternalSources2.dbo.getDateKey(S.OrderDate) OrderDateKey,
	ExternalSources2.dbo.getDateKey(S.ShippedDate) ShippedDateKey,
	S.OrderId,
	S.Quantity,
	S.Quantity * S.UnitPrice ExtendedPriceAmount,
	S.Quantity * S.UnitPrice * S.Discount DiscountAmount,
	S.Quantity * S.UnitPrice * (1 - S.Discount) SoldAmount
FROM
	ist722_nvidetti_stage.dbo.stgNorthwindSales S
INNER JOIN
	ist722_nvidetti_dw.mynorth.DimCustomer C
		ON S.CustomerID = C.CustomerID
INNER JOIN
	ist722_nvidetti_dw.mynorth.DimEmployee E
		ON S.EmployeeID = E.EmployeeID
INNER JOIN
	ist722_nvidetti_dw.mynorth.DimProduct P
		ON S.ProductID = P.ProductID