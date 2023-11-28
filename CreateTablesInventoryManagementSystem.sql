CREATE SCHEMA inventorymanagement;
USE inventorymanagement;

CREATE TABLE Product (
	ProductID 		SMALLINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    ProductName 	VARCHAR(30) NOT NULL,
    Price			DEC(5,2),
    NumSales		SMALLINT UNSIGNED DEFAULT 0,
    NumInStock		SMALLINT UNSIGNED
);

CREATE TABLE Customer (
	CustomerID		SMALLINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    Email			VARCHAR(30) NOT NULL,
    FullName		VARCHAR(30) NOT NULL
);

CREATE TABLE CustomerOrder (
	OrderID			SMALLINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    OrderDate		DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CustomerID		SMALLINT UNSIGNED NOT NULL,
    ProductID		SMALLINT UNSIGNED NOT NULL,
    NumProduct		SMALLINT UNSIGNED NOT NULL,
    OrderTotal		DEC(5,2) NOT NULL,
    FOREIGN KEY(CustomerID) REFERENCES Customer(CustomerID),
    FOREIGN KEY(ProductID) REFERENCES Product(ProductID)
);
