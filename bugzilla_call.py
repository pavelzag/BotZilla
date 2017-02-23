import bugzilla
import configuration
import normalizer
import logging
import re
from validate_email import validate_email


URL = configuration.get_config(parameter_type='bugzilla-creds', parameter_name='bugzilla_url')
default_product = configuration.get_config(parameter_type='default-params', parameter_name='default_product')
default_component = configuration.get_config(parameter_type='default-params', parameter_name='default_component')
user = configuration.get_config(parameter_type='bugzilla-creds', parameter_name='user')
password = configuration.get_config(parameter_type='bugzilla-creds', parameter_name='password')
domain_name = configuration.get_config(parameter_type='bugzilla-creds', parameter_name='domain')
bzapi = bugzilla.Bugzilla(URL)


def query_builder(**kwargs):
    bzapi.interactive_login(user=user, password=password)
    query_dict = bzapi.build_query(**kwargs)
    return query_dict


def extract_params(updates, type):
    full_text_string = updates['message']['text']
    if type == 'user':
        full_text_string = full_text_string.lower()
    params_list = re.findall(r'(\w+)\s*:\s*((?:\w+\b\s*)+)(?!\s*:)', full_text_string)
    for param in params_list:
        if type in param:
            parameter, name = param
            return name.replace(' ', '')
    else:
        return ''


def extract_user(updates):
    requested_user_name = extract_params(updates, type='user').lower()
    if '@' not in requested_user_name:
        requested_user_name = requested_user_name + domain_name
    return requested_user_name


def extract_component(updates):
    try:
        cut_string = extract_params(updates, type='component')
    except IndexError:
        return default_component
    cut_string = cut_string.replace('_', ' ')
    if cut_string == None:
        return default_component
    return cut_string


def extract_product(updates):
    try:
        cut_string = extract_params(updates, type='product')
    except IndexError:
        return default_product
    cut_string = cut_string.replace('_', ' ')
    if cut_string == None:
        return default_product
    return cut_string


def extract_status(updates):
    cut_string = extract_params(updates, type='status')
    return cut_string.upper()


def extract_assigned_to(updates):
    requested_assignee = extract_params(updates, type='assigned_to').lower()
    if '@' not in requested_assignee:
        requested_assignee = requested_assignee + domain_name
    return requested_assignee


def query_params(updates):
    bugzilla_user = extract_user(updates)
    bugzilla_status = extract_status(updates)
    bugzilla_assigned_to = extract_assigned_to(updates)
    bugzilla_product = extract_product(updates)
    print('query params bugzilla product was ' + str(bugzilla_product))
    bugzilla_product = normalizer.normalize_product_new(bugzilla_product)
    print('query params after normalization was bugzilla product was ' + str(bugzilla_product))
    bugzilla_component = extract_component(updates)
    bugzilla_component = normalizer.normalize_component_new(bugzilla_component, bugzilla_product)
    return bugzilla_user, bugzilla_status, bugzilla_assigned_to, bugzilla_component, bugzilla_product


def send_query(query):
    reporter_email = query['email2']
    if validate_email(reporter_email):
        bugs = bzapi.query(query)
        if not bugs:
            return "There are no " + query['bug_status'].lower() + " bugs"
        else:
            return bugs
    else:
        return "Incorrect E-mail address. Please try again"
