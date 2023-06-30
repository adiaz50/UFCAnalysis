import requests
import pandas as pd
from bs4 import BeautifulSoup
import re 
from openpyxl.workbook import Workbook
import sqlalchemy


def workingCode():
    url = 'http://ufcstats.com/fight-details/6c2199524d762b11'
    soup = BeautifulSoup(requests.get(url).text, 'html.parser')
    columns = ['FIGHTER', 'W/L', 'OPPONENT', 'METHOD', 'ROUND', 'REFEREE', 'KD', 'TOTAL.SIG.LAND', 'TOTAL.SIG.THROWN','SIG.STR%','TOTAL.STR.LAND', 'TOTAL.STR.THROWN', 'TOTAL.TD.LAND', 'TOTAL.TD.THROWN','TD%','SUB.ATT','REV','CTRL',
               'RND1.KD','RND1.SIG.LAND', 'RND1.SIG.THROWN', 'RND1.SIG.STR%','RND1.STR.LAND', 'RND1.STR.THROWN','RND1.TD.LAND', 'RND1.TD.THROWN','RND1.TD%','RND1.SUB.ATT','RND1.REV','RND1.CTRL',
               'RND2.KD','RND2.SIG.LAND', 'RND2.SIG.THROWN', 'RND2.SIG.STR%','RND2.STR.LAND', 'RND2.STR.THROWN','RND2.TD.LAND', 'RND2.TD.THROWN','RND2.TD%','RND2.SUB.ATT','RND2.REV','RND2.CTRL',
               'RND3.KD','RND3.SIG.LAND', 'RND3.SIG.THROWN', 'RND3.SIG.STR%','RND3.STR.LAND', 'RND3.STR.THROWN','RND3.TD.LAND', 'RND3.TD.THROWN','RND3.TD%','RND3.SUB.ATT','RND3.REV','RND3.CTRL',
               'RND4.KD','RND4.SIG.LAND', 'RND4.SIG.THROWN', 'RND4.SIG.STR%','RND4.STR.LAND', 'RND4.STR.THROWN','RND4.TD.LAND', 'RND4.TD.THROWN','RND4.TD%','RND4.SUB.ATT','RND4.REV','RND4.CTRL',
               'RND5.KD','RND5.SIG.LAND', 'RND5.SIG.THROWN', 'RND5.SIG.STR%','RND5.STR.LAND', 'RND5.STR.THROWN','RND5.TD.LAND', 'RND5.TD.THROWN','RND5.TD%','RND5.SUB.ATT','RND5.REV','RND5.CTRL',
               'REPEAT','REPEAT','REPEAT','TOTAL.HEAD.LAND','TOTAL.HEAD.THROWN','TOTAL.BODY.LAND','TOTAL.BODY.THROWN','TOTAL.LEG.LAND','TOTAL.LEG.THROWN','TOTAL.DISTANCE.LAND','TOTAL.DISTANCE.THROWN','TOTAL.CLINCH.LAND','TOTAL.CLINCH.THROWN','TOTAL.GROUND.LAND','TOTAL.GROUND.THROWN',
               'REPEAT','REPEAT','REPEAT','RND1.HEAD.LAND','RND1.HEAD.THROWN','RND1.BODY.LAND','RND1.BODY.THROWN','RND1.LEG.LAND','RND1.LEG.THROWN','RND1.DISTANCE.LAND','RND1.DISTANCE.THROWN','RND1.CLINCH.LAND','RND1.CLINCH.THROWN','RND1.GROUND.LAND','RND1.GROUND.THROWN',
               'REPEAT','REPEAT','REPEAT','RND2.HEAD.LAND','RND2.HEAD.THROWN','RND2.BODY.LAND','RND2.BODY.THROWN','RND2.LEG.LAND','RND2.LEG.THROWN','RND2.DISTANCE.LAND','RND2.DISTANCE.THROWN','RND2.CLINCH.LAND','RND2.CLINCH.THROWN','RND2.GROUND.LAND','RND2.GROUND.THROWN',
               'REPEAT','REPEAT','REPEAT','RND3.HEAD.LAND','RND3.HEAD.THROWN','RND3.BODY.LAND','RND3.BODY.THROWN','RND3.LEG.LAND','RND3.LEG.THROWN','RND3.DISTANCE.LAND','RND3.DISTANCE.THROWN','RND3.CLINCH.LAND','RND3.CLINCH.THROWN','RND3.GROUND.LAND','RND3.GROUND.THROWN',
               'REPEAT','REPEAT','REPEAT','RND4.HEAD.LAND','RND4.HEAD.THROWN','RND4.BODY.LAND','RND4.BODY.THROWN','RND4.LEG.LAND','RND4.LEG.THROWN','RND4.DISTANCE.LAND','RND4.DISTANCE.THROWN','RND4.CLINCH.LAND','RND4.CLINCH.THROWN','RND4.GROUND.LAND','RND4.GROUND.THROWN',
               'REPEAT','REPEAT','REPEAT','RND5.HEAD.LAND','RND5.HEAD.THROWN','RND5.BODY.LAND','RND5.BODY.THROWN','RND5.LEG.LAND','RND5.LEG.THROWN','RND5.DISTANCE.LAND','RND5.DISTANCE.THROWN','RND5.CLINCH.LAND','RND5.CLINCH.THROWN','RND5.GROUND.LAND','RND5.GROUND.THROWN']
    print(len(columns))
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

    method = []
    round = []
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
    
    # give boutDetails1 and 2 the fighter name, method, round and ref
    boutDetails1 = boutDetails(half1, method, round, referee)
    boutDetails2 = boutDetails(half2, method, round, referee)
    
    ofRex = re.compile("[* of *]")
    tempOf = ""
    percRex= re.compile("[*%]")
    # populate the list for boutdetails1 and boutdetails2
    for j in range(0, len(all_data)):
        if all_data[j] != []:
            for i in range(0, len(all_data[j]),2):
                # r = re.compile("*:**")
                # print(all_data[j][i])
                if all_data[j][i] == all_data[j][0]:
                    continue
                if ofRex.search(all_data[j][i]):
                    tempOf = all_data[j][i]
                    ret = splitOf(tempOf)
                    boutDetails1.append(ret[0])
                    boutDetails1.append(ret[1])
                    continue
                if percRex.search(all_data[j][i]):
                    tempOf = all_data[j][i]
                    ret = castPercentage(tempOf)
                    boutDetails1.append(ret)
                    continue

                boutDetails1.append(all_data[j][i])


    for j in range(0, len(all_data)):
        if all_data[j] != []:
            for i in range(1, len(all_data[j]),2):
                # r = re.compile("*:**")
                # print(all_data[j][i])
                if all_data[j][i] == all_data[j][1]:
                    continue
                if ofRex.search(all_data[j][i]):
                    tempOf = all_data[j][i]
                    ret = splitOf(tempOf)
                    boutDetails2.append(ret[0])
                    boutDetails2.append(ret[1])
                    continue
                if percRex.search(all_data[j][i]):
                    tempOf = all_data[j][i]
                    ret = castPercentage(tempOf)
                    boutDetails2.append(ret)
                    continue

                boutDetails2.append(all_data[j][i])

    intRound = int(round)

    if intRound != 5:
        print("IFSTATEMENT:" )
        boutDetails1 = fillInFuncs(intRound, boutDetails1)
        print(boutDetails1)
        # print("FUNCTION1: ", boutDetails1, "\n", len(boutDetails1))
        boutDetails2 = fillInFuncs(intRound, boutDetails2)
        # print("FUNCTION2: ", boutDetails2, "\n", len(boutDetails2))
    
    # print("FUNCTION1: ", boutDetails1, "\n", len(boutDetails1))
    # print("FUNCTION2: ", boutDetails2, "\n", len(boutDetails2))


    df = pd.DataFrame([], columns=columns)

            #look into DF.CONCAT
    df = df.append(pd.Series(boutDetails1, index=df.columns[:len(boutDetails1)]), ignore_index=True)
    df = df.append(pd.Series(boutDetails2, index=df.columns[:len(boutDetails2)]), ignore_index=True)
    df.drop(columns=['REPEAT'], inplace=True)
    # Removed more than just repeat!! 
    # df = df.loc[:,~df.T.duplicated(keep=False)]
    #DROP THEM IN SQL MIGHT BE BEST
    # df = df.loc[:,~df.T.duplicated()]
    

    # engine = sqlalchemy.create_engine('mssql+pyodbc://MSI\SQLEXPRESS01/UFCData?driver=ODBC Driver 17 for SQL Server')
    # df.to_sql("TESTPY1", engine)

    print(df)

def boutDetails(half, method, round, referee):
    boutDetails = half
    boutDetails.append(method)
    boutDetails.append(round)
    boutDetails.append(referee)
    return boutDetails

# fix the function LITERAL ANSWER IS ABOVE!!!
def fillInFuncs(intRound, boutDetails1):
    x = 0
    totalRounds = 6
    roundDiff = 0
    roundDiff = totalRounds - (intRound+1)
    r = re.compile("[*:**]")
    ctrlTimeCount = 0
    bout = boutDetails1

    # FILL IN THE MISSING COLUMNS FOR FIRST PART
    for element in range(0, len(bout)):
        # Check element to count for "*:**" format
        if bout[element] == None:
            continue
        elif r.search(str(bout[element])):
            ctrlTimeCount += 1

        if ctrlTimeCount == intRound+1 and x != 1:
            x = 1
            # we need the difference between the number of rounds and the total number of rounds
            # rounds is 1 but plus 1 is two the total is 6 so the difference is 4 
            # for every round there are 9 values in between so 4 * 9 = 36 
            if roundDiff < 6 and roundDiff > 1:
                for i in range(0, (roundDiff*9)):
                    boutDetails1.insert(element+1, None)

    # FILL IN THE MISSING COLUMNS FOR SECOND PART
    for element in range(len(boutDetails1), 168):
        boutDetails1.insert(element+1, None)
    return boutDetails1

# make extra columns for total strikes thrown and total strikes landed
# DIDNT ACCOUNT FOR ODD NUMBERS EZ FIX YO!
def splitOf(string):
    if len(string)%2 == 0:
        if len(string) == 6:
            return [int(string[0]), int(string[5])]
        elif len(string) == 8:
            return [int(string[:2]), int(string[6:])]
        elif len(string) == 10:
            return [int(string[:3]), int(string[7:])]
        elif len(string) == 12:
            return [int(string[:4]), int(string[8:])]
    else:
        if len(string) == 7:
            return [int(string[0]), int(string[5:])]
        elif len(string) == 9:
            return [int(string[:2]), int(string[6:])]
        elif len(string) == 11:
            return [int(string[:4]), int(string[7:])]
    
def castPercentage(string):
    percentage = 0
    if len(string) == 2:
        percentage = float(string[0])/100
    if len(string) == 3:
        percentage = float(string[:2])/100
    if len(string) == 4:
        percentage = float(string[:3])/100
    return percentage
workingCode()
# url = 'https://www.espn.com/nba/player/gamelog/_/id/3012/kyle-lowry'

# all_data = []
# for row in soup.select('.Table__TR'):
#     tds = [td.get_text(strip=True, separator=' ') for td in row.select('.Table__TD')]
    # if len(tds) != 17:
    #     continue
    # all_data.append(tds)

# df = pd.DataFrame(all_data, columns=columns)
# print(df)