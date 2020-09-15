# coding: utf-8

from __future__ import unicode_literals, print_function

import codecs
import itertools
import os
import random
import re
import time

import joblib
import hashlib
import string
from glob import glob
from render_html import render, page_layout, address

# --matin-- text_utils library commented(TODO: include library)
# from text_utils import add_keshidegi_line

# --matin-- imports added
from configparser import ConfigParser

ltr = re.compile(r'[ <>*+\t\n\\\/\[\]\(\)0-9۰-۹\.:;،_-]*[A-Za-z]')
direction = lambda text: 'ltr' if ltr.match(text) else 'rtl'
hashed = lambda text: hashlib.sha224(text.encode('utf-8')).hexdigest()

config_object = ConfigParser()


def gen_table(text, rows, columns, border, outer_border, top_header, right_header, config_file, full_width=0,
              header_words=2):
    config_object.read(config_file)
    config_gen_table = config_object['gen_table']

    idx = config_gen_table['idx']  # --matin-- reads from config file!

    content = '<table id="{}">'.format(idx)
    pt = 0
    words = text.split(' ')
    if columns > 5:
        header_words = 1

    if top_header:
        style = config_gen_table['top_header-style']  # --matin-- reads from config file!

        rows -= 1
        content += '<tr{}>'.format(style)
        for _ in range(columns):
            nw = random.randint(1, header_words)
            t = ' '.join(words[pt:pt + nw])
            if columns > 7:
                t = t[:10]
            content += '<th>' + ' '.join(words[pt:pt + nw]) + '</th>'
            pt += nw
        content += '</tr>'

    if right_header:
        columns -= 1

    for _ in range(rows):
        content += '<tr>'

        if right_header:
            style = config_gen_table['right_header-style']  # --matin-- reads from config file!

            nw = random.randint(1, header_words)
            content += '<th{}>{}</th>'.format(style, ' '.join(words[pt:pt + nw]))
            pt += nw

        for _ in range(columns):
            # os.system('python table-config.py')  # --matin-- testing
            c = int(config_gen_table['c'])  # --matin-- reads from config file!
            r = ''
            if c == 1:
                r = config_gen_table['r1']  # --matin-- reads from config file!
            elif c == 2:
                r = config_gen_table['r2']  # --matin-- reads from config file!
            elif c == 3:
                r = config_gen_table['r3']  # --matin-- reads from config file!
            print(r)  # --matin-- testing
            if r != '':
                content += '<td>{}</td>'.format(r)
            else:
                content += '<td></td>'

        content += '</tr>'

    content += '</table> <style>'

    content += '#{} {{border: {}px solid}}'.format(idx, outer_border)

    if full_width:
        content += '#{} {{width: 100%}}'.format(idx)
    else:
        border_space = config_gen_table['border_space']  # --matin-- reads from config file!
        content += '#{0} td,#{0} th {{padding: {1}px}}'.format(idx, border_space)

    # if border:
    #     content += '#{0} td,#{0} th {{border: 1px solid}}'.format(idx)
    if border == 1:
        content += config_gen_table['border1'].format(idx)  # --matin-- reads from config file!
    elif border == 2:
        content += config_gen_table['border2'].format(idx)  # --matin-- reads from config file!
    elif border == 3:
        content += config_gen_table['border3'].format(idx)  # --matin-- reads from config file!

    # content += '</style>'
    content += 'table, td, th {border: 1px solid black;}</style>'  # --matin-- changed lined to generate grid lines in all tables!

    return content


def generate_table_layout(texts, config_file):
    config_object.read(config_file)
    config_generate_table_layout = config_object['generate_table_layout']

    lines = 0
    content = ''
    while (lines < 10):
        style = ''
        item = config_generate_table_layout['item']  # --matin-- reads from config file!
        font_size = ''
        text = next(texts)
        if item == 'h1':
            font_size = config_generate_table_layout['font_size1']  # --matin-- reads from config file!
            ts = int(config_generate_table_layout['ts1'])  # --matin-- reads from config file!
            text = text[:ts]
        elif item == 'h2':
            font_size = config_generate_table_layout['font_size2']  # --matin-- reads from config file!
            ts = int(config_generate_table_layout['ts2'])  # --matin-- reads from config file!
            text = text[:ts]
        elif item == 'h3':
            font_size = config_generate_table_layout['font_size3']  # --matin-- reads from config file!
            ts = int(config_generate_table_layout['ts3'])  # --matin-- reads from config file!
            text = text[:ts]

        if item != '':
            style += 'font-size:{}px;'.format(font_size)
            content += '<{0} dir="{2}" style="{3}">{1}</{0}><br/>'.format(item, text.strip(u'ـ'), direction(text),
                                                                          style)

        if random.randint(0, 1):
            style = ''
            text = next(texts)
            font_size = config_generate_table_layout['font_size4']  # --matin-- reads from config file!
            ts = int(config_generate_table_layout['ts4'])  # --matin-- reads from config file!
            text = text[:ts]

            # --matin-- text_utils library commented(TODO: include library)
            # text = add_keshidegi_line(text)

            style += 'text-align:justify;'
            if random.random() > .9:
                style += 'font-style:italic;'

            style += 'font-size:{}px;'.format(font_size)
            content += '<p dir="{1}" style="{2}">{0}</p><br/>'.format(text.strip(u'ـ'), direction(text), style)

        r = random.randint(5, 22 - lines)
        c = int(config_generate_table_layout['c'])  # --matin-- reads from config file!
        b = config_generate_table_layout['b']  # --matin-- reads from config file!
        ob = config_generate_table_layout['ob']  # --matin-- reads from config file!

        # select one of the two methods for top header
        th = config_generate_table_layout['th1']  # --matin-- reads from config file!
        th = config_generate_table_layout['th2']  # --matin-- reads from config file!

        # select one of the two methods for right header
        rh = config_generate_table_layout['rh1']  # --matin-- reads from config file!
        rh = config_generate_table_layout['rh2']  # --matin-- reads from config file!

        text = next(texts)
        lines += r
        table = gen_table(text, r, c, b, ob, th, rh, config_file)  # --matin-- pass config file as parameter!

        content += '<div style="text-align:center;overflow:hidden">{}</div><br/><br/>'.format(table)

    return content


def generate_multi_columns_layout(texts, images, config_file):
    config_object.read(config_file)
    config_generate_table_layout = config_object['generate_multi_columns_layout']

    content = ''
    columns = int(config_generate_table_layout['columns'])
    column_gap = config_generate_table_layout['column_gap']
    content += '<style> #content {{column-count: {};column-gap: {}em}}</style>'.format(columns, column_gap)
    item, last_item = '', ''
    while len(content) < 7000:
        item = config_generate_table_layout['item']

        if item.startswith('h') and last_item.startswith('h'):
            continue
        if item == 'img' and last_item == 'img':
            continue
        last_item = item

        if item == 'img':
            content += '<div style="text-align:center"><img src="{}"></div>'.format(next(images))
            continue

        text = next(texts)
        if not text:
            continue

        if item == 'table':
            r = int(config_generate_table_layout['r'])
            c = int(config_generate_table_layout['c'])
            b = config_generate_table_layout['b']
            ob = config_generate_table_layout['ob']
            th = config_generate_table_layout['th']
            rh = config_generate_table_layout['rh']
            table = gen_table(text, r, c, b, ob, th, rh, config_file, 1)  # --matin-- pass config file as parameter!
            content += '<div style="text-align:center;overflow:hidden">{}</div>'.format(table)
            continue

        style = ''
        font_size = ''
        if item == 'h1':
            font_size = config_generate_table_layout['font_size1']
            ts = int(int(config_generate_table_layout['ts1']) / columns)
            text = text[:ts]
        if item == 'h2':
            font_size = config_generate_table_layout['font_size2']
            ts = int(int(config_generate_table_layout['ts2']) / columns)
            text = text[:ts]
        if item == 'h3':
            font_size = config_generate_table_layout['font_size3']
            ts = int(int(config_generate_table_layout['ts3']) / columns)
            text = text[:ts]
        if item == 'p':
            font_size = config_generate_table_layout['font_sizep']
            ts = int(int(config_generate_table_layout['tsp']) / columns)
            text = text[:ts]

            # --matin-- text_utils library commented(TODO: include library)
            # text = add_keshidegi_line(text)

            style += 'text-align:justify;'
            if random.random() > .9:
                style += 'font-style:italic;'

        style += 'font-size:{}px;'.format(font_size)
        content += '<{0} dir="{2}" style="{3}">{1}</{0}>'.format(item, text.strip(u'ـ'), direction(text), style)
    return content


def create_page_html(texts, images, fonts, layout):
    config_file = 'table-config.ini'  # --matin-- declare config file as variable
    content = ''
    if layout == 'tabale':
        content = generate_table_layout(texts, config_file)
    elif layout == 'multi-col':
        content = generate_multi_columns_layout(texts, images, config_file)

    html = page_layout(content, font_files=next(fonts))
    return html


if __name__ == '__main__':
    texts = [line for line in codecs.open('resources/texts.txt', 'r', 'utf-8') if line.strip()]

    # images = sum([[os.path.join(root, filename).replace('resources/', '') for filename in files] for root, _, files in os.walk('resources/images')], [])
    with open('resources/white_list.txt', 'r') as f:
        images = f.read().split('\n')

    fonts = [
        ('AMashinTahrir.ttf', 'AMashinTahrirBold.ttf', 'AMashinTahrirItalic.ttf'),
        ('Arial.ttf', 'ArialBold.ttf', 'ArialItalic.ttf'),
        ('BBadr.ttf', 'BBadrBold.ttf', 'BBadrItalic.ttf'),
        ('BBCNassim.ttf', 'BBCNassimBold.ttf', 'BBCNassimItalic.ttf'),
        ('BDavat.ttf', 'BDavat.ttf', 'BDavatItalic.ttf'),
        ('BHoma.ttf', 'BHoma.ttf', 'BHomaItalic.ttf'),
        ('BKoodakBold.ttf',),
        ('BLotus.ttf', 'BLotusBold.ttf', 'BLotusItalic.ttf'),
        ('BMitra.ttf', 'BMitraBold.ttf', 'BMitraItalic.ttf'),
        ('BNazanin.ttf', 'BNazaninBold.ttf', 'BNazaninItalic.ttf'),
        ('BTitrBold.ttf',),
        ('BYagut.ttf', 'BYagutBold.ttf', 'BYagutItalic.ttf'),
        ('BYekan+.ttf', 'BYekan+.ttf', 'BYekan+Italic.ttf'),
        ('BZar.ttf', 'BZarBold.ttf', 'BZarItalic.ttf'),
        ('CourierNew.ttf', 'CourierNewBold.ttf', 'CourierNewItalic.ttf'),
        ('HelveticaNormal.ttf', 'HelveticaBold.ttf'),
        ('IRANSans.ttf', 'IRANSansBold.ttf', 'IRANSansItalic.ttf'),
        ('NotoNaskhArabic.ttf', 'NotoNaskhArabicBold.ttf', 'NotoNaskhArabicItalic.ttf'),
        ('Tahoma.ttf', 'TahomaBold.ttf'),
        ('TimesNewRoman.ttf', 'TimesNewRomanBold.ttf', 'TimesNewRomanItalic.ttf'),
    ]
    fonts = [['fonts/' + name for name in item] for item in fonts]
    random.shuffle(images)
    texts, images, fonts = itertools.cycle(texts), itertools.cycle(images), itertools.cycle(fonts)

    # create htmls
    page_htmls = [create_page_html(texts, images, fonts, random.choice(['tabale', 'multi-col'])) for i in range(5000)]

    joblib.Parallel(n_jobs=4, backend='multiprocessing')(
        [joblib.delayed(render)(html, address('resources/generated/{}/{}.png'.format(hashed(html)[:2], hashed(html))))
         for html in page_htmls])
    # print json names
    # print([os.path.abspath(filename) for filename in glob('resources/generated/*/*.json')])
