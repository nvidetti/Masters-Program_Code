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

/*
DimCustomer loaded in part 2
DimEmployee loaded in part 2
DimDate loaded in part 2
*/

--Load DimShipper
INSERT INTO mynorth.DimShipper
	(ShipperID, Shipper, ShipperPhone)
SELECT
	ShipperID,
	CompanyName,
	Phone
FROM
	ist722_nvidetti_stage.dbo.stgNorthwindShippers

--Load FactOrderFulfillment
INSERT INTO mynorth.FactOrderFulfillment
	(OrderID, CustomerKey, EmployeeKey,	OrderDateKey,
	ShippedDateKey,	RequiredDateKey, DimShipperID, OrderToShipDays,
	OrderToShipSeconds,	OnTime,	Freight)
SELECT
	O.OrderID,
	C.CustomerKey,
	E.EmployeeKey,
	ExternalSources2.dbo.getDateKey(O.OrderDate) OrderDateKey,
	ExternalSources2.dbo.getDateKey(O.ShippedDate) ShippedDateKey,
	ExternalSources2.dbo.getDateKey(O.RequiredDate) RequiredDateKey,
	S.DimShipperID,
	DATEDIFF(SECOND, O.OrderDate, O.ShippedDate) / 86400 OrderToShipDays,
	DATEDIFF(SECOND, O.OrderDate, O.ShippedDate) OrderToShipSeconds,	
	CASE 
		WHEN O.ShippedDate <= O.RequiredDate
			THEN 1
		WHEN O.ShippedDate IS NULL AND O.RequiredDate < GETDATE()
			THEN 1
		ELSE 0
	END OnTime,
	O.Freight
FROM
	ist722_nvidetti_stage.dbo.stgNorthwindOrderFulfillment O
INNER JOIN
	ist722_nvidetti_dw.mynorth.DimCustomer C
		ON O.CustomerID = C.CustomerID
INNER JOIN
	ist722_nvidetti_dw.mynorth.DimEmployee E
		ON O.EmployeeID = E.EmployeeID
INNER JOIN
	ist722_nvidetti_dw.mynorth.DimShipper S
		ON O.ShipVia = S.ShipperID