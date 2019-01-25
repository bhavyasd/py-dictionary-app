import bs4
import requests
import re
from bs4 import NavigableString


def main():
    print_header()
    cmd = input('Please enter a word: ')
    print()
    html = get_word_html(cmd)
    get_meaning_from_html(html)




def print_header():
    print('-----------------------------------------------')
    print('---------------DICTIONARY APP------------------')
    print('-----------------------------------------------')


def get_word_html(word):
    url = 'https://www.merriam-webster.com/dictionary/{}'.format(word)
    html_text = requests.get(url).text
    return html_text


def get_meaning_from_html(html):
    soup = bs4.BeautifulSoup(html, 'html.parser')
    headers = soup.findAll('h2')
    headers_list = [h.text for h in headers]
    definitions = soup.find_all(class_='dtText')
    if definitions is not None:
        raw_words = [tag.text for tag in definitions]
        meanings = []
        sentences = []
        for word in raw_words:
            # match = re.search(r'^\\n.*\\n', word)  //this might not be needed.
            match_word = re.search(r':.*', word)
            if match_word:
                meanings.append(match_word.group().strip(': '))
            match_sen = re.search(r'\n.*', word)
            if match_sen:
                sentences.append(match_sen.group().strip())

        sub_hd = soup.find_all(class_='function-label')
        sub_header = [sh.text for sh in sub_hd]
        syn_div = soup.find("div", {"class": "widget synonyms_list thesaurus-synonyms-module-anchor"})
        raw_data = []
        if syn_div is not None:
            for divtag in syn_div:
                # atag = divtag.find_all('a')
                if isinstance(divtag, NavigableString):
                    continue
                else:
                    raw_data.append(divtag.text.strip())

        if len(headers_list) > 0:
            print(f'{str(headers_list[0]).upper()}: ')
            for m in meanings:
                print(f'* {m}', end='\n')

            print()
            print('SAMPLE EXAMPLES')
            for s in sentences:
                if s is not "":
                    print(f'* {s}', end='\n')

            print()
            print(f'{str(headers_list[1]).upper()}: ')
            if len(sub_header) > 1:
                print(sub_header[0])
                synonyms = raw_data[2:3]
                for sy in synonyms:
                    print(f'* {sy}', end='\n')
                print()
                print(sub_header[1])
                antonyms = raw_data[4:5]
                for at in antonyms:
                    print(f'* {at}', end='\n')
            else:
                print('No data returned from the web!')
        else:
            print('No data returned from the web!')
    else:
        print('No data returned from the web!')


if __name__ == '__main__':
    main()