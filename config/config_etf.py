import logging.config
import logging
import os
import site
import yaml
        
ETF_CONFIG = {}
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
    config_path = '{}/config/config_etf_{}.yaml'.format(path, environment)
    config_exists = True

    if os.path.exists(config_path):
        print('found config file : {}'.format(config_path))
        break
else:
    config_path = os.path.join(dir_name, 'config_{}.yaml'.format(environment))

with open(config_path, 'r') as file:
    docs = yaml.load_all(file, Loader=yaml.FullLoader)
    for doc in docs:
        ETF_CONFIG = doc['ETF_CONFIG']
