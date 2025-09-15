use mysql;
create table menu_card
(item_id int primary key,items varchar(30),category varchar(30),price int);
select * from menu_card;
insert into menu_card values(1,'chicken biryani','non-vegetarian',220);
insert into menu_card values(2,'mutton biryani','non-vegetarian',340);
insert into menu_card values(3,'panner biryani','vegetarian',180);
insert into menu_card values(4,'veg fried rice','vegetarian',70);
drop table menu_card;