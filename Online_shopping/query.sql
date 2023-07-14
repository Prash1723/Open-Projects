# Create table
CREATE TABLE customer_master(ID VARCHAR(10), customer_name VARCHAR(30), transactions INT, last_transaction DATE);

# Insert values
INSERT INTO customer_master VALUES('cust1', 'vijay', 4, '2023/03/12'), ('cust2', 'sushila', 13, '2023/03/21'), ('cust3', 'fernandas', 11, '2022/11/04');
INSERT INTO customer_master VALUES('cust4', 'shubham', 19, '2023/02/15'), ('cust5', 'shivani', 27, '2023/02/01'), ('cust6', 'pooja', 11, '2022/05/24');

# Create transaction table
CREATE TABLE transactions(Transaction_ID VARCHAR(10), Customer_ID VARCHAR(10), Quantity INT, Amount INT);

# Insert transaction data
INSERT INTO transactions VALUES('transact1', 'cust3', 2, 1200), ('transact2',  'cust2', 5, 3450), ('transact3', 'cust4', 1, 500), ('transact4', 'cust3', 1, 304), ('transact5', 'cust1', 1, 13000), ('transact6', 'cust6', 2, 2934),  ('transact7', 'cust5', 9, 9023);

# Analysis
## Calculate total amount by each customer
SELECT a.customer_name, SUM(b.Amount) FROM customer_master a INNER JOIN transactions b on a.ID=b.Customer_ID GROUP BY a.customer_name;

## Calculate the token size of each customer
SELECT a.customer_name, ROUND(SUM(b.Amount)/SUM(b.Quantity), 2) as token_size FROM customer_master a INNER JOIN transactions b on a.ID=b.Customer_ID GROUP BY a.customer_name;
