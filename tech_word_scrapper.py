import os
import re
import config
import requests
import urllib.request
from bs4 import BeautifulSoup

# github url
# https://github.com/sindresorhus/awesome#big-data

# Fields
# Platforms|Programming Languages|Front-End Development|Back-End Development|Big Data|Editors|Development Environment|Databases|Content Management Systems|Testing|Miscellaneous
re_fields = re.compile("(Platforms|Programming Languages|Front-End Development|Back-End Development|Big Data|Editors|Development Environment|Databases|Content Management Systems|Testing|Miscellaneous)")

def scrape_base_tech_words():

    url = "https://github.com/sindresorhus/awesome#big-data"
    # response
    url_response = requests.get(url)
    # create a soup object
    soup = BeautifulSoup(url_response.content, "html.parser")

    # heads = soup.find('div',attrs={'id':'readme'}).find_all('h2')

    # for h in heads:
    #     if re_fields.match(h.text):
    #         print(h)

    rows = soup.find('div',attrs={'id':'readme'}).find_all('ul')

    for row in rows:
        head = row.find_all('h2')
        print(head.text)
        if re_fields.match(head.text):
            # print(head.text)
            print(head)

def scrape_tech_words():
    
    # url = "https://github.com/josephmisiti/awesome-machine-learning#readme"
    # # "https://github.com/onurakpolat/awesome-bigdata#readme"
    # # "https://github.com/sindresorhus/awesome#big-data"
    # # https://github.com/igorbarinov/awesome-data-engineering#readme
    # # https://github.com/josephmisiti/awesome-machine-learning#readme
    
    # # response
    # url_response = requests.get(url)
    # # create a soup object
    # soup = BeautifulSoup(url_response.content, "html.parser")

    # # this <tr> tag with given attrs corresponds to ad rows
    # ul_rows = soup.find('div', attrs={'id':'readme'}).find_all('ul')

    # words = []

    # for row in ul_rows:
    #     # find all <h1> tags from soup object (row)
    #     ul_word = [w.text for w in row.find_all('a')]
    #     words.extend(ul_word)

    # word_file = open('ml_words.txt','w')

    # for word in words:
    #     word_file.write(word)
    #     word_file.write('\n')
    import pandas as pd
    df = pd.read_fwf('ml_words.txt')
    df_new = df.drop_duplicates(subset=['APL'], keep='first')
    df_new.to_csv('ml_w.csv', index = False)
    # print(df)

def main():
    print(scrape_tech_words())
    # print(scrape_base_tech_words())

if __name__ == "__main__":
    main()