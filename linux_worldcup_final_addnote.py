# -*- coding: utf-8 -*-
from Tkinter import *
import ttk
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
import urllib,urllib2
import csv

'''
DATA IMPORT
'''
#The class definition of result of a sepcific year worldcup
class resultOfWorldcup:
    def __init__(self,year,country,winner,second,third,fourth):
        self.year = year
        self.country = country
        self.winner = winner
        self.second = second
        self.third = third
        self.fourth = fourth

#The class definition of sepecific match of worldcup
class matchOfWorldcup:
    def __init__(self,year,datetime,stage,team1,goal1,goal2,team2,matchID):
        self.year = year
        self.datetime = datetime
        self.stage = stage
        self.result = {}
        self.result[team1] = goal1
        self.result[team2] = goal2
        self.matchID = matchID

#The class definition of player of worldcup
class playerOfWorldcup:
    def __init__(self,name,nation):
        self.name = name        
        self.nation = nation
        self.yearNum = {}
        self.matchNum = {}

csvFile1 = open('dataset/WorldCups.csv')
csvLines1 = csv. reader(csvFile1)
data1 = []
#The dictionary of every year worldcup result
dictOfResult = {}
row1 = 0
for oneLine1 in csvLines1:
    data1.append(oneLine1)
    row1 = row1 + 1
i = 1
while i < row1:
   dictOfResult[data1[i][0]] = resultOfWorldcup(data1[i][0],data1[i][1],data1[i][2],data1[i][3],data1[i][4],data1[i][5])
   i = i + 1

csvFile2 = open('dataset/WorldCupMatches.csv')
csvLines2 = csv.reader(csvFile2)
data2 = []
#The dictionary of every sepecific match of worldcup
dictOfMatch = {}
#The dictionay of {roundID:year}
dictOfRound = {}
#The dictionary of {Team Initials:Team Full Name}
dictOfTeamname = {}
#The dictionary of {row:MatchID}
dictOfRow = {}
row2 = 0
for oneLine2 in csvLines2:
    data2.append(oneLine2)
    row2 = row2 + 1
j = 1
while j < row2:
    dictOfMatch[data2[j][17]] = matchOfWorldcup(data2[j][0],data2[j][1],data2[j][2],data2[j][5],data2[j][6],data2[j][7],data2[j][8],data2[j][17])
    dictOfRound[data2[j][16]] = data2[j][0]
    dictOfTeamname[data2[j][18]] = data2[j][5]
    dictOfTeamname[data2[j][19]] = data2[j][8]
    dictOfRow[j] = data2[j][17]
    j = j + 1

csvFile3 = open('dataset/WorldCupPlayers.csv')
csvLines3 = csv.reader(csvFile3)
data3 = []
#The dictionary of every specific player in worldcup
dictOfPlayer = {}
row3 = 0
for oneLine3 in csvLines3:
    data3.append(oneLine3)
    row3 = row3 + 1
k = 1
while k < row3:
   if data3[k][6] not in dictOfPlayer.keys():
       dictOfPlayer[data3[k][6]] = playerOfWorldcup(data3[k][6],data3[k][2])
       numberOfScore = data3[k][8].count("G")
       dictOfPlayer[data3[k][6]].matchNum[data3[k][1]] = numberOfScore
       dictOfPlayer[data3[k][6]].yearNum[dictOfRound[data3[k][0]]] = numberOfScore
   else:
       numberOfScore = data3[k][8].count("G")
       dictOfPlayer[data3[k][6]].matchNum[data3[k][1]] = numberOfScore
       if dictOfRound[data3[k][0]] in dictOfPlayer[data3[k][6]].yearNum.keys():
           dictOfPlayer[data3[k][6]].yearNum[dictOfRound[data3[k][0]]] += numberOfScore
       else:
           dictOfPlayer[data3[k][6]].yearNum[dictOfRound[data3[k][0]]] = numberOfScore
   k = k + 1    

'''
SEARCH
'''
#年份
def yearSearch(year):
    for key in dictOfResult:
        if year == int(key):
            country1 = str(dictOfResult[key].winner)
            country2 = str(dictOfResult[key].second)
            country3 = str(dictOfResult[key].third)
            country4 = str(dictOfResult[key].fourth)
            country_list = [country1,country2,country3,country4]
            print dictOfResult[key].country, country_list
            return dictOfResult[key].country, country_list   

#传入国家名，传出关于{年份：[赢的场数，进球数，输球数]}
def countryResult(countryname):
  dictOfACountry = {}
  for key in dictOfMatch:
    teams = list(dictOfMatch[key].result.keys())
    scores = list(dictOfMatch[key].result.values())
    if countryname == teams[0]:
        if dictOfMatch[key].year not in dictOfACountry:
            if int(scores[0]) > int(scores[-1]):
                win =  1
            else:
                win = 0
            get = int(scores[0])
            loss = int(scores[-1])*(-1)
            dictOfACountry[dictOfMatch[key].year] = [win,get,loss]
        else:
            if int(scores[0]) > int(scores[-1]):
                win =  1
            else:
                win = 0
            get = int(scores[0])
            loss = int(scores[-1])*(-1)
            dictOfACountry[dictOfMatch[key].year][0] += win
            dictOfACountry[dictOfMatch[key].year][1] += get
            dictOfACountry[dictOfMatch[key].year][2] += loss
    elif countryname == teams[-1]:
        if dictOfMatch[key].year not in dictOfACountry:
            if int(scores[0]) < int(scores[-1]):
                win =  1
            else:
                win = 0
            get = int(scores[-1])
            loss = int(scores[0])*(-1)
            dictOfACountry[dictOfMatch[key].year] = [win,get,loss]
        else:
            if int(scores[0]) < int(scores[-1]):
                win =  1
            else:
                win = 0
            get = int(scores[-1])
            loss = int(scores[0])*(-1)
            dictOfACountry[dictOfMatch[key].year][0] += win
            dictOfACountry[dictOfMatch[key].year][1] += get
            dictOfACountry[dictOfMatch[key].year][2] += loss
    else:
        if dictOfMatch[key].year not in dictOfACountry:
            dictOfACountry[dictOfMatch[key].year] = [0,0,0]    
  return dictOfACountry

#国家作图
def graphOfGFGA(countryname):
    dictOfACountry = countryResult(countryname)
    X = list(dictOfACountry.keys())
    X.sort() 
    W = []
    L = []
    for years in X:
        W.append(dictOfACountry[years][1])
        L.append(dictOfACountry[years][-1])

    x = list(range(len(W)))
    total_width,n = 0.8,2
    width = total_width / n
    plt.xticks(rotation=90)
    title = "The GF and GA of "+countryname
    fileName = title+".png"
    plt.title(title)
    plt.bar(x, W, width=width, label='GF',fc = 'y')
    for i in range(len(x)):
        x[i] = x[i] + width
    plt.bar(x, L, width=width, label='GA',tick_label = X,fc = 'r')
    fig=plt.gcf()
    fig.set_facecolor('none')
    plt.legend()
    ax1=plt.gca()
    ax1.patch.set_facecolor('none')                      
    ax1.patch.set_alpha(0.2)
    #plt.savefig(fileName)                     
    plt.show()
    plt.close()
    
def graphOfWintimes(countryname):
    dictOfACountry = countryResult(countryname)
    X = list(dictOfACountry.keys())
    X.sort() 

    Y = []
    for years in X:
        Y.append(dictOfACountry[years][0])
    plt.xlabel("Year")
    plt.ylabel("The Times of Win")
    plt.xticks(rotation=90)
    plt.bar(X,Y,width = 0.5)
    title = "The numbers of win of "+countryname
    fileName = title+".png"
    plt.title(title)
    #plt.savefig(fileName)
    plt.show()
    plt.close()
    
#搜索国家
    '''
def countrySearch():
    country = raw_input ("Country: ")
    graphOfGFGA(country)
    graphOfWintimes(country)
    '''

#搜索特定比赛
def matchSearch(year,country):
    listOfYearCountry = []
    for row in dictOfRow:
        if str(year) == dictOfMatch[dictOfRow[row]].year and country in dictOfMatch[dictOfRow[row]].result:
            listAMatch = [dictOfMatch[dictOfRow[row]].year,dictOfMatch[dictOfRow[row]].datetime,dictOfMatch[dictOfRow[row]].stage,country,dictOfMatch[dictOfRow[row]].result[country]]
            for team in dictOfMatch[dictOfRow[row]].result:
                if cmp(team,country) != 0:
                    listAMatch.append(team)
                    listAMatch.append(dictOfMatch[dictOfRow[row]].result[team])
            if listAMatch in listOfYearCountry:
                continue
            listOfYearCountry.append(listAMatch)
    return  listOfYearCountry


#搜索球员
def playerSearch(player):
    print player
    #player = raw_input ("Player: ")
    for key in dictOfPlayer:
        if player == key:
            #the string of the nationality of a player
            Nationality = dictOfTeamname[dictOfPlayer[key].nation]
            list1 = list(dictOfPlayer[key].yearNum.keys())
            list1.sort()
            listOfScore = []
            for year in list1:
                listOfScore.append([year,dictOfPlayer[key].yearNum[year]])
            return Nationality, listOfScore

'''
COMPARE
'''

#图像,对比时输出关于两个国家自year来赢过多少次
def graphOfComparewin(country1,country2,sinceyear):
    dict1 = countryResult(country1)
    dict2 = countryResult(country2)
    X = list(dict1.keys())
    X.sort() 
    X2 = []
    for years in X:
        if cmp(years,sinceyear) >= 0:
            X2.append(years)
    A = []
    B = []
    for years in X2:
        A.append(dict1[years][0])
        B.append(dict2[years][0])
        
    x = list(range(len(A)))
    total_width,n = 0.8,2
    width = total_width / n
    plt.xticks(rotation=90)
    title = "The compare of win times("+country1+"-"+country2+")"
    fileName = title+".png"
    plt.title(title)
    plt.bar(x, A, width=width, label=country1,fc = 'lightskyblue')
    for i in range(len(x)):
        x[i] = x[i] + width
    plt.bar(x, B, width=width, label=country2,tick_label = X2,fc = 'steelblue')
    plt.legend()
    #plt.savefig(fileName)                     
    plt.show()
    plt.close()
    
    
#图像,对比时输出关于两个国家自year来进过与丢过多少球   
def graphOfCompareGFGA(country1,country2,sinceyear):
    dict1 = countryResult(country1)
    dict2 = countryResult(country2)
    X = list(dict1.keys())
    X.sort()
    X2 = []
    for years in X:
        if cmp(years,sinceyear) >= 0:
            X2.append(years)
    A = []
    B = []
    C = []
    D = []
    for years in X2:
        A.append(dict1[years][1])
        B.append(dict1[years][-1])
        C.append(dict2[years][1])
        D.append(dict2[years][-1])
    x = list(range(len(A)))
    total_width,n = 0.8,2
    width = total_width / n
    plt.xticks(rotation=90)
    title = "The compare of GF and GA("+country1+"-"+country2+")"
    fileName = title+".png"
    plt.title(title)
    plt.bar(x, A, width=width, label='GF-'+country1,fc = 'lightskyblue')
    plt.bar(x, B, width=width, label='GA-'+country1,fc = 'lightsalmon')
    for i in range(len(x)):
        x[i] = x[i] + width
    plt.bar(x, C, width=width, label='GF-'+country2,tick_label = X2,fc = 'steelblue')
    plt.bar(x, D, width=width, label='GA-'+country2,fc = 'peachpuff')
    plt.legend()
    #plt.savefig(fileName)                     
    plt.show()
    plt.close()


#两个国家(country1, country2)间自某一年(year)战绩比较
def compareCountry(country1, country2, year):
    ##用flag统计交战次数
    flag = 0
    win1 = 0  #country1赢的次数
    fair = 0
    win2 = 0  #country2赢的次数
    for key in dictOfMatch:
        ##判断该场比赛是否在year范围里
        if year > int(dictOfMatch[key].year):
            continue
        ##在year范围内的比赛
        i = dictOfMatch[key].result.keys()[-1]
        j = dictOfMatch[key].result.keys()[0]

        if (country1 == i and country2 == j) or (country2 == i and country1 == j):
            print"MatchID:"+key+"  Score:  "+i+":"+j+"  "+dictOfMatch[key].result[i]+":"+dictOfMatch[key].result[j]
            flag += 1
            if country1 == i and country2 == j:
                if int(dictOfMatch[key].result[i]) > int(dictOfMatch[key].result[j]):
                    win1 += 1
                elif int(dictOfMatch[key].result[i]) == int(dictOfMatch[key].result[j]):
                    fair += 1
                else:
                    win2 += 1
            if country2 == i and country1 == j:
                if int(dictOfMatch[key].result[i]) > int(dictOfMatch[key].result[j]):
                    win2 += 1
                elif int(dictOfMatch[key].result[i]) == int(dictOfMatch[key].result[j]):
                    fair += 1
                else:
                    win1 += 1               
     
    ##判断flag已确定是否交战，若是，计算胜率         
    if flag != 0:
        rate1 = float(win1)/float(flag)
        rate2 = float(win2)/float(flag)
        print "Since "+str(year)+", "+country1+" and "+country2+" have fought "+str(flag)+" games"
        print country1+":"+country2+"  Win:"+str(win1)+"  Fair:"+str(fair)+"  Lose:"+str(win2)
        print "Winning rate："+str('%.2f%%' % (rate1 * 100))+" : "+str('%.2f%%' % (rate2 * 100))
        return str(win1),str(fair),str(win2),str('%.2f%%' % (rate1 * 100)),str('%.2f%%' % (rate2 * 100))
    else:
        return None


##字典相加的函数
def dict_add(*objs):
    _keys = set(sum([obj.keys() for obj in objs], []))
    _total = {}
    for _key in _keys:
        _total[_key] = sum([int(obj.get(_key, 0)) for obj in objs])
    return _total

'''
STATISTIC
'''
##数据统计：国家进球总个数，国家获胜场数
##另开section，计算前16强自1930年以来
    
##用于绘制图表
def makeList(goal):
    sort_d=sorted(goal.items(),key = lambda d:d[1],reverse=True)
    count = 0
    list1 = []
    list2 = []
    for key, value in sort_d:
        count += 1
        list1.append(key)
        list2.append(value)
        if count >= 16:
            break   
    list1=list(reversed(list1))
    list2=list(reversed(list2))
    return list1, list2
 
##1930年来国家进球总数图表   
def graphGoal():
    dictOfGoal = {}
    for key in dictOfMatch:
        dictOfGoal = dict_add(dictOfGoal, dictOfMatch[key].result)
    list1, list2 = makeList(dictOfGoal)
    title = "Top 16 countries in the 1930 World Cup goals"
    plt.title(title)
    plt.barh(range(len(list2)), list2, color = ['lightskyblue','steelblue'], tick_label = list1)
    plt.show()
    
    
##1930年来国家获胜场数表
def graphWin():
    dictOfWin = {}
    for key in dictOfMatch:
        i = dictOfMatch[key].result.keys()[-1]
        j = dictOfMatch[key].result.keys()[0]
        if int(dictOfMatch[key].result[i])>int(dictOfMatch[key].result[j]):
            if i not in dictOfWin.keys():
                dictOfWin[i] = 0
            dictOfWin[i] = dictOfWin[i] + 1
        if int(dictOfMatch[key].result[i])<int(dictOfMatch[key].result[j]):
            if j not in dictOfWin.keys():
                dictOfWin[j] = 0
            dictOfWin[j] = dictOfWin[j] + 1
    list1, list2 = makeList(dictOfWin)
    title = "Top 16 countries in the 1930 World Cup victory"
    plt.title(title)
    plt.barh(range(len(list2)), list2, color = ['lightskyblue','steelblue'], tick_label = list1)
    plt.show()
    

##用于年份的每个国家进球数统计表
def graphYear():
    year = input("Please input a year: ")
    yearOfGoal = {}
    for key in dictOfMatch:
        if int(dictOfMatch[key].year) != year:
            continue
        yearOfGoal = dict_add(yearOfGoal, dictOfMatch[key].result)
    makeGraph(yearOfGoal)


'''
INTERFACE
'''

root = Tk() 
root.title("FIFA World Cup")
root.geometry("1440x810")

# add picture
## background
bg = PhotoImage(file = "figures/background.gif")
## main button
search = PhotoImage(file = "figures/search.gif")
compare = PhotoImage(file = "figures/compare.gif")
stat = PhotoImage(file = "figures/stat.gif")
best = PhotoImage(file = "figures/best.gif")
## return
return_logo = PhotoImage(file = "figures/return_1.gif")
## search
team_match = PhotoImage(file = "figures/Matches Won  in Each World Cup.gif")
team_goal = PhotoImage(file = "figures/Goals Achieved  in Each World Cup.gif")
## compare
vs = PhotoImage(file = "figures/vs.gif")
## statistics
stat_match = PhotoImage(file = "figures/stat_match.gif")
stat_goal = PhotoImage(file = "figures/stat_goal.gif")
## flags
Algeria = PhotoImage(file = "flag/Algeria.gif")
Angola = PhotoImage(file = "flag/Angola.gif")
Argentina = PhotoImage(file = "flag/Argentina.gif")
Australia = PhotoImage(file = "flag/Australia.gif")
Austria = PhotoImage(file = "flag/Austria.gif")
Belgium = PhotoImage(file = "flag/Belgium.gif")
Bolivia = PhotoImage(file = "flag/Bolivia.gif")
Bosnia_and_Herzegovina = PhotoImage(file = "flag/Bosnia and Herzegovina.gif")
Brazil = PhotoImage(file = "flag/Brazil.gif")
Bulgaria = PhotoImage(file = "flag/Bulgaria.gif")
Cameroon = PhotoImage(file = "flag/Cameroon.gif")
Canada = PhotoImage(file = "flag/Canada.gif")
Chile = PhotoImage(file = "flag/Chile.gif")
China_PR = PhotoImage(file = "flag/China PR.gif")
Colombia = PhotoImage(file = "flag/Colombia.gif")
Costa_Rica = PhotoImage(file = "flag/Costa Rica.gif")
Cote_dIvoire = PhotoImage(file = "flag/Cote d'Ivoire.gif")
Croatia = PhotoImage(file = "flag/Croatia.gif")
Cuba = PhotoImage(file = "flag/Cuba.gif")
Czech_Republic = PhotoImage(file = "flag/Czech Republic.gif")
Czechoslovakia = PhotoImage(file = "flag/Czechoslovakia.gif")
Denmark = PhotoImage(file = "flag/Denmark.gif")
Dutch_East_Indies = PhotoImage(file = "flag/Dutch East Indies.gif")
Ecuador = PhotoImage(file = "flag/Ecuador.gif")
Egypt = PhotoImage(file = "flag/Egypt.gif")
El_Salvador = PhotoImage(file = "flag/El Salvador.gif")
England = PhotoImage(file = "flag/England.gif")
France = PhotoImage(file = "flag/France.gif")
Germany = PhotoImage(file = "flag/Germany.gif")
Ghana = PhotoImage(file = "flag/Ghana.gif")
Greece = PhotoImage(file = "flag/Greece.gif")
Haiti = PhotoImage(file = "flag/Haiti.gif")
Honduras = PhotoImage(file = "flag/Honduras.gif")
Hungary = PhotoImage(file = "flag/Hungary.gif")
IR_Iran = PhotoImage(file = "flag/IR Iran.gif")
Iran = PhotoImage(file = "flag/Iran.gif")
Iraq = PhotoImage(file = "flag/Iraq.gif")
Israel = PhotoImage(file = "flag/Israel.gif")
Italy = PhotoImage(file = "flag/Italy.gif")
Jamaica = PhotoImage(file = "flag/Jamaica.gif")
Japan = PhotoImage(file = "flag/Japan.gif")
Korea_DPR = PhotoImage(file = "flag/Korea DPR.gif")
Korea_Republic = PhotoImage(file = "flag/Korea Republic.gif")
Kuwait = PhotoImage(file = "flag/Kuwait.gif")
Mexico = PhotoImage(file = "flag/Mexico.gif")
Morocco = PhotoImage(file = "flag/Morocco.gif")
Netherlands = PhotoImage(file = "flag/Netherlands.gif")
New_Zealand = PhotoImage(file = "flag/New Zealand.gif")
Nigeria = PhotoImage(file = "flag/Nigeria.gif")
Northern_Ireland = PhotoImage(file = "flag/Northern Ireland.gif")
Norway = PhotoImage(file = "flag/Norway.gif")
Paraguay = PhotoImage(file = "flag/Paraguay.gif")
Peru = PhotoImage(file = "flag/Peru.gif")
Poland = PhotoImage(file = "flag/Poland.gif")
Portugal = PhotoImage(file = "flag/Portugal.gif")
Republic_of_Ireland = PhotoImage(file = "flag/Republic of Ireland.gif")
Romania = PhotoImage(file = "flag/Romania.gif")
Russia = PhotoImage(file = "flag/Russia.gif")
Saudi_Arabia = PhotoImage(file = "flag/Saudi Arabia.gif")
Scotland = PhotoImage(file = "flag/Scotland.gif")
Senegal = PhotoImage(file = "flag/Senegal.gif")
Serbia = PhotoImage(file = "flag/Serbia.gif")
Serbia_and_Montenegro = PhotoImage(file = "flag/Serbia and Montenegro.gif")
Slovakia = PhotoImage(file = "flag/Slovakia.gif")
Slovenia = PhotoImage(file = "flag/Slovenia.gif")
South_Africa = PhotoImage(file = "flag/South Africa.gif")
Soviet_Union = PhotoImage(file = "flag/Soviet Union.gif")
Spain = PhotoImage(file = "flag/Spain.gif")
Sweden = PhotoImage(file = "flag/Sweden.gif")
Switzerland = PhotoImage(file = "flag/Switzerland.gif")
Togo = PhotoImage(file = "flag/Togo.gif")
Trinidad_and_Tobago = PhotoImage(file = "flag/Trinidad and Tobago.gif")
Tunisia = PhotoImage(file = "flag/Tunisia.gif")
Turkey = PhotoImage(file = "flag/Turkey.gif")
Ukraine = PhotoImage(file = "flag/Ukraine.gif")
United_Arab_Emirates = PhotoImage(file = "flag/United Arab Emirates.gif")
Uruguay = PhotoImage(file = "flag/Uruguay.gif")
USA = PhotoImage(file = "flag/USA.gif")
Wales = PhotoImage(file = "flag/Wales.gif")
Yugoslavia = PhotoImage(file = "flag/Yugoslavia.gif")
Zaire = PhotoImage(file = "flag/Zaire.gif")

# dictionary of team names and flags
country_d={"Algeria":Algeria, "Angola":Angola, "Argentina":Argentina, "Australia":Australia, "Austria":Austria, "Belgium":Belgium, "Bolivia":Bolivia, "Bosnia and Herzegovina":Bosnia_and_Herzegovina, "Brazil":Brazil, "Bulgaria":Bulgaria, "Cameroon":Cameroon, "Canada":Canada, "Chile":Chile, "China PR":China_PR, "Colombia":Colombia, "Costa Rica":Costa_Rica, "Cote d'Ivoire":Cote_dIvoire, "Croatia":Croatia, "Cuba":Cuba, "Czech Republic":Czech_Republic, "Czechoslovakia":Czechoslovakia, "Denmark":Denmark, "Dutch East Indies":Dutch_East_Indies, "Ecuador":Ecuador, "Egypt":Egypt, "El Salvador":El_Salvador, "England":England, "France":France, "Germany":Germany, "Ghana":Ghana, "Greece":Greece, "Haiti":Haiti, "Honduras":Honduras, "Hungary":Hungary, "IR Iran":IR_Iran, "Iran":Iran, "Iraq":Iraq, "Israel":Israel, "Italy":Italy, "Jamaica":Jamaica, "Japan":Japan, "Korea DPR":Korea_DPR, "Korea Republic":Korea_Republic, "Kuwait":Kuwait, "Mexico":Mexico, "Morocco":Morocco, "Netherlands":Netherlands, "New Zealand":New_Zealand, "Nigeria":Nigeria, "Northern Ireland":Northern_Ireland, "Norway":Norway, "Paraguay":Paraguay, "Peru":Peru, "Poland":Poland, "Portugal":Portugal, "Republic of Ireland":Republic_of_Ireland, "Romania":Romania, "Russia":Russia, "Saudi Arabia":Saudi_Arabia, "Scotland":Scotland, "Senegal":Senegal, "Serbia":Serbia, "Serbia and Montenegro":Serbia_and_Montenegro, "Slovakia":Slovakia, "Slovenia":Slovenia, "South Africa":South_Africa, "Soviet Union":Soviet_Union, "Spain":Spain, "Sweden":Sweden, "Switzerland":Switzerland, "Togo":Togo, "Trinidad and Tobago":Trinidad_and_Tobago, "Tunisia":Tunisia, "Turkey":Turkey, "Ukraine":Ukraine, "United Arab Emirates":United_Arab_Emirates, "Uruguay":Uruguay, "USA":USA, "Wales":Wales, "Yugoslavia":Yugoslavia, "Zaire":Zaire}

# define global variables
f_main_button = Frame(root, height = 600, width = 600)
f_search = Frame(root, height = 600, width = 600)
f_compare = Frame(root, height = 600, width = 600)
f_stat = Frame(root, height = 600, width = 600)
f_best = Frame(root, height = 600, width = 600)
b_return = Button(root, text = "Return")

# add background or cover previous widgets
def add_bg():
    backf = Frame(root, width = 1440, height = 810, borderwidth = 0)
    background = Label(backf, image = bg)
    background.place(x=0,y=0,anchor=NW)
    #Label(backf, text = "Designed by Yang Xue, Ma Qing, Gao Ruitian, Ma Xueyi\nVersion 1.2", font = ("Arial", 10), justify = RIGHT).place(relx = 1.0, rely = 1.0, anchor = SE)
    backf.place(x=0,y=0,anchor=NW)

# main return button
def b_return_create():
    b_return = Button(root, width = 57, height = 57, image = return_logo, bg = "white", bd = 0, command = b_return_main)
    b_return.place(relx = 0.979, rely = 0.904, anchor = SE)

def b_return_main():
    add_bg()
    menu()

# search interfaces
def search_year(x):
    add_bg()
    f_search = Frame(root, height = 500, width = 1440)
    f_search.place(x = 720, y = 504.2, anchor = CENTER)
    Label(f_search, text = "Search for Year", font = ("Skia", 50), fg = "#003366").place(relx = 0.02, rely = 0.05, anchor = NW)

    # get results
    host, top_four = yearSearch(int(x))
    
    # results display
    Label(f_search, text = "Host Country: "+host, font = ("Skia", 40), fg = "#003366").place(relx = 0.3, rely = 0.2)
    Label(f_search, text = "Champion: "+top_four[0], font = ("Skia", 40), fg = "#990000").place(relx = 0.3, rely = 0.35)
    Label(f_search, text = "Second: "+top_four[1], font = ("Skia", 40), fg = "#990000").place(relx = 0.3, rely = 0.5)
    Label(f_search, text = "Third: "+top_four[2], font = ("Skia", 40), fg = "#990000").place(relx = 0.3, rely = 0.65)
    Label(f_search, text = "Fourth: "+top_four[3], font = ("Skia", 40), fg = "#990000").place(relx = 0.3, rely = 0.8)

    b_return = Button(root, width = 57, height = 57, image = return_logo, bg = "white", bd = 0, command = b_search)
    b_return.place(relx = 0.979, rely = 0.904, anchor = SE)
    
def search_team(y):
    add_bg()
    f_search = Frame(root, height = 500, width = 1440)
    f_search.place(x = 720, y = 504.2, anchor = CENTER)
    Label(f_search, text = "Search for Teams", font = ("Skia", 50), fg = "#003366").place(relx = 0.02, rely = 0.05, anchor = NW)

    # buttons for graphs
    Button(f_search, image = team_match, width = 364, height = 327, command = lambda: graphOfGFGA(y)).place(relx = 0.2, rely = 0.25, anchor = NW)
    Button(f_search, image = team_goal, width = 364, height = 327, command = lambda: graphOfWintimes(y)).place(relx = 0.8, rely = 0.25, anchor = NE)
    
    b_return = Button(root, width = 57, height = 57, image = return_logo, bg = "white", bd = 0, command = b_search)
    b_return.place(relx = 0.979, rely = 0.904, anchor = SE)

def search_match(year,team):
    # get results
    result = matchSearch(year, team)

    # results display
    if result != []:
        add_bg()
        f_search = Frame(root, height = 500, width = 1440)
        f_search.pack()

        # show results
        tree = ttk.Treeview(f_search, show="headings")
        tree["columns"]=("Year","Time","Stage","Opponents","Score1","Score2")
        tree.column("Year",width=100, anchor='center') 
        tree.column("Time",width=200, anchor='center')
        tree.column("Stage",width=120, anchor='center')
        tree.column("Opponents",width=120, anchor='center') 
        tree.column("Score1",width=100, anchor='center')
        tree.column("Score2",width=100, anchor='center')

        tree.heading("Year",text="Year") 
        tree.heading("Time",text="Time")
        tree.heading("Stage",text="Stage")
        tree.heading("Opponents",text="Opponent") 
        tree.heading("Score1",text="Goal")
        tree.heading("Score2",text="Opp. Goal")
        
        count = 0
        for match in result:
            print match
            tree.insert('',count,values=(match[0],match[1],match[2],match[5],match[4],match[6]))
            count += 1
        Label(f_search, text = team + " in " + year, font = ("Skia", 50), fg = "#003366").pack()
        tree.pack(side = BOTTOM)
        f_search.place(x=720, y=455, anchor = CENTER)

        b_return = Button(root, width = 57, height = 57, image = return_logo, bg = "white", bd = 0, command = b_search)
        b_return.place(x=1090,y=630, anchor = NE)
    else:
        Label(root, text = team+" did not join the World Cup in "+year+"!\nPlease choose again!", justify = LEFT).place(relx=0.4, rely=0.63)

# get year and team from menubuttons and select search mode
def get_yt(x,y):
    print x,y
    if x == "DEFAULT" and y == "DEFAULT":
        Label(root, text = "Please choose a team or a year!\nPlease choose again!", justify = LEFT).place(relx=0.4, rely=0.63)
    elif x != "DEFAULT" and y == "DEFAULT":
        search_year(x)
    elif x == "DEFAULT" and y != "DEFAULT":
        search_team(y)
    elif x != "DEFAULT" and y != "DEFAULT":
        search_match(x,y)
        

def search_player(player):
    name = player.get()
    if playerSearch(name) != None:
        add_bg()
        f_search = Frame(root, height = 500, width = 1440)
        f_search.pack()

        # get results
        nation, score = playerSearch(name)

        # results display
        tree = ttk.Treeview(f_search, show="headings")
        tree["columns"]=("Year","Goals")
        tree.column("Year",width=250, anchor='center')
        tree.column("Goals",width=250, anchor='center')

        tree.heading("Year",text="Year") 
        tree.heading("Goals",text="Goals")
        
        count = 0
        for year in score:
            tree.insert('',count,values=(year[0], year[1]))
            count += 1
        Label(f_search, text = name + " from " + nation, font = ("Skia", 50), fg = "#003366").pack()
        tree.pack(side = BOTTOM)
        f_search.place(x=720, y=455, anchor = CENTER)

        b_return = Button(root, width = 57, height = 57, image = return_logo, bg = "white", bd = 0, command = b_search)
        b_return.place(x=1090,y=630, anchor = NE)
    else:
        Label(root, text = "Wrong Input of Players!\nPlease Enter Again!", justify = LEFT).place(relx = 0.8, rely = 0.63, anchor = W)

def b_search():
    add_bg()
    f_search = Frame(root, height = 500, width = 1440)
    f_search.place(x = 720, y = 504.2, anchor = CENTER)
    Label(f_search, text = "Search", font = ("Skia", 50), fg = "#003366").place(relx = 0.02, rely = 0.05, anchor = NW)
    Label(f_search, text = "Choose a year:", font = ("Skia", 30), fg = "#003366").place(relx = 0.05, rely = 0.3, anchor = NW)
    Label(f_search, text = "Choose a team:", font = ("Skia", 30), fg = "#003366").place(relx = 0.05, rely = 0.45, anchor = NW)
    Label(f_search, text = "Note:\nSearch for a certain year: Choose a year only and choose team as defalut;\nSearch for a certain team: Choose a team only and choose year as defalut;\nSearch for a certain match: Choose both a year and a team.", justify = "left", font = ("Skia", 20), fg = "#003366").place(relx = 0.05, rely = 0.7, anchor = NW)

    # two menu_buttons for year and team
    number = StringVar()
    yearChosen = ttk.Combobox(f_search, width=12, textvariable=number)
    yearChosen['values'] = ("DEFAULT",1930,1934,1938,1950,1954,1958,1962,1966,1970,1974,1978,1982,1986,1990,1994,1998,2002,2006,2010,2014)
    yearChosen.place(relx=0.25,rely=0.3)
    yearChosen.current(0)

    number = StringVar(0)
    teamChosen = ttk.Combobox(f_search, width=12, textvariable=number, background = "white")
    teamChosen['values'] = ("DEFAULT","Algeria","Angola","Argentina","Australia","Austria","Belgium","Bolivia","Bosnia and Herzegovina","Brazil","Bulgaria","Cameroon","Canada","Chile","China PR","Colombia","Costa Rica","Cote d'Ivoire","Croatia","Cuba","Czech Republic","Czechoslovakia","Denmark","Dutch East Indies","Ecuador","Egypt","El Salvador","England","France","Germany","Ghana","Greece","Haiti","Honduras","Hungary","IR Iran","Iran","Iraq","Israel","Italy","Jamaica","Japan","Korea DPR","Korea Republic","Kuwait","Mexico","Morocco","Netherlands","New Zealand","Nigeria","Northern Ireland","Norway","Paraguay","Peru","Poland","Portugal","Republic of Ireland","Romania","Russia","Saudi Arabia","Scotland","Senegal","Serbia","Serbia and Montenegro","Slovakia","Slovenia","South Africa","Soviet Union","Spain","Sweden","Switzerland","Togo","Trinidad and Tobago","Tunisia","Turkey","Ukraine","United Arab Emirates","Uruguay","USA","Wales","Yugoslavia","Zaire")
    teamChosen.place(relx=0.25,rely=0.45)
    teamChosen.current(0)
    
    Button(f_search, text = "SEARCH", font = ("Skia", 20), width = 7, height = 2, command = lambda: get_yt(yearChosen.get(), teamChosen.get())).place(relx=0.4, rely=0.38)

    # button for player
    Label(f_search, text = "Enter a player:", font = ("Skia", 30), fg = "#003366").place(relx = 0.6, rely = 0.3, anchor = NW)
    player = Entry(f_search)
    player.place(relx = 0.6, rely = 0.45, anchor = NW)
    Label(f_search, text = "Some Entering Examples for Best Players:\nMESSI (Lionel Messi)\nCRISTIANO RONALDO (Cristiano Ronaldo)\nPELE (Pele)\nKLOSE (Miroslav Klose)\nRONALDO (Ronaldo)\nJust FONTAINE (Just Fontaine)", justify = "left", font = ("Skia", 20), fg = "#003366").place(relx = 0.6, rely = 0.87, anchor = SW)
    
    Button(f_search, text = "SEARCH", font = ("Skia", 20), width = 7, height = 2, command = lambda: search_player(player)).place(relx=0.8, rely=0.38)
    b_return_create()

# compare interface
def get_team(x, y, z):
    # interface
    z = int(z)
    add_bg()
    f_compare = Frame(root, height = 500, width = 1440)
    f_compare.place(x = 720, y = 504.2, anchor = CENTER)
    Label(f_compare, text = "Compare", font = ("Skia", 50), fg = "#003366").place(relx = 0.02, rely = 0.05, anchor = NW)

    ## national flag and team
    Label(root, width = 283, height = 190, image = country_d[x]).place(relx = 0.06, rely = 0.50)
    Label(root, width = 283, height = 190, image = country_d[y]).place(relx = 0.74, rely = 0.50)
    Label(root, text = x, font = ("Skia", 30), fg = "#003366").place(relx = 0.16, rely = 0.78, anchor = CENTER)
    Label(root, text = y, font = ("Skia", 30), fg = "#003366").place(relx = 0.84, rely = 0.78, anchor = CENTER)

    b_return = Button(root, width = 57, height = 57, image = return_logo, bg = "white", bd = 0, command = b_compare)
    b_return.place(relx = 0.979, rely = 0.904, anchor = SE)

    # get data analysis result
    if compareCountry(x, y, z) == None:
        # sub interface for Wrong input
        Label(root, text = "No Match Before!", font = ("Skia", 50), fg = "#003366").place(relx=0.5, rely=0.6, anchor = CENTER)
    else:
        # get data results
        win, draw, lose, rate1, rate2 = compareCountry(x, y, z)

        # compare sub_interface
        ## result
        Label(root, width = 129, height = 174, image = vs).place(relx = 0.45, rely = 0.49)
        Label(root, text = win, font = ("Skia", 90), fg = "#003366").place(relx = 0.36, rely = 0.57, anchor = CENTER)
        Label(root, text = lose, font = ("Skia", 90), fg = "#003366").place(relx = 0.63, rely = 0.57, anchor = CENTER)
        Label(root, text = rate1+" Wins", font = ("Skia", 25), fg = "#003366").place(relx = 0.36, rely = 0.67, anchor = CENTER)
        Label(root, text = rate2+" Wins", font = ("Skia", 25), fg = "#003366").place(relx = 0.63, rely = 0.67, anchor = CENTER)
        Label(root, text = draw+" Draws", font = ("Skia", 25), fg = "#003366").place(relx = 0.5, rely = 0.74, anchor = CENTER)

    # buttons for further information (graphs)
    Button(root, text = "Goals Achieved and Lost\nin Each World Cup", font = ("Skia", 20), width = 20, height = 3, command = lambda:graphOfCompareGFGA(x, y, str(z)) ).place(relx = 0.27, rely = 0.81)
    Button(root, text = "Matches Won\nin Each World Cup", font = ("Skia", 20), width = 20, height = 3, command = lambda:graphOfComparewin(x, y, str(z)) ).place(relx = 0.73, rely = 0.81, anchor = NE)

def b_compare():
    add_bg()
    f_compare = Frame(root, height = 500, width = 1440)
    f_compare.place(x = 720, y = 504.2, anchor = CENTER)
    
    Label(f_compare, text = "Compare", font = ("Skia", 50), fg = "#003366").place(relx = 0.02, rely = 0.05, anchor = NW)
    Label(f_compare, text = "Choose Team 1: ", font = ("Skia", 30), fg = "#003366").place(relx = 0.23, rely = 0.3, anchor = NW)
    Label(f_compare, text = "Choose Team 2: ", font = ("Skia", 30), fg = "#003366").place(relx = 0.23, rely = 0.45, anchor = NW)
    Label(f_compare, text = "Choose Begin Year: ", font = ("Skia", 30), fg = "#003366").place(relx = 0.23, rely = 0.6, anchor = NW)

    # three menu_buttons for two teams and year
    number = StringVar()
    team1Chosen = ttk.Combobox(f_compare, width=12, textvariable=number)
    team1Chosen['values'] = ("Algeria","Angola","Argentina","Australia","Austria","Belgium","Bolivia","Bosnia and Herzegovina","Brazil","Bulgaria","Cameroon","Canada","Chile","China PR","Colombia","Costa Rica","Cote d'Ivoire","Croatia","Cuba","Czech Republic","Czechoslovakia","Denmark","Dutch East Indies","Ecuador","Egypt","El Salvador","England","France","Germany","Ghana","Greece","Haiti","Honduras","Hungary","IR Iran","Iran","Iraq","Israel","Italy","Jamaica","Japan","Korea DPR","Korea Republic","Kuwait","Mexico","Morocco","Netherlands","New Zealand","Nigeria","Northern Ireland","Norway","Paraguay","Peru","Poland","Portugal","Republic of Ireland","Romania","Russia","Saudi Arabia","Scotland","Senegal","Serbia","Serbia and Montenegro","Slovakia","Slovenia","South Africa","Soviet Union","Spain","Sweden","Switzerland","Togo","Trinidad and Tobago","Tunisia","Turkey","Ukraine","United Arab Emirates","Uruguay","USA","Wales","Yugoslavia","Zaire")
    team1Chosen.place(relx=0.5,rely=0.3)
    team1Chosen.current(0)

    number = StringVar(0)
    team2Chosen = ttk.Combobox(f_compare, width=12, textvariable=number, background = "white")
    team2Chosen['values'] = ("Algeria","Angola","Argentina","Australia","Austria","Belgium","Bolivia","Bosnia and Herzegovina","Brazil","Bulgaria","Cameroon","Canada","Chile","China PR","Colombia","Costa Rica","Cote d'Ivoire","Croatia","Cuba","Czech Republic","Czechoslovakia","Denmark","Dutch East Indies","Ecuador","Egypt","El Salvador","England","France","Germany","Ghana","Greece","Haiti","Honduras","Hungary","IR Iran","Iran","Iraq","Israel","Italy","Jamaica","Japan","Korea DPR","Korea Republic","Kuwait","Mexico","Morocco","Netherlands","New Zealand","Nigeria","Northern Ireland","Norway","Paraguay","Peru","Poland","Portugal","Republic of Ireland","Romania","Russia","Saudi Arabia","Scotland","Senegal","Serbia","Serbia and Montenegro","Slovakia","Slovenia","South Africa","Soviet Union","Spain","Sweden","Switzerland","Togo","Trinidad and Tobago","Tunisia","Turkey","Ukraine","United Arab Emirates","Uruguay","USA","Wales","Yugoslavia","Zaire")
    team2Chosen.place(relx=0.5,rely=0.45)
    team2Chosen.current(0)

    number = StringVar(0)
    yearsChosen = ttk.Combobox(f_compare, width=12, textvariable=number, background = "white")
    yearsChosen['values'] = (1930,1934,1938,1950,1954,1958,1962,1966,1970,1974,1978,1982,1986,1990,1994,1998,2002,2006,2010,2014)
    yearsChosen.place(relx=0.5,rely=0.6)
    yearsChosen.current(0)
    
    Button(f_compare, text = "COMPARE", font = ("Skia", 20), width = 9, height = 2, command = lambda: get_team(team1Chosen.get(), team2Chosen.get(),yearsChosen.get())).place(relx=0.75, rely=0.45)

    b_return_create()

# statistics interface
def b_stat():
    f_main_button.destroy()
    f_stat = Frame(root, height = 500, width = 1440)
    f_stat.place(x = 720, y = 504.2, anchor = CENTER)

    Label(f_stat, text = "Statistics", font = ("Skia", 50), fg = "#003366").place(relx = 0.02, rely = 0.05, anchor = NW)
    Button(root, image = stat_goal, width = 339, height = 370, command = graphGoal).place(relx = 0.16, rely = 0.43, anchor = NW)
    Button(root, image = stat_match, width = 349, height = 370, command = graphWin).place(relx = 0.6, rely = 0.43, anchor = NW)

    b_return_create()

# records interface
def b_best():
    add_bg()
    f_best = Frame(root, height = 500, width = 1440)
    f_best.pack()

    # results display
    tree = ttk.Treeview(f_best, show="headings")
    tree["columns"]=("Records","Belongers")
    tree.column("Records",width=450, anchor='center') 
    tree.column("Belongers",width=450, anchor='center')

    tree.heading("Records",text="Records") 
    tree.heading("Belongers",text="Belongers")

    tree.insert('',0,values=("Youngest player in the World Cup", "Norman Whiteside; Northern Ireland; 17 years and 40 days"))
    tree.insert('',1,values=("Oldest player in the World Cup", "Essam El Hadary; Egypt; 45 years and 161 days old"))
    tree.insert('',2,values=("Youngest goal player in the World Cup", "Pelé; Brazil; 17 years and 239 days old"))
    tree.insert('',2,values=("Oldest goal player in the World Cup", "Albert Roger Milla; Cameroon; 42 years and 39 days old"))
    tree.insert('',2,values=("Player with most number of goals in the World Cup", "16 goals; Miroslav Klose; Germany"))
    tree.insert('',2,values=("Player with most number of appearances in the World Cup", "25 matches; Lothar Matthäus; Germany"))
    tree.insert('',2,values=("Team with most number of goals in the World Cup", "226 goals; Brazil and Germany"))
    tree.insert('',2,values=("Fastest goal record in the World Cup", "11 seconds; Hakan Şükür; Turkey; 2002 Korea and Japan World Cup"))
    tree.insert('',2,values=("Most champions in the World Cup", "5 times; Brazil"))
    tree.insert('',2,values=("Most goals in one match", "12 goals; Hungary 7:5 Switzerland; 1954 Switzerland World Cup"))

    Label(f_best, text = "Records of World Cup", font = ("Skia", 50), fg = "#003366").pack()
    tree.pack(side = BOTTOM)
    f_best.place(x=720, y=455, anchor = CENTER)
    
    b_return = Button(root, width = 57, height = 57, image = return_logo, bg = "white", bd = 0, command = b_return_main)
    b_return.place(x=1150,y=630, anchor = NE)

# main menu
def menu():
    f_main_button = Frame(root, height = 456.87, width = 866.6, bg = "#003399")

    # buttons for four selections
    Button(f_main_button, width = 433, height = 229, image = search, bd = 10, command = b_search).place(relx = 0, rely = 0, anchor = NW)
    Button(f_main_button, width = 433, height = 229, image = compare, bd = 10, command = b_compare).place(relx = 1.0, rely = 0, anchor = NE)
    Button(f_main_button, width = 433, height = 229, image = stat, bd = 10, command = b_stat).place(relx = 0, rely = 1.0, anchor = SW)
    Button(f_main_button, width = 433, height = 229, image = best, bd = 10, command = b_best).place(relx = 1.0, rely = 1.0, anchor = SE)
   
    f_main_button.place(x = 286.6, y = 275.74, anchor = NW)

add_bg()
menu()
root.mainloop()
