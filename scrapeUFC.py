import requests
from bs4 import BeautifulSoup
import re 
import pandas as pd



def main():
    r = requests.get("http://ufcstats.com/statistics/events/completed?page=all")

    bs = BeautifulSoup(r.text,"html.parser")

    raw_data = []

    # table = bs.find_all("i", {"class": "b-statistics__table-content"})
    # print(table)

    titleDict = {}
    for i in bs.find_all('a', href = True):
        # fight card details
        if("http://ufcstats.com/event-details/" in i['href']):

            nextPage = requests.get(i['href'])
            nextPageBs = BeautifulSoup(nextPage.text, "html.parser")
            for row in nextPageBs.find_all('tr', onclick = True):
                if("http://ufcstats.com/fight-details/" in row['data-link']):
                    followingPage = requests.get(row['data-link'])
                    followingPageBs = BeautifulSoup(followingPage.text, "html.parser")
                    # print(followingPageBs)
                    
                    line = followingPageBs.find_all(["th", "p", {"class": "b-fight-details__table-col", "class":"b-fight-details__table-text"}])
                    fighterStats = followingPageBs.find_all("p", {"class": "b-fight-details__table-text"})
                    fs = fighterStats[0].text
                    print("++++++++++++++++++++++++++++++++++++++",fs,len(line),"++++++++++++++++++++++++++++++++++++++")
                    # for x in line:
                    #     print(re.sub('\s+',' ', x.text))

                    # ITS 10 COLUMN NAMES
                    # THEN 20 VALUES
                    # REPEAT EXCEPT FOR ROUNDS 
                    for x in line:
                        title = re.sub('\s+',' ', x.text)
                        test = title.split()
                        faw = [" ".join(test)]
                        print(faw)

                    # for j in fighterStats:
                    #     details = re.sub('\s+',' ', j.text)
                    #     test = details.split()
                    #     faw = [" ".join(test)]
                    #     print(faw)
                    
                    

main()




# for row in table:
#     line = row.find_all("a")
    # print(line[0])
    # if "http://ufcstats.com/event-details/" in line['href']:
        # nextPage = requests.get(i['href'])
        # print(line)





# for row in table:
#     line = row.find_all("span")
#     rank = line[0].text
#     if rank == "Rnk":
#         continue
#     name = line[1].find_all("a")[0].text
#     total = line[2].text
#     print(rank,name,total)