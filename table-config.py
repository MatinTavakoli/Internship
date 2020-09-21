import random
import string
from configparser import ConfigParser

config_object = ConfigParser()

#three config versions are, let's call them gen_table, generate_table_layout and generate_multi_columns_layout
config_object['gen_table'] = {
    'idx': random.choice(string.ascii_uppercase) + ''.join(
        random.choice(string.ascii_uppercase + string.digits) for _ in range(4)),

    'top_header-style_lb': 0,  # --matin-- randint lower bound
    'top_header-style_ub': 1,  # --matin-- randint upper bound

    'right_header-style_lb': 0,  # --matin-- randint lower bound
    'right_header-style_ub': 1,  # --matin-- randint upper bound


    'c': [1, 2, 3],  # --matin-- random choice

    'r1_lb': 10,  # --matin-- randint lower bound
    'r1_ub': 1000,  # --matin-- randint upper bound

    'r2_lb': 0,  # --matin-- randint lower bound
    'r2_ub': 10,  # --matin-- randint upper bound

    'r3': ['', '', '-', '.'],  # --matin-- random choice (replaced '۰' with '.')


    'border_space_lb': 5,  # --matin-- randint lower bound
    'border_space_ub': 35,  # --matin-- randint upper bound

    'border1': '#{0} td,#{0} th {{border: 1px solid}}',
    'border2': '#{0} td,#{0} th {{border-bottom: 1px solid}}',
    'border3': '#{0} td,#{0} th {{border: solid;border-width: 0 1px}}'

}

config_object['generate_table_layout'] = {

    'item': ['', 'h1', 'h2', 'h3'],  # --matin-- random choice


    'font_size1_lb': 60,  # --matin-- randint lower bound
    'font_size1_ub': 120,  # --matin-- randint upper bound

    'font_size2_lb': 50,  # --matin-- randint lower bound
    'font_size2_ub': 100,  # --matin-- randint upper bound

    'font_size3_lb': 30,  # --matin-- randint lower bound
    'font_size3_ub': 60,  # --matin-- randint upper bound

    'font_size4_lb': 30,  # --matin-- randint lower bound
    'font_size4_ub': 50,  # --matin-- randint upper bound


    'ts1': [40, 60, 80],  # --matin-- random choice
    'ts2': [60, 80, 100],  # --matin-- random choice
    'ts3': [80, 100, 120],  # --matin-- random choice
    'ts4': [100, 200, 500],  # --matin-- random choice


    'c_lb': 4,  # --matin-- randint lower bound
    'c_ub': 11,  # --matin-- randint upper bound

    'b_lb': 0,  # --matin-- randint lower bound
    'b_ub': 3,  # --matin-- randint upper bound

    'ob_lb': 0,  # --matin-- randint lower bound
    'ob_ub': 5,  # --matin-- randint upper bound

    'th1_lb': 0,  # --matin-- randint lower bound
    'th1_ub': 1,  # --matin-- randint upper bound
    'th2': [1, 1, 0],  # --matin-- random choice

    'rh1': [1, 1, 0],  # --matin-- random choice
    'rh2_lb': 0,  # --matin-- randint lower bound
    'rh2_ub': 1,  # --matin-- randint upper bound
}
config_object['generate_multi_columns_layout'] = {

    'columns_lb': 2,  # --matin-- randint lower bound
    'columns_ub': 3,  # --matin-- randint upper bound

    'column_gap_randint_lb': 1,  # --matin-- randint lower bound
    'column_gap_randint_ub': 2,  # --matin-- randint upper bound
    'column_gap_round_prec': 2,  # --matin-- round precision


    'item': 5 * ['p'] + ['h1', 'h2', 'h3', 'img', 'table'], ## --matin-- random choice


    'r_lb': 4,
    'r_ub': 6,

    'c_lb': 3,  # --matin-- randint lower bound
    'c_ub': 4,  # --matin-- randint upper bound

    'b_lb': 0,  # --matin-- randint lower bound
    'b_ub': 1,  # --matin-- randint upper bound

    'ob_lb': 0,  # --matin-- randint lower bound
    'ob_ub': 1,  # --matin-- randint upper bound

    'th_lb': 0,  # --matin-- randint lower bound
    'th_ub': 1,  # --matin-- randint upper bound

    'rh_lb': 0,  # --matin-- randint lower bound
    'rh_ub': 1,  # --matin-- randint upper bound

    'font_size1_lb': 60,  # --matin-- randint lower bound
    'font_size1_ub': 120,  # --matin-- randint upper bound

    'font_size2_lb': 50,  # --matin-- randint lower bound
    'font_size2_ub': 100,  # --matin-- randint upper bound

    'font_size3_lb': 30,  # --matin-- randint lower bound
    'font_size3_ub': 60,  # --matin-- randint upper bound

    'font_sizep_lb': 30,  # --matin-- randint lower bound
    'font_sizep_ub': 50,  # --matin-- randint upper bound

    'ts1': [40, 60, 80],  # --matin-- random choice
    'ts2': [60, 80, 100],  # --matin-- random choice
    'ts3': [80, 100, 120],  # --matin-- random choice
    'ts4': [100, 200, 500]  # --matin-- random choice
}

#Write the above sections to config.ini file
with open('table-config.ini', 'w') as conf:
    config_object.write(conf)