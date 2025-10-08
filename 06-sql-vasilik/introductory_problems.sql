/* Useful commands */
SHOW TABLES;
SHOW COLUMNS FROM Employees;
DESCRIBE Employees; -- show columns in MySQL
SELECT * FROM Employees LIMIT 5;

/*
mysql> SHOW TABLES;
+--------------------------+
| Tables_in_northwindmysql |
+--------------------------+
| Categories               |
| CustomerGroupThresholds  |
| Customers                |
| Employees                |
| OrderDetails             |
| Orders                   |
| Products                 |
| Shippers                 |
| Suppliers                |
+--------------------------+
9 rows in set (0.01 sec)
*/

/*
Some useful commands that were explored in this section of the book are:
1) Logical operators: `=` - equal to (NOT `==`), `!=` - not equal to (the same as <>); 
      AND, OR (different from pandas which uses & and |);
2) Pattern matching with LIKE. It is a basic form of regular expressions.
      There are ONLY two wildcards:
      `%` matches any sequence of characters (including zero characters), 
      `_` matches any single character;
      More complex pattern matching can be done with REGEXP or RLIKE in MySQL;
3) `IN` operator to specify multiple values in a WHERE clause. It is used instead 
      of multiple OR conditions with a list of values: `WHERE column IN (value1, value2, ...)`.
4) There are some useful functions: 
      `DATE()` extracts the date part of a date or datetime expression;
      `TIME()` extracts the time part of a time or datetime expression;
      `CONCAT()` concatenates two or more strings;
      `COUNT()` returns the number of rows that matches a specified criterion;
      `MIN()` returns the smallest value of the selected column;
5) It is possible to have an expression in the SELECT statement, 
      for example: `(UnitPrice * Quantity) AS TotalPrice` (better to use parentheses);
      Here `AS` is used to rename a column or table with an alias (a variable name).
*/

/*
# 1. Which shippers do we have?
We have a table called Shippers. 
Return all the fields from all the shippers
*/
SELECT * FROM Shippers;

/*
# 2. Which orders were shipped by Speedy Express?
In the Categories table, selecting all the fields using this SQL:  
Select * from Categories  
will return 4 columns. 
We only want to see two columns, CategoryName and Description.
*/
SELECT CategoryName, Description 
FROM Categories;

/*
# 3. Sales Representatives
We’d like to see just the FirstName, LastName, and
HireDate of all the employees with the Title of Sales
Representative. Write a SQL statement that returns
only those employees.
*/
SELECT FirstName, LastName, HireDate
FROM Employees
WHERE Title = 'Sales Representative'
LIMIT 5;

/*
# 4. Sales Representatives in the United States
Now we’d like to see the same columns as above, but
only for those employees that both have the title of
Sales Representative, and also are in the United
States.
*/
SELECT FirstName, LastName, HireDate, Title, Country
FROM Employees
WHERE Title = 'Sales Representative' AND 
      Country = 'USA'
LIMIT 5;

/*
# 5. Orders placed by specific EmployeeID
Show all the orders placed by a specific employee.
The EmployeeID for this Employee (Steven
Buchanan) is 5.
*/
SELECT OrderID, OrderDate
FROM Orders
WHERE EmployeeID = 5
LIMIT 5;

/*
# 6. Suppliers and ContactTitles
In the Suppliers table, show the SupplierID,
ContactName, and ContactTitle for those Suppliers
whose ContactTitle is not Marketing Manager.
*/
SELECT SupplierID, ContactName, ContactTitle
FROM Suppliers
WHERE ContactTitle != 'Marketing Manager'
LIMIT 5;

/*
# 7. Products with “queso” in ProductName
In the products table, we’d like to see the ProductID
and ProductName for those products where the
ProductName includes the string “queso”
.*/
SELECT ProductID, ProductName
FROM Products
WHERE ProductName LIKE '%queso%'
LIMIT 5;

/*
# 8. Orders shipping to France or Belgium
Looking at the Orders table, there’s a field called
ShipCountry. Write a query that shows the OrderID,
CustomerID, and ShipCountry for the orders where
the ShipCountry is either France or Belgium.
*/
SELECT OrderID, CustomerID, ShipCountry
FROM Orders
-- WHERE ShipCountry IN ('France', 'Belgium')
WHERE ShipCountry = 'France' OR ShipCountry = 'Belgium'
LIMIT 5;

/*
# 9. Orders shipping to any country in Latin America
Now, instead of just wanting to return all the orders
from France of Belgium, we want to show all the
orders from any Latin American country. But we
don’t have a list of Latin American countries in a
table in the Northwind database. So, we’re going to
just use this list of Latin American countries that
happen to be in the Orders table:
Brazil
Mexico
Argentina
Venezuela
It doesn’t make sense to use multiple Or statements
anymore, it would get too convoluted. Use the In
statement.
*/
SELECT OrderID, CustomerID, ShipCountry
FROM Orders
WHERE ShipCountry IN ('Brazil', 'Mexico', 'Argentina', 'Venezuela')
LIMIT 5;

/*
# 10. Employees, in order of age
For all the employees in the Employees table, show
the FirstName, LastName, Title, and BirthDate.
Order the results by BirthDate, so we have the oldest
employees first.
*/
SELECT FirstName, LastName, Title, BirthDate
FROM Employees
ORDER BY BirthDate ASC
LIMIT 5;

/*
# 11. Showing only the Date with a DATETIME field
In the previous problem 10 we saw the BirthDate field
was a DATETIME field, and so it included the time as
well as the date. We only want to see the date part of
the BirthDate. Use the DATE() function to show only
the date part of the BirthDate.
*/
SELECT 
    FirstName, 
    LastName, 
    Title, 
    DATE(BirthDate) AS BirthDate
FROM 
    Employees
ORDER BY 
    BirthDate ASC
LIMIT 5;

/*
# 12. Employees full name
Show the full name of each employee by concatenating the FirstName and LastName fields.
*/
SELECT 
    FirstName, 
    LastName, 
    CONCAT(FirstName, ' ', LastName) AS FullName
FROM 
    Employees
LIMIT 5;

/*
# 13. OrderDetails amount per line item
Select OrderID
,ProductID
,UnitPrice
,Quantity
,TotalPrice = UnitPrice * Quantity
FROM OrderDetails
Ordered by OrderID, ProductID
*/
SELECT 
    OrderID, 
    ProductID, 
    UnitPrice, 
    Quantity, 
    (UnitPrice * Quantity) AS TotalPrice
FROM 
    OrderDetails
ORDER BY 
    OrderID, ProductID
LIMIT 5;

/*
14. How many customers?
*/
SELECT 
    COUNT(*) AS TotalCustomers
FROM 
    Customers;

/*
15. When was the first order?
*/
SELECT 
    OrderID, 
    MIN(OrderDate) AS FirstOrderDate
FROM 
    Orders;

/*
16. Countries where there are customers
*/
SELECT DISTINCT 
    Country
FROM 
    Customers
ORDER BY 
    Country
LIMIT 5;

/*
17. Contact titles for customers
*/
SELECT 
    ContactTitle, 
    COUNT(*) AS NumberOfTitles
FROM 
    Customers
GROUP BY 
    ContactTitle
ORDER BY 
    NumberOfTitles DESC
LIMIT 5;

/* Expected output:
+----------------------+----------------+
| ContactTitle         | NumberOfTitles |
+----------------------+----------------+
| Sales Representative |             17 |
| Owner                |             17 |
| Marketing Manager    |             12 |
| Sales Manager        |             11 |
| Accounting Manager   |             10 |
+----------------------+----------------+
5 rows in set (0.00 sec)
*/

/*
18. Products with associated supplier names
    1) Show the ProductID, ProductName, and CompanyName AS Supplier for each product.
    2) Use an INNER JOIN to join the Products table to the Suppliers table on the SupplierID field.
    3) Order the results by CompanyName, then by ProductName.
*/

SELECT 
    p.ProductID, 
    p.ProductName, 
    s.CompanyName AS Supplier
FROM 
    Products AS p
    INNER JOIN Suppliers AS s
    ON p.SupplierID = s.SupplierID
ORDER BY 
    s.CompanyName, 
    p.ProductName
LIMIT 5;

/* Expected output:
+-----------+---------------------------+-----------------------------+
| ProductID | ProductName               | Supplier                    |
+-----------+---------------------------+-----------------------------+
|        39 | Chartreuse verte          | Aux joyeux ecclésiastiques  |
|        38 | Côte de Blaye             | Aux joyeux ecclésiastiques  |
|        67 | Laughing Lumberjack Lager | Bigfoot Breweries           |
|        34 | Sasquatch Ale             | Bigfoot Breweries           |
|        35 | Steeleye Stout            | Bigfoot Breweries           |
+-----------+---------------------------+-----------------------------+
5 rows in set (0.04 sec)
*/

/*
19. Orders and the Shipper that was used
    1) SELECT the OrderID, OrderDate, and CompanyName AS Shipper from the Orders table.
    2) Extract the date part of the OrderDate using the DATE() function.
    3) Use an INNER JOIN to join the Orders table to the Shippers table on
            the ShipVia field in Orders and the ShipperID field in Shippers.
    4) OrderID should be less than 10300.
    4) Order the results by OrderID.
    5) Limit the results to 5 rows.
*/

SELECT 
    o.OrderID, 
    DATE(o.OrderDate) AS OrderDate, 
    s.CompanyName AS Shipper
FROM 
    Orders AS o
    INNER JOIN Shippers AS s
    ON o.ShipVia = s.ShipperID
WHERE
    o.OrderID < 10300
ORDER BY 
    o.OrderID
LIMIT 5;

/* Expected output:
+---------+------------+------------------+
| OrderID | OrderDate  | Shipper          |
+---------+------------+------------------+
|   10248 | 2014-07-04 | Federal Shipping |
|   10249 | 2014-07-05 | Speedy Express   |
|   10250 | 2014-07-08 | United Package   |
|   10251 | 2014-07-08 | Speedy Express   |
|   10252 | 2014-07-09 | United Package   |
+---------+------------+------------------+
*/

/*
These were some introductory problems to practice basic SQL queries.
Next we will see some intermediate queries in the file `intermediate_problems.sql`.
*/
