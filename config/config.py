import logging.config
import logging
import os
import site
import yaml


def setup_logging( config):
    print('Bootstrapping logging with config file {}'.format(config))
    if config !=None:
        try:
            logging.config.dictConfig(config['LOGGING'])
            print(config['LOGGING'])
        except Exception as e:
            print(e)
            print('Error in Logging Configuration. Using default configs')
            logging.basicConfig(level=logging.INFO)
    else:
        logging.basicConfig(level=logging.INFO)
        print('Using default logging configuration ')
        
        
DATABASE_CONFIG = {}
LOGGING_CONFIG = {}
packages = site.getsitepackages()
dir_name = os.path.dirname(os.path.abspath(__file__))
logging.info(os.path.dirname(os.path.abspath(__file__)))

try:
    user_paths = os.environ['PYTHONPATH'].split(os.pathsep)
except KeyError:
    user_paths = []

environment = os.environ['env'] if 'env' in os.environ else 'dev'
config_exists = False

for path in user_paths + packages:
    print('looking config in path {} '.format(path))
    config_path = '{}/config/config_{}.yaml'.format(path, environment)
    config_exists = True

    if os.path.exists(config_path):
        print('found config file : {}'.format(config_path))
        break
else:
    config_path = os.path.join(dir_name, 'config_{}.yaml'.format(environment))

with open(config_path, 'r') as file:
    docs = yaml.load_all(file, Loader=yaml.FullLoader)
    for doc in docs:
        DATABASE_CONFIG = doc['DATABASE_CONFIG']
        LOGGING_CONFIG = doc['LOGGING_CONFIG']

setup_logging(LOGGING_CONFIG)