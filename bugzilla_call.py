import bugzilla
import configuration
import re

URL = "partner-bugzilla.redhat.com"
default_product = "Red Hat CloudForms Management Engine"
default_component = "Web UI"
default_status = "OPEN"
default_reporter = ""
default_assignee = ""
user = configuration.get_config(parameter_type='redhat-creds', parameter_name='user')
password = configuration.get_config(parameter_type='redhat-creds', parameter_name='password')


bzapi = bugzilla.Bugzilla(URL)


def query_builder(product=default_product,
                  component=default_component,
                  status="",
                  reporter="",
                  assigned_to=""
                  ):

    bzapi.interactive_login(user=user, password=password)
    query_dict = bzapi.build_query(
        product=product, component=component, status=status, reporter=reporter, assigned_to=assigned_to
    )
    return query_dict


def extract_user(updates):
    full_text_string = updates['result'][0]['message']['text']
    match = re.search(r'[\w\.-]+@[\w\.-]+', full_text_string)
    before_cut = match.group(0)
    return before_cut.split(" ")[0]


def extract_status(updates):
    full_text_string = updates['result'][0]['message']['text']
    try:
        cut_string = full_text_string.split("status:", 1)[1].split(" ")[0]
    except IndexError:
        return default_status
    return cut_string


def extract_assignee(updates):
    full_text_string = updates['result'][0]['message']['text']
    try:
        cut_string = full_text_string.split("assigned:", 1)[1]
    except IndexError:
        return ''
    return cut_string


def send_query(query):
    selected_reporter = query['email2']
    selected_assigned_to = query['email1']
    selected_bug_status = query['bug_status']
    bugs = bzapi.query(query_builder(status=selected_bug_status, assigned_to=selected_assigned_to,
                                     reporter=selected_reporter))
    if not bugs:
        return "There are no bugs"
    else:
        return bugs
