from urllib.request import urlopen,Request
from urllib.error import  HTTPError
from bs4 import BeautifulSoup
import re
import json
import requests
import validators
from time import time,sleep
data = ''
html = ''
url = ''
keyword = ''


def is_valid_url(url):
    if not (validators.url(url)):
        print("Please Enter a Valid URL")
        exit()


def fetch_initialize(url):
    global data
    global html
    try:
        print('Fetching Web Page Please wait......')
        start_time = time()
        req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        html =urlopen(req).read()
        data = BeautifulSoup(html, "html.parser")
        print('Total time taken to fetch Web page {} secoonds'.format(round(time()-start_time, 2)))
        sleep(1)

    except HTTPError as e:
        print(str(e))


def seo_title_length(data):
    print('\n\n')
    print("1.0 Analysing Title")
    if data.title:
        if len(data.title.text) < 60:
            length = "Your title length is {} which is under 60 characters \n {}".format(len(data.title.text), data.title.text)
        else:
            length = "Warning!! your title length is {} which exceed 60 character limit".format(len(data.title.text))
    else:
        return "Warning!! no title found in your Web page"
        if keyword in data.title.text:
            print('Keyword Found in Title')
        if keyword not in data.title.text:
            print('Keyword not Found in Title')
    return length


def seo_title_stop_words(data):
    print('\n\n')
    word_count = 0
    word_list =[]
    print("2.0 Looking for Stop Words in you page title")

    if data.title:
        with open('stopwords.txt','r') as f:
            for line in f:
                if re.search(r'\b' + line.rstrip('\n')+ r'\b', data.title.text.casefold()):
                    word_count += 1
                    word_list.append(line.rstrip('\n'))
        if word_count > 0:
            stop_words = 'Warning!! found {} stop words in your title '.format(word_count)
            stop_words += 'You should consider removing them {} '.format(word_list)
        else:
            stop_words = "No stop words were found in your title"
    else:
        stop_words = "Warning!! no title found in your Web page"
    return stop_words


def analyse_image_alt(data):
    print('\n\n')
    print("3.0 Analysing Images on entire page...")
    missing_alts = []
    keyword_found = []
    for a in data.find_all('a'):
        src = 'data-src'

        if a.img:
            try:
                if len(a.img['data-src']) == 0:
                    src = 'src'
            except KeyError:
                src = 'src'
                pass

            try:
                if keyword in a.img['alt'].casefold():
                    keyword_found.append(a.img[src])
                if len(a.img['alt']) == 0:
                    missing_alts.append(a.img[src])
            except KeyError:
                pass
    print("3.1 Looking for Keyword in images... ")

    if len(keyword_found) > 0:
        print('Keyword found in {} times images'.format(len(keyword_found)))
        for i in keyword_found:
            print('{}:{}'.format(keyword, i))
    else:
        print('!! {} images found with matching keyword '.format(len(keyword_found)))
    if len(missing_alts)> 0:
        print('Warning!! {} images found with missing alt tag'.format(len(missing_alts)))
        for i in missing_alts:
            print(i)
    else:
        print('!! {} images found with missing alt tag'.format(len(missing_alts)))





def analyse_meta_desc(data):
    print('\n\n')
    print("4.0 Analysing Metadata Description on your page")

    desc = data.findAll('meta', {'name': 'description'})
    if desc:
        desc = desc[0].get('content')
        if len(desc) == 0:
            return "'Warning Missing description"
        elif len(desc) < 140:
            return 'Description is too short (less than 140 characters): {0}'.format(desc)
        elif len(desc) > 255:
            return 'Description is too long (more than 255 characters): {0}'.format(desc)
        elif keyword in desc:
            return 'Keyword found in Description \nDescription:{}'.format(desc)
        else:
             return 'Keyword not found in Description \nDescription:{}'.format(desc)



def analyse_meta_keywords(data):
    print('\n\n')
    print("5.0 Analysing Metadata Keyword on your page")

    desc_key = data.findAll('meta', {'name': 'keywords'})
    if desc_key:
        desc_key = desc_key[0].get('content')
        if len(desc_key)== 0:
            return "Warning Missing Keywords in meta tag"
        elif keyword in desc_key:
            return 'Keyword {} found in meta tag keywords {}'.format(keyword, desc_key)
        else:
            return 'Warning !! Keyword not found in meta tag keywords {}'.format(keyword, desc_key)
    else:
        return "Warning metadata keyword tag does not exist in your page"


def analyse_h1_heading(data):
    print('\n\n')
    print("6.0 Analysing H1 and H2 on your page")

    htags = data.findAll('h1')
    htags2 = data.findAll('h2')

    if not htags:
        return "Warning!! missing H1 tag"
    if not htags2:
        return "Warning!! missing H2 tag"
    else:
        return "Found H1 and H2 tag on page"


def analyse_a_tags(data):
    print('\n\n')
    print("7.0 Analysing Anchor tags on page")
    no_title = []
    title = []
    anchor = data.findAll('a', href=True)
    for a in anchor:
        if not a.get('title'):
            no_title.append(a.get('href'))
        elif a.get('title'):
            title.append(a.get('href'))
        if a.text.lower().strip in ['click here', 'page', 'article']:
            print('Anchor text contains generic text: {}'.format(a.text.lower().strip))
    if len(no_title) > 0:
        print('Warning!! Total {} link found with missing title tag '.format(len(no_title)))
        print('Displaying first 5 links with missing title tag')
        for i in no_title[10: 15]:
            print(i)


def social_shares():
    print('\n\n')
    print("7.0 Analysing Social Media Impact of Web page")

    fb_share_count = 0
    update_time = ''
    tweets = 0

    try:
        page = requests.get(
            'https://graph.facebook.com/?id={}'.format(url))

        fb_data = json.loads(page.text)
        fb_share_count = fb_data['share']['share_count']
        fb_comment_count = fb_data['share']['comment_count']
        update_time = fb_data['og_object']['updated_time']
        # fb_reaction_count = fb_data['engagement']['reaction_count']
    except:
        pass

    try:
        page = requests.get(
            'http://public.newsharecounts.com/count.json?url={}'.format(url))

        twitter_data = json.loads(page.text)
        tweets = twitter_data['count']

        # fb_reaction_count = fb_data['engagement']['reaction_count']
    except:
        pass

    social = {
        'shares': fb_share_count,
        'Update Time': update_time,
        'tweets': tweets
    }
    return 'Number of Facebook Share:{} Number of Twitter Tweets {}'.format(social['shares'], social['tweets'])


def google_checker(data):
    print('\n\n')

    print("8.0 GOOGLE PAGESPEED INSIGHTS RESULTS")

    page = requests.get('https://www.googleapis.com/pagespeedonline/v1/runPagespeed?url={}'
                        .format(url))
    google_data = json.loads(page.text)
    try:
        print('Google page score {}/100'.format(google_data['score']))
        print('Page Stats')
        for key, value in google_data['pageStats'].items():
            print('{}:{}  '.format(key, value))

        print('\nRules negatively impacting score:')
        for i in google_data['formattedResults']['ruleResults']:
            print('{}: {}'.format(google_data['formattedResults'] \
                                ['ruleResults'][i]['localizedRuleName'], \
                            google_data['formattedResults']['ruleResults'][i] \
                                ['ruleImpact']))

    except Exception as e:
        print(str(e))
        pass







def main():
    global keyword, url
    url = input("which page would you like to open: Enter full URL:")
    is_valid_url(url)
    fetch_initialize(url)
    keyword = input("Enter the SEO keyword :").casefold()
    sleep(1)
    print(seo_title_length(data))
    print(seo_title_stop_words(data))
    analyse_image_alt(data)
    print(analyse_meta_desc(data))
    print(analyse_meta_keywords(data))
    print(analyse_h1_heading(data))
    analyse_a_tags(data)
    print(social_shares())
    google_checker(data)

main()