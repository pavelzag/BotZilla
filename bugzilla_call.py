import bugzilla
import configuration

URL = configuration.get_config(parameter_type='bugzilla-creds', parameter_name='bugzilla-url')
default_product = "Red Hat CloudForms Management Engine"
default_component = "Web UI"
default_status = ""
default_reporter = ""
default_assignee = ""
user = configuration.get_config(parameter_type='bugzilla-creds', parameter_name='user')
password = configuration.get_config(parameter_type='bugzilla-creds', parameter_name='password')


bzapi = bugzilla.Bugzilla(URL)


def query_builder(product=default_product,
                  component="",
                  status="",
                  reporter="",
                  assigned_to=""
                  ):
    bzapi.interactive_login(user=user, password=password)
    query_dict = bzapi.build_query(
        product=product, component=component, status=status, reporter=reporter, assigned_to=assigned_to
    )
    return query_dict


def extract_default(updates, type):
    full_text_string = updates['result'][0]['message']['text']
    cut_string = full_text_string.split(type + ":", 1)[1].split(" ")[0]
    if cut_string == '':
        cut_string = full_text_string.split(type + ": ", 1)[1].split(" ")[0]
    return cut_string


def extract_user(updates):
    try:
        cut_string = extract_default(updates, type='user').lower()
        if '@' not in cut_string:
            requested_user_name = cut_string + configuration.get_config(parameter_type='bugzilla-creds',
                                                                                 parameter_name='domain')
    except IndexError:
        return default_reporter
    return requested_user_name


def extract_component(updates):
    try:
        cut_string = extract_default(updates, type='component')
    except IndexError:
        return default_component
    return cut_string


def extract_status(updates):
    try:
        cut_string = extract_default(updates, type='status')
    except IndexError:
        return default_status
    return cut_string.upper()


def extract_assigned_to(updates):
    full_text_string = updates['result'][0]['message']['text']
    try:
        cut_string = full_text_string.split("assigned:", 1)[1]
    except IndexError:
        return ''
    return cut_string


def query_params(updates):
    bugzilla_user = extract_user(updates)
    bugzilla_status = extract_status(updates)
    bugzilla_assigned_to = extract_assigned_to(updates)
    bugzilla_component = extract_component(updates)
    return bugzilla_user, bugzilla_status, bugzilla_assigned_to, bugzilla_component


def send_query(query):
    selected_reporter = query['email2']
    selected_assigned_to = query['email1']
    selected_bug_status = query['bug_status']
    selected_component = query['component'][0]
    bugs = bzapi.query(query_builder(status=selected_bug_status,
                                     assigned_to=selected_assigned_to,
                                     reporter=selected_reporter,
                                     component=selected_component))
    if not bugs:
        return "There are no bugs"
    else:
        return bugs
