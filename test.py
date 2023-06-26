import requests
import pandas as pd
from bs4 import BeautifulSoup
import re 



url = 'http://ufcstats.com/fight-details/175d9e1ac0725145'
soup = BeautifulSoup(requests.get(url).text, 'html.parser')
columns = ['fei','foi','Date','OPP','Result','MIN','FG','FG%','3PT','3P%','FT','FT%','REB','AST','BLK','STL','PF','TO', 'PTS','feafe']

all_data = []
info1 = []
winnerLoser = []
# print("SOUP", soup.find_all('th', {"class": 'b-fight-details__table-row'}))
for row in soup.find_all('tr', {"class": 'b-fight-details__table-row'}):
    tds = [td.get_text(strip=True, separator=' ') for td in row.find_all('p',{"class": 'b-fight-details__table-text'})]
    all_data.append(tds)
# print("TDS:", all_data)
# print(len(all_data))
for row in soup.find_all('div', {"class": 'b-fight-details__content'}):
    info = [td.get_text(strip=True, separator=' ') for td in row.find_all("p", {"class": "b-fight-details__text"})]
    info1.append(info)

for row in soup.find_all('div', {'class': "b-fight-details__persons clearfix"}):
    info = [td.get_text(strip=True, separator=' ') for td in row.find_all("div", {"class": "b-fight-details__person"})]
    winnerLoser.append(info)

name = []
opponent = []
method = []
wDetails = []
round = []
win = []
loss = []
half1 = []
half2 = []
boutDetails1 = []
boutDetails2 = []

# splitting Winning details
winMethod = re.split("[A-Z]+[a-z]+:", info1[0][0])
if(re.search("[\d]", info1[0][1]) == "None"):
    print("IDK")
# if re.search("[\d]", info1[0][1]).group().isdigit():
#     winDetails = re.split("[:]", info1[0][1])
print(winMethod)
# print(winDetails)

method = winMethod[1]
round = winMethod[2]
referee = winMethod[4]


#split the winner and loser
fighter1 = winnerLoser[0][0]
fighter2 = winnerLoser[0][1]

# name, who won, opponent 
half1 = [fighter1[1:], fighter1[0], fighter2[1:]]
half2 = [fighter2[1:], fighter2[0], fighter1[1:]]

boutDetails1 = half1
boutDetails1.extend({method, round, referee})
boutDetails2 = half2
boutDetails2.extend({method, round, referee})

# print(boutDetails1)
# print(boutDetails2)

tempWinner = winnerLoser[0][1]
tempLoser = [0][0]


test1 = ["Marvin Vettori", "opponent", "STUFFS"]
test2 = ["Jordan", "idk", "and idk"]
# print(all_data)
for j in range(0, len(all_data)):
    if all_data[j] != []:
        for i in range(0, len(all_data[j]),2):
            if all_data[j][i] == all_data[j][0]:
                continue
            boutDetails1.append(all_data[j][i])

for j in range(0, len(all_data)):
    if all_data[j] != []:
        print(all_data[j])
        for i in range(1, len(all_data[j]),2):
            # print(all_data[j][i])
            if all_data[j][i] == all_data[j][1]:
                        continue
            
            boutDetails2.append(all_data[j][i])
x = 1
y = 2
t = [x, "Marvin Vettori", "opponent", "STUFFS"]
print("BOUT1:", boutDetails1, len(boutDetails1))
print("BOUT2:", boutDetails2, len(boutDetails2))

df = pd.DataFrame([], columns=range(120))

        #look into DF.CONCAT
df = df.append(pd.Series(boutDetails1, index=df.columns[:len(boutDetails1)]), ignore_index=True)
df = df.append(pd.Series(boutDetails2, index=df.columns[:len(boutDetails2)]), ignore_index=True)

# print(df)



# url = 'https://www.espn.com/nba/player/gamelog/_/id/3012/kyle-lowry'

# all_data = []
# for row in soup.select('.Table__TR'):
#     tds = [td.get_text(strip=True, separator=' ') for td in row.select('.Table__TD')]
    # if len(tds) != 17:
    #     continue
    # all_data.append(tds)

# df = pd.DataFrame(all_data, columns=columns)
# print(df)