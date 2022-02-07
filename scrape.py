import requests
from bs4 import BeautifulSoup
import pprint

res = requests.get('https://news.ycombinator.com/news')  # Web browser we're using without an actual window
res2 = requests.get('https://news.ycombinator.com/news?p=2')
soup_obj = BeautifulSoup(res.text, 'html.parser')
soup_obj2 = BeautifulSoup(res2.text, 'html.parser')

links = soup_obj.select('.titlelink')
sub_text = soup_obj.select('.subtext')
links2 = soup_obj2.select('.titlelink')
sub_text2 = soup_obj2.select('.subtext')

mega_links = links + links2
mega_subtext = sub_text + sub_text2

def sortStoriesByVotes(hnlist):
    return sorted(hnlist, key= lambda k:k['votes'], reverse=True)


def createCustomHN(links, sub_text):
    hnl = []
    for idx, item in enumerate(links):
        title = item.getText()
        href = item.get('href', None)
        vote = sub_text[idx].select('.score')
        if len(vote):
            votes = int(vote[0].getText().replace(' points', ''))
            if votes > 99:
                hnl.append({'title': title, 'link' : href, 'votes': votes})
    return sortStoriesByVotes(hnl)

pprint.pprint(createCustomHN(mega_links, mega_subtext))