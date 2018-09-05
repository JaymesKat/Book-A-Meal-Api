from app.models import User, Meal, Menu, Order, Day


def insert_table_data(db):

    customer1 = User(
        first_name='James',
        last_name='Katarikawe',
        username='james_katarikawe',
        email='james@example.com',
        is_caterer=False)
    customer1.password = 'james'
    customer2 = User(
        first_name='Paul',
        last_name='Kayongo',
        username='paul_kayongo',
        email='paulkayongo@gmail.com',
        is_caterer=False)
    customer2.password = 'kayongo'

    admin1 = User(
        first_name='Joseph',
        last_name='Odur',
        username='joseph_odur',
        email='odur@gmail.com',
        is_caterer=True)
    admin1.password = 'odur'
    admin2 = User(
        first_name='Phillip',
        last_name='Seryazi',
        username='phillip_seryazi',
        email='seryazi@gmail.com',
        is_caterer=True)
    admin2.password = 'seryazi'

    db.session.add(customer1)
    db.session.add(customer2)
    db.session.add(admin1)
    db.session.add(admin2)
    db.session.commit()

    meal1 = Meal(name="Chicken Tandoori", price=18.5, caterer=admin1)
    meal2 = Meal(name="Fish Tikka", price=11.0, caterer=admin1)
    meal3 = Meal(name="Butter Chicken", price=17, caterer=admin1)
    meal4 = Meal(name="Biryani Rice", price=19, caterer=admin1)

    meal11 = Meal(name="Rice & Chicken", price=10.5, caterer=admin2)
    meal22 = Meal(name="Posho & Beans", price=9.0, caterer=admin2)
    meal33 = Meal(name="Potatoes & Meat", price=12, caterer=admin2)
    meal44 = Meal(name="Spaghetti", price=11, caterer=admin2)

    menu1 = Menu()
    menu1.caterer = admin1
    menu1.items.append(meal1)
    menu1.items.append(meal2)
    menu1.items.append(meal3)
    menu1.items.append(meal4)

    menu2 = Menu()
    menu2.caterer = admin1
    menu2.items.append(meal1)
    menu2.items.append(meal2)
    menu2.items.append(meal3)
    menu2.items.append(meal4)

    order1 = Order(meal=meal1, customer=customer1, caterer=admin1)
    order2 = Order(meal=meal3, customer=customer2, caterer=admin1)

    day1 = Day(name="Monday")
    db.session.add(day1)
    db.session.commit()

    day2 = Day(name="Tuesday")
    db.session.add(day2)
    db.session.commit()

    day3 = Day(name="Wednesday")
    db.session.add(day3)
    db.session.commit()

    day4 = Day(name="Thursday")
    db.session.add(day4)
    db.session.commit()

    day5 = Day(name="Friday")
    db.session.add(day5)
    db.session.commit()

    day6 = Day(name="Saturday")
    db.session.add(day6)
    db.session.commit()

    day7 = Day(name="Sunday")
    db.session.add(day7)
    db.session.commit()

    db.session.add(meal1)
    db.session.add(meal2)
    db.session.add(meal3)
    db.session.add(meal4)

    db.session.add(meal11)
    db.session.add(meal22)
    db.session.add(meal33)
    db.session.add(meal44)

    menu1.day_id = 4
    menu2.day_id = 5
    db.session.add(menu1)
    db.session.add(menu2)

    db.session.add(order1)
    db.session.add(order2)

    db.session.commit()
