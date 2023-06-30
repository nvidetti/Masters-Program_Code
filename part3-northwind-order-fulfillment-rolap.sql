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

--schema mynorth created in part 2

IF EXISTS(SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA = 'mynorth' AND TABLE_NAME = 'FactOrderFulfillment')
	BEGIN
		DROP TABLE mynorth.FactOrderFulfillment
	END

IF EXISTS(SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA = 'mynorth' AND TABLE_NAME = 'DimShipper')
	BEGIN
		DROP TABLE mynorth.DimShipper
	END

/*
mynorth.DimEmployee created in part 2
mynorth.DimDate created in part 2
mynorth.DimCustomer created in part 2
*/

--Shippers Dimension
CREATE TABLE
	mynorth.DimShipper(
		DimShipperID INT IDENTITY NOT NULL,
		ShipperID INT NOT NULL,
		Shipper NVARCHAR(100) NOT NULL,
		ShipperPhone NVARCHAR(50) NOT NULL,
		CONSTRAINT PK_DimShipper PRIMARY KEY (DimShipperID)
	)
GO

--Order Fulfillment Fact
CREATE TABLE
	mynorth.FactOrderFulfillment(
		OrderID INT NOT NULL,
		CustomerKey INT NOT NULL,
		EmployeeKey INT NOT NULL,
		OrderDateKey INT NOT NULL,
		ShippedDateKey INT,
		RequiredDateKey INT NOT NULL,
		DimShipperID INT NOT NULL,
		OrderToShipDays DECIMAL,
		OrderToShipSeconds BIGINT,
		OnTime BIT NOT NULL,
		Freight MONEY NOT NULL,
		CONSTRAINT PK_FactOrderFulfillment PRIMARY KEY (OrderID),
		CONSTRAINT FK_FactOrderFulfillment_CustomerKey FOREIGN KEY (CustomerKey)
			REFERENCES mynorth.DimCustomer(CustomerKey),
		CONSTRAINT FK_FactOrderFulfillment_EmployeeKey FOREIGN KEY (EmployeeKey)
			REFERENCES mynorth.DimEmployee(EmployeeKey),
		CONSTRAINT FK_FactOrderFulfillment_OrderDateKey FOREIGN KEY (OrderDateKey)
			REFERENCES mynorth.DimDate(DateKey),
		CONSTRAINT FK_FactOrderFulfillment_ShippedDateKey FOREIGN KEY (ShippedDateKey)
			REFERENCES mynorth.DimDate(DateKey),
		CONSTRAINT FK_FactOrderFulfillment_RequiredDateKey FOREIGN KEY (RequiredDateKey)
			REFERENCES mynorth.DimDate(DateKey),
		CONSTRAINT FK_FactOrderFulfillment_DimShipperID FOREIGN KEY (DimShipperID)
			REFERENCES mynorth.DimShipper(DimShipperID)
	)
GO