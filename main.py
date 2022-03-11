"""
author: Carly Raskin
DU ID: 873185794
this is the main .py file for my final project. The goal of this project is to web scrape data from
specified websites, and then have the program aggregate the data and create charts mapping each
teams' progress in their scores and rankings throughout the weeks. The data I am using is from this year's NCAA D1 gymnastics season.
While the season does not end until well after this quarter is over, I thought using something I am a fan of
for my final project would help me to keep passion for this final project throughout the quarter.

I do want to note that the original idea I had for this project ended up not panning out because the
main website I wanted to use does not actually use HTML tables and instead uses Javascript to make
pseudo-tables. This website (Roadtonationals.com if you want to look at the code) is the official
ranking site used by the NCAA. Because I was not able to use this main website, I had to rely on scraping
data from a blog site that is not at all run by a professional. Therefore there are extreme inconsistencies
with how the data is formatted from week-to-week (see the differences in code
between my web_scraping function and nqs6 function to see what I mean) and the HTML code is a MESS
which has caused me many problems (see the working function nqs7 to see what I mean about the HTML being wonky)
"""
import pandas as pd
from urllib import request
import ssl
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup
import requests

def web_scraping(url,week):
        context = ssl._create_unverified_context()
        page = requests.get(url)
        response = request.urlopen(url, context=context)
        html = response.read()
        df = pd.read_html(html)
        print(f"Week {week} Rankings")
        rankings = []
        i = 0
        for i in range(0, 15):
            print(df[0][0].values[i], df[0][1].values[i],df[0][2].values[i])
            if df[0][0].values[i] < 13.0:
                rankings.append([df[0][0].values[i], df[0][1].values[i],df[0][2].values[i]])
        return rankings

def nqs6():
    ''' for some reason there's a bug where the #7 team alabama's score is only
    being scraped as a 19, this causes a huge issue when I then try and graph the
    scores weekly. There is no difference in the HTML code for this team so
    I am unsure where the issue is. However I have made it so this team does not appear
    in the rankings for this week, so the teams ranked 1-6 and 8-15 will be added to the
    aggregated data '''
    url = "https://balancebeamsituation.com/2022/02/15/week-6-rankings-nqs-update/"
    context = ssl._create_unverified_context()
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    response = request.urlopen(url, context=context)
    rankings = []
    unfiltered = []
    i = 0
    print("Week 6 Rankings")
    for i in range(0, 25):
        results = soup.findAll(id=lambda x: x and x.startswith(f'{i+1}-'))
        x = str(results)
        x = x.split(f"{i+1}.")
        a = x[1].split("–")
        z = a[1].split('<')
        y = x[1].split("–")[0].strip()
        if i +1 <= 15.0 and i+1 != 7.0: # I need to exlude the 7th ranked team because the score isn't being scraped properly
            rankings.append([i+1,y,z[0]])
        unfiltered.append([i+1, y, z[0]])
    for i in range (0,15):
        print(unfiltered[i])
    return rankings

def nqs7():
    ''' I tried to do what I did for week 6 above with week 7, but unfortunately
    the source I am getting the scores from has yet ANOTHER WAY they display the results
    and use the html, therefore a team like michigan that technically went down from
    ranked 1st to ranked 3rd, will still display as the first ranked team when
    parsing the HTML because the creator of this webpage still gave Michigan the
    rank 1 in the HTML, but then just changed the text to display a 3'''
    url = "https://balancebeamsituation.com/2022/03/08/week-9-rankings-nqs-update-2/"
    context = ssl._create_unverified_context()
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    response = request.urlopen(url, context=context)
    html = response.read()
    print("Week 7 Rankings")
    df = pd.read_html(html)
    rankings = []
    i = 0
    for i in range(0, 25):
        results = soup.findAll(id=lambda x: x and x.startswith(f'{i+1}-'))
        x = str(results)
        x = x.split(f"{i+1}.")
        a = x[0].split(">")[1]
        y = a[3:len(a)-4]
        rank = a[0:1]
        # print(rank)
        # print(y)
        # print(x)
        # y = x[1].split("–")[0].strip()
        # print(a[3:len(a)-4])
        # print(df[i].values[6][1])
        # print(y)
        if i + 1 <= 15.0:
            rankings.append([rank,y,df[i].values[6][1]])
    for i in range (0,15):
        print(rankings[i])
    return rankings
nqs7()
""" see how #1 Oklahoma's score is actually attributed to Michigan??????? 
This website I get my data from is very frustrating"""

def scraping():
    urlist = []
    nqslist = []
    blanklist = []
    urlist.append("https://balancebeamsituation.com/2022/01/10/week-1-rankings-and-reactions/")
    urlist.append("https://balancebeamsituation.com/2022/01/18/week-2-rankings-and-reactions/")
    urlist.append("https://balancebeamsituation.com/2022/01/25/week-3-rankings-and-reactions/")
    urlist.append("https://balancebeamsituation.com/2022/02/01/week-4-rankings-and-reactions/")
    urlist.append("https://balancebeamsituation.com/2022/02/08/week-5-rankings-and-reactions/")
    nqslist.append("https://balancebeamsituation.com/2022/02/15/week-6-rankings-nqs-update/")
    # nqslist.append("https://balancebeamsituation.com/2022/03/08/week-9-rankings-nqs-update-2/")
    i = 1
    for val in urlist:
        blanklist.append(web_scraping(val,i))
        i+=1
    blanklist.append(nqs6())
    # print("string", blanklist)
    return blanklist

def parsingScore(list1):
    dict1 = {}
    for val in list1:
        for val2 in val:
            name = val2[1]
            dict1[name] = ['NA','NA','NA','NA','NA', "NA", "NA"]

    for idx, val in enumerate(list1):
        # print(val)
        for i in range(0, len(val)):
            # print(val[i][1])
            name = val[i][1]
            score = val[i][2]
            tmp = dict1[name]
            # print("tmp:  ",tmp)
            tmp[idx] = score
            dict1[name] = tmp
    return dict1

def parsingRank(list1):
    dict1 = {}
    for val in list1:
        for val2 in val:
            name = val2[1]
            dict1[name] = ['NA','NA','NA','NA','NA', "NA", "NA"]

    for idx, val in enumerate(list1):
        # print(val)
        for i in range(0, len(val)):
            # print(val[i][1])
            name = val[i][1]
            rank = val[i][0]
            tmp = dict1[name]
            # print("tmp:  ",tmp)
            tmp[idx] = rank
            dict1[name] = tmp
    return dict1

def main():
    x = scraping()
    y = parsingScore(x)
    z = parsingRank(x)
    dfrank = pd.DataFrame(z)
    dfrank.index = [1,2,3,4,5,6,7]
    for col in dfrank.columns:
        dfrank[col] = pd.to_numeric(dfrank[col],errors='coerce')
    colordict = {"Michigan": "pink", "Florida":"blue", "Oklahoma":"red", "Utah":'black', "Denver":"#9E0000", "LSU": "#6C007D", "Missouri":"#00FF00", "Auburn":"orange", "San Jose State": "#9090DF", "Iowa":"#4E3C00", "Alabama":"#FF00EF", "Michigan State":"green", "Minnesota":"#00D5FF", "Kentucky":"#080355", "Cal":"#BB52FF", "Arkansas":"#FF5500", "Oregon State": "#B06503", "UCLA":"yellow"}
    # print(dfrank)
    dfrank.plot(xlabel='week',ylabel='rank', color = colordict).legend(bbox_to_anchor = (1,1))
    plt.show()


    dfscore = pd.DataFrame(y)
    dfscore.index = [1, 2, 3, 4, 5, 6, 7]
    for col in dfscore.columns:
        dfscore[col] = pd.to_numeric(dfscore[col],errors='coerce')

    # print(dfscore)
    dfscore.plot(xlabel='week',ylabel='score', color = colordict).legend(bbox_to_anchor = (1,1))
    plt.show()


main()




