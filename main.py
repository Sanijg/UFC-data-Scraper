# -*- coding: utf-8 -*-
"""
Created on Mon Jul 22 08:38:50 2019

@author: Sanij
"""

import requests
from bs4 import BeautifulSoup
    
def parse_UFC_events():
    
    list_of_events = []
    event_links = {}
    
    r = requests.get('https://en.wikipedia.org/wiki/List_of_UFC_events')
    #print(r.status_code)
    #print(r.text)
    soup = BeautifulSoup(r.text, 'html.parser')
    #print(soup.title)
    table_element = soup.find("table", {"id": "Past_events"})
    rows = table_element.find_all('tr')
    
    count=0
    for row in rows:
        count+= 1
        if count>1:
            try:
                cols = row.find_all('td')
                data = cols[1]
                link = data.find('a')
                link_text = link['href']
                list_of_events.append(data.text.strip())
                event_links[data.text.strip()] = link_text.strip()
                
            except:
                print("could not parse through the event, --->", data.text)
#                print(data.text)
    #print(count)
    return list_of_events,event_links

def parse_single_event(link):
        fighters_list = []
        fighters_link = {}

        r = requests.get('https://en.wikipedia.org' + link)
        soup = BeautifulSoup(r.text, 'html.parser')
        table_element = soup.find("table", {"class": "toccolours"})
        rows = table_element.find_all('tr')
        
        for row in rows:
            try:
                cols = row.find_all('td')
                for i in [1,3]:
                    data = cols[i]
                    link = data.find('a')
                    link_text = link['href']
                    #if data.text.strip() not in fighters_list:
                    fighters_list.append(data.text.strip())
                    fighters_link[data.text.strip()] = link_text.strip()
            except:
                pass
        return fighters_list, fighters_link


def helping_single_event_parser(list_of_events, event_links):
    #I want to write the fighters' names and links to a file.
    total_list = []
    total_dict = {}
    for list in list_of_events:
        list1, dict1 = parse_single_event(event_links[list])
        for one in list1:
            if one not in total_list:
                total_list.append(one)
                total_dict[one] = dict1[one]
    
    print(*total_list, sep=' ******* ')        
    print(len(total_list))

    outfile = open('fighterLinks', 'w', encoding="utf-8")
    for k,v in total_dict.items():
        outfile.write(k+'<SEPARATOR>'+v+'\n')
    outfile.close()




def main():
    list_of_events, event_links = parse_UFC_events()
#    Sanity check
    #print(len(list_of_events),len(event_links))
    helping_single_event_parser(list_of_events, event_links)
    
if __name__ == '__main__':
    main()