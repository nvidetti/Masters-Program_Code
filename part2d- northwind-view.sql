USE
	ist722_nvidetti_dw
GO

IF EXISTS(SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA = 'mynorth' AND TABLE_NAME = 'SalesMart')
	BEGIN
		DROP VIEW mynorth.SalesMart
	END
GO

CREATE VIEW
	mynorth.SalesMart
	AS
		SELECT
			S.OrderID,
			S.Quantity,
			S.ExtendedPriceAmount,
			S.DiscountAmount,
			S.SoldAmount,
			C.CompanyName,
			C.ContactName,
			C.ContactTitle,
			C.CustomerCity,
			C.CustomerCountry,
			C.CustomerRegion, 
			C.CustomerPostalCode,
			E.EmployeeName,
			E.EmployeeTitle,
			P.ProductName,
			P.Discontinued,
			P.CategoryName,
			OD.*
		FROM
			mynorth.FactSales S
		INNER JOIN
			mynorth. DimCustomer C
				ON S.CustomerKey = C.CustomerKey
		INNER JOIN
			mynorth. DimEmployee E
				ON S.EmployeeKey = E.EmployeeKey
		INNER JOIN
			mynorth. DimProduct P
				ON S.ProductKey = P.ProductKey
		INNER JOIN
			mynorth. DimDate OD
				ON S.OrderDateKey = OD.DateKey