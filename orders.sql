use mysql;
CREATE TABLE orders (order_id INT AUTO_INCREMENT PRIMARY KEY,user_name VARCHAR(50),user_mobile_no VARCHAR(15),
item_name VARCHAR(100),category VARCHAR(50),quantity INT,price FLOAT,total FLOAT);
select * from orders;
alter table orders drop order_id;
ALTER TABLE orders ADD order_date DATE DEFAULT (CURDATE());
drop table orders;
ALTER TABLE orders MODIFY order_date DATE;
desc orders;

UPDATE orders SET order_date = CURDATE() WHERE order_date IS NULL;
ALTER TABLE orders 
MODIFY order_date DATE NOT NULL DEFAULT (CURDATE());

