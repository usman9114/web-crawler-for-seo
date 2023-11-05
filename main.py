from urllib.request import urlopen, Request
from urllib.error import HTTPError
from bs4 import BeautifulSoup
import re
import json
import requests
import validators
from time import time, sleep

def is_valid_url(url):
    if not validators.url(url):
        print("Please Enter a Valid URL")
        exit()

def fetch_page(url):
    try:
        print('Fetching Web Page. Please wait...')
        start_time = time()
        req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        html = urlopen(req).read()
        data = BeautifulSoup(html, "html.parser")
        print(f'Total time taken to fetch the web page: {round(time() - start_time, 2)} seconds')
        sleep(1)
        return data
    except HTTPError as e:
        print(f"Failed to fetch the web page: {str(e)}")
        return None

def analyze_title(data, keyword):
    print('\n\n')
    print("1.0 Analyzing Title")
    if data.title:
        title_text = data.title.text
        if len(title_text) < 60:
            length = f"Your title length is {len(title_text)} which is under 60 characters:\n{title_text}"
        else:
            length = f"Warning!! Your title length is {len(title_text)} which exceeds the 60 character limit."

        if keyword in title_text:
            print('Keyword Found in Title')
        else:
            print('Keyword not Found in Title')

        return length
    else:
        return "Warning!! No title found on your web page"

def analyze_stop_words(data):
    print('\n\n')
    word_count = 0
    word_list = []
    print("2.0 Looking for Stop Words in your page title")

    if data.title:
        with open('stopwords.txt', 'r') as f:
            for line in f:
                if re.search(r'\b' + line.rstrip('\n') + r'\b', data.title.text.casefold()):
                    word_count += 1
                    word_list.append(line.rstrip('\n'))

        if word_count > 0:
            stop_words = f'Warning!! Found {word_count} stop words in your title. You should consider removing them: {word_list}'
        else:
            stop_words = "No stop words were found in your title"

        return stop_words
    else:
        return "Warning!! No title found on your web page"

def analyze_image_alt(data, keyword):
    print('\n\n')
    print("3.0 Analyzing Images on the entire page...")
    missing_alts = []
    keyword_found = []

    for a in data.find_all('a'):
        src = 'data-src'

        if a.img:
            try:
                if len(a.img.get('data-src', '')) == 0:
                    src = 'src'
            except KeyError:
                src = 'src'

            try:
                if keyword in a.img.get('alt', '').casefold():
                    keyword_found.append(a.img[src])

                if len(a.img.get('alt', '')) == 0:
                    missing_alts.append(a.img[src])
            except KeyError:
                pass

    print("3.1 Looking for Keyword in images...")

    if keyword_found:
        print(f'Keyword found in {len(keyword_found)} images')
        for img_src in keyword_found:
            print(f'{keyword}: {img_src}')
    else:
        print(f'No images found with a matching keyword')

    if missing_alts:
        print(f'Warning!! {len(missing_alts)} images found with missing alt tags')
        for img_src in missing_alts:
            print(img_src)
    else:
        print(f'No images found with missing alt tags')

def analyze_meta_desc(data, keyword):
    print('\n\n')
    print("4.0 Analyzing Metadata Description on your page")

    desc = data.find('meta', {'name': 'description'})
    if desc:
        description_content = desc.get('content', '').strip()

        if not description_content:
            return "Warning: Missing description"

        if len(description_content) < 140:
            return f'Description is too short (less than 140 characters): {description_content}'
        elif len(description_content) > 255:
            return f'Description is too long (more than 255 characters): {description_content}'
        elif keyword in description_content:
            return f'Keyword found in Description:\nDescription: {description_content}'
        else:
            return f'Keyword not found in Description:\nDescription: {description_content}'
    else:
        return "Warning: Metadata description tag does not exist on your page"

def analyze_meta_keywords(data, keyword):
    print('\n\n')
    print("5.0 Analyzing Metadata Keywords on your page")

    desc_key = data.find('meta', {'name': 'keywords'})
    if desc_key:
        keywords_content = desc_key.get('content', '').strip()

        if not keywords_content:
            return "Warning: Missing Keywords in meta tag"

        if keyword in keywords_content:
            return f'Keyword "{keyword}" found in meta tag keywords: {keywords_content}'
        else:
            return f'Warning: Keyword "{keyword}" not found in meta tag keywords: {keywords_content}'
    else:
        return "Warning: Metadata keywords tag does not exist on your page"

def analyze_h1_heading(data):
    print('\n\n')
    print("6.0 Analyzing H1 and H2 on your page")

    h1_tags = data.find_all('h1')
    h2_tags = data.find_all('h2')

    if not h1_tags:
        return "Warning: Missing H1 tags"
    if not h2_tags:
        return "Warning: Missing H2 tags"

    return "Found H1 and H2 tags on the page"

def analyze_a_tags(data):
    print('\n\n')
    print("7.0 Analyzing Anchor tags on the page")
    no_title = []
    title = []
    anchor_tags = data.find_all('a', href=True)

    for a in anchor_tags:
        if not a.get('title'):
            no_title.append(a.get('href'))
        elif a.get('title'):
            title.append(a.get('href'))

        if a.text.lower().strip() in ['click here', 'page', 'article']:
            print(f'Anchor text contains generic text: {a.text.lower().strip()}')

    if len(no_title) > 0:
        print(f'Warning: Total {len(no_title)} links found with missing title tags')
        print('Displaying first 5 links with missing title tag:')
        for link in no_title[:5]:
            print(link)

def social_shares(url):
    print('\n\n')
    print("8.0 Analyzing Social Media Impact of the web page")

    fb_share_count = 
