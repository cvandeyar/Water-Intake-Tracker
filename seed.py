from sqlalchemy import func
from model import User
from model import Water
# from model import Bathroom

from model import connect_to_db, db
from server import app

def delete_users():
    User.query.delete()
def delete_water():
    Water.query.delete()

def load_users():

    for row in open(user_filename):
        row = row.rstrip()

        user_id, fname, lname, weight, age, email, password, time_zone = row.split('|')

        user = User(user_id=user_id, fname=fname, lname=lname, weight=weight, age=age, email=email, password=password, time_zone=time_zone)

        db.session.add(user)

    db.session.commit()

def load_water():

    for row in open(water_filename):
        row = row.rstrip()

        water_intake_id, time_updated, ounces, user_id, postal = row.split('|')

        water = Water(water_intake_id=water_intake_id, time_updated=time_updated, ounces=ounces, user_id=user_id, postal=postal)

        db.session.add(water)

    db.session.commit()

# def load_bathroom():

#     Bathroom.query.delete()

#     for row in open('seed_data/u.bathroom'):
#         row = row.rstrip()

#         bathroom_use_id, time, color, user_id = row.split('|')

#         bathroom = Bathroom(bathroom_use_id=bathroom_use_id, time=time, color=color, user_id=user_id)

#         db.session.add(bathroom)

#     db.session.commit()

def set_val_user_id():
    """Set value for the next user_id after seeding database"""

    # Get the Max user_id in the database
    max_id = db.session.query(func.max(User.user_id)).scalar() 
    
    # Set the value for the next user_id to be max_id + 1
    query = "SELECT setval('users_user_id_seq', :new_id)"
    db.session.execute(query, {'new_id': max_id})
    db.session.commit()

def set_val_water_id():
    """Set value for the next user_id after seeding database"""

    # Get the Max user_id in the database
    max_id = db.session.query(func.max(Water.water_intake_id)).scalar() 
    
    # Set the value for the next user_id to be max_id + 1
    query = "SELECT setval('water_consumption_water_intake_id_seq', :new_id)"
    db.session.execute(query, {'new_id': max_id})
    db.session.commit()

if __name__ == "__main__":
    connect_to_db(app)

    # In case tables haven't been created, create them
    db.create_all()

    user_filename = 'seed_data/u.user'
    water_filename = 'seed_data/u.water'
    delete_water()
    delete_users()
    load_users()
    load_water()
    set_val_user_id()
    set_val_water_id()
    # load_bathroom()