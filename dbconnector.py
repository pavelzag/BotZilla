from pymongo import MongoClient
import configuration
import logging
import sys

domain_name = configuration.get_config(parameter_type='bugzilla-creds',parameter_name='domain')
dbconfiguration = configuration.get_config(parameter_type='db-params', parameter_name='MONGODB_URI')
logging.debug("the configuration that was passed was: " + str(dbconfiguration))
sys.stdout.flush()
print("the configuration that was passed was: " + str(dbconfiguration))
client = MongoClient(dbconfiguration)
db = client.test


def add_user(telegram_user_id, user_name):
    user_name = user_name + domain_name
    if not is_user_in(user_name):
        db.test.insert({'user_id': telegram_user_id, 'user_name': user_name})
        cursor = db.test.find({'user_name': user_name})
        for document in cursor:
            print(document)
        return "The user " + user_name + " was registered"
    else:
        return "The user " + user_name + " is already registered"


def is_user_in(user_name):
    if db.test.find({'user_name': user_name}).count() > 0:
        return True
    else:
        return False
