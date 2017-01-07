from pymongo import MongoClient
import configuration
import os

domain_name = configuration.get_config(parameter_type='bugzilla-creds',parameter_name='domain')

if 'DYNO' in os.environ:
    client = MongoClient(os.environ['MONGODB_URI'])
    db = client.get_default_database()
else:
    client = MongoClient()
    db = client.registration


def add_user(telegram_user_id, user_name):
    user_name = user_name + domain_name
    if not is_user_name_in(user_name):
        db.registration.insert({'user_id': telegram_user_id, 'user_name': user_name})
        cursor = db.registration.find({'user_name': user_name})
        for document in cursor:
            print(document)
        return "The user " + user_name + " was registered"
    else:
        return "The user " + user_name + " is already registered"


def remove_user(telegram_user_id, user_name):
    user_name = user_name + domain_name
    if not is_user_name_in(user_name):
        db.registration.insert({'user_id': telegram_user_id, 'user_name': user_name})
        cursor = db.registration.find({'user_name': user_name})
        for document in cursor:
            print(document)
        return "The user " + user_name + " was unregistered"
    else:
        return "The user " + user_name + " is not registered"


def get_user(telegram_user_id):
    if is_user_id_in(telegram_user_id):
        result = db.registration.find({'user_id': telegram_user_id})
        for document in result:
            for value in document.items():
                if 'user_name' in value:
                    id, name = value
            return name
    else:
        return ''


def is_user_name_in(user_name):
    if db.registration.find({'user_name': user_name}).count() > 0:
        return True
    else:
        return False


def is_user_id_in(user_id):
    if db.registration.find({'user_id': user_id}).count() > 0:
        return True
    else:
        return False