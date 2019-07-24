# -*- coding: utf-8 -*-
"""
Created on Mon Jul 22 21:55:44 2019

@author: Sanij
"""

import requests
from bs4 import BeautifulSoup

def readfile(filename):
    with open(filename, 'r',  encoding="utf-8") as fp:
        list_fighter_name=[]
        fighter_link={}
       
        for line in fp:
           read1= list(line.strip().split('<SEPARATOR>'))
           list_fighter_name.append(read1[0])
           fighter_link[read1[0]]=read1[1]
    fp.close()
    return fighter_link
    
    
def parse_fighter_basics(link):
    
    basic_attribute = ['Born', 'Height', 'Weight', 'Division', 'Reach', 'Style']
    atts_seen = []
    fighter_basic={}
    
                
    r = requests.get('https://en.wikipedia.org'+link)
    #print(r.status_code)
    #print(r.text)
    soup = BeautifulSoup(r.text, 'html.parser')
    #print(soup.title)
    
    try:
        table_element = soup.findAll("table",{'class' :"infobox vcard"})[0]
    except:
        table_element = soup.findAll("table",{'class' :"infobox biography vcard"})[0]
    rows = table_element.find_all('tr') 
    
    for i in range(1, len(rows)):
        row = rows[i]
            
        headers = row.find_all('th')
        cols = row.find_all('td')
        
        if len(headers)> 0 and len(cols) >0:
            header_text = headers[0].text
            value_text = cols[0].text
        
       # print(header_text, value_text)

            if header_text in basic_attribute:
                fighter_basic[header_text.strip()]= value_text.strip()
                atts_seen.append(header_text)

    count = 0
    for att in basic_attribute[1:4]:
        if att not in atts_seen:
            count+=1
    if count>1:
            outfile1 = open('manual_input', 'a', encoding='utf-8')
            outfile1.write(link+'\n')  
            outfile1.close()
    for att in basic_attribute:
        if att not in atts_seen:
            fighter_basic[att] = 'Not Available'


    return fighter_basic            

def write_fighter_basics():
     fighter_link = readfile('fighterLinks1')
     outfile = open('fighter_basics', 'w', encoding="utf-8")
     outfile1 = open('manual_input', 'w', encoding='utf-8') #look through the file and manually input the data for some known fighters
     outfile1.write("Below is the list of fighters' link with missing details.\n")
     outfile1.close()
     
     outfile.write('Name<SEP>Born<SEP>Height<SEP>Weight<SEP>Division<SEP>Reach<SEP>Style\n')
     errorfile = open('errors', 'w',  encoding="utf-8")
     
     for k,v in fighter_link.items():
         #print(k)
         outfile.write(k+'<SEP>')
         try:
             fighter_details = parse_fighter_basics(v)
         except:
             errorfile.write(k+'<SEP>'+v+'\n')
             print(k)
             print('*'*100)
         #print(fighter_details)
         outfile.write(fighter_details['Born']+'<SEP>'+fighter_details['Height']+'<SEP>'+fighter_details['Weight']+'<SEP>'+fighter_details['Division']+'<SEP>'+fighter_details['Reach']+'<SEP>'+fighter_details['Style']+'\n')
         outfile.flush()
     
     errorfile.close()
     
     outfile.close()
#     outfile1.close()
     
def parse_fighter_details(link):
    fights_list=[]
    
    r = requests.get('https://en.wikipedia.org'+link)
    soup = BeautifulSoup(r.text, 'html.parser')
    fight_table_candidates = soup.find_all(lambda tag: tag.name == 'table' and tag.get('class') == ['wikitable'])
    
    for table in fight_table_candidates:
        header_row = table.find_all('tr')[0]
        headers = header_row.find_all('th')
        if len(headers)>= 3 and headers[0].text.strip() == 'Res.' and headers[1].text.strip() == 'Record' and headers[2].text.strip() == 'Opponent':
            fight_table = table
            break
        
        
    
    #print(fight_table)
    rows = fight_table.find_all('tr') 
    #00print(rows)
    for row in rows:
        per_row= []
        cols = row.find_all('td')
        if len(cols) > 7:
            #print(cols)
            #print('*'*10)
            for i in range(8):
                data = cols[i]
                per_row.append(data.text.strip())
            fights_list.append(per_row)
            
    
    return fights_list    
    
    
    
    
    
def main():
    write_fighter_basics()

# =============================================================================
#      fighter_link = readfile('fighterLinks1')
#      errorfile = open('fightListerror','w', encoding= "utf-8")
#      outFile = open('fightsList','w', encoding= "utf-8")
#      outFile.write('Fighter_name<SEP>Result<SEP>Record<SEP>Opponent<SEP>Method<SEP>Event<SEP>Date<SEP>Round<SEP>Time\n')
#      counter = 1
#      for k,v in fighter_link.items():
#          #outFile.write(k+'<SEP>')
#          print(counter, k)
#          counter += 1
#          try:
#              fightList= parse_fighter_details(v)
#          except:
#              errorfile.write(k+'<SEP>'+v+'\n')
#              print(k)
#              print('*'*100)
#          #print(fightList)
#          for f in fightList:
#              outFile.write(k+'<SEP>'+f[0]+'<SEP>'+f[1]+'<SEP>'+f[2]+'<SEP>'+f[3]+'<SEP>'+f[4]+'<SEP>'+f[5]+'<SEP>'+f[6]+'<SEP>'+f[7]+'\n')
#          #outFile.write(fightList)
#          outFile.flush()
#      outFile.close()
#      errorfile.close()   
# =============================================================================
    
if __name__ == "__main__":
    main()
    