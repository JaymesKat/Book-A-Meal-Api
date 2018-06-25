from app.models import User, Meal, Menu, Order

def insert_table_data(db):

    customer1 = User(first_name='James',last_name='Katarikawe',username='james_katarikawe', email='james@example.com',is_caterer=False)
    customer1.password('james')
    customer2 = User(first_name='Paul',last_name='Kayongo',username='paul_kayongo', email='paulkayongo@gmail.com',is_caterer=False)
    customer2.password('kayongo')

    admin1 = User(first_name='Joseph',last_name='Odur',username='joseph_odur', email='odur@gmail.com',is_caterer=True)
    admin1.password('odur')
    admin2 = User(first_name='Phillip',last_name='Seryazi',username='phillip_seryazi', email='seryazi@gmail.com',is_caterer=True)
    admin1.password('seryazi')
    
    meal1 = Meal(name="Rice & Chicken", price=10.5)
    meal2 = Meal(name="Posho & Beans", price=9.0)
    meal3 = Meal(name="Potatoes & Meat", price=12)
    meal4 = Meal(name="Spaghetti", price=11)
    menu = Menu()
    menu.items.append(meal1)
    menu.items.append(meal2)
    menu.items.append(meal3)
    menu.items.append(meal4)

    order1 = Order(meal=meal1,user=customer1)
    order2 = Order(meal=meal3,user=customer2)

    db.session.add(customer1)
    db.session.add(customer2)
    db.session.add(admin1)
    db.session.add(admin2)
   
    db.session.add(meal1)
    db.session.add(meal2)
    db.session.add(meal3)
    db.session.add(menu)


    db.session.add(order1)
    db.session.add(order2)

    db.session.commit()