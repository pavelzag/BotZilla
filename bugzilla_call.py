import bugzilla
import configuration


URL = "partner-bugzilla.redhat.com"
default_product = "Red Hat CloudForms Management Engine"
default_component = "Web UI"
default_status = "OPEN"
default_reporter = "pzagalsk@redhat.com"
user = configuration.get_config(parameter_type='redhat-creds', parameter_name='user')
password = configuration.get_config(parameter_type='redhat-creds', parameter_name='password')


bzapi = bugzilla.Bugzilla(URL)


def query_builder(product=default_product,
                  component=default_component,
                  status=default_status,
                  reporter=default_reporter):

    bzapi.interactive_login(user=user, password=password)
    whatsthere = bzapi.build_query(
        product=product, component=component, status=status, reporter=reporter
    )
    return whatsthere


def extract_user(updates):
    return updates['result'][0]['message']['text']


def send_query(query):
    bugs = bzapi.query(query_builder(reporter=query['email1']))
    if not bugs:
        return "There are no bugs"
    else:
        return bugs
        # for bug in bugs:
        #     return bug.weburl
