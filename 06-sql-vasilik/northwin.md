## NorthwindMySQL Database Description

The NorthwindMySQL database is a sample database that represents a fictitious company called Northwind Traders. It contains various tables that store information about customers, orders, products, suppliers, employees, and other related data. The database is commonly used for learning and practicing SQL queries and database management.

### 01 Tables in the NorthwindMySQL Database

    1) Categories. Contains information about product categories.
    2) Customers. Stores details about customers.
    3) Employees. Contains data about employees.
    4) OrderDetails. Stores details about individual order items.
    5) Orders. Contains information about customer orders.
    6) Products. Stores details about products.
    7) Shippers. Contains information about shipping companies.
    8) Suppliers. Stores details about product suppliers.

### 02 Columns in the tables in the NorthwindMySQL Database

#### 01 Categories

+--------------+-------------+------+-----+---------+----------------+
| Field        | Type        | Null | Key | Default | Extra          |
+--------------+-------------+------+-----+---------+----------------+
| CategoryID   | int         | NO   | PRI | NULL    | auto_increment |
| CategoryName | varchar(15) | NO   | UNI | NULL    |                |
| Description  | text        | YES  |     | NULL    |                |
+--------------+-------------+------+-----+---------+----------------+

#### 02 Customers

+--------------+-------------+------+-----+---------+-------+
| Field        | Type        | Null | Key | Default | Extra |
+--------------+-------------+------+-----+---------+-------+
| CustomerID   | varchar(5)  | NO   | PRI | NULL    |       |
| CompanyName  | varchar(40) | NO   | MUL | NULL    |       |
| ContactName  | varchar(30) | YES  |     | NULL    |       |
| ContactTitle | varchar(30) | YES  |     | NULL    |       |
| Address      | varchar(60) | YES  |     | NULL    |       |
| City         | varchar(15) | YES  | MUL | NULL    |       |
| Region       | varchar(15) | YES  | MUL | NULL    |       |
| PostalCode   | varchar(10) | YES  | MUL | NULL    |       |
| Country      | varchar(15) | YES  |     | NULL    |       |
| Phone        | varchar(24) | YES  |     | NULL    |       |
| Fax          | varchar(24) | YES  |     | NULL    |       |
+--------------+-------------+------+-----+---------+-------+

+------------+------------------------------------+--------------------+----------------------+
| CustomerID | CompanyName                        | ContactName        | ContactTitle         |
+------------+------------------------------------+--------------------+----------------------+
| ALFKI      | Alfreds Futterkiste                | Maria Anders       | Sales Representative |
| ANATR      | Ana Trujillo Emparedados y helados | Ana Trujillo       | Owner                |
| ANTON      | Antonio Moreno Taquería            | Antonio Moreno     | Owner                |
| AROUT      | Around the Horn                    | Thomas Hardy       | Sales Representative |
| BERGS      | Berglunds snabbköp                 | Christina Berglund | Order Administrator  |
+------------+------------------------------------+--------------------+----------------------+

#### 03 Employees

+-----------------+--------------+------+-----+---------+----------------+
| Field           | Type         | Null | Key | Default | Extra          |
+-----------------+--------------+------+-----+---------+----------------+
| EmployeeID      | int          | NO   | PRI | NULL    | auto_increment |
| LastName        | varchar(20)  | NO   | MUL | NULL    |                |
| FirstName       | varchar(10)  | NO   |     | NULL    |                |
| Title           | varchar(30)  | YES  |     | NULL    |                |
| TitleOfCourtesy | varchar(25)  | YES  |     | NULL    |                |
| BirthDate       | datetime     | YES  |     | NULL    |                |
| HireDate        | datetime     | YES  |     | NULL    |                |
| Address         | varchar(60)  | YES  |     | NULL    |                |
| City            | varchar(15)  | YES  |     | NULL    |                |
| Region          | varchar(15)  | YES  |     | NULL    |                |
| PostalCode      | varchar(10)  | YES  |     | NULL    |                |
| Country         | varchar(15)  | YES  |     | NULL    |                |
| HomePhone       | varchar(24)  | YES  |     | NULL    |                |
| Extension       | varchar(4)   | YES  |     | NULL    |                |
| Photo           | varchar(255) | YES  |     | NULL    |                |
| Notes           | text         | YES  |     | NULL    |                |
| ReportsTo       | int          | YES  |     | NULL    |                |
| PhotoPath       | varchar(255) | YES  |     | NULL    |                |
+-----------------+--------------+------+-----+---------+----------------+

#### 04 OrderDetails 

+-----------+----------+------+-----+---------+-------+
| Field     | Type     | Null | Key | Default | Extra |
+-----------+----------+------+-----+---------+-------+
| OrderID   | int      | NO   | PRI | NULL    |       |
| ProductID | int      | NO   | PRI | NULL    |       |
| UnitPrice | float    | NO   |     | 0       |       |
| Quantity  | smallint | NO   |     | 1       |       |
| Discount  | float    | NO   |     | 0       |       |
+-----------+----------+------+-----+---------+-------+

+---------+-----------+-----------+----------+----------+
| OrderID | ProductID | UnitPrice | Quantity | Discount |
+---------+-----------+-----------+----------+----------+
|   10248 |        11 |        14 |       12 |        0 |
|   10248 |        42 |       9.8 |       10 |        0 |
|   10248 |        72 |      34.8 |        5 |        0 |
|   10249 |        14 |      18.6 |        9 |        0 |
|   10249 |        51 |      42.4 |       40 |        0 |
+---------+-----------+-----------+----------+----------+

#### 05 Orders

+----------------+-------------+------+-----+---------+----------------+
| Field          | Type        | Null | Key | Default | Extra          |
+----------------+-------------+------+-----+---------+----------------+
| OrderID        | int         | NO   | PRI | NULL    | auto_increment |
| CustomerID     | varchar(5)  | YES  | MUL | NULL    |                |
| EmployeeID     | int         | NO   | MUL | NULL    |                |
| OrderDate      | datetime    | YES  | MUL | NULL    |                |
| RequiredDate   | datetime    | YES  |     | NULL    |                |
| ShippedDate    | datetime    | YES  | MUL | NULL    |                |
| ShipVia        | int         | NO   | MUL | NULL    |                |
| Freight        | float       | YES  |     | 0       |                |
| ShipName       | varchar(40) | YES  |     | NULL    |                |
| ShipAddress    | varchar(60) | YES  |     | NULL    |                |
| ShipCity       | varchar(15) | YES  |     | NULL    |                |
| ShipRegion     | varchar(15) | YES  |     | NULL    |                |
| ShipPostalCode | varchar(10) | YES  | MUL | NULL    |                |
| ShipCountry    | varchar(15) | YES  |     | NULL    |                |
+----------------+-------------+------+-----+---------+----------------+

+---------+------------+------------+---------------------+---------------------+---------+---------------------------+
| OrderID | CustomerID | EmployeeID | OrderDate           | ShippedDate         | ShipVia | ShipName                  |
+---------+------------+------------+---------------------+---------------------+---------+---------------------------+
|   10248 | VINET      |          5 | 2014-07-04 08:00:00 | 2014-07-16 00:00:00 |       3 | Vins et alcools Chevalier |
|   10249 | TOMSP      |          6 | 2014-07-05 04:00:00 | 2014-07-10 00:00:00 |       1 | Toms Spezialitäten        |
|   10250 | HANAR      |          4 | 2014-07-08 15:00:00 | 2014-07-12 00:00:00 |       2 | Hanari Carnes             |
|   10251 | VICTE      |          3 | 2014-07-08 14:00:00 | 2014-07-15 00:00:00 |       1 | Victuailles en stock      |
|   10252 | SUPRD      |          4 | 2014-07-09 01:00:00 | 2014-07-11 00:00:00 |       2 | Suprêmes délices          |
+---------+------------+------------+---------------------+---------------------+---------+---------------------------+

#### 06 Products

+-----------------+-------------+------+-----+---------+----------------+
| Field           | Type        | Null | Key | Default | Extra          |
+-----------------+-------------+------+-----+---------+----------------+
| ProductID       | int         | NO   | PRI | NULL    | auto_increment |
| ProductName     | varchar(40) | NO   | MUL | NULL    |                |
| SupplierID      | int         | NO   | MUL | NULL    |                |
| CategoryID      | int         | NO   | MUL | NULL    |                |
| QuantityPerUnit | varchar(20) | YES  |     | NULL    |                |
| UnitPrice       | float       | YES  |     | 0       |                |
| UnitsInStock    | smallint    | YES  |     | 0       |                |
| UnitsOnOrder    | smallint    | YES  |     | 0       |                |
| ReorderLevel    | smallint    | YES  |     | 0       |                |
| Discontinued    | tinyint     | NO   |     | 0       |                |
+-----------------+-------------+------+-----+---------+----------------+

+-----------+------------------------------+------------+------------+---------------------+-----------+--------------+
| ProductID | ProductName                  | SupplierID | CategoryID | QuantityPerUnit     | UnitPrice | UnitsInStock |
+-----------+------------------------------+------------+------------+---------------------+-----------+--------------+
|         1 | Chai                         |          1 |          1 | 10 boxes x 20 bags  |        18 |           39 |
|         2 | Chang                        |          1 |          1 | 24 - 12 oz bottles  |        19 |           17 |
|         3 | Aniseed Syrup                |          1 |          2 | 12 - 550 ml bottles |        10 |           13 |
|         4 | Chef Anton's Cajun Seasoning |          2 |          2 | 48 - 6 oz jars      |        22 |           53 |
|         5 | Chef Anton's Gumbo Mix       |          2 |          2 | 36 boxes            |     21.35 |            0 |
+-----------+------------------------------+------------+------------+---------------------+-----------+--------------+

#### 07 Shippers

+-------------+-------------+------+-----+---------+----------------+
| Field       | Type        | Null | Key | Default | Extra          |
+-------------+-------------+------+-----+---------+----------------+
| ShipperID   | int         | NO   | PRI | NULL    | auto_increment |
| CompanyName | varchar(40) | NO   |     | NULL    |                |
| Phone       | varchar(24) | YES  |     | NULL    |                |
+-------------+-------------+------+-----+---------+----------------+

+-----------+------------------+----------------+
| ShipperID | CompanyName      | Phone          |
+-----------+------------------+----------------+
|         1 | Speedy Express   | (503) 555-9831 |
|         2 | United Package   | (503) 555-3199 |
|         3 | Federal Shipping | (503) 555-9931 |
+-----------+------------------+----------------+

#### 08 Suppliers

+--------------+--------------+------+-----+---------+----------------+
| Field        | Type         | Null | Key | Default | Extra          |
+--------------+--------------+------+-----+---------+----------------+
| SupplierID   | int          | NO   | PRI | NULL    | auto_increment |
| CompanyName  | varchar(50)  | NO   |     | NULL    |                |
| ContactName  | varchar(50)  | YES  |     | NULL    |                |
| ContactTitle | varchar(50)  | YES  |     | NULL    |                |
| Address      | varchar(60)  | YES  |     | NULL    |                |
| City         | varchar(15)  | YES  |     | NULL    |                |
| Region       | varchar(15)  | YES  |     | NULL    |                |
| PostalCode   | varchar(10)  | YES  |     | NULL    |                |
| Country      | varchar(15)  | YES  |     | NULL    |                |
| Phone        | varchar(24)  | YES  |     | NULL    |                |
| Fax          | varchar(24)  | YES  |     | NULL    |                |
| HomePage     | varchar(100) | YES  |     | NULL    |                |
+--------------+--------------+------+-----+---------+----------------+

+------------+------------------------------------+----------------------------+----------------------+
| SupplierID | CompanyName                        | ContactName                | ContactTitle         |
+------------+------------------------------------+----------------------------+----------------------+
|          1 | Exotic Liquids                     | Charlotte Cooper           | Purchasing Manager   |
|          2 | New Orleans Cajun Delights         | Shelley Burke              | Order Administrator  |
|          3 | Grandma Kelly's Homestead          | Regina Murphy              | Sales Representative |
|          4 | Tokyo Traders                      | Yoshi Nagase               | Marketing Manager    |
|          5 | Cooperativa de Quesos 'Las Cabras' | Antonio del Valle Saavedra | Export Administrator |
+------------+------------------------------------+----------------------------+----------------------+
