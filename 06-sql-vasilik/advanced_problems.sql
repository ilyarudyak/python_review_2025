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
32. High-value customers
We want to send all of our high-value customers a special VIP gift. We're
defining high-value customers as those who've made at least 1 order with a total
value (not including the discount) equal to $10,000 or more. We only want to
consider orders made in the year 2016.
*/

-- First, let's compute the net total for each order in 2016
SELECT
    OrderID,
    ROUND(SUM(UnitPrice * Quantity * (1 - Discount)), 2) AS OrderTotal
FROM
    OrderDetails
GROUP BY
    OrderID
LIMIT 5;

-- Let's now filter for orders that are at least $10,000
-- It turns out there are only 10 such orders
SELECT
    OrderID,
    ROUND(SUM(UnitPrice * Quantity * (1 - Discount)), 2) AS OrderTotal
FROM
    OrderDetails
GROUP BY
    OrderID
HAVING
    OrderTotal >= 10000
ORDER BY
    OrderTotal DESC;

/* 
+---------+------------+
| OrderID | OrderTotal |
+---------+------------+
|   10417 |    11188.4 |
|   10479 |    10495.6 |
|   10540 |    10191.7 |
|   10691 |    10164.8 |
|   10817 |   10952.84 |
|   10865 |    16387.5 |
|   10889 |      11380 |
|   10897 |   10835.24 |
|   10981 |      15810 |
|   11030 |   12615.05 |
+---------+------------+
10 rows in set (0.01 sec)
*/

-- Let's filter for orders made in 2016 using OrderDate without a join
SELECT
    o.OrderID
FROM
    Orders AS o
WHERE
    YEAR(o.OrderDate) = 2016
LIMIT 5;

-- Now let's use the first query as a subquery to get the high-value orders in 2016
SELECT
    o.OrderID
FROM
    Orders AS o
WHERE
    YEAR(o.OrderDate) = 2016 AND o.OrderID IN (
        SELECT
            od.OrderID
        FROM
            OrderDetails AS od
        GROUP BY
            od.OrderID
        HAVING
            SUM(od.UnitPrice * od.Quantity * (1 - od.Discount)) >= 10000
    );

/*
Actual results:
+---------+
| OrderID |
+---------+
|   10817 |
|   10865 |
|   10889 |
|   10897 |
|   10981 |
|   11030 |
+---------+
6 rows in set (0.00 sec)
*/

-- Finally, let's get the customer details for these orders
SELECT
    c.CustomerID,
    c.CompanyName,
    o.OrderID
FROM 
    Orders AS o
    JOIN
    Customers AS c ON o.CustomerID = c.CustomerID
WHERE
    o.OrderID IN (
        SELECT
            o.OrderID
        FROM
            Orders AS o
        WHERE
            YEAR(o.OrderDate) = 2016 AND o.OrderID IN (
                SELECT
                    od.OrderID
                FROM
                    OrderDetails AS od
                GROUP BY
                    od.OrderID
                HAVING
                    SUM(od.UnitPrice * od.Quantity * (1 - od.Discount)) >= 10000
            )
    )
ORDER BY
    o.OrderID;

/*
Actual results:
+------------+------------------------------+---------+
| CustomerID | CompanyName                  | OrderID |
+------------+------------------------------+---------+
| KOENE      | Königlich Essen              |   10817 |
| QUICK      | QUICK-Stop                   |   10865 |
| RATTC      | Rattlesnake Canyon Grocery   |   10889 |
| HUN        | Hungry Owl All-Night Grocers |   10897 |
| HANAR      | Hanari Carnes                |   10981 |
| SAVEA      | Save-a-lot Markets           |   11030 |
+------------+------------------------------+---------+
6 rows in set (0.01 sec)
*/

-- Version with Joins only
SELECT DISTINCT
    c.CustomerID,
    c.CompanyName
FROM 
    Customers AS c
    JOIN 
    Orders AS o ON c.CustomerID = o.CustomerID
    JOIN 
    OrderDetails AS od ON o.OrderID = od.OrderID
WHERE 
    YEAR(o.OrderDate) = 2016
GROUP BY 
    o.OrderID 
    -- c.CustomerID, 
    -- c.CompanyName
HAVING 
    SUM(od.UnitPrice * od.Quantity * (1 - od.Discount)) >= 10000
ORDER BY 
    c.CustomerID;

/*
33. High-value customers - total orders
The manager has changed his mind. Instead of requiring that customers have at
least one individual orders totaling $10,000 or more, he wants to define high-
value customers as those who have orders totaling $15,000 or more in 2016. How
would you change the answer to the problem above?
*/

SELECT
    c.CustomerID,
    c.CompanyName,
    ROUND(SUM(od.UnitPrice * od.Quantity), 2) AS TotalOrders
FROM 
    Customers AS c
    JOIN 
    Orders AS o ON c.CustomerID = o.CustomerID
    JOIN 
    OrderDetails AS od ON o.OrderID = od.OrderID
WHERE 
    YEAR(o.OrderDate) = 2016
GROUP BY 
    -- o.OrderID 
    c.CustomerID
    -- c.CompanyName
HAVING 
    TotalOrders >= 15000
ORDER BY 
    TotalOrders DESC;

/*
34. High-value customers - with discount
Change the above query to use the discount when calculating high-value
customers. Order by the total amount which includes the discount.
*/

SELECT
    c.CustomerID,
    c.CompanyName,
    ROUND(SUM(od.UnitPrice * od.Quantity), 2) AS TotalOrders,
    ROUND(SUM(od.UnitPrice * od.Quantity * (1 - od.Discount)), 2) AS TotalWithDiscount
FROM 
    Customers AS c
    JOIN 
    Orders AS o ON c.CustomerID = o.CustomerID
    JOIN 
    OrderDetails AS od ON o.OrderID = od.OrderID
WHERE 
    YEAR(o.OrderDate) = 2016
GROUP BY 
    -- o.OrderID 
    c.CustomerID,
    c.CompanyName
HAVING 
    TotalWithDiscount >= 10000
ORDER BY 
    TotalWithDiscount DESC;

/*
Actual results:
+------------+------------------------------+-------------+-------------------+
| CustomerID | CompanyName                  | TotalOrders | TotalWithDiscount |
+------------+------------------------------+-------------+-------------------+
| ERNSH      | Ernst Handel                 |     42598.9 |          41210.65 |
| QUICK      | QUICK-Stop                   |    40526.99 |          37217.31 |
| SAVEA      | Save-a-lot Markets           |    42806.25 |          36310.11 |
| HANAR      | Hanari Carnes                |    24238.05 |           23821.2 |
| RATTC      | Rattlesnake Canyon Grocery   |     21725.6 |          21238.27 |
| HUN        | Hungry Owl All-Night Grocers |    22796.34 |          20402.12 |
| KOENE      | Königlich Essen              |    20204.95 |          19582.77 |
| WHITC      | White Clover Markets         |     15278.9 |           15278.9 |
| FOLKO      | Folk och fä HB               |    15973.85 |          13644.07 |
| SUPRD      | Suprêmes délices             |     11862.5 |           11644.6 |
| BOTTM      | Bottom-Dollar Markets        |     12227.4 |          11338.55 |
+------------+------------------------------+-------------+-------------------+
11 rows in set (0.06 sec)
*/

/*
35. Month-end orders
At the end of the month, salespeople are likely to try much harder to get
orders, to meet their month-end quotas. Show all orders made on the last day of
the month. Order by EmployeeID and OrderID.
*/

-- First, let's find the last day of each month in 2016
SELECT
    o.OrderDate,
    MONTH(o.OrderDate) AS OrderMonth,
    LAST_DAY(o.OrderDate) AS LastDay
FROM
    Orders AS o
LIMIT 5;

-- Let's filter for orders made on the last day of the month
SELECT
    o.OrderID,
    LAST_DAY(o.OrderDate) AS LastDay
FROM
    Orders AS o
WHERE
    DATE(o.OrderDate) = LAST_DAY(o.OrderDate)
LIMIT 5;

-- Let's finalize the query by ordering the results
SELECT
    o.EmployeeID,
    o.OrderID,
    o.OrderDate
FROM
    Orders AS o
WHERE
    DATE(o.OrderDate) = LAST_DAY(o.OrderDate)
ORDER BY 
    o.EmployeeID, 
    o.OrderID
LIMIT 5;

/*
Actual results:
+------------+---------+---------------------+
| EmployeeID | OrderID | OrderDate           |
+------------+---------+---------------------+
|          1 |   10461 | 2015-02-28 00:00:00 |
|          1 |   10616 | 2015-07-31 00:00:00 |
|          2 |   10583 | 2015-06-30 00:00:00 |
|          2 |   10686 | 2015-09-30 00:00:00 |
|          2 |   10989 | 2016-03-31 00:00:00 |
+------------+---------+---------------------+
5 rows in set (0.05 sec)
*/

/*
36. Orders with many line items
The Northwind mobile app developers are testing an app that customers will use
to show orders. In order to make sure that even the largest orders will show up
correctly on the app, they'd like some samples of orders that have lots of
individual line items. Show the 10 orders with the most line items, in order of
total line items.
*/

-- First, let's count the number of line items per order
SELECT
    od.OrderID,
    COUNT(od.ProductID) AS NumLineItems
FROM
    OrderDetails AS od
GROUP BY
    od.OrderID
LIMIT 10;

-- Let's order the results by number of line items
SELECT
    od.OrderID,
    COUNT(od.ProductID) AS NumLineItems
FROM
    OrderDetails AS od
GROUP BY
    od.OrderID
ORDER BY
    NumLineItems DESC
LIMIT 10;

/*
Actual results:
+---------+--------------+
| OrderID | NumLineItems |
+---------+--------------+
|   11077 |           25 |
|   10979 |            6 |
|   10657 |            6 |
|   10847 |            6 |
|   10393 |            5 |
|   10294 |            5 |
|   10324 |            5 |
|   10273 |            5 |
|   10337 |            5 |
|   10360 |            5 |
+---------+--------------+
10 rows in set (0.01 sec)
*/

/*
37. Orders - random assortment
The Northwind mobile app developers would now like to just get a random
assortment of orders for beta testing on their app. Show a random set of 2% of
all orders.
*/

SELECT
    o.OrderID,
    o.OrderDate
FROM
    Orders AS o
WHERE RAND() <= 0.02;

/*
38. Orders - accidental double-entry
Janet Leverling, one of the salespeople, has come to you with a request. She
thinks that she accidentally double-entered a line item on an order, with a
different ProductID, but the same quantity. She remembers that the quantity was
60 or more. Show all the OrderIDs with line items that match this, in order of
OrderID.
*/

-- Start with all orders by Janet Leverling
SELECT
    o.OrderID
FROM
    Orders AS o
    JOIN Employees AS e ON o.EmployeeID = e.EmployeeID
WHERE
    e.FirstName = 'Janet' AND e.LastName = 'Leverling'
LIMIT 5;

-- Now let's also join with OrderDetails to get the line items
SELECT
    o.OrderID,
    od.ProductID,
    od.Quantity
FROM
    Orders AS o
    JOIN Employees AS e ON o.EmployeeID = e.EmployeeID
    JOIN OrderDetails AS od ON o.OrderID = od.OrderID
WHERE
    e.FirstName = 'Janet' AND e.LastName = 'Leverling'
LIMIT 5;

-- Now let's filter for line items with quantity >= 60
SELECT
    o.OrderID,
    od.ProductID,
    od.Quantity
FROM
    Orders AS o
    JOIN Employees AS e ON o.EmployeeID = e.EmployeeID
    JOIN OrderDetails AS od ON o.OrderID = od.OrderID
WHERE
    e.FirstName = 'Janet' 
    AND 
    e.LastName = 'Leverling' 
    AND 
    od.Quantity >= 60
LIMIT 5;

/* 
Only 25 such entries exist
+---------+-----------+----------+
| OrderID | ProductID | Quantity |
+---------+-----------+----------+
|   10273 |        40 |       60 |
|   10442 |        54 |       80 |
|   10442 |        66 |       60 |
|   10479 |        59 |       60 |
|   10492 |        25 |       60 |
|   10514 |        56 |       70 |
|   10540 |         3 |       60 |
|   10547 |        36 |       60 |
|   10570 |        56 |       60 |
|   10638 |        72 |       60 |
|   10693 |        54 |       60 |
|   10700 |        71 |       60 |
|   10758 |        52 |       60 |
|   10762 |        56 |       60 |
|   10765 |        65 |       80 |
|   10817 |        40 |       60 |
|   10854 |        10 |      100 |
|   10854 |        13 |       65 |
|   10895 |        24 |      110 |
|   10895 |        40 |       91 |
|   10895 |        60 |      100 |
|   10897 |        29 |       80 |
|   10918 |         1 |       60 |
|   10988 |         7 |       60 |
|   11021 |        26 |       63 |
+---------+-----------+----------+
25 rows in set (0.00 sec)
*/

-- Now let's find the OrderIDs with multiple such line items
SELECT
    o.OrderID
FROM
    Orders AS o
    JOIN Employees AS e ON o.EmployeeID = e.EmployeeID
    JOIN OrderDetails AS od ON o.OrderID = od.OrderID
WHERE
    e.FirstName = 'Janet' 
    AND 
    e.LastName = 'Leverling' 
    AND 
    od.Quantity >= 60
GROUP BY
    o.OrderID
HAVING
    COUNT(od.ProductID) > 1
LIMIT 5;

/*
Actual results:
+---------+
| OrderID |
+---------+
|   10442 |
|   10854 |
|   10895 |
+---------+
3 rows in set (0.02 sec)
*/

/*
39. Orders - accidental double-entry details
Based on the previous question, we now want to show details of the order, for
orders that match the above criteria. Show OrderID, ProductID, UnitPrice, 
Quantity and Discount.
*/

-- We just need to use the previous query as a subquery
SELECT
    o.OrderID,
    od.ProductID,
    od.UnitPrice,
    od.Quantity,
    od.Discount
FROM
    Orders AS o
    JOIN Employees AS e ON o.EmployeeID = e.EmployeeID
    JOIN OrderDetails AS od ON o.OrderID = od.OrderID
WHERE
    o.OrderID IN (
        SELECT
            o.OrderID
        FROM
            Orders AS o
            JOIN Employees AS e ON o.EmployeeID = e.EmployeeID
            JOIN OrderDetails AS od ON o.OrderID = od.OrderID
        WHERE
            e.FirstName = 'Janet' 
            AND 
            e.LastName = 'Leverling' 
            AND 
            od.Quantity >= 60
        GROUP BY
            o.OrderID
        HAVING
            COUNT(od.ProductID) > 1
    );

/*
Actual results:
+---------+-----------+-----------+----------+----------+
| OrderID | ProductID | UnitPrice | Quantity | Discount |
+---------+-----------+-----------+----------+----------+
|   10442 |        11 |      16.8 |       30 |        0 |
|   10442 |        54 |       5.9 |       80 |        0 |
|   10442 |        66 |      13.6 |       60 |        0 |
|   10854 |        10 |        31 |      100 |     0.15 |
|   10854 |        13 |         6 |       65 |     0.15 |
|   10895 |        24 |       4.5 |      110 |        0 |
|   10895 |        39 |        18 |       45 |        0 |
|   10895 |        40 |      18.4 |       91 |        0 |
|   10895 |        60 |        34 |      100 |        0 |
+---------+-----------+-----------+----------+----------+
9 rows in set (0.08 sec)
*/

/*
41. Late orders
Some customers are complaining about their orders arriving late. Which orders
are late?
*/

-- First, let's see the relevant columns in Orders table
SELECT 
    o.OrderID,
    o.OrderDate,
    o.RequiredDate,
    o.ShippedDate
FROM 
    Orders AS o
LIMIT 5;

/*
+---------+---------------------+---------------------+---------------------+
| OrderID | OrderDate           | RequiredDate        | ShippedDate         |
+---------+---------------------+---------------------+---------------------+
|   10248 | 2014-07-04 08:00:00 | 2014-08-01 00:00:00 | 2014-07-16 00:00:00 |
|   10249 | 2014-07-05 04:00:00 | 2014-08-16 00:00:00 | 2014-07-10 00:00:00 |
|   10250 | 2014-07-08 15:00:00 | 2014-08-05 00:00:00 | 2014-07-12 00:00:00 |
|   10251 | 2014-07-08 14:00:00 | 2014-08-05 00:00:00 | 2014-07-15 00:00:00 |
|   10252 | 2014-07-09 01:00:00 | 2014-08-06 00:00:00 | 2014-07-11 00:00:00 |
+---------+---------------------+---------------------+---------------------+
5 rows in set (0.04 sec)
*/

-- Let's filter for late orders where ShippedDate is strictly after RequiredDate
-- In the book they use >= but that would also include orders shipped on the required date
SELECT 
    o.OrderID,
    o.OrderDate,
    o.RequiredDate,
    o.ShippedDate
FROM 
    Orders AS o
WHERE
    o.ShippedDate > o.RequiredDate
LIMIT 5;

/*
42. Late orders - which employees?
Some salespeople have more orders arriving late than others. Maybe they're not
following up on the order process, and need more training. Which salespeople
have the most orders arriving late?
*/

SELECT
    e.EmployeeID,
    e.FirstName,
    e.LastName,
    COUNT(o.OrderID) AS LateOrderCount
FROM
    Orders AS o
    JOIN Employees AS e ON o.EmployeeID = e.EmployeeID
WHERE
    o.ShippedDate > o.RequiredDate
GROUP BY
    e.EmployeeID
ORDER BY
    LateOrderCount DESC
LIMIT 5;

/* 
+------------+-----------+-----------+----------------+
| EmployeeID | FirstName | LastName  | LateOrderCount |
+------------+-----------+-----------+----------------+
|          4 | Margaret  | Peacock   |             10 |
|          3 | Janet     | Leverling |              5 |
|          2 | Andrew    | Fuller    |              4 |
|          7 | Robert    | King      |              4 |
|          8 | Laura     | Callahan  |              4 |
|          9 | Anne      | Dodsworth |              4 |
|          6 | Michael   | Suyama    |              3 |
|          1 | Nancy     | Davolio   |              2 |
+------------+-----------+-----------+----------------+
8 rows in set (0.00 sec)
*/

/*
43. Late orders vs. total orders
Andrew, the VP of sales, has been doing some more thinking some more about the
problem of late orders. He realizes that just looking at the number of orders
arriving late for each salesperson isn't a good idea. It needs to be compared
against the total number of orders per salesperson.
*/

-- Let's use conditional aggregation to get both counts in one query
SELECT
    e.EmployeeID,
    e.FirstName,
    e.LastName,
    COUNT(o.OrderID) AS TotalOrders,
    SUM(CASE WHEN o.ShippedDate > o.RequiredDate THEN 1 ELSE 0 END) AS LateOrders
FROM
    Orders AS o
    JOIN Employees AS e ON o.EmployeeID = e.EmployeeID
GROUP BY
    e.EmployeeID
ORDER BY
    LateOrders DESC,
    TotalOrders DESC
LIMIT 10;
/*
Actual results:
+------------+-----------+-----------+-------------+------------+
| EmployeeID | FirstName | LastName  | TotalOrders | LateOrders |
+------------+-----------+-----------+-------------+------------+
|          4 | Margaret  | Peacock   |         156 |         10 |
|          3 | Janet     | Leverling |         127 |          5 |
|          8 | Laura     | Callahan  |         104 |          4 |
|          2 | Andrew    | Fuller    |          96 |          4 |
|          7 | Robert    | King      |          72 |          4 |
|          9 | Anne      | Dodsworth |          43 |          4 |
|          6 | Michael   | Suyama    |          67 |          3 |
|          1 | Nancy     | Davolio   |         123 |          2 |
|          5 | Steven    | Buchanan  |          42 |          0 |
+------------+-----------+-----------+-------------+------------+
9 rows in set (0.00 sec)
*/

/*
48. Customer grouping
Andrew Fuller, the VP of sales at Northwind, would like to do a sales campaign
for existing customers. He'd like to categorize customers into groups, based on
how much they ordered in 2016. Then, depending on which group the customer is
in, he will target the customer with different sales materials. The customer
grouping categories are 0 to 1,000, 1,000 to 5,000, 5,000 to 10,000, and over
10,000. A good starting point for this query is the answer from the problem
High-value customers - total orders. We don’t want to show customers who don’t
have any orders in 2016. Order the results by CustomerID.
*/

-- Let's first compute the total orders per customer in 2016
SELECT
    c.CustomerID,
    c.CompanyName,
    ROUND(SUM(od.UnitPrice * od.Quantity), 2) AS TotalOrders
FROM
    Customers AS c
    JOIN Orders AS o ON c.CustomerID = o.CustomerID
    JOIN OrderDetails AS od ON o.OrderID = od.OrderID
WHERE
    YEAR(o.OrderDate) = 2016
GROUP BY
    c.CustomerID,
    c.CompanyName
ORDER BY
    c.CustomerID
LIMIT 5;

-- Let's finalize the query by adding the CASE statement for grouping
SELECT
    c.CustomerID,
    c.CompanyName,
    ROUND(SUM(od.UnitPrice * od.Quantity), 2) AS TotalOrders,
    CASE 
        WHEN ROUND(SUM(od.UnitPrice * od.Quantity), 2) BETWEEN 0 AND 1000 THEN 'Low'
        WHEN ROUND(SUM(od.UnitPrice * od.Quantity), 2) BETWEEN 1000 AND 5000 THEN 'Medium'
        WHEN ROUND(SUM(od.UnitPrice * od.Quantity), 2) BETWEEN 5000 AND 10000 THEN 'High'
        ELSE 'Very High'
    END AS CustomerGroup
FROM
    Customers AS c
    JOIN Orders AS o ON c.CustomerID = o.CustomerID
    JOIN OrderDetails AS od ON o.OrderID = od.OrderID
WHERE
    YEAR(o.OrderDate) = 2016
GROUP BY
    c.CustomerID,
    c.CompanyName
ORDER BY
    c.CustomerID
LIMIT 5;

/*
Actual results:
+------------+------------------------------------+-------------+---------------+
| CustomerID | CompanyName                        | TotalOrders | CustomerGroup |
+------------+------------------------------------+-------------+---------------+
| ALFKI      | Alfreds Futterkiste                |      2302.2 | Medium        |
| ANATR      | Ana Trujillo Emparedados y helados |       514.4 | Low           |
| ANTON      | Antonio Moreno Taquería            |         660 | Low           |
| AROUT      | Around the Horn                    |      5838.5 | High          |
| BERGS      | Berglunds snabbköp                 |     8110.55 | High          |
+------------+------------------------------------+-------------+---------------+
5 rows in set (0.06 sec)
*/

/*
50. Customer grouping with percentage
Based on the above query, show all the defined CustomerGroups, and the
percentage in each. Sort by the total in each group, in descending order.

Expected output:
CustomerGroup TotalInGroup PercentageInGroup
------------- ------------ ------------------
Medium         35           0.432098765432 
Low            20           0.246913580246 
High           13           0.160493827160 
Very High      13           0.160493827160 

(4 row(s) affected)
*/

-- Let's use the previous query as a subquery and start from grouping by CustomerGroup
SELECT
    CustomerGroup,
    COUNT(CustomerID) AS TotalInGroup
FROM
    (
        SELECT
            c.CustomerID,
            c.CompanyName,
            ROUND(SUM(od.UnitPrice * od.Quantity), 2) AS TotalOrders,
            CASE 
                WHEN ROUND(SUM(od.UnitPrice * od.Quantity), 2) BETWEEN 0 AND 1000 THEN 'Low'
                WHEN ROUND(SUM(od.UnitPrice * od.Quantity   ), 2) BETWEEN 1000 AND 5000 THEN 'Medium'
                WHEN ROUND(SUM(od.UnitPrice * od.Quantity), 2) BETWEEN 5000 AND 10000 THEN 'High'
                ELSE 'Very High'
            END AS CustomerGroup
        FROM
            Customers AS c
            JOIN Orders AS o ON c.CustomerID = o.CustomerID
            JOIN OrderDetails AS od ON o.OrderID = od.OrderID
        WHERE
            YEAR(o.OrderDate) = 2016
        GROUP BY
            c.CustomerID,
            c.CompanyName
    ) AS CustomerTotals
GROUP BY
    CustomerGroup
ORDER BY
    TotalInGroup DESC;

-- Let's finalize the query by adding the percentage calculation
SELECT
    CustomerGroup,
    COUNT(CustomerID) AS TotalInGroup,
    COUNT(CustomerID) / (SELECT COUNT(*) FROM Customers) AS PercentageInGroup
FROM
    (
        SELECT
            c.CustomerID,
            c.CompanyName,
            ROUND(SUM(od.UnitPrice * od.Quantity), 2) AS TotalOrders,
            CASE
                WHEN ROUND(SUM(od.UnitPrice * od.Quantity), 2) BETWEEN 0 AND 1000 THEN 'Low'
                WHEN ROUND(SUM(od.UnitPrice * od.Quantity), 2) BETWEEN 1000 AND 5000 THEN 'Medium'
                WHEN ROUND(SUM(od.UnitPrice * od.Quantity), 2) BETWEEN 5000 AND 10000 THEN 'High'
                ELSE 'Very High'
            END AS CustomerGroup
        FROM
            Customers AS c
            JOIN Orders AS o ON c.CustomerID = o.CustomerID
            JOIN OrderDetails AS od ON o.OrderID = od.OrderID
        WHERE
            YEAR(o.OrderDate) = 2016
        GROUP BY
            c.CustomerID,
            c.CompanyName
    ) AS CustomerTotals
GROUP BY
    CustomerGroup
ORDER BY
    TotalInGroup DESC;

-- Let;s do the same with a temporary table
CREATE TEMPORARY TABLE CustomerTotals AS (
    SELECT
        c.CustomerID,
        c.CompanyName,
        ROUND(SUM(od.UnitPrice * od.Quantity), 2) AS TotalOrders,
        CASE
            WHEN ROUND(SUM(od.UnitPrice * od.Quantity), 2) BETWEEN 0 AND 1000 THEN 'Low'
            WHEN ROUND(SUM(od.UnitPrice * od.Quantity), 2) BETWEEN 1000 AND 5000 THEN 'Medium'
            WHEN ROUND(SUM(od.UnitPrice * od.Quantity), 2) BETWEEN 5000 AND 10000 THEN 'High'
            ELSE 'Very High'
        END AS CustomerGroup
    FROM
        Customers AS c
        JOIN Orders AS o ON c.CustomerID = o.CustomerID
        JOIN OrderDetails AS od ON o.OrderID = od.OrderID
    WHERE
        YEAR(o.OrderDate) = 2016
    GROUP BY
        c.CustomerID,
        c.CompanyName 
);

SELECT
    CustomerGroup,
    COUNT(CustomerID) AS TotalInGroup,
    COUNT(CustomerID) / (SELECT COUNT(*) FROM Customers) AS PercentageInGroup
FROM
    CustomerTotals
GROUP BY
    CustomerGroup
ORDER BY
    TotalInGroup DESC;

/*
Actual results:
+---------------+--------------+-------------------+
| CustomerGroup | TotalInGroup | PercentageInGroup |
+---------------+--------------+-------------------+
| Medium        |           35 |            0.3846 |
| Low           |           20 |            0.2198 |
| High          |           13 |            0.1429 |
| Very High     |           13 |            0.1429 |
+---------------+--------------+-------------------+
4 rows in set (0.00 sec)
*/

/*
51. Customer grouping - flexible
Andrew, the VP of Sales is still thinking about how best to group customers, and
define low, medium, high, and very high value customers. He now wants complete
flexibility in grouping the customers, based on the dollar amount they've
ordered. He doesn’t want to have to edit SQL in order to change the boundaries
of the customer groups. How would you write the SQL? There's a table called
CustomerGroupThreshold that you will need to use. Use only orders from 2016.
*/

-- First, let's see the contents of the CustomerGroupThresholds table
/*
mysql> DESCRIBE CustomerGroupThresholds;
+-------------------+---------------+------+-----+---------+-------+
| Field             | Type          | Null | Key | Default | Extra |
+-------------------+---------------+------+-----+---------+-------+
| CustomerGroupName | varchar(20)   | YES  |     | NULL    |       |
| RangeBottom       | decimal(16,5) | YES  |     | NULL    |       |
| RangeTop          | decimal(20,5) | YES  |     | NULL    |       |
+-------------------+---------------+------+-----+---------+-------+
3 rows in set (0.03 sec)

mysql> SELECT * FROM CustomerGroupThresholds;
+-------------------+-------------+-----------------------+
| CustomerGroupName | RangeBottom | RangeTop              |
+-------------------+-------------+-----------------------+
| Low               |     0.00000 |             999.99990 |
| Medium            |  1000.00000 |            4999.99990 |
| High              |  5000.00000 |            9999.99990 |
| Very High         | 10000.00000 | 922337203685477.58070 |
+-------------------+-------------+-----------------------+
4 rows in set (0.01 sec)
*/

-- Let's first prepare a temporary table with the customer totals. We group by
-- CustomerID and sum the total orders without discount. We use orders from 2016 only.

-- CustomerTotals temporary table already exists from previous query, so we need to drop it first
DROP TEMPORARY TABLE IF EXISTS CustomerTotals;
CREATE TEMPORARY TABLE CustomerTotals AS (
    SELECT
        c.CustomerID,
        c.CompanyName,
        ROUND(SUM(od.UnitPrice * od.Quantity), 2) AS TotalOrders
    FROM
        Customers AS c
        JOIN Orders AS o ON c.CustomerID = o.CustomerID
        JOIN OrderDetails AS od ON o.OrderID = od.OrderID
    WHERE
        YEAR(o.OrderDate) = 2016
    GROUP BY
        c.CustomerID,
        c.CompanyName
);

-- (1) Using a conditional join: ON ct.TotalOrders BETWEEN cgt.RangeBottom AND cgt.RangeTop
SELECT
    ct.CustomerID,
    ct.CompanyName,
    ct.TotalOrders,
    cgt.CustomerGroupName
FROM
    CustomerTotals AS ct
    JOIN CustomerGroupThresholds AS cgt ON 
        ct.TotalOrders BETWEEN cgt.RangeBottom AND cgt.RangeTop
LIMIT 5;

/*
Actual results:
+------------+------------------------------------+-------------+-------------------+
| CustomerID | CompanyName                        | TotalOrders | CustomerGroupName |
+------------+------------------------------------+-------------+-------------------+
| ALFKI      | Alfreds Futterkiste                |      2302.2 | Medium            |
| ANATR      | Ana Trujillo Emparedados y helados |       514.4 | Low               |
| ANTON      | Antonio Moreno Taquería            |         660 | Low               |
| AROUT      | Around the Horn                    |      5838.5 | High              |
| BSBEV      | B's Beverages                      |        2431 | Medium            |
+------------+------------------------------------+-------------+-------------------+
5 rows in set (0.00 sec)
*/

-- (2) Using a CASE in SELECT with a correlated subquery
SELECT
    ct.CustomerID,
    ct.CompanyName,
    ct.TotalOrders,
    (SELECT
        cgt.CustomerGroupName
    FROM
        CustomerGroupThresholds AS cgt
    WHERE
        ct.TotalOrders BETWEEN cgt.RangeBottom AND cgt.RangeTop
    LIMIT 1
    ) AS CustomerGroupName
FROM
    CustomerTotals AS ct
LIMIT 5;

/*
Actual results:
+------------+------------------------------------+-------------+-------------------+
| CustomerID | CompanyName                        | TotalOrders | CustomerGroupName |
+------------+------------------------------------+-------------+-------------------+
| ALFKI      | Alfreds Futterkiste                |      2302.2 | Medium            |
| ANATR      | Ana Trujillo Emparedados y helados |       514.4 | Low               |
| ANTON      | Antonio Moreno Taquería            |         660 | Low               |
| AROUT      | Around the Horn                    |      5838.5 | High              |
| BSBEV      | B's Beverages                      |        2431 | Medium            |
+------------+------------------------------------+-------------+-------------------+
5 rows in set (0.04 sec)
*/

/*
52. Countries with suppliers or customers
Some Northwind employees are planning a business trip, and would like to visit
as many suppliers and customers as possible. For their planning, they’d like to
see a list of all countries where suppliers and/or customers are based.
*/

-- Let's first create a table with countries with customers and suppliers.
-- It should contain 2 columns: Country and Source (Customer or Supplier)
SELECT
    c.Country,
    'Customer' AS Source
FROM
    Customers AS c
UNION
SELECT
    s.Country,
    'Supplier' AS Source
FROM
    Suppliers AS s
ORDER BY
    Source, 
    Country ASC
LIMIT 5;

-- Let's create another variant of this table. 
-- It should contain 3 columns: Country, HasCustomer (Yes/No), HasSupplier (Yes/No)
SELECT
    Country,
    'Yes' AS HasCustomer,
    'No' AS HasSupplier
FROM
    Customers AS c
UNION
SELECT
    Country,
    'No' AS HasCustomer,
    'Yes' AS HasSupplier
FROM
    Suppliers AS s
ORDER BY
    Country ASC
LIMIT 5;
