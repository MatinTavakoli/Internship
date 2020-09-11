import random
import string
from configparser import ConfigParser

config_object = ConfigParser()

#three config versions are, let's call them gen_table and generate_table_layout and generate_multi_columns_layout
config_object['gen_table'] = {
    'idx': random.choice(string.ascii_uppercase) + ''.join(
        random.choice(string.ascii_uppercase + string.digits) for _ in range(4)),
    'top_header-style': ' style="border-bottom: 1px solid"' if random.randint(0, 1) else '',
    'right_header-style': ' style="border-left: 1px solid"' if random.randint(0, 1) else '',
    'c': random.choice([1, 2, 3]),
    'r1': random.randint(10, 1000),
    'r2': random.randint(0, 10),
    'r3': random.choice(['', '', '-', '۰']),
    'border_space': random.randint(5, 35),
    'border1': '#{0} td,#{0} th {{border: 1px solid}}',
    'border2': '#{0} td,#{0} th {{border-bottom: 1px solid}}',
    'border3': '#{0} td,#{0} th {{border: solid;border-width: 0 1px}}'

}

config_object['generate_table_layout'] = {
    'item': random.choice(['', 'h1', 'h2', 'h3']),
    'font_size1': random.randint(60, 120),
    'font_size2': random.randint(50, 100),
    'font_size3': random.randint(30, 60),
    'font_size4': random.randint(30, 50),
    'ts1': random.choice([40, 60, 80]),
    'ts2': random.choice([60, 80, 100]),
    'ts3': random.choice([80, 100, 120]),
    'ts4': random.choice([100, 200, 500]),

    'c': random.randint(4, 11),
    'b': random.randint(0, 3),
    'ob': random.randint(0, 5),
    'th1': random.randint(0, 1),
    'th2': random.choice([1, 1, 0]),
    'rh1': random.choice([1, 1, 0]),
    'rh2': random.randint(0, 1)
}
config_object['generate_multi_columns_layout'] = {
    'columns': random.randint(2, 3),
    'column_gap': round(random.uniform(1, 2), 2),
    'item': random.choice(5 * ['p'] + ['h1', 'h2', 'h3', 'img', 'table']),
    'r': random.randint(4, 6),
    'c': random.randint(3, 4),
    'b': random.randint(0, 1),
    'ob': random.randint(0, 1),
    'th': random.randint(0, 1),
    'rh': random.randint(0, 1),
    'font_size1': random.randint(60, 120),
    'font_size2': random.randint(50, 100),
    'font_size3': random.randint(30, 60),
    'font_sizep': random.randint(30, 50),
    'ts1': random.choice([40, 60, 80]),
    'ts2': random.choice([60, 80, 100]),
    'ts3': random.choice([80, 100, 120]),
    'tsp': random.choice([100, 200, 500])
}

#Write the above sections to config.ini file
with open('table-config.ini', 'w') as conf:
    config_object.write(conf)