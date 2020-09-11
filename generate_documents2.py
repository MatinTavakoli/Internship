# coding: utf-8

from __future__ import unicode_literals, print_function

import codecs
import itertools
import os
import random
import re
import joblib
import hashlib
import string
from glob import glob
from render_html import render, page_layout, address
from text_utils import add_keshidegi_line

ltr = re.compile(r'[ <>*+\t\n\\\/\[\]\(\)0-9۰-۹\.:;،_-]*[A-Za-z]')
direction = lambda text: 'ltr' if ltr.match(text) else 'rtl'
hashed = lambda text: hashlib.sha224(text.encode('utf-8')).hexdigest()

def gen_table(text, rows, columns, border, outer_border, top_header, right_header, full_width=0, header_words=2):
    idx = random.choice(string.ascii_uppercase) + ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(4))
    content = '<table id="{}">'.format(idx)
    pt = 0
    words = text.split(' ')
    if columns > 5:
        header_words = 1
    
    if top_header:
        style = ''
        if random.randint(0, 1):
            style = ' style="border-bottom: 1px solid"'

        rows -= 1
        content += '<tr{}>'.format(style)
        for _ in range(columns):
            nw = random.randint(1, header_words)
            t = ' '.join(words[pt:pt+nw])
            if columns > 7:
                t = t[:10]
            content += '<th>' + ' '.join(words[pt:pt+nw]) + '</th>'
            pt += nw
        content += '</tr>'
    
    if right_header:
        columns -= 1

    for _ in range(rows):
        content += '<tr>'
        
        if right_header:
            style = ''
            if random.randint(0, 1):
                style = ' style="border-left: 1px solid"'

            nw = random.randint(1, header_words)
            content += '<th{}>{}</th>'.format(style, ' '.join(words[pt:pt+nw]))
            pt += nw

        for _ in range(columns):
            c = random.choice([1, 2, 3])
            if c == 1:
                r = random.randint(10, 1000)
            if c == 2:
                r = random.randint(0, 10)
            if c == 3:
                r = random.choice(['', '', '-', '۰'])
            content += '<td>{}</td>'.format(r)
        
        content += '</tr>'
        
    content += '</table> <style>'
    
    content += '#{} {{border: {}px solid}}'.format(idx, outer_border)

    if full_width:
        content += '#{} {{width: 100%}}'.format(idx)
    else:
        border_space = random.randint(5, 35)
        content += '#{0} td,#{0} th {{padding: {1}px}}'.format(idx, border_space)

    # if border:
    #     content += '#{0} td,#{0} th {{border: 1px solid}}'.format(idx)
    if border == 1:
        content += '#{0} td,#{0} th {{border: 1px solid}}'.format(idx)
    elif border == 2:
        content += '#{0} td,#{0} th {{border-bottom: 1px solid}}'.format(idx)
    elif border == 3:
        content += '#{0} td,#{0} th {{border: solid;border-width: 0 1px}}'.format(idx)
    
    content += '</style>'

    return content


def generate_table_layout(texts):
    lines = 0
    content = ''
    while(lines < 10):
        style = ''
        item = random.choice(['', 'h1', 'h2', 'h3'])
        text = next(texts)
        if item == 'h1':
            font_size = random.randint(60, 120)
            ts = random.choice([40, 60, 80])
            text = text[:ts]
        elif item == 'h2':
            font_size = random.randint(50, 100)
            ts = random.choice([60, 80, 100])
            text = text[:ts]
        elif item == 'h3':
            font_size = random.randint(30, 60)
            ts = random.choice([80, 100, 120])
            text = text[:ts]

        if item != '':
            style += 'font-size:{}px;'.format(font_size)
            content += '<{0} dir="{2}" style="{3}">{1}</{0}><br/>'.format(item, text.strip(u'ـ'), direction(text), style)
            

        if random.randint(0, 1):
            style = ''
            text = next(texts)
            font_size = random.randint(30, 50)
            ts = random.choice([100, 200, 500])
            text = text[:ts]
            text = add_keshidegi_line(text)
            style += 'text-align:justify;'
            if random.random() > .9:
                style += 'font-style:italic;'

            style += 'font-size:{}px;'.format(font_size)
            content += '<p dir="{1}" style="{2}">{0}</p><br/>'.format(text.strip(u'ـ'), direction(text), style)

        r = random.randint(5, 22 - lines)
        c = random.randint(4, 11)
        b = random.randint(0, 3)
        ob = random.randint(0, 5)
        th = random.randint(0, 1)
        th = random.choice([1, 1, 0])
        rh = random.choice([1, 1, 0])
        rh = random.randint(0, 1)
        text = next(texts)
        lines += r
        table = gen_table(text, r, c, b, ob, th, rh)

        content += '<div style="text-align:center;overflow:hidden">{}</div><br/><br/>'.format(table)

    return content


def generate_multi_columns_layout(texts, images):
    content = ''
    columns = random.randint(2, 3)
    column_gap = round(random.uniform(1, 2), 2)
    content += '<style> #content {{column-count: {};column-gap: {}em}}</style>'.format(columns, column_gap)
    item, last_item = '', ''
    while len(content) < 7000:
        item = random.choice(5*['p'] + ['h1', 'h2', 'h3', 'img', 'table'])

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
            r = random.randint(4, 6)
            c = random.randint(3, 4)
            b = random.randint(0, 1)
            ob = random.randint(0, 1)
            th = random.randint(0, 1)
            rh = random.randint(0, 1)
            table = gen_table(text, r, c, b, ob, th, rh, 1)
            content += '<div style="text-align:center;overflow:hidden">{}</div>'.format(table)
            continue

        style = ''
        if item == 'h1':
            font_size = random.randint(60, 120)
            ts = int(random.choice([40, 60, 80]) / columns)
            text = text[:ts]
        if item == 'h2':
            font_size = random.randint(50, 100)
            ts = int(random.choice([60, 80, 100]) / columns)
            text = text[:ts]
        if item == 'h3':
            font_size = random.randint(30, 60)
            ts = int(random.choice([80, 100, 120]) / columns)
            text = text[:ts]
        if item == 'p':
            font_size = random.randint(30, 50)
            ts = int(random.choice([100, 200, 500]) / columns)
            text = text[:ts]
            text = add_keshidegi_line(text)
            style += 'text-align:justify;'
            if random.random() > .9:
                style += 'font-style:italic;'

        style += 'font-size:{}px;'.format(font_size)
        content += '<{0} dir="{2}" style="{3}">{1}</{0}>'.format(item, text.strip(u'ـ'), direction(text), style)
    return content


def create_page_html(texts, images, fonts, layout):

    if layout == 'tabale':
        content = generate_table_layout(texts)
    elif layout == 'multi-col':
        content = generate_multi_columns_layout(texts, images)
    
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
        ('BKoodakBold.ttf', ),
        ('BLotus.ttf', 'BLotusBold.ttf', 'BLotusItalic.ttf'),
        ('BMitra.ttf', 'BMitraBold.ttf', 'BMitraItalic.ttf'),
        ('BNazanin.ttf', 'BNazaninBold.ttf', 'BNazaninItalic.ttf'),
        ('BTitrBold.ttf', ),
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
    fonts = [['fonts/'+name for name in item] for item in fonts]
    random.shuffle(images)
    texts, images, fonts = itertools.cycle(texts), itertools.cycle(images), itertools.cycle(fonts)

    # create htmls
    page_htmls = [create_page_html(texts, images, fonts, random.choice(['tabale', 'multi-col'])) for i in range(5000)]

    # render htmls
    joblib.Parallel(n_jobs=4, backend='multiprocessing')([joblib.delayed(render)(html, address('resources/generated/{}/{}.png'.format(hashed(html)[:2], hashed(html)))) for html in page_htmls])

    # print json names
    # print([os.path.abspath(filename) for filename in glob('resources/generated/*/*.json')])
