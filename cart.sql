use mysql;
create table cart
(item_id int ,Name varchar(30), category varchar(30), price int,quantity int);
select * from cart;
alter table cart add quantity int;
alter table cart 
change items Name varchar(50);
alter table cart drop id;
alter table cart add id int primary key auto_increment;
alter table cart modify item_id int;
desc cart;
alter table cart add constraint pk_item_id primary key(item_id);



ALTER TABLE cart ADD COLUMN user_mobile_no VARCHAR(15);
truncate table cart;