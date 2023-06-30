import csv
import pandas
import time
print('\nNick Videtti\nIST-659 Summer 2022\nHomework 1\n')
directory = input('Please Enter Directory Where donors_data.csv is Saved:\n')
directory+'/donors_data.csv'
donors = []
with open(directory+'/donors_data.csv', 'r') as donorsfile:
    # create csv reader
    reader = csv.reader(donorsfile)

   # add column names and then append each row to the donors list
    for row in reader:
        donors.append(row)
donorsfile.close()

#make donors list a pandas data frame
donors = pandas.DataFrame(donors)

#set column headers to first row and then remove first row
donors.columns = donors.iloc[0,:]
donors = donors[1:]
donors.set_index('Row Id', inplace = True, drop = True)

print('\npandas DataFrame created: "donors"\nNow, let\'s answer some data questions!\n')

print('Question 1:\nDoes the number of children a donor has impact the size of their donations?\n\nFirst, let\'s look at average donation.')
time.sleep(5)

import matplotlib.pyplot

#Average Donation and Number of Children
donors['AVGGIFT_DOLLAR'] = donors['AVGGIFT']
for i in range(len(donors['AVGGIFT_DOLLAR'])):
    donors['AVGGIFT_DOLLAR'][i] = round(float(donors['AVGGIFT_DOLLAR'][i]),0)
matplotlib.pyplot.scatter(donors['NUMCHLD'],donors['AVGGIFT_DOLLAR'])
matplotlib.pyplot.xlabel('Number of Children')
matplotlib.pyplot.ylabel('Average Donation Gift To Nearest Dollar')
matplotlib.pyplot.show()

print('\nNow, let\'s look at Largest Donation.')
#Largest Donation and Number of Children
donors['MAXRAMNT_DOLLAR'] = donors['MAXRAMNT']
for i in range(len(donors['MAXRAMNT_DOLLAR'])):
    donors['MAXRAMNT_DOLLAR'][i] = round(float(donors['MAXRAMNT_DOLLAR'][i]),0)
matplotlib.pyplot.scatter(donors['NUMCHLD'],donors['MAXRAMNT_DOLLAR'])
matplotlib.pyplot.xlabel('Number of Children')
matplotlib.pyplot.ylabel('Largest Donation Gift To Nearest Dollar')
matplotlib.pyplot.show()

#Number of children for smallest average donation
print('\nNext, we will look at the number of children corresponding to the smallest average donation.')
donors['AVGGIFT_FLOAT'] = donors['AVGGIFT']
for i in range(len(donors['AVGGIFT_FLOAT'])):
    donors['AVGGIFT_FLOAT'][i] = float(donors['AVGGIFT_FLOAT'][i])
smallavgchldnum = []
for row in range(len(donors)):
    if donors['AVGGIFT_FLOAT'][row] == min(donors['AVGGIFT_FLOAT']):
        smallavgchldnum.append(donors['NUMCHLD'][row])
print('Number of Children Corresponding to Smallest Average Donation',smallavgchldnum,'\n')
time.sleep(5)

#Number of children for largest average donation
print('Lastly, we will look at the number of children corresponding to the largest average donation.')
largeavgchldnum = []
for row in range(len(donors)):
    if donors['AVGGIFT_FLOAT'][row] == max(donors['AVGGIFT_FLOAT']):
        largeavgchldnum.append(donors['NUMCHLD'][row])
print('Number of Children Corresponding to Largest Average Donation',largeavgchldnum,'\n')
time.sleep(5)

print('Both the largest and the smallest average donation corresponds to somebody with 1 child.')
print('This may be due to an uneven number of donations made by people with 1 child. Let\'s ask these questions again, this time aggregating by number of children.\n')
time.sleep(5)

#Average by Number of Children
print('Now, let\'s look at average of the average donations by number of children.')
agg = donors[['AVGGIFT_FLOAT','NUMCHLD']]
agg = agg.groupby('NUMCHLD').mean()
matplotlib.pyplot.scatter(agg.index,agg['AVGGIFT_FLOAT'])
matplotlib.pyplot.xlabel('Number of Children')
matplotlib.pyplot.ylabel('Average of Average Donation Gift')
matplotlib.pyplot.show()

#Largest by Number of Children
print('\nNext, let\'s look at average of the largest donations by number of children.')
donors['MAXRAMNT_FLOAT'] = donors['MAXRAMNT']
for i in range(len(donors['MAXRAMNT_FLOAT'])):
    donors['MAXRAMNT_FLOAT'][i] = float(donors['MAXRAMNT_FLOAT'][i])
agg = donors[['MAXRAMNT_FLOAT','NUMCHLD']]
agg = agg.groupby('NUMCHLD').mean()
matplotlib.pyplot.scatter(agg.index,agg['MAXRAMNT_FLOAT'])
matplotlib.pyplot.xlabel('Number of Children')
matplotlib.pyplot.ylabel('Average of Largest Donation Gift')
matplotlib.pyplot.show()

#Number of children with smallest average donation
print('\nThen, we will look at the number of children corresponding to the smallest average of the average donations.')
agg = donors[['AVGGIFT_FLOAT','NUMCHLD']]
agg = agg.groupby('NUMCHLD').mean()
smallavgchldnum = []
for row in range(len(agg)):
    if agg['AVGGIFT_FLOAT'][row] == min(agg['AVGGIFT_FLOAT']):
        smallavgchldnum.append(agg.index[row])
print('Number of Children Corresponding to Smallest Average of Average Donations',smallavgchldnum,'\n')
time.sleep(5)

#Number of children for largest average donation
print('Lastly, we will look at the number of children corresponding to the largest average of the donations.')
largeavgchldnum = []
for row in range(len(agg)):
    if agg['AVGGIFT_FLOAT'][row] == max(agg['AVGGIFT_FLOAT']):
        largeavgchldnum.append(agg.index[row])
print('Number of Children Corresponding to Largest Average of Average Donations',largeavgchldnum,'\n')
time.sleep(5)

print('This gives us a much better picture of what is going on here! On average, donations corresponding to 5 children are the smallest, and donations corresponding to 4 children are the largest.')
print('For one last metric, let\'s look at the total number of donations by number of children.\n')
time.sleep(5)

#Donations by Number of Children
Q1output = donors[['NUMCHLD','AVGGIFT']]
Q1output.columns = ['Number of Children', 'Donations']
Q1output = Q1output.groupby('Number of Children').count()
print(Q1output)
time.sleep(5)

print('\nIt appears that a vast majority of donations came from those with 1 child. This may actually be the most indicative metric we have discovered thus far.')
print('However, this could be due to the fact that not many people have a large amount of children, or the fact that the more children somebody has, the less disposable income they have to donate.\n\n\n')
time.sleep(15)

#QUESTION 2
print('Question 2:\nLet\'s expand on the hypothesis that was just stated about number of children affecting disposable income.')
print('This is not exactly the same as disposable income, but there are wealth ratings for each donor that we can use to find average number of children by wealth.')
time.sleep(5)
print('\nWealth Rating Ranges From 0-9, with 9 Being The Most Wealthy Group.\n')
time.sleep(5)

#Question 2 tables
donors['NUMCHLD_INT'] = donors['NUMCHLD']
for i in range(len(donors['NUMCHLD_INT'])):
    donors['NUMCHLD_INT'][i] = int(donors['NUMCHLD'][i])
agg = donors[['NUMCHLD_INT', 'WEALTH']]
agg.columns = ['Average Number of Children','Wealth Rating']
agg = agg.groupby('Wealth Rating').mean()
print(agg)
time.sleep(5)

print('\nIt seems the number of donors with 1 child still skews our data when comparing them vs donors with multiple children.')
print('Let\'s instead look at the average wealth rating by number of children.')
time.sleep(5)

donors['WEALTH_INT'] = donors['WEALTH']
for i in range(len(donors['WEALTH_INT'])):
    donors['WEALTH_INT'][i] = int(donors['WEALTH'][i])
Q2output = donors[['NUMCHLD', 'WEALTH_INT']]
Q2output.columns = ['Number of Children','Average Wealth Rating']
Q2output = Q2output.groupby('Number of Children').mean()
print('\n')
print(Q2output)
time.sleep(5)

print('\nIt seems that these results tell more about how wealth may relate to donating, rather than how number of children affects wealth.\n')

#Output files
print('For the "Donations by Number of Children" part of Question 1, and the "Average Wealth Rating by Number of Children" part of Question 2, csv files will be written and saved to the directory of your choice.')
output_dir = input('Please Enter Directory Where You Would Like The Output Files Saved:\n')

with open(output_dir+'/Donations_by_NumChildren.csv','w',newline = '') as Q1csv:
    writer = csv.writer(Q1csv)
    writer.writerow([Q1output.index.name,Q1output.columns[0]])
    for row in range(len(Q1output)):
        writer.writerow([Q1output.index[row],Q1output.iloc[row,0]])
Q1csv.close()
time.sleep(5)
print('\n"Donations_by_NumChildren.csv" saved to '+output_dir)

with open(output_dir+'/Wealth_by_NumChildren.csv','w',newline = '') as Q2csv:
    writer = csv.writer(Q2csv)
    writer.writerow([Q2output.index.name,Q2output.columns[0]])
    for row in range(len(Q2output)):
        writer.writerow([Q2output.index[row],Q2output.iloc[row,0]])
Q2csv.close()
time.sleep(5)
print('\n"Wealth_by_NumChildren.csv" saved to '+output_dir)
print('\nEnd of Homework 1.\n')