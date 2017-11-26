import json

def load_config():
    with open("/usr/local/etc/bbb-hal.conf", 'r') as conf_file:
        config = json.load(conf_file)
    return config
