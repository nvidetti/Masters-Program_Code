/*
Nick Videtti
NetID: nvidetti
IST 722 - Data Warehouse
Assignment 5: Implementing Dimensional Models
2/16/2023
*/

USE
	ist722_nvidetti_dw
GO

IF EXISTS(SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA = 'mynorth' AND TABLE_NAME = 'OrderFulfillmentMart')
	BEGIN
		DROP VIEW mynorth.OrderFulfillmentMart
	END
GO

CREATE VIEW
	mynorth.OrderFulfillmentMart
	AS
		SELECT
			O.OrderID "Order ID",
			O.Freight,
			OD.FullDateUSA "Ordered Date",
			O.OrderToShipDays "Days to Ship",
			O.OrderToShipSeconds "Seconds To Ship",
			SD.FullDateUSA "Shipped Date",
			CASE O.OnTime
				WHEN 0 THEN 'No'
				WHEN 1 THEN 'Yes'
			END "On Time",
			RD.FullDateUSA "Required Date",
			S.Shipper,
			S.ShipperPhone "Shipper Phone Number",
			C.CompanyName "Customer",
			C.ContactName "Customer Contact",
			C.ContactTitle "Customer Contact Title",
			C.CustomerCity "Customer City",
			C.CustomerCountry "Customer Country",
			C.CustomerRegion "Customer Region", 
			C.CustomerPostalCode "Customer Postal Code",
			E.EmployeeName "Employee",
			E.EmployeeTitle "Employee Title"
		FROM
			mynorth.FactOrderFulfillment O
		LEFT JOIN
			mynorth.DimCustomer C
				ON O.CustomerKey = C.CustomerKey
		LEFT JOIN
			mynorth.DimEmployee E
				ON O.EmployeeKey = E.EmployeeKey
		LEFT JOIN
			mynorth.DimDate OD
				ON O.OrderDateKey = OD.DateKey
		LEFT JOIN
			mynorth.DimDate SD
				ON O.ShippedDateKey = SD.DateKey
		LEFT JOIN
			mynorth.DimDate RD
				ON O.RequiredDateKey = RD.DateKey
		LEFT JOIN
			mynorth.DimShipper S
				ON O.DimShipperID = S.DimShipperID