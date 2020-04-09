import yaml
import os

BASE_PATH = os.path.dirname(__file__)
conf_file = os.path.join(BASE_PATH, 'conf/all.yaml')


def load_file(filename):
    with open(filename, 'r') as f:
        data = yaml.load(f, Loader=yaml.FullLoader)
    return data


CFG = load_file(conf_file)