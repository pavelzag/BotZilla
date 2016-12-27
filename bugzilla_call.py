import bugzilla
import configuration
import re

URL = configuration.get_config(parameter_type='bugzilla-creds', parameter_name='bugzilla-url')
default_product = configuration.get_config(parameter_type='default-params', parameter_name='default_product')
default_component = configuration.get_config(parameter_type='default-params', parameter_name='default_component')
default_status = ""
default_reporter = ""
default_assignee = ""
user = configuration.get_config(parameter_type='bugzilla-creds', parameter_name='user')
password = configuration.get_config(parameter_type='bugzilla-creds', parameter_name='password')


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
    try:
        cut_string = extract_params(updates, type='user').lower()
        if cut_string == '':
            return default_reporter
        if '@' not in cut_string:
            requested_user_name = cut_string + configuration.get_config(parameter_type='bugzilla-creds',
                                                                                 parameter_name='domain')
    except IndexError:
        return default_reporter
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


def extract_status(updates):
    try:
        cut_string = extract_params(updates, type='status')
    except IndexError:
        return default_status
    return cut_string.upper()


def extract_assigned_to(updates):
    try:
        cut_string = extract_params(updates, type='assigned_to')
    except IndexError:
        return default_status
    return cut_string.upper()


def query_params(updates):
    bugzilla_user = extract_user(updates)
    bugzilla_status = extract_status(updates)
    bugzilla_assigned_to = extract_assigned_to(updates)
    bugzilla_component = extract_component(updates)
    return bugzilla_user, bugzilla_status, bugzilla_assigned_to, bugzilla_component


def send_query(query):
    selected_reporter = query['email2']
    if not selected_reporter:
        return "A reporter must be selected"
    selected_assigned_to = query['email1']
    selected_bug_status = query['bug_status']
    selected_component = query['component'][0]
    bugs = bzapi.query(query_builder(status=selected_bug_status,
                                     assigned_to=selected_assigned_to,
                                     reporter=selected_reporter,
                                     component=selected_component))
    if not bugs:
        return "There are no " + selected_bug_status.lower() + " bugs"
    else:
        return bugs