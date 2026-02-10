import mysql.connector
from datetime import datetime
try:
    connection = mysql.connector.connect(
        host = "localhost",
        password = "Dieng",
        database = "supply_system",
        user = "root"
    )

    if connection.is_connected():
        print("DB connected to Python")
except Exception as e :
    print(f"An error occurs {e}")


def add_category():
    """Add a new category"""
    try:
        cursor = connection.cursor()
        query = """INSERT INTO Categories(category_name) values (%s)"""
        category_name = input("Category's name : ").capitalize()
        cursor.execute(query, (category_name,))
        connection.commit()
        print()
    except Exception as e:
        print(f"This error occurs {e}")



def show_categories():
    """Show all categories"""
    try:
        cursor = connection.cursor()
        query = """SELECT category_name FROM Categories"""
        cursor.execute(query)
        print("==Categories==")
        for row in cursor.fetchall():
            print(f"No{cursor.rowcount} : {row[0]}")
    except Exception as e :
        print(f"This error occurs {e}")



def add_product():
    """Add a new product"""
    try:
        cursor = connection.cursor()
        query = """INSERT INTO Products(designation, prix, id_category,stock) 
        values (%s,%s,%s,%s)"""
        print("==Adding a new product==")
        designation = input("Designation : ").capitalize()
        price = int(input("Price : "))
        show_categories()
        id_category = int(input("Category number : "))
        stock = int(input("Quantity : "))
        cursor.execute(query, (designation, price, id_category,stock))
        connection.commit()
        print(f"{designation} added with success !")
    except Exception as e :
        print(f"This error occurs {e}")
    

def show_products():
    """Show list of products"""
    cursor = connection.cursor()
    query = """SELECT * FROM Products JOIN Categories ON Products.id_category = Categories.id_category"""
    cursor.execute(query)
    print("==HERE IS THE PRODUCT'S LIST")
    for row in dict(cursor.fetchall()):
        print(f"ID : {row[0]}")
        print(f"Designation : {row[1]}")
        print(f"Price : {row[2]}")
        print(f"Category : {row[7]}\n")
    


def retrieving_supply():
    """Retrieving supply"""
    cursor = connection.cursor()
    query = """INSERT INTO Mouvements_stock(id_produit, quantite,date_mouvement, type_mouvement)
    values (%s,%s, %s)"""
    id_produit = int(input("Product id : "))
    quantite = int(input("Quantity : "))
    date_mvt = datetime.today()
    cursor.execute(query, (id_produit, quantite, date_mvt,))
    connection.commit()
    print(f"{quantite} of product {id_produit} are taken ")


def alerte_product():
    try:
        cursor = connection.cursor(buffered=True)
        query = """SELECT * FROM Products where etat_stock = %s"""
        cursor.execute(query,("en rupture",))
        connection.commit()
        print("HERE IS THE PRODUCT'S LIST THAT SUPPLY IS UNDER 5")
        for row in cursor.fetchall():
            print(row)
    except Exception as e:
        print(f"This error occurs {e}")


def input_in_mouvements_stock():
    """Show inputs in historic"""
    cursor = connection.cursor()
    query = """SELECT * FROM Mouvements_stock where type_mouvement = %s"""
    cursor.execute(query, ("entree",))
    for row in cursor.fetchall():
        print(row)


def output_in_mouvements_stock():
    """Show outputs in historic"""
    cursor = connection.cursor()
    query = """SELECT * FROM Mouvements_stock where type_mouvement = %s"""
    cursor.execute(query, ("sortie",))
    for row in cursor.fetchall():
        print(row)


def make_a_product_output():
    """Save an output operation"""
    try : 
        cursor = connection.cursor()
        id_product = int(input("Product id : "))
        quantity = int(input("Quantity : "))
        query = """UPDATE Products SET stock = stock - %s where id_product = %s"""
        cursor.execute(query, (quantity, id_product,))
        connection.commit()
        print("Allocated")
    except mysql.connector.errors.DatabaseError :
        print("Not enough supply ! Try to recharge this product.")



def menu():
    """Menu"""
    print("1. Add a new category \
          2. Show categories list \
          3. Add a new product \
          4. Show product's list \
          5. Show inputs in historic \
          6. Show outputs in historic \
          7. Red stock products \
          8. Save an output") 
    


#Main program
while True :
    print("===WELCOME TO YOUR SUPPLY MANAGER")
    menu()
    choice = input("Please make a choice : ")
    match (choice):
        case "1":
            add_category()
            break;
        case "2":
            show_categories()
            break;
        case "3":
            add_product()
            break;
        case "4":
            show_products()
            break;
        case "5":
            input_in_mouvements_stock()
            break;
        case "6":
            output_in_mouvements_stock()
            break;
        case "7":
            alerte_product()
            break;
        case "8":
            make_a_product_output()
            break;
        case "9":
            exit()
            break;
