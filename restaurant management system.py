import mysql.connector as db
con = db.connect(
    user='root',
    password='Rajini@123',
    host='localhost',
    database='mysql'
)
admin_id='123'
password='123'
from datetime import datetime
def menu_items():
    cur=con.cursor()
    cur.execute('select * from menu_card')
    data=cur.fetchall()
    print("\n--- Menu Card ---")
    print("="*60)
    print(f"{'Item ID':<10}{'Item Name':<20}{'Category':<15}{'Price (Rs)':<10}")
    print("="*60)

    

    for i in data:
        print(f"{i[0]:<10}{i[1]:<20}{i[2]:<15}{i[3]:<10}")
    print("="*60)    
    cur.close()
def add_items():
    cur=con.cursor()
    ch=input("do you want to add new items(yes\no): ")
    if ch=="yes":
        item_id=int(input("enter item_id: "))
        items=input("enter an item: ")
        category=input("enter a category: ")
        price=float(input("enter item price: "))
        cur.execute("insert into menu_card(item_id,items,category,price)values(%s,%s,%s,%s)",(item_id,items,category,price))
        con.commit()
        print("item added sucessfully")
    elif ch=="no":
        print("no more items to add")
    else:
        print("choose the correct one")
    cur.close()
def delete_item():
    cur=con.cursor()
    item_id=int(input("what item id do you want to delete: "))
    cur.execute('select * from menu_card where item_id=%s',(item_id,))
    data=cur.fetchone()
    if data:
        confirm=input("do you want to delete the item(yes\no): ")
        if confirm=="yes":
            cur.execute("delete from menu_card where item_id=%s",(item_id,))
            con.commit()
            print("item deleted sucessfully")
        else:
            print("deletion cancelled")                             
    else:
        print("no item id found")
    cur.close()
def modify_item():
    cur=con.cursor()
    item_id=int(input("which item do you want to modify: "))
    cur.execute('select * from menu_card where item_id=%s',(item_id,))
    data=cur.fetchone()
    if data:
        print(f"Item ID: {data[0]}, Name: {data[1]}, category: {data[2]}, Price: {data[3]} Rs")
        confirm=input("do you want to modify the item(yes\no): ")
        if confirm=="yes":
            new_name = input("Enter new item name: ")
            new_category=input("Enter new category: ")
            new_price = float(input("Enter new price: "))
            cur.execute("UPDATE menu_card SET items=%s,category=%s, price=%s WHERE item_id=%s",(new_name, new_category, new_price, item_id))
            con.commit()
            print("item modified sucessfully")
        else:
            print("modification cancelled")
    else:
        print("item not found")
    cur.close()
    
def add_to_cart():
    
    add = int(input("Select an item ID to add: "))

    cur = con.cursor()
    cur.execute('SELECT * FROM menu_card WHERE item_id = %s', (add,))
    data = cur.fetchone()

    if data:
        confirm = input("Do you want to add the item (yes/no): ")
        if confirm.lower() == "yes":
            quantity = int(input("Select the quantity to add: "))
            item_id, name, category, price = data
            cur.execute(
                "INSERT INTO cart (item_id, name, category, price, quantity, user_mobile_no) "
                "VALUES (%s, %s, %s, %s, %s, %s)",
                (item_id, name, category, price, quantity, user_mobile_no)
            )
            con.commit()
            print("Item added to cart successfully.")
        else:
            print("Item not added.")
    else:
        print("Item not found.")
    cur.close()
def view_cart():
    
    cur = con.cursor()
    cur.execute("SELECT item_id, name, category, price, quantity FROM cart WHERE user_mobile_no = %s", (user_mobile_no,))
    data = cur.fetchall()
   


    if not data:
        print("Cart is empty.")
        cur.close()
        return

    total = 0
    print("\n--- Your Cart ---")
    print("="*80)
    print(f"{'Item ID':<10}{'Item Name':<20}{'Category':<15}{'Price':<10}{'Qty':<8}{'Total':<10}")
    print("="*80)

    for item in data:
        item_id, name, category, price, quantity = item
        item_total = price * quantity
        total += item_total
        
        print(f"{item_id:<10}{name:<20}{category:<15}{price:<10}{quantity:<8}{item_total:<10}")

    print("="*80)
    print(f"{'':<55}{'Grand Total:':<12}{total:<10}")
    print("="*80)
    
    cur.close()

def modify_cart():
    cur = con.cursor()
    cur.execute("SELECT item_id, name, category, price, quantity FROM cart WHERE user_mobile_no = %s", (user_mobile_no,))
    data = cur.fetchall()

    if not data:
        print("Cart is empty.")
        cur.close()
        return
    print("\n--- Your Cart (Before Modification) ---")
    print("="*80)
    print(f"{'Item ID':<10}{'Item Name':<20}{'Category':<15}{'Price':<10}{'Qty':<8}{'Total':<10}")
    print("="*80)

    for item in data:
        item_id, name, category, price, quantity = item
        item_total = price * quantity
        print(f"{item_id:<10}{name:<20}{category:<15}{price:<10}{quantity:<8}{item_total:<10}")

    print("="*80)

    item_id_input = input("Enter the item ID you want to modify: ")

    if not item_id_input.isdigit():
        print("Invalid input. Item ID must be a number.")
        cur.close()
        return

    item_id = int(item_id_input)

    cur.execute("SELECT * FROM cart WHERE item_id = %s AND user_mobile_no = %s", (item_id, user_mobile_no))
    item = cur.fetchone()

    if not item:
        print("Item not found in your cart.")
        cur.close()
        return

    print("1. Change quantity")
    print("2. Remove item from cart")
    choice = input("Choose an option (1 or 2): ")

    if choice == '1':
        quantity_input = input("Enter new quantity: ")
        if quantity_input.isdigit():
            new_quantity = int(quantity_input)
            if new_quantity > 0:
                cur.execute(
                    "UPDATE cart SET quantity = %s WHERE item_id = %s AND user_mobile_no = %s",
                    (new_quantity, item_id, user_mobile_no)
                )
                con.commit()
                print("Quantity updated successfully.")
            else:
                print("Quantity must be greater than 0.")
        else:
            print("Invalid quantity input.")

    elif choice == '2':
        cur.execute("DELETE FROM cart WHERE item_id = %s AND user_mobile_no = %s", (item_id, user_mobile_no))
        con.commit()
        print("Item removed from cart.")
    else:
        print("Invalid choice.")

    cur.close()


def generate_bill():
    cur = con.cursor()
    cur.execute("SELECT name, category, price, quantity FROM cart WHERE user_mobile_no = %s", (user_mobile_no,))
    data = cur.fetchall()
    
    if not data:
        print("Cart is empty. Nothing to bill.")
        cur.close()
        return

    
    total = 0
    print("\n--- Final Bill ---")
    print("="*80)
    print(f"{'Item Name':<20}{'Category':<15}{'Price':<10}{'Qty':<8}{'Total':<10}")
    print("="*80)

    for item in data:
        name, category, price, quantity = item
        item_total = price * quantity
        total += item_total
        print(f"{name:<20}{category:<15}{price:<10}{quantity:<8}{item_total:<10}")
        
        cur.execute(
            "INSERT INTO orders (user_name, user_mobile_no, item_name, category, quantity, price, total) "
            "VALUES (%s, %s, %s, %s, %s, %s, %s)",
            (user_name, user_mobile_no, name, category, quantity, price, item_total))

    
    con.commit()
    print("="*80)
    print(f"{'':<53}{'Grand Total:':<12}{total:<10}")
    print("="*80)
    print("✅ Thank you for your order! Please visit again.")
    print("="*80)      
    
    
    cur.close()

def view_all_orders():
    cur = con.cursor()
    cur.execute("SELECT * FROM orders")
    data = cur.fetchall()

    if not data:
        print("No orders found.")
    else:
        print("\n--- All Orders ---")
        print("="*120)
        print(f"{'User Name':<15}{'Mobile No':<15}{'Item Name':<20}{'Category':<15}{'Qty':<8}{'Price':<10}{'Total':<10}{'Date':<15}")
        print("="*120)

        for user, phone, item, category, qty, price, total, order_date in data:
            if order_date:  # if date exists
                order_date_str = order_date.strftime("%Y-%m-%d")
            
            print(f"{user:<15}{phone:<15}{item:<20}{category:<15}{qty:<8}{price:<10}{total:<10}{order_date_str:<15}")

        print("="*120)

    cur.close()

def day_wise_profit():
    cur = con.cursor()
    cur.execute("SELECT order_date, SUM(total) FROM orders GROUP BY order_date")
    data = cur.fetchall()

    if not data:
        print("No orders found.")
    else:
        print("\n--- Day Wise Profit ---")
        print("="*50)

        for order_date, profit in data:
            if order_date is None:   
                continue
            order_date_str = order_date.strftime("%Y-%m-%d")
            print(f"Date:{order_date_str}-Total Profit: {profit}Rs")

        print("="*50)

    cur.close()
def profit_between_dates():
    cur = con.cursor()
    start_date = input("Enter start date (YYYY-MM-DD): ")
    end_date = input("Enter end date (YYYY-MM-DD): ")

    query = "SELECT SUM(total) FROM orders WHERE order_date BETWEEN %s AND %s"
    cur.execute(query, (start_date, end_date))
    result = cur.fetchone()

    if result[0] is None:
        print(f"No orders found between {start_date} and {end_date}.")
    else:
        print(f"\nTotal Profit between {start_date} and {end_date}: {result[0]} Rs")

    cur.close()

while True:
    print("1.Admin login")
    print("2.User login")
    print("3.Exit")
    choose=input("enter your choice(1/2/3):")
    if choose=="1":
        crct_admin_id=input("enter admin id:")
        crct_admin_password=input("enter admin password:")
        if crct_admin_id==admin_id and crct_admin_password==password:
            print("Admin login succesfully")
            print()
            while True:
                print('1.admin menu')
                print('2.add items')
                print('3.delete menu')
                print('4.modify menu')
                print('5.view all orders')
                print('6.day wise profit')
                print('7.profit between dates')
                print('8.logout')
                print()
                ch=input("choose one option: ")
                if ch=='1':
                    menu_items()
                elif ch=='2':
                    add_items()
                elif ch=='3':
                    delete_item()
                elif ch=='4':
                    modify_item()
                elif ch=='5':
                    view_all_orders()
                elif ch=='6':
                    day_wise_profit()
                elif ch=='7':
                    profit_between_dates()    
                elif ch=='8':
                    break
                else:
                    print("please choose the correct option")                  
                    
    elif choose=='2':
        user_name=input("enter user name: ")
        while True:
            
            user_mobile_no=input("enter user mobile no: ")
            s=['9','8','7','6']
            if len(user_mobile_no)==10 and user_mobile_no.isdigit() and  user_mobile_no[0] in s:
                print("user login sucessfull!")
                break
            else:
                print("please enter correct credentials")
                continue
        while True:
            user=input("do you want to order: ")
            if user=="yes":
                    while True:
                        print("1.view menu")
                        print("2.add items to cart")
                        print("3.view items in cart")
                        print("4.modify cart")
                        print("5.bill")
                        print("6.logout")
                        print()
                        ch=input("choose one option: ")
                        if ch=="1":
                            menu_items()
                        elif ch=="2":
                            add_to_cart()
                        elif ch=="3":
                            view_cart()
                        elif ch=="4":
                            modify_cart()
                        elif ch=="5":
                            generate_bill()    
                        elif ch=="6":
                            break
                        else:
                            print("plese choose the corrct one")
            elif user=="no":
                break
            else:
                print("please choose the correct one!")
    elif choose=='3':
        print("Thank you for visiting. please visit again!")
        break
    else:
        print("please choose the correct option")
    
con.close()
