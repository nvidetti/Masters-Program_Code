import pandas

#READ IN SEASON GAME LOG CSVs FROM BASKETBALL REFERENCE
loop = 1
while loop == 1:
    try:
        directory = input('Please Enter Directory Where Kevin Durant\'s Game Logs are Located, or Enter 1 to End Program: ')
        Season_07_08 = pandas.read_csv(directory+'07_08.csv')
        loop = 0
    except: 
        if directory == '1':
            loop = 2
            print('\nEnding Program...\n\n')
        else: print('\nDirectory Not Found.')

if loop == 0:
    Season_08_09 = pandas.read_csv(directory+'08_09.csv')
    Season_09_10 = pandas.read_csv(directory+'09_10.csv')
    Season_10_11 = pandas.read_csv(directory+'10_11.csv')
    Season_11_12 = pandas.read_csv(directory+'11_12.csv')
    Season_12_13 = pandas.read_csv(directory+'12_13.csv')
    Season_13_14 = pandas.read_csv(directory+'13_14.csv')
    Season_14_15 = pandas.read_csv(directory+'14_15.csv')
    Season_15_16 = pandas.read_csv(directory+'15_16.csv')
    Season_16_17 = pandas.read_csv(directory+'16_17.csv')
    Season_17_18 = pandas.read_csv(directory+'17_18.csv')
    Season_18_19 = pandas.read_csv(directory+'18_19.csv')
    Season_20_21 = pandas.read_csv(directory+'20_21.csv')
    Season_21_22 = pandas.read_csv(directory+'21_22.csv')
    Playoffs_Through_2022 = pandas.read_csv(directory+'Playoffs_Through_2022.csv')

    #COMBINE INTO ONE DATAFRAME
    GameLogs = pandas.concat([Season_07_08,\
    Season_08_09,\
    Season_09_10,\
    Season_10_11,\
    Season_11_12,\
    Season_12_13,\
    Season_13_14,\
    Season_14_15,\
    Season_15_16,\
    Season_16_17,\
    Season_17_18,\
    Season_18_19,\
    Season_20_21,\
    Season_21_22,\
    Playoffs_Through_2022])

    #FIX NULL DATES DUE TO DIFFERENT FORMAT IN PLAYOFF GAME LOGS
    GameLogs['Date'] = GameLogs['Date'].fillna(GameLogs['2010 Playoffs'])

    #CREATE WON/LOST COLUMN
    GameLogs['Won/Lost'] = GameLogs['Unnamed: 7'].fillna(GameLogs['Unnamed: 8']).str[0]

    #USE ONLY COLUMNS THAT ARE NEEDED
    GameLogs = GameLogs[['Date','Won/Lost','FG%','FT%','3P%','PTS','TOV']]

    #CHANGE COLUMN NAMES
    GameLogs.columns = ['Date','Won/Lost','FG%','FT%','3P%','Points','Turnovers']

    #REMOVE GAMES WHERE DURANT DID NOT PLAY

    GameLogs = GameLogs[~GameLogs['FG%'].isin(['Did Not Dress','Inactive','Did Not Play','Not With Team'])]

    #CHANGE DATA TYPES
    #for date in GameLogs['Date']: date = datetime.datetime.strptime(date,'%Y-%m-%d')
    GameLogs['Date'] = pandas.to_datetime(GameLogs['Date'])
    GameLogs['FG%'] = GameLogs['FG%'].astype(float)
    GameLogs['FT%'] = GameLogs['FT%'].astype(float)
    GameLogs['3P%'] = GameLogs['3P%'].astype(float)
    GameLogs['Points'] = GameLogs['Points'].astype(int)
    GameLogs['Turnovers'] = GameLogs['Turnovers'].astype(int)

    #FIX ROW INDICES
    GameLogs.set_index('Date', inplace = True)

    #TWITTER DATA
    #Copied and pasted from https://www.trackalytics.com/twitter/profile/kdtrey5/

    #Read in data
    tweets = pandas.read_excel(directory+'DurantTweets.xlsx')[['Date','Tweets']]
    
    #Rename columns
    tweets.columns = ['Date','Total Tweets']
    
    #Clean data and add column to show tweets in day
    tweets = tweets[tweets['Date'].notna()]
    tweets['Tweets'] = tweets['Total Tweets'] - tweets['Total Tweets'].shift(-1)
    
    #Remove any days without tweets and join to Game Logs on date
    tweets = tweets[tweets['Tweets'] > 0]
    tweets.set_index('Date', inplace = True)#, drop = False)  
    GameLogs_Tweets = GameLogs.join(tweets, how = 'inner')

    import matplotlib.pyplot

    #Graph Total Tweets over Date
    matplotlib.pyplot.scatter(GameLogs_Tweets.index,GameLogs_Tweets['Total Tweets'], c= GameLogs_Tweets['Won/Lost'].map({'W': 'blue', 'L': 'red'}))
    matplotlib.pyplot.title('Total Tweets over Time')
    matplotlib.pyplot.xlabel('Date')
    matplotlib.pyplot.ylabel('Total Tweets')
    matplotlib.pyplot.legend(['Won Game','Lost Game'])
    matplotlib.pyplot.show()

    #Graph Tweets vs Points and Turnovers
    pointsturns, pointsturnsplot = matplotlib.pyplot.subplots(1,3)
    pointsturnsplot[0].scatter(GameLogs_Tweets['Points'],GameLogs_Tweets['Tweets'], c = 'green')
    pointsturnsplot[1].scatter(GameLogs_Tweets['Turnovers'],GameLogs_Tweets['Tweets'], c = 'orange')
    pointsturnsplot[2].scatter(GameLogs_Tweets['Won/Lost'],GameLogs_Tweets['Tweets'], c = GameLogs_Tweets['Won/Lost'].map({'W': 'blue', 'L': 'red'}))
    pointsturnsplot[0].set_title('Points vs Tweets')
    pointsturnsplot[1].set_title('Turnovers vs Tweets')
    pointsturnsplot[2].set_title('Won/Lost vs Tweets')
    pointsturnsplot[0].set_yticks(range(GameLogs_Tweets['Tweets'].max() + 1))
    pointsturnsplot[1].set_yticks(range(GameLogs_Tweets['Tweets'].max() + 1))
    pointsturnsplot[2].set_yticks(range(GameLogs_Tweets['Tweets'].max() + 1))
    pointsturns.show()   

    #Graph Tweeets vs Shooting Percentages
    shooting, shootingplot = matplotlib.pyplot.subplots(3)
    shooting.suptitle('Shooting Performance vs Tweets')
    shootingplot[0].scatter(GameLogs_Tweets['FG%']*100, GameLogs_Tweets['Tweets'], c = GameLogs_Tweets['Won/Lost'].map({'W': 'blue', 'L': 'red'}))
    shootingplot[1].scatter(GameLogs_Tweets['FT%']*100, GameLogs_Tweets['Tweets'], c = GameLogs_Tweets['Won/Lost'].map({'W': 'blue', 'L': 'red'}))
    shootingplot[2].scatter(GameLogs_Tweets['3P%']*100, GameLogs_Tweets['Tweets'], c = GameLogs_Tweets['Won/Lost'].map({'W': 'blue', 'L': 'red'}))
    shootingplot[0].set_title('Field Goal %')
    shootingplot[1].set_title('Free Throw %')
    shootingplot[2].set_title('Three Pointer %')
    shooting.legend(['Won Game'])
    shooting.show()
    
    input('\nPress Enter to Finish Program...')
    print('End of Code for IST-652 Final Project.')