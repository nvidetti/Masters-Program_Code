/****** Object:  Database ist722_hhkhan_oa3_dw    Script Date: 3/19/2023 8:38:03 PM ******/
/*
Kimball Group, The Microsoft Data Warehouse Toolkit
Generate a database from the datamodel worksheet, version: 4

You can use this Excel workbook as a data modeling tool during the logical design phase of your project.
As discussed in the book, it is in some ways preferable to a real data modeling tool during the inital design.
We expect you to move away from this spreadsheet and into a real modeling tool during the physical design phase.
The authors provide this macro so that the spreadsheet isn't a dead-end. You can 'import' into your
data modeling tool by generating a database using this script, then reverse-engineering that database into
your tool.

Uncomment the next lines if you want to drop and create the database
*/
/*
DROP DATABASE ist722_hhkhan_oa3_dw
GO
CREATE DATABASE ist722_hhkhan_oa3_dw
GO
ALTER DATABASE ist722_hhkhan_oa3_dw
SET RECOVERY SIMPLE
GO
*/
USE ist722_hhkhan_oa3_dw
;
IF EXISTS (SELECT Name from sys.extended_properties where Name = 'Description')
    EXEC sys.sp_dropextendedproperty @name = 'Description'
EXEC sys.sp_addextendedproperty @name = 'Description', @value = 'Default description - you should change this.'
;


/* Drop table dbo.SalesTransactionsFact */
IF EXISTS (SELECT * FROM dbo.sysobjects WHERE id = OBJECT_ID(N'dbo.SalesTransactionsFact') AND OBJECTPROPERTY(id, N'IsUserTable') = 1)
DROP TABLE dbo.SalesTransactionsFact 
;



/* Drop table dbo.CustomersDim */
IF EXISTS (SELECT * FROM dbo.sysobjects WHERE id = OBJECT_ID(N'dbo.CustomersDim') AND OBJECTPROPERTY(id, N'IsUserTable') = 1)
DROP TABLE dbo.CustomersDim 
;

/* Create table dbo.CustomersDim */
CREATE TABLE dbo.CustomersDim (
   [CustomersDimID]  INT IDENTITY  NOT NULL
,  [CustomerID]  INT   NOT NULL
,  [CompanyDivision]  NVARCHAR(3)   NOT NULL
,  [CustomerEmail]  VARCHAR(200)   NOT NULL
,  [CustomerName]  NVARCHAR(101)   NOT NULL
,  [CustomerAddress]  VARCHAR(1000)  DEFAULT 'N/A' NULL
,  [CustomerZipCode]  VARCHAR(20)  DEFAULT '-----' NOT NULL
,  [CustomerCity]  VARCHAR(50)   NOT NULL
,  [CustomerState]  VARCHAR(2)  DEFAULT '--' NULL
,  [CustomerCityState]  NVARCHAR(53)   NOT NULL
,  [RowIsCurrent]  BIT   NOT NULL
,  [RowStartDate]  DATE  DEFAULT '1/1/1970' NOT NULL
,  [RowEndDate]  DATE  DEFAULT '12/31/9999' NOT NULL
,  [RowChangeReason]  NVARCHAR(50)   NULL
, CONSTRAINT [PK_dbo.CustomersDim] PRIMARY KEY CLUSTERED 
( [CustomersDimID] )
) ON [PRIMARY]
;



SET IDENTITY_INSERT dbo.CustomersDim ON
;
INSERT INTO dbo.CustomersDim (CustomersDimID, CustomerID, CompanyDivision, CustomerEmail, CustomerName, CustomerAddress, CustomerZipCode, CustomerCity, CustomerState, CustomerCityState, RowIsCurrent, RowStartDate, RowEndDate, RowChangeReason)
VALUES (-1, -1, '---', 'Missing Data', 'Missing Data', 'Missing Data', '-----', 'Missing Data', '--', 'Missing Data', 1, '1/1/1970', '12/31/9999', 'Missing Data')
;
SET IDENTITY_INSERT dbo.CustomersDim OFF
;



/* Drop table dbo.ProductsDim */
IF EXISTS (SELECT * FROM dbo.sysobjects WHERE id = OBJECT_ID(N'dbo.ProductsDim') AND OBJECTPROPERTY(id, N'IsUserTable') = 1)
DROP TABLE dbo.ProductsDim 
;

/* Create table dbo.ProductsDim */
CREATE TABLE dbo.ProductsDim (
   [ProductsDimID]  INT IDENTITY  NOT NULL
,  [ProductID]  INT   NOT NULL
,  [CompanyDivision]  NVARCHAR(3)   NOT NULL
,  [ProductName]  VARCHAR(50)   NOT NULL
,  [ProductActiveStatus]  BIT   NOT NULL
,  [RowIsCurrent]  BIT   NOT NULL
,  [RowStartDate]  DATE  DEFAULT '1/1/1970' NOT NULL
,  [RowEndDate]  DATE  DEFAULT '12/31/9999' NOT NULL
,  [RowChangeReason]  NVARCHAR(50)   NULL
, CONSTRAINT [PK_dbo.ProductsDim] PRIMARY KEY CLUSTERED 
( [ProductsDimID] )
) ON [PRIMARY]
;



SET IDENTITY_INSERT dbo.ProductsDim ON
;
INSERT INTO dbo.ProductsDim (ProductsDimID, ProductID, CompanyDivision, ProductName, ProductActiveStatus, RowIsCurrent, RowStartDate, RowEndDate, RowChangeReason)
VALUES (-1, -1, '---', 'Missing Data', 1, 1, '1/1/1970', '12/31/9999', 'Missing Data')
;
SET IDENTITY_INSERT dbo.ProductsDim OFF
;


/* Create table dbo.SalesTransactionsFact */
CREATE TABLE dbo.SalesTransactionsFact (
   [CustomersDimID]  INT   NOT NULL
,  [ProductsDimID]  INT   NOT NULL
,  [CompanyDivision]  NVARCHAR(3)   NOT NULL
,  [Quantity]  INT  DEFAULT 0 NOT NULL
,  [PricePerUnit]  DECIMAL(14,2)  DEFAULT 0 NOT NULL
,  [Revenue]  DECIMAL(14,2)  DEFAULT 0 NOT NULL
,  [OrderID]  INT   NOT NULL
,  [ProfitPerUnit]  DECIMAL(14,2)  DEFAULT 0 NOT NULL
,  [Profit]  DECIMAL(14,2)  DEFAULT 0 NOT NULL
,  [SalesDateKey]  INT  DEFAULT -1 NOT NULL
) ON [PRIMARY]
;


ALTER TABLE dbo.SalesTransactionsFact ADD CONSTRAINT
   FK_dbo_SalesTransactionsFact_CustomersDimID FOREIGN KEY
   (
   CustomersDimID
   ) REFERENCES CustomersDim
   ( CustomersDimID )
     ON UPDATE  NO ACTION
     ON DELETE  NO ACTION
;
 
ALTER TABLE dbo.SalesTransactionsFact ADD CONSTRAINT
   FK_dbo_SalesTransactionsFact_ProductsDimID FOREIGN KEY
   (
   ProductsDimID
   ) REFERENCES ProductsDim
   ( ProductsDimID )
     ON UPDATE  NO ACTION
     ON DELETE  NO ACTION
;
 
ALTER TABLE dbo.SalesTransactionsFact ADD CONSTRAINT
   FK_dbo_SalesTransactionsFact_SalesDateKey FOREIGN KEY
   (
   SalesDateKey
   ) REFERENCES DimDate
   ( DateKey )
     ON UPDATE  NO ACTION
     ON DELETE  NO ACTION
;
 
