import requests
from bs4 import BeautifulSoup
import pprint
import tkinter as tk
import webbrowser

# Height and widgth of window
HEIGHT = 800
WIDTH = 1300

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
    num =1
    for idx, item in enumerate(links):
        title = item.getText()
        href = item.get('href', None)
        vote = sub_text[idx].select('.score')

        if len(vote):
            votes = int(vote[0].getText().replace(' points', ''))
            if votes > 99:
                hnl.append({'title': title, 'link' : href, 'votes': votes})
                createInformation(title,href,votes,num)
                num+=1
    return sortStoriesByVotes(hnl)

# Create a label for inputted title, link and vote
def createInformation(title,link,votes, row_pos):
    str_title = str(title)
    str_link = str(link)
    str_votes = str(votes)

    title_label = tk.Label(frame1, text=str_title,justify="left",anchor="w",width=60,height=2,font='Helvetica 10 bold')
    title_label.grid(row=row_pos, column=0)

    link_label = tk.Label(frame1, text=str_link,fg="blue")
    link_label.grid(row=row_pos, column=1)
    link_label.bind("<Button-1>", lambda e:callBack(str_link))

    vote_label = tk.Label(frame1, text=str_votes)
    vote_label.grid(row=row_pos, column=2)

def callBack(url):
    webbrowser.open_new_tab(url)

#pprint.pprint(createCustomHN(mega_links, mega_subtext))

# Creating a canvas for the rest of the frames to be put on
root = tk.Tk()
root.title("Web Scraper")
canvas = tk.Canvas(root, height=HEIGHT, width=WIDTH)
canvas.pack()
frame1 = tk.Frame(root)
frame1.place(relheight=1,relwidth=1)

# Creates list and also all accompanying information
title_label = tk.Label(frame1, text="Title")
title_label.grid(row=0,column=0)
hyperlink_label = tk.Label(frame1, text="Hyperlink")
hyperlink_label.grid(row=0,column=1)
votes_label = tk.Label(frame1, text="Votes")
votes_label.grid(row=0,column=2)


createCustomHN(mega_links, mega_subtext)




root.mainloop()
