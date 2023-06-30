USE
	ist722_nvidetti_dw
GO

IF NOT EXISTS(SELECT * FROM SYS.SCHEMAS WHERE NAME = 'mynorth')
	BEGIN
		EXEC('CREATE SCHEMA mynorth')
	END
GO

IF EXISTS(SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA = 'mynorth' AND TABLE_NAME = 'FactSales')
	BEGIN
		DROP TABLE mynorth.FactSales
	END

IF EXISTS(SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA = 'mynorth' AND TABLE_NAME = 'DimProduct')
	BEGIN
		DROP TABLE mynorth.DimProduct
	END

IF EXISTS(SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA = 'mynorth' AND TABLE_NAME = 'DimEmployee')
	BEGIN
		DROP TABLE mynorth.DimEmployee
	END
GO

IF EXISTS(SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA = 'mynorth' AND TABLE_NAME = 'DimDate')
	BEGIN
		DROP TABLE mynorth.DimDate
	END
GO

IF EXISTS(SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA = 'mynorth' AND TABLE_NAME = 'DimCustomer')
	BEGIN
		DROP TABLE mynorth.DimCustomer
	END
GO

--Customer Dimension
CREATE TABLE
	mynorth.DimCustomer(
		CustomerKey INT IDENTITY NOT NULL,
		CustomerId NVARCHAR(5) NOT NULL,
		CompanyName NVARCHAR(40) NOT NULL,
		ContactName NVARCHAR(30) NOT NULL,
		ContactTitle NVARCHAR(30) NOT NULL,
		CustomerCountry NVARCHAR(15) NOT NULL,
		CustomerRegion NVARCHAR(15) DEFAULT('N/A') NOT NULL,
		CustomerCity NVARCHAR(15) NOT NULL,
		CustomerPostalCode NVARCHAR(10) NOT NULL,
		RowIsCurrent BIT DEFAULT(1) NOT NULL,
		RowStartDate DATETIME DEFAULT(1/1/1900) NOT NULL,
		RowEndDate DATETIME DEFAULT(12/31/9999) NOT NULL,
		RowChangeReason NVARCHAR(200),
		CONSTRAINT PK_DimCustomer PRIMARY KEY (CustomerKey)
	)
GO

--Date Dimension
CREATE TABLE
	mynorth.DimDate(
		DateKey INT NOT NULL,
		Date Date,
		FullDateUSA NCHAR(11) NOT NULL,
		DayOfWeek TINYINT NOT NULL,
		DayName NCHAR(10) NOT NULL,
		DayOfMonth TINYINT NOT NULL,
		DayOfYear SMALLINT NOT NULL,
		WeekOfYear TINYINT NOT NULL,
		MonthName NCHAR(10) NOT NULL,
		MonthOfYear TINYINT NOT NULL,
		Quarter TINYINT NOT NULL,
		QuarterName NCHAR(10) NOT NULL,
		Year SMALLINT NOT NULL,
		IsWeekday BIT DEFAULT(0) NOT NULL,
		CONSTRAINT PK_DimDate PRIMARY KEY (DateKey)
	)
GO

--Employee Dimension
CREATE TABLE
	mynorth.DimEmployee(
		EmployeeKey INT IDENTITY NOT NULL,
		EmployeeID INT NOT NULL,
		EmployeeName NVARCHAR(40) NOT NULL,
		EmployeeTitle NVARCHAR(30) NOT NULL,
		RowIsCurrent BIT DEFAULT(1) NOT NULL,
		RowStartDate DATETIME DEFAULT(1/1/1900) NOT NULL,
		RowEndDate DATETIME DEFAULT(12/31/9999) NOT NULL,
		RowChangeReason NVARCHAR(200),
		CONSTRAINT PK_DimEmployee PRIMARY KEY (EmployeeKey)
	)
GO

--Product Dimension
CREATE TABLE
	mynorth.DimProduct(
		ProductKey INT IDENTITY NOT NULL,
		ProductID INT NOT NULL,
		ProductName NVARCHAR(40) NOT NULL,
		Discontinued NCHAR(1) DEFAULT('N') NOT NULL,
		SupplierName NVARCHAR(40) NOT NULL,
		CategoryName NVARCHAR(15) NOT NULL,
		RowIsCurrent BIT DEFAULT(1) NOT NULL,
		RowStartDate DATETIME DEFAULT(1/1/1900) NOT NULL,
		RowEndDate DATETIME DEFAULT(12/31/9999) NOT NULL,
		RowChangeReason NVARCHAR(200),
		CONSTRAINT PK_DimProduct PRIMARY KEY (ProductKey)
	)
GO

--Sales Fact
CREATE TABLE
	mynorth.FactSales(
		ProductKey INT NOT NULL,
		CustomerKey INT NOT NULL,
		EmployeeKey INT NOT NULL,
		OrderDateKey INT NOT NULL,
		ShippedDateKey INT,
		OrderID INT NOT NULL,
		Quantity SMALLINT NOT NULL,
		ExtendedPriceAmount MONEY NOT NULL,
		DiscountAmount MONEY DEFAULT(0) NOT NULL,
		SoldAmount MONEY NOT NULL,
		CONSTRAINT PK_FactSales PRIMARY KEY (ProductKey, OrderID),
		CONSTRAINT FK_FactSales_ProductKey FOREIGN KEY (ProductKey)
			REFERENCES mynorth.DimProduct(ProductKey),
		CONSTRAINT FK_FactSales_CustomerKey FOREIGN KEY (CustomerKey)
			REFERENCES mynorth.DimCustomer(CustomerKey),
		CONSTRAINT FK_FactSales_EmployeeKey FOREIGN KEY (EmployeeKey)
			REFERENCES mynorth.DimEmployee(EmployeeKey),
		CONSTRAINT FK_FactSales_OrderDateKey FOREIGN KEY (OrderDateKey)
			REFERENCES mynorth.DimDate(DateKey),
		CONSTRAINT FK_FactSales_ShippedDateKey FOREIGN KEY (ShippedDateKey)
			REFERENCES mynorth.DimDate(DateKey)
	)
GO