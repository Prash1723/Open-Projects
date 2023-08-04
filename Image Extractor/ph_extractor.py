from PIL import Image
import os, pyperclip, re, send2trash
from pytesseract import image_to_string
from Screenshot import Screenshot_Clipping
from rich.console import Console

rc = Console()

# Assign Path
path = os.path.dirname(os.path.realpath(__file__))
input_path = path + '/Input/'

def open_img():
    """Open Screenshot"""
    # Open Image
    all_text = []

    for root, dirs, filenames in os.walk(input_path):
        for filename in filenames:
            try:
                img = Image.open(input_path + filename)
                all_text.append(image_to_string(img))
                # Deleting the files scanned
                send2trash.send2trash(input_path + filename)
            except:
                continue

    text = str('\n'.join(all_text))
    return text

def number_parse(text):
    """Parse phone number from the screenshot"""
    # Regex code
    phone_regex = re.compile(r'''(
        (\+91|0)?                                   # country code
        (\s|-|\.)?                                  # seperator
        (\d{5})                                     # 5 digits
        (\s|-|\.)?                                  # seperator
        (\d{5})                                     # 5 digits
    )''', re.VERBOSE)

    matches = []
    phone_num = ''

    # Extract and Arrange Phone Numbers
    for groups in phone_regex.findall(text):
        phone_num = ''.join([groups[3], groups[5]])
        matches.append(phone_num)

    if len(matches) > 0:
        distinct_matches = list(dict.fromkeys(matches))

        if len(matches)!=len(distinct_matches):
            rc.log(str(len(matches) - len(distinct_matches)) + ' Duplicates Removed')
        else:
            rc.log('No duplicates found!')

        pyperclip.copy('\n'.join(distinct_matches))
        rc.log('CopieD to clipboard')
    else:
        rc.log('No Phone no. was found!!')
