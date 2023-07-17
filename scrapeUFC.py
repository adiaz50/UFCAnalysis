import requests
import pandas as pd
from bs4 import BeautifulSoup
import re 
from openpyxl.workbook import Workbook
import sqlalchemy


def main():
    r = requests.get("http://ufcstats.com/statistics/events/completed?page=1")

    bs = BeautifulSoup(r.text,"html.parser")
    columns = ['FIGHTER', 'W/L', 'OPPONENT', 'METHOD', 'ROUND', 'REFEREE', 'TIMESTOPPAGE', 'ELO', 'CURRENTELO','TOTALROUNDS', 'TITLEFIGHTS', 'WEIGHTCLASS', 'KD', 'TOTAL.SIG.LAND', 'TOTAL.SIG.THROWN','SIG.STR%','TOTAL.STR.LAND', 'TOTAL.STR.THROWN', 'TOTAL.TD.LAND', 'TOTAL.TD.THROWN','TD%','SUB.ATT','REV','CTRL',
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
    
    df = pd.DataFrame([], columns=columns)
    raw_data = []

    # table = bs.find_all("i", {"class": "b-statistics__table-content"})
    # print(table)

    titleDict = {}

    dfLists = []
    list = []
    dic = {}
    # NOW THERE ARE 2 IMG AND A CLASSES SO JUST 
    # IF IMG class="b-statistics__icon"
    #   Continue
    # Else 
    # run for i in bs.find_all('a', href = True):
    # to get all the right links for the table data 
    for i in bs.find_all('td', {"class": 'b-statistics__table-col'}):
        for j in i.find_all('a', {"class": 'b-link b-link_style_black'}):
            if("http://ufcstats.com/event-details/" in j['href']):
                nextPage = requests.get(j['href'])
                nextPageBs = BeautifulSoup(nextPage.text, "html.parser")
                for row in nextPageBs.find_all('tr', onclick=True):
                     if("http://ufcstats.com/fight-details/" in row['data-link']):
                        


                        followingPage = requests.get(row['data-link'])
                        followingPageBs = BeautifulSoup(followingPage.text, "html.parser")
                        # print(followingPageBs)
                        fighterStats = followingPageBs.find_all("p", {"class": "b-fight-details__table-text"})
                        fightLink = row['data-link']
                        print(fightLink)
                        # return list of lists 
                        list = workingCode(fightLink, dic, len(columns))
                        dic = list[1]
                        dfLists.append(list[0])
                        print(dic)
    for i in dfLists:
        for j in i:
            for x in j:
                df = df.append(pd.Series(x, index=df.columns[:len(x)]), ignore_index=True)
    
    for i in dic.keys():
        if i in dic:
            df.loc[(df['FIGHTER']==i), 'CURRENTELO'] = dic[i][1]

    engine = sqlalchemy.create_engine('mssql+pyodbc://MSI\SQLEXPRESS01/UFCData?driver=ODBC Driver 17 for SQL Server')
    
    df.drop(columns=['REPEAT'], inplace=True)
    df.to_sql("testingElo2", engine)
    print(df)
        # if i.find_all('a', {'class': 'b-link b-link_style_white'}, href=True):
        #     continue
        # if i.find_all('a', href=True):
        #     print(i)


        # for i in bs.find_all('td', href = True):
        #     print("uhuhhuhu")
        # fight card details

        # if("http://ufcstats.com/event-details/" in i['href']):

        #     nextPage = requests.get(i['href'])
        #     nextPageBs = BeautifulSoup(nextPage.text, "html.parser")
        #     for row in nextPageBs.find_all('tr', onclick = True):
        #         if("http://ufcstats.com/fight-details/" in row['data-link']):
        #             print("WHATEVER")

                    # fightLink = row['data-link']
                    # workingCode(fightLink, df)
                    
                    


def workingCode(url, dic, columnLength):
    soup = BeautifulSoup(requests.get(url).text, 'html.parser')
    all_data = []
    info1 = []
    winnerLoser = []
    weightData = []
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
    
    for row in soup.find_all('div', {'class': 'b-fight-details__fight-head'} ):
        weightInfo = [td.get_text(strip=True, separator=' ') for td in row.find_all("i", {"class": "b-fight-details__fight-title"})]
        weightData.append(weightInfo[0])

    method = []
    round = []
    half1 = []
    half2 = []
    boutDetails1 = []
    boutDetails2 = []
    totalRounds = []
    titleFights = []
    weightClass = []
    weightT = []


    weight = weightData[0].split(' ')
    weightT = weightTitle(weight)
    titleFights = weightT[1]
    weightClass = weightT[0]

    winMethod = re.split("[A-Z]+[a-z]+:", info1[0][0])
    
    totalRounds = winMethod[3].split(' ')
    totalRounds = totalRounds[4]

    method = winMethod[1].strip(" ")
    round = winMethod[2].strip(" ")
    tempStop = re.split(" ", winMethod[3])
    timeStopppage = tempStop[1]
    referee = winMethod[4].strip(" ")


    #split the winner and loser
    fighter1 = winnerLoser[0][0]
    fighter2 = winnerLoser[0][1]

    # name, who won, opponent 
    name1 = fighter1[1:].strip()
    winLoss1 = fighter1[0].strip()
    oppo1 = fighter2[1:].strip()

    name2 = fighter2[1:].strip()
    winLoss2 = fighter2[0].strip()
    oppo2 = fighter1[1:].strip()

    half1 = [name1, winLoss1, oppo1]
    half2 = [name2, winLoss2, oppo2]
    
    # call ELO FUNCTION HEA
    fillDic(dic, name1, oppo1, winLoss1, method)
    fillDic(dic, name2, oppo2, winLoss2, method)
    fighter1Elo = dic[name1]
    fighter2Elo = dic[name2]
    currentElo1 = 0
    currentElo2 = 0

    # give boutDetails1 and 2 the fighter name, method, round and ref
    boutDetails1 = boutDet(half1, method, round, referee, timeStopppage, int(fighter1Elo[1]), int(currentElo1), totalRounds, titleFights, weightClass)
    boutDetails2 = boutDet(half2, method, round, referee, timeStopppage, int(fighter2Elo[1]), int(currentElo2), totalRounds, titleFights, weightClass)
    
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
        boutDetails1 = fillInFuncs(intRound, boutDetails1, columnLength)
        # print("FUNCTION1: ", boutDetails1, "\n", len(boutDetails1))
        boutDetails2 = fillInFuncs(intRound, boutDetails2, columnLength)
        # print("FUNCTION2: ", boutDetails2, "\n", len(boutDetails2))
    
    # print("FUNCTION1: ", boutDetails1, "\n", len(boutDetails1))
    # print("FUNCTION2: ", boutDetails2, "\n", len(boutDetails2))


    # print(boutDetails1)
    # print(boutDetails2)
            #look into DF.CONCAT

    # df = df.append(pd.Series(boutDetails1, index=df.columns[:len(boutDetails1)]), ignore_index=True)
    # df = df.append(pd.Series(boutDetails2, index=df.columns[:len(boutDetails2)]), ignore_index=True)
    # df.drop(columns=['REPEAT'], inplace=True)

    # Removed more than just repeat!! 
    # df = df.loc[:,~df.T.duplicated(keep=False)]
    #DROP THEM IN SQL MIGHT BE BEST
    # df = df.loc[:,~df.T.duplicated()]
    # print("FUNCTION2: ", boutDetails2, "\n", len(boutDetails2))
    lists = []
    lists.append([boutDetails1, boutDetails2])
    return [lists, dic]

    # engine = sqlalchemy.create_engine('mssql+pyodbc://MSI\SQLEXPRESS01/UFCData?driver=ODBC Driver 17 for SQL Server')
    # df.to_sql("TESTPY1", engine)

    # print(df)

def fillDic(dic, name, opponentName, winLoss, winMethod):

    if name in dic:
        prevElo = dic[name][0]
        
        if opponentName in dic:
            newElo = callEloFunc(prevElo, winMethod, dic[opponentName][0], winLoss)
        else:
            newElo = callEloFunc(prevElo, winMethod, 1200, winLoss)
        if len(dic[name]) == 2:
            dic[name][0] = newElo
            dic[name][1] = newElo
        else:
            dic[name].append(newElo)
    else:
        defaultElo = 1200
        dic[name] = [defaultElo]
        if opponentName in dic:
            newElo = callEloFunc(defaultElo, winMethod, dic[opponentName][0], winLoss)
        else:
            newElo = callEloFunc(defaultElo, winMethod, defaultElo, winLoss)
            
        dic[name].append(newElo)

# what we need from dictionary
# 1) fighter, opponent
# 2) win Method 
# 3) winner
# 4) previous Elo


# Include opponent Elo if win/Draw against someone higher more points + winmethod
# if lose against someone Higher Elo lose a few points + winmethod
# if win against someone lower elo win a few points + winMethod
# if lose/Draw against someone lower elo lose more points + winMethod

def callEloFunc(prevElo, winMethod, opponentElo, winLoss):
    if winLoss == 'W':
        winnerElo = prevElo
        loserElo = opponentElo
        fix = sum(margin(winMethod, loserElo, winnerElo))
        winner = prevElo + 1 + fix + (inflation(loserElo, winnerElo) * (1 - expected(loserElo, winnerElo)))
        return winner
    elif winLoss == 'L':
        winnerElo = opponentElo
        loserElo = prevElo
        fix = margin(winMethod, loserElo, winnerElo)
        subElo = fix[1] * -1.5
        subElo += fix[0]
        winner = prevElo + 1 + subElo + (inflation(loserElo, winnerElo) * (1 - expected(loserElo, winnerElo)))
        return winner
    else:
        winnerElo = opponentElo
        loserElo = prevElo
        winner = prevElo + 1 + 1 + (inflation(loserElo, winnerElo) * (1 - expected(loserElo, winnerElo)))
        return winner

# go more into depth regarding the amount of points difference between fighters
def margin(winMethod, loserElo, winnerElo):
    diffElo = loserElo - winnerElo
    newElo = eloDifference(diffElo)
    if winMethod == "Decision - Split" or winMethod == "Decision - Unanimous" or winMethod == "DQ" or winMethod == "Decision - Majority":
        return [newElo, 3]
    elif winMethod == "KO/TKO" or winMethod == "Submission" or winMethod == "TKO - Doctor's Stoppage":
        return [newElo, 5]
    # Overturned and Could not continue
    else:
        return [0,0]

def eloDifference(diffElo):
    # if winner has more elo than loser
    newElo = 0
    if diffElo < 0:
        diffElo = diffElo*-1
        if diffElo > 100:
            newElo = 1
        elif diffElo < 100 and diffElo > 75:
            newElo = 3
        elif diffElo < 75 and diffElo > 50:
            newElo = 4
        elif diffElo < 50 and diffElo > 25:
            newElo = 6
        elif diffElo < 25 and diffElo > 0:
            newElo = 7
    # if winner has less elo than loser 
    elif diffElo > 0:
        if diffElo > 100:
            newElo = 11
        elif diffElo < 100 and diffElo > 75:
            newElo = 7
        elif diffElo < 75 and diffElo > 50:
            newElo = 6
        elif diffElo < 50 and diffElo > 25:
            newElo = 4
        elif diffElo < 25 and diffElo > 0:
            newElo = 3
    return newElo


def inflation(loserElo, winnerElo):
    return 1/(1 - ((loserElo - winnerElo) / 2200))

def expected(loserElo, winnerElo):
    exponent = (loserElo - winnerElo) / 400.0
    return 1 / ((10.0 ** (exponent)) + 1)



# Maybe make 2 tables? the first BIGDATA table we transform the columns 
# into Integers
# and the automated table wether it is a seperate table or not we 
# change it through SQL or Python? idk maybe right???? AM I CRAZY??
# idk maybe i am...
def convertToInt(df):
    if df['RND3.KD'] == None:
        print("WORKS?")

def weightTitle(weight):
    length = len(weight)
    weightClass = "Open Weight"
    titleFights = None
    # 2 normal bout
    # 3 catch weight light heavyweight bout 
    # 4 and 5 ufc title bout plus weight 
    for i in range(len(weight)):
        if length == 2:
            if "weight" in weight[i].lower():
                weightClass = weight[i]
        elif length == 3:
            if "weight" in weight[i].lower():
                weightClass = weight[i-1] +" "+ weight[i]
        elif length == 4:
            if "weight" in weight[i].lower():
                weightClass = weight[i]
            if "title" == weight[i].lower():
                titleFights = weight[i]
        elif length == 5:
            if "weight" in weight[i].lower():
                weightClass = weight[i-1] +" "+ weight[i]
            if "title" == weight[i].lower():
                titleFights = weight[i]
    
    return [weightClass, titleFights]

def boutDet(half, method, round, referee, timeStop, elo, currentElo, totalRounds,titleFights, weightClass):
    boutDetails = half
    boutDetails.append(method)
    boutDetails.append(round)
    boutDetails.append(referee)
    boutDetails.append(timeStop)
    boutDetails.append(elo)
    boutDetails.append(currentElo)
    boutDetails.append(totalRounds)
    boutDetails.append(titleFights)
    boutDetails.append(weightClass)
    return boutDetails

def fillInFuncs(intRound, boutDetails1, columnLength):
    x = 0
    totalRounds = 6
    roundDiff = 0
    roundDiff = totalRounds - (intRound+1)
    rTime = re.compile("[*:**]")
    rDash = re.compile("--")
    ctrlTimeCount = 0
    bout = boutDetails1

    # FILL IN THE MISSING COLUMNS FOR FIRST PART
    for element in range(7, len(bout)):
        # Check element to count for "*:**" format
        if bout[element] == None:
            continue
        elif rTime.search(str(bout[element])):
            ctrlTimeCount += 1
        elif rDash.search(str(bout[element])):
            if(len(str(bout[element])) == 2):
                ctrlTimeCount += 1
        
        if ctrlTimeCount == intRound+1 and x != 1:
            x = 1
            # we need the difference between the number of rounds and the total number of rounds
            # rounds is 1 but plus 1 is two the total is 6 so the difference is 4 
            # for every round there are 9 values in between so 4 * 9 = 36 
            if roundDiff < 6 and roundDiff >= 1:
                for i in range(0, (roundDiff*12)):
                    boutDetails1.insert(element+1, None)

    # FILL IN THE MISSING COLUMNS FOR SECOND PART
    for element in range(len(boutDetails1), columnLength):
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