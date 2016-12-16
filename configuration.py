import yaml


def get_config(parameter_type, parameter_name):
    with open("config.yml", 'r') as ymlfile:
        cfg = yaml.load(ymlfile)
    if parameter_type == 'bugzilla-creds':
        return cfg['bugzilla-creds'][parameter_name]
    elif parameter_type == 'telegram-creds':
        return cfg['telegram-creds'][parameter_name]
    elif parameter_type == 'default-params':
        return cfg['default-params'][parameter_name]
