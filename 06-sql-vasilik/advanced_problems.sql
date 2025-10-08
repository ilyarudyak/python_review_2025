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