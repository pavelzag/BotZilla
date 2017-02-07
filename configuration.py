import os
import yaml


def get_config(parameter_type, parameter_name):
    if 'DYNO' in os.environ:
        is_heroku = True
    else:
        is_heroku = False

    if is_heroku:
        return os.environ.get(parameter_name, 'Theres\'s nothing here')
    else:
        with open("config.yml", 'r') as ymlfile:
            cfg = yaml.load(ymlfile)
        if parameter_type == 'bugzilla-creds':
            return cfg['bugzilla-creds'][parameter_name]
        elif parameter_type == 'telegram-creds':
            return cfg['telegram-creds'][parameter_name]
        elif parameter_type == 'default-params':
            return cfg['default-params'][parameter_name]
