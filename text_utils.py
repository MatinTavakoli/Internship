# -*- coding: utf-8 -*-
from random import randint, uniform

keshidegi_count_word = 8
keshidegi_probability_word = .6
keshidegi_probability_line = .4

some_string = 'ئبتثجحخسشصضطظعغـفقكلمنهيپچکگی'
sticky_chars_to_next = some_string.encode().decode(encoding='utf8')

some_string2 = 'آأؤإئابةتثجحخدذرزسشصضطظعغـفقكلمنهويپچژکگی'
non_english_chars = some_string2.encode().decode(encoding='utf8')


def add_keshidegi_word(word):
    for i in range(keshidegi_count_word):
        if len(word) > 1:
            index = randint(1, len(word) - 1)
            if word[index - 1] in sticky_chars_to_next and \
                    word[index] in non_english_chars and \
                    uniform(0., 1.) < keshidegi_probability_word:
                if word[index - 1] != u'ل' or \
                        (word[index] != u'ا' and word[index] != u'آ' and word[index] != u'أ'):
                    word = word[:index] + u'ـ' + word[index:]
    return word.strip(u'ـ')


def add_keshidegi_line(line):
    if uniform(0., 1.) < keshidegi_probability_line:
        line = ' '.join(map(add_keshidegi_word, line.strip().split()))
    return line
