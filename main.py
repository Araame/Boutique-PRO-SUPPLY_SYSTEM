import mysql.connector
from datetime import datetime
import hashlib
import getpass



try:
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Root@1234",
        database="arame_dump"
    )

    if connection.is_connected():
        print("DB connected to Python")
except Exception as e:
    print(f"An error occurs {e}")


def add_category():
    """Add a new category"""
    try:
        cursor = connection.cursor()
        query = """INSERT INTO Categories(category_name) VALUES (%s)"""
        category_name = input("Category's name : ").capitalize()
        cursor.execute(query, (category_name,))
        connection.commit()
        print(f"Category '{category_name}' added successfully!")
    except Exception as e:
        print(f"This error occurs {e}")


def show_categories():
    """Show all categories"""
    try:
        cursor = connection.cursor()
        query = """SELECT id_category, category_name FROM Categories"""
        cursor.execute(query)
        print("==Categories==")
        for row in cursor.fetchall():
            print(f"No{row[0]} : {row[1]}")
    except Exception as e:
        print(f"This error occurs {e}")


def add_product():
    """Add a new product"""
    try:
        cursor = connection.cursor()
        query = """INSERT INTO Products(designation, prix, id_category, stock) 
                   VALUES (%s,%s,%s,%s)"""
        print("==Adding a new product==")
        designation = input("Designation : ").capitalize()
        price = int(input("Price : "))
        show_categories()
        id_category = int(input("Category number (id_category) : "))
        stock = int(input("Quantity : "))
        cursor.execute(query, (designation, price, id_category, stock))
        connection.commit()
        print(f"{designation} added with success!")
    except Exception as e:
        print(f"This error occurs {e}")


def show_products():
    """Show list of products"""
    try:
        cursor = connection.cursor()
        query = """SELECT Products.id_product, Products.designation, Products.prix, 
                          Products.stock, Categories.category_name
                   FROM Products 
                   JOIN Categories ON Products.id_category = Categories.id_category"""
        cursor.execute(query)
        print("==HERE IS THE PRODUCT'S LIST==")
        for row in cursor.fetchall():
            print(f"ID : {row[0]}")
            print(f"Designation : {row[1]}")
            print(f"Price : {row[2]}")
            print(f"Stock : {row[3]}")
            print(f"Category : {row[4]}\n")
    except Exception as e:
        print(f"This error occurs {e}")


def retrieving_supply():
    """Retrieving supply"""
    try:
        cursor = connection.cursor()
        query = """INSERT INTO Mouvements_stock(id_produit, quantite, date_mouvement, type_mouvement)
                   VALUES (%s,%s,%s,%s)"""
        id_produit = int(input("Product id : "))
        quantite = int(input("Quantity : "))
        date_mvt = datetime.today()
        cursor.execute(query, (id_produit, quantite, date_mvt, "entree"))
        connection.commit()
        print(f"{quantite} of product {id_produit} are taken")
    except Exception as e:
        print(f"This error occurs {e}")


def alerte_product():
    """Show products with low stock"""
    try:
        cursor = connection.cursor()
        query = """SELECT * FROM Products WHERE stock < 5"""
        cursor.execute(query)
        print("HERE IS THE PRODUCT'S LIST THAT SUPPLY IS UNDER 5")
        for row in cursor.fetchall():
            print(row)
    except Exception as e:
        print(f"This error occurs {e}")


def input_in_mouvements_stock():
    """Show inputs in historic"""
    cursor = connection.cursor()
    query = """SELECT * FROM Mouvements_stock WHERE type_mouvement = %s"""
    cursor.execute(query, ("entree",))
    for row in cursor.fetchall():
        print(row)


def output_in_mouvements_stock():
    """Show outputs in historic"""
    cursor = connection.cursor()
    query = """SELECT * FROM Mouvements_stock WHERE type_mouvement = %s"""
    cursor.execute(query, ("sortie",))
    for row in cursor.fetchall():
        print(row)


def make_a_product_output():
    """Save an output operation"""
    try:
        cursor = connection.cursor()
        id_product = int(input("Product id : "))
        quantity = int(input("Quantity : "))
        query = """UPDATE Products SET stock = stock - %s WHERE id_product = %s"""
        cursor.execute(query, (quantity, id_product))
        connection.commit()

        # Save movement in history
        query_mvt = """INSERT INTO Mouvements_stock(id_produit, quantite, date_mouvement, type_mouvement)
                       VALUES (%s,%s,%s,%s)"""
        cursor.execute(query_mvt, (id_product, quantity, datetime.today(), "sortie"))
        connection.commit()

        print("Allocated")
    except mysql.connector.errors.DatabaseError:
        print("Not enough supply! Try to recharge this product.")
    except Exception as e:
        print(f"This error occurs {e}")



def hash_password(password: str) -> str: 
    """Hash password with SHA256 (simple example, use bcrypt for production).""" 
    return hashlib.sha256(password.encode()).hexdigest() 

def register_user(): 
    """Enregister =un new utilisateur et son  mdp """ 
    cursor = connection.cursor() 
    email = input("Enter  l'email à enregister: ").strip() 
    password = getpass.getpass("Enter le password à enregister: ").strip() 
    role = input("definir le role pour cette utilisateur ('admin' or 'simple'): ") or None
    hashed_pw = hash_password(password) 
    query = """INSERT INTO Users(email, password, role) VALUES (%s, %s, %s)""" 
    cursor.execute(query, (email, hashed_pw, role)) 
    connection.commit() 
    print("User registered successfully!") 


def login_user(): 
    """Verification de l'utilisateur """ 
    cursor = connection.cursor() 
    while True:
        email = input("Enter your email: ").strip() 
        password = getpass.getpass("Enter your password: ").strip()
        

        hashed_pw = hash_password(password) 
        query = """SELECT * FROM Users WHERE email = %s AND password = %s""" 
        cursor.execute(query, (email, hashed_pw)) 
        user = cursor.fetchone() 
        if user:
            email= user[1] 
            role =user[3]
            if role =="admin" :  
                print(f"Bienvenue trés chere {email} admin ") 
                menu_admin()
                
            elif role == "simple":
                print(f"bienvenue {email} simple")
                menu_simple()

        else: 
            print("Invalid email or password.")

   
        

    
def menu_admin():
    """Menu"""
    while True :
        print("===WELCOME TO YOUR SUPPLY MANAGER (admin)")
        print("""1. Add a new category
2. Show categories list
3. Add a new product
4. Show product's list
5. Show inputs in historic
6. Show outputs in historic
7. Red stock products
8. Save an output
9. Enregister Users
0. Exit""")

        choice = input("Please make a choice : ")
        match (choice):
            case "1":
                add_category()
            
            case "2":
                show_categories()
            
            case "3":
                add_product()
            
            case "4":
                show_products()
            
            case "5":
                input_in_mouvements_stock()
            
            case "6":
                output_in_mouvements_stock()
            
            case "7":
                alerte_product()
            
            case "8":
                make_a_product_output()
        
            case "9":
                register_user()
            
            case "0":
                print("bye!! bye!!!")
                exit()



def menu_simple():
    while True :
        print("===WELCOME TO YOUR SUPPLY MANAGER(simple)")
        print("""1. Show categories list
2. Show product's list
3. Show inputs in historic
4. Show outputs in historic
5. Red stock products
0. Exit""")

        choice = input("Please make a choice : ")
        match (choice):
            
            case "1":
                show_categories()
            
            case "2":
                show_products()
            
            case "3":
                input_in_mouvements_stock()
            
            case "4":
                output_in_mouvements_stock()
            
            case "5":
                alerte_product()
            
            case "0":
                print("bye!! bye!!!")
                exit()

    

login_user()

    
    