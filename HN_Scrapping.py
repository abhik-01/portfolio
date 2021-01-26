from bs4 import BeautifulSoup
import requests


# function to grab the page number
def import_links(page_num):
    total_links = []
    total_sub = []
    for i in range(1, int(page_num) + 1):
        # scraping the website to get the data

        res = requests.get(f'https://news.ycombinator.com/news?p={i}')
        soup = BeautifulSoup(res.text, 'html.parser')
        links = soup.select('.storylink')
        subtexts = soup.select('.subtext')
        total_links += links
        total_sub += subtexts
    return custom_hn(total_links, total_sub)


# function to sort the list on the basis of the scores
def sorted_hn(hn_list):
    return sorted(hn_list, key=lambda k: k['Score'], reverse=True)


hn = []


# function to grab the storylink and subtext classes and make the list on the basis of the score
def custom_hn(link, subtext):
    hn.clear()
    for idx, item in enumerate(link):
        title = item.get_text()
        url = item.get('href', None)
        vote = subtext[idx].select('.score')
        if len(vote):
            score = int(vote[0].getText().replace(' points', ''))
            if score > 99:
                hn.append({'Title': title, 'Link': url, 'Score': score})
    return sorted_hn(hn)

