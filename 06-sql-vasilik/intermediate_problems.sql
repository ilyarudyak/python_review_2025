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
20. Categories, and the total products in each category.
For this problem, we’d like to see the total number of products in each category. 
Sort the results by the total number of products, in descending order.
*/
SELECT
    c.CategoryName,
    COUNT(p.ProductID) AS TotalProducts
FROM
    Categories AS c
    LEFT JOIN
    Products AS p ON c.CategoryID = p.CategoryID
GROUP BY
    c.CategoryID, 
    c.CategoryName
ORDER BY
    TotalProducts DESC;

/*
Actual output:
+----------------+---------------+
| CategoryName   | TotalProducts |
+----------------+---------------+
| Confections    |            13 |
| Beverages      |            12 |
| Condiments     |            12 |
| Seafood        |            12 |
| Dairy Products |            10 |
| Grains/Cereals |             7 |
| Meat/Poultry   |             6 |
| Produce        |             5 |
+----------------+---------------+
8 rows in set (0.00 sec)
*/

/*
21. Total customers per country/city
In the Customers table, show the total number of customers per Country and City.
*/

SELECT
    Country,
    City,
    COUNT(CustomerID) AS TotalCustomers
FROM
    Customers
GROUP BY
    Country,
    City
ORDER BY
    TotalCustomers DESC
LIMIT 10;

/*
Actual output:
+-----------+----------------+----------------+
| Country   | City           | TotalCustomers |
+-----------+----------------+----------------+
| UK        | London         |              6 |
| Mexico    | México D.F.    |              5 |
| Brazil    | Sao Paulo      |              4 |
| Brazil    | Rio de Janeiro |              3 |
| Spain     | Madrid         |              3 |
| Argentina | Buenos Aires   |              3 |
| France    | Paris          |              2 |
| Portugal  | Lisboa         |              2 |
| USA       | Portland       |              2 |
| France    | Nantes         |              2 |
+-----------+----------------+----------------+
10 rows in set (0.00 sec)
*/

/*
22. Products that need reordering
What products do we have in our inventory that should be reordered? For now,
just use the fields UnitsInStock and ReorderLevel, where UnitsInStock is less
than the ReorderLevel, ignoring the fields UnitsOnOrder and Discontinued. Order
the results by ProductID.
*/

SELECT
    ProductID,
    ProductName,
    UnitsInStock,
    ReorderLevel
FROM
    Products
WHERE
    UnitsInStock < ReorderLevel
ORDER BY
    ProductID
LIMIT 10;

/*
Actual output:
+-----------+-----------------------+--------------+--------------+
| ProductID | ProductName           | UnitsInStock | ReorderLevel |
+-----------+-----------------------+--------------+--------------+
|         2 | Chang                 |           17 |           25 |
|         3 | Aniseed Syrup         |           13 |           25 |
|        11 | Queso Cabrales        |           22 |           30 |
|        21 | Sir Rodney's Scones   |            3 |            5 |
|        30 | Nord-Ost Matjeshering |           10 |           15 |
|        31 | Gorgonzola Telino     |            0 |           20 |
|        32 | Mascarpone Fabioli    |            9 |           25 |
|        37 | Gravad lax            |           11 |           25 |
|        43 | Ipoh Coffee           |           17 |           25 |
|        45 | Rogede sild           |            5 |           15 |
+-----------+-----------------------+--------------+--------------+
10 rows in set (0.00 sec)
*/

/*
23. Products that need reordering, continued
Now we need to incorporate these fields—UnitsInStock, UnitsOnOrder,
ReorderLevel, Discontinued—into our calculation. We’ll define products that need
reordering with the following: 
    - UnitsInStock plus UnitsOnOrder are less than or equal to ReorderLevel;
    - The Discontinued flag is false (0).
*/

SELECT
    ProductID,
    ProductName,
    UnitsInStock,
    UnitsOnOrder,
    ReorderLevel,
    Discontinued
FROM
    Products
WHERE
    (UnitsInStock + UnitsOnOrder) <= ReorderLevel
    AND Discontinued = 0
ORDER BY
    ProductID
LIMIT 10;

/*
Actual output:
+-----------+-----------------------+--------------+--------------+--------------+--------------+
| ProductID | ProductName           | UnitsInStock | UnitsOnOrder | ReorderLevel | Discontinued |
+-----------+-----------------------+--------------+--------------+--------------+--------------+
|        30 | Nord-Ost Matjeshering |           10 |            0 |           15 |            0 |
|        70 | Outback Lager         |           15 |           10 |           30 |            0 |
+-----------+-----------------------+--------------+--------------+--------------+--------------+
2 rows in set (0.04 sec)
*/

/*
24. Customer list by region
A salesperson for Northwind is going on a business trip to visit customers, and
would like to see a list of all customers, sorted by region, alphabetically.
However, he wants the customers with no region (null in the Region field) to be
at the end, instead of at the top, where you’d normally find the null values.
Within the same region, companies should be sorted by CustomerID.
*/

SELECT
    CustomerID,
    CompanyName,
    Region
FROM
    Customers
ORDER BY
    (Region IS NULL),  -- This puts NULLs at the end
    Region,
    CustomerID
LIMIT 10;

/*
Actual output:
+------------+-------------------------------+---------------+
| CustomerID | CompanyName                   | Region        |
+------------+-------------------------------+---------------+
| OLDWO      | Old World Delicatessen        | AK            |
| BOTTM      | Bottom-Dollar Markets         | BC            |
| LAUGB      | Laughing Bacchus Wine Cellars | BC            |
| LETSS      | Let's Stop N Shop             | CA            |
| HUN        | Hungry Owl All-Night Grocers  | Co. Cork      |
| GROSR      | GROSELLA-Restaurante          | DF            |
| SAVEA      | Save-a-lot Markets            | ID            |
| ISLAT      | Island Trading                | Isle of Wight |
| LILAS      | LILA-Supermercado             | Lara          |
| THECR      | The Cracker Box               | MT            |
+------------+-------------------------------+---------------+
10 rows in set (0.04 sec)
*/

/*
25. High freight charges
Some of the countries we ship to have very high freight charges. We'd like to
investigate some more shipping options for our customers, to be able to offer
them lower freight charges. Return the three ship countries with the highest
average freight overall, in descending order by average freight.
*/

SELECT
    ShipCountry,
    ROUND(AVG(Freight), 4) AS AvgFreight
FROM
    Orders
GROUP BY
    ShipCountry
ORDER BY
    AvgFreight DESC
LIMIT 3;

/*
Actual output:
+-------------+------------+
| ShipCountry | AvgFreight |
+-------------+------------+
| Austria     |   184.7875 |
| Ireland     |   145.0126 |
| USA         |   112.8794 |
+-------------+------------+
3 rows in set (0.00 sec)
*/

/*
26. High freight charges - 2015
We're continuing on the question above on high freight charges. Now, instead of
using all the orders we have, we only want to see orders from the year 2015.
*/

SELECT
    ShipCountry,
    ROUND(AVG(Freight), 4) AS AvgFreight
FROM
    Orders
WHERE
    YEAR(OrderDate) = 2015
GROUP BY
    ShipCountry
ORDER BY
    AvgFreight DESC
LIMIT 3;

/*
Actual output:
+-------------+------------+
| ShipCountry | AvgFreight |
+-------------+------------+
| Austria     |   178.3643 |
| Switzerland |   117.1775 |
| France      |    113.991 |
+-------------+------------+
3 rows in set (0.01 sec)
*/

/*
27. High freight    charges with between
*/

SELECT 
    ShipCountry,
    ROUND(AVG(Freight), 4) AS AvgFreight
FROM 
    Orders
WHERE
    OrderDate BETWEEN '2015-01-01' AND '2015-12-31'
GROUP BY
    ShipCountry
ORDER BY
    AvgFreight DESC
LIMIT 3;

/*
Actual output:
+-------------+------------+
| ShipCountry | AvgFreight |
+-------------+------------+
| Austria     |   178.3643 |
| Switzerland |   117.1775 |
| Sweden      |     105.16 |
+-------------+------------+
3 rows in set (0.02 sec)
*/

SELECT 
    ShipCountry,
    ROUND(AVG(Freight), 4) AS AvgFreight
FROM 
    Orders
WHERE
    OrderDate BETWEEN '2015-01-01' AND '2015-12-31 23:59:59'
GROUP BY
    ShipCountry
ORDER BY
    AvgFreight DESC
LIMIT 3;

/*
Actual output:
+-------------+------------+
| ShipCountry | AvgFreight |
+-------------+------------+
| Austria     |   178.3643 |
| Switzerland |   117.1775 |
| France      |    113.991 |
+-------------+------------+
3 rows in set (0.00 sec)
*/

/*
28. High freight charges - last year
We're continuing to work on high freight charges. We now want to get the three
ship countries with the highest average freight charges. But instead of
filtering for a particular year, we want to use the last 12 months of order
data, using as the end date the last OrderDate in Orders.
*/

SELECT 
    ShipCountry,
    ROUND(AVG(Freight), 4) AS AvgFreight
FROM 
    Orders
WHERE
    OrderDate BETWEEN DATE_SUB((SELECT MAX(OrderDate) FROM Orders), INTERVAL 1 YEAR) 
                   AND (SELECT MAX(OrderDate) FROM Orders)
GROUP BY
    ShipCountry
ORDER BY
    AvgFreight DESC
LIMIT 3;

/*
Actual output:
+-------------+------------+
| ShipCountry | AvgFreight |
+-------------+------------+
| Ireland     |     200.21 |
| Austria     |   186.4596 |
| USA         |   119.3033 |
+-------------+------------+
3 rows in set (0.07 sec)
*/

/*
29. Inventory list
We're doing inventory, and need to show information like the below:
    EmployeeID, LastName, OrderID, ProductName, Quantity
for all orders. Sort by OrderID and Product ID.
*/

SELECT 
    e.EmployeeID,
    e.LastName,
    o.OrderID,
    p.ProductName,
    od.Quantity
FROM 
    Employees AS e
    JOIN Orders AS o ON e.EmployeeID = o.EmployeeID
    JOIN OrderDetails AS od ON o.OrderID = od.OrderID
    JOIN Products AS p ON od.ProductID = p.ProductID
ORDER BY
    o.OrderID,
    p.ProductID
LIMIT 10;

/*
Actual output:
+------------+-----------+---------+----------------------------------+----------+
| EmployeeID | LastName  | OrderID | ProductName                      | Quantity |
+------------+-----------+---------+----------------------------------+----------+
|          5 | Buchanan  |   10248 | Queso Cabrales                   |       12 |
|          5 | Buchanan  |   10248 | Singaporean Hokkien Fried Mee    |       10 |
|          5 | Buchanan  |   10248 | Mozzarella di Giovanni           |        5 |
|          6 | Suyama    |   10249 | Tofu                             |        9 |
|          6 | Suyama    |   10249 | Manjimup Dried Apples            |       40 |
|          4 | Peacock   |   10250 | Jack's New England Clam Chowder  |       10 |
|          4 | Peacock   |   10250 | Manjimup Dried Apples            |       35 |
|          4 | Peacock   |   10250 | Louisiana Fiery Hot Pepper Sauce |       15 |
|          3 | Leverling |   10251 | Gustaf's Knäckebröd              |        6 |
|          3 | Leverling |   10251 | Ravioli Angelo                   |       15 |
+------------+-----------+---------+----------------------------------+----------+
10 rows in set (0.06 sec)
*/

/*
30. Customers with no orders
There are some customers who have never actually placed an order. Show these
customers.
*/

-- First let's check if for some CustomerID in Orders OrderID is NULL
SELECT
    CustomerID,
    COUNT(OrderID) AS TotalOrders
FROM
    Orders
GROUP BY
    CustomerID
ORDER BY
    TotalOrders
LIMIT 10;

-- Let's use LEFT JOIN to find customers with no orders
SELECT 
    c.CustomerID,
    c.CompanyName,
    o.OrderID
FROM 
    Customers AS c
    LEFT JOIN 
    Orders AS o ON c.CustomerID = o.CustomerID
WHERE
    o.OrderID IS NULL;

/*
Actual output:
+------------+--------------------------------------+---------+
| CustomerID | CompanyName                          | OrderID |
+------------+--------------------------------------+---------+
| FISSA      | FISSA Fabrica Inter. Salchichas S.A. |    NULL |
| PARIS      | Paris spécialités                    |    NULL |
+------------+--------------------------------------+---------+
2 rows in set (0.05 sec)
*/

/*
31. Customers with no orders for EmployeeID 4
One employee (Margaret Peacock, EmployeeID 4) has placed the most orders.
However, there are some customers who've never placed an order with her. Show
only those customers who have never placed an order with her.
*/

-- First let's find the (distinct) customers who PLACED orders with EmployeeID 4
SELECT DISTINCT
    CustomerID  
FROM
    Orders
WHERE
    EmployeeID = 4;

-- Now let's find the NUMBER of (distinct) customers who have placed an order with EmployeeID 4
-- The answer is 75 customers
SELECT 
   COUNT(DISTINCT CustomerID) AS DistinctCustomers
FROM 
   Orders
WHERE 
    EmployeeID = 4;

-- Let's now find the total number of customers
-- The answer is 91 customers, so we should get 91 - 75 = 16 customers for Ex. 31
SELECT 
   COUNT(CustomerID) AS TotalCustomers
FROM 
   Customers;

-- Let's use LEFT JOIN of Customers and Orders first, and later we use a subquery
SELECT 
    c.CustomerID,
    c.CompanyName
FROM 
    Customers AS c
LEFT JOIN 
    Orders AS o ON c.CustomerID = o.CustomerID AND o.EmployeeID = 4
WHERE 
    o.OrderID IS NULL;

/*
Actual output:
+------------+--------------------------------------+
| CustomerID | CompanyName                          |
+------------+--------------------------------------+
| CONSH      | Consolidated Holdings                |
| DUMON      | Du monde entier                      |
| FISSA      | FISSA Fabrica Inter. Salchichas S.A. |
| FRANR      | France restauration                  |
| GROSR      | GROSELLA-Restaurante                 |
| LAUGB      | Laughing Bacchus Wine Cellars        |
| LAZYK      | Lazy K Kountry Store                 |
| NORTS      | North/South                          |
| PARIS      | Paris spécialités                    |
| PERIC      | Pericles Comidas clásicas            |
| PRINI      | Princesa Isabel Vinhos               |
| SANTG      | Santé Gourmet                        |
| SEVES      | Seven Seas Imports                   |
| SPECD      | Spécialités du monde                 |
| THEBI      | The Big Cheese                       |
| VINET      | Vins et alcools Chevalier            |
+------------+--------------------------------------+
16 rows in set (0.01 sec)
*/

/* DEBUGGING the above query 
SELECT 
    c.CustomerID,
    c.CompanyName,
    o.EmployeeID,
    o.OrderID
FROM 
    Customers AS c
    LEFT JOIN 
    Orders AS o ON c.CustomerID = o.CustomerID;

SELECT 
    c.CustomerID,
    c.CompanyName,
    o.EmployeeID,
    o.OrderID
FROM 
    Customers AS c
    LEFT JOIN 
    Orders AS o ON c.CustomerID = o.CustomerID
WHERE o.EmployeeID != 4;

SELECT 
    c.CustomerID,
    c.CompanyName,
    o.EmployeeID,
    o.OrderID
FROM 
    Customers AS c
    LEFT JOIN 
    Orders AS o ON c.CustomerID = o.CustomerID AND o.EmployeeID = 4;

SELECT 
    c.CustomerID,
    c.CompanyName,
    o.EmployeeID,
    o.OrderID
FROM 
    Customers AS c
    LEFT JOIN 
    Orders AS o ON c.CustomerID = o.CustomerID
WHERE 
    c.CustomerID = 'SPECD';
*/

/*
These were intermediate problems from the book.
Next - advanced problems Ex. 32 - 57 (26 problems).
*/