# coding: utf-8
from __future__ import unicode_literals, print_function

import codecs
import os
import tempfile
import json
import traceback

import scipy.misc
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

#--matin-- imports added
from urllib.parse import quote
import base64
from io import BytesIO
from PIL import Image

address = lambda name: os.path.abspath(os.path.join(os.path.dirname(__file__), name))

chrome_options = Options()
# chrome_options.add_argument('--headless')
chrome_options.add_argument('--window-size=2066x2924')


def filter_out_of_page(boxes, x=2066, y=2924):
    res = []
    for b in boxes:
        x1 = int(b[0])
        y1 = int(b[1])
        w = int(b[2])
        h = int(b[3])

        if x1 >= x or y1 >= y:
            continue
        x2 = int(b[0]) + int(b[2])
        y2 = int(b[1]) + int(b[3])
        dx = dy = 0
        if x2 >= x:
            dx = x2 - x
        if y2 >= y:
            dy = y2 - y
        res.append([x1, y1, w - dx, h - dy])

    return res


def render(content, output):
    try:
        # todo: use one driver for each process
        driver = webdriver.Chrome(chrome_options=chrome_options, executable_path=address('resources/chromedriver'))
        html = codecs.open(address('document.html'), 'r', 'utf-8').read()
        html = html.replace('{{ content }}', content)

        # create directory
        if not os.path.exists(os.path.dirname(output)):
            os.makedirs(os.path.dirname(output))

        # method 1
        with tempfile.NamedTemporaryFile(dir=address('resources'), suffix='.html', delete=True) as html_file:
            print(html, file=codecs.open(html_file.name, 'w', 'utf-8'))
            driver.get('file://' + html_file.name)
            driver.get_screenshot_as_file(output)

        # method 2
        # driver.get('data:text/html;charset=utf-8, ' + quote(html))
        # image = Image.open(BytesIO(base64.b64decode(driver.get_screenshot_as_base64())))
        # driver.get_screenshot_as_file(output)

        # save image file
        # driver.get_screenshot_as_file(output) # --matin-- testing
        line_boxes, image_boxes, table_boxes = driver.execute_script('return [lineBoxes, imageBoxes, tableBoxes]')

        driver.quit()
        line_boxes = filter_out_of_page(line_boxes)
        image_boxes = filter_out_of_page(image_boxes)
        table_boxes = filter_out_of_page(table_boxes)

        # write json file
        print(json.dumps({
            'image_url': output,
            'document': {'parts': [{'box': ' '.join(map(str, box)), 'type': 'image'} for box in image_boxes] \
                                  + [{'lines': [{'box': ' '.join(map(str, box))} for box in line_boxes],
                                      'type': 'text'}] \
                                  + [{'box': ' '.join(map(str, box)), 'type': 'table'} for box in table_boxes]}
        }), file=codecs.open(output.replace('.png', '.json'), 'w', 'utf-8'))

        print(html, file=codecs.open(output.replace('.png', '.html'), 'w', 'utf-8'))

        return line_boxes, image_boxes, table_boxes
    except:
        print('error', output)
        print(traceback.print_exc())


def page_layout(content, font_files=[]):
    fonts = ''
    if len(font_files):
        fonts += """
        @font-face {
            font-family: AlefbaFont;
            font-weight: normal;
            src: url(""" + font_files[0] + """) format('truetype');
        }
        html {
            font-family: AlefbaFont;
        }
        table {
            border-collapse:collapse;
            max-width: 100%;
            margin: auto;
        }
        th, tr {
            text-align: center;
        }
        """
    if len(font_files) > 1:
        fonts += """
        @font-face {
            font-family: AlefbaFont;
            font-weight: bold;
            src: url(""" + font_files[1] + """) format('truetype');
        }
        """
    if len(font_files) > 2:
        fonts += """
        @font-face {
            font-family: AlefbaFont;
            font-style: italic;
            src: url(""" + font_files[2] + """) format('truetype');
        }
        """

    return """
    <style>
    """ + fonts + """

    html {
        direction: rtl;
        font-size: 40px;
    }

    body {
        height: 2924;
    }

    span {
        line-height: 1.2;
    }

    p {
        padding-bottom: 20px;
    }

    h1 {
        padding: 20px 0 10px;
    }

    img {
        max-width: 100%;
        margin: 20px 0;
    }

    #content {
        padding: 10px;
    }

    #content > * {
        overflow: hidden;
        max-width: 100%;
        break-inside: avoid-column;
    }
    </style>

    <div id="content">
    """ + content + """
    </div>
    """
