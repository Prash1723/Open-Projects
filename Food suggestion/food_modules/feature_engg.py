-import numpy as np
import pandas as pd
from googletrans import Translator
import pycld2 as cld2

# Import Ingredients data
with open(r'/home/praveen/Projects/Open-Projects/Food recommendation/ingredients_data/ingredients.csv') as f:
    id_dict = csv.reader(f)
    d = dict(id_dict)

d['vegetarian'] = d['vegetarian'].replace("\"", '')

# Assign translator
translator = Translator()

# Functions
def find_hi(x):
    """Translate string from hindi to english"""
    translated_text = []
    t = None
    _, _, details = cld2.detect(str(x), hintLanguage='hi')
    if details[0][1] == 'hi':
        t = translator.translate(str(x).strip())
        translated_text.append(t.text)
    else:
        translated_text.append(str(x).strip())
    return translated_text

def trim_masala(ingred):
    """Trim masalas used in the preparation for food"""
    r = []
    for i in d['masalas']:
        if ingred.find(i) != -1:
            r.append(i)
    return r

def trim_veggies(ingred):
    """Trim masalas used in the preparation for food"""
    r = []
    for i in d['vegetarian']:
        if ingred.find(i) != -1:
            r.append(i)
    return r

def value_ing(elem_ing):
    """Triming ingredients from the string"""
    numbers = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "/"]
    val = ""
    for i in elem_ing[:round(:len(elem_ing)/2)]:
        for j in numbers:
            if i in j:
                val+=i
    return val

def clean_list(ingred):
    """Split and clean the lists in the feature"""
    item_list = None
    item_list = list(ingred[1:-1].split(','))

    return [i[1:-1] for i in item_list]
