import random
import string
from configparser import ConfigParser

config_object = ConfigParser()

#three config versions are, let's call them gen_table and generate_table_layout and generate_multi_columns_layout
config_object['gen_table'] = {
    'idx': random.choice(string.ascii_uppercase) + ''.join(
        random.choice(string.ascii_uppercase + string.digits) for _ in range(4)),
    'top_header-style': ' style="border-bottom: 1px solid"' if random.randint(0, 1) else ''
}

config_object['generate_table_layout'] = {
}
config_object['generate_multi_columns_layout'] = {
}

#Write the above sections to config.ini file
with open('table-config.ini', 'w') as conf:
    config_object.write(conf)