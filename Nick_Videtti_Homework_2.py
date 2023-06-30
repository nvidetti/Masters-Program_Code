import pandas
import tkinter.filedialog
import json
import geopy

print('\n'+'Nick Videtti')
print('IST-652 - Homework 2')
print('Summer 2022')
print("JSON-Formatted Data for Chipotle Locations in The United States.\nData found at https://www.kaggle.com/datasets/jeffreybraun/chipotle-locations?select=us-states.json"+'\n')

#Read in data from "Chopotle_HW2_Data.json"
raw_json = json.loads(tkinter.filedialog.askopenfile(title = 'Please Select "Chipotle_HW2_Data.json"').read())

#Narrow down to what is needed
chipotle = raw_json['features']

#Create list for each item in the data
states = []

#Add state and list of coordinates of each Chipotle location to "states" list, creating a list of dictionaries
for state in range(len(chipotle)):
    states.append({chipotle[state]['properties']['name']:  chipotle[state]['geometry']['coordinates']})

#Create list to parse through each dictionary to effecively turn state list of dictionaries into "locations" list of lists 
locations = []
for state in states:
    for key in state.keys():
        for loc in state[key][0]:
            locations.append([key,loc[0],loc[1]])

#Use "locations" list of lists to create pandas DataFrame. Then, fix column names 
data = pandas.DataFrame(locations)
data.columns = ['State', 'Longitude','Latitude']

#Fix oddly structured records
for row in range(len(data)):
    if type(data['Longitude'][row]) == list:
        data.loc[len(data)] = [data['State'][row],data['Longitude'][row][0], data['Longitude'][row][1]]
        data.iloc[row] = [data['State'][row],data['Latitude'][row][0], data['Latitude'][row][1]]
        data.index = range(len(data))

#Pull in Address of each location and set it to new column in data frame. Let user choose since this takes a while.
if input('Please Enter 1 to Add Addresses to the Location Data.\nEnter anything else to skip over this step, as THIS WILL TAKE A FEW MINUTES.\n') == '1':
    data['Address'] = range(len(data))
    for row in range(len(data['Address'])):
        try: data['Address'][row] = geopy.geocoders.Nominatim(user_agent = 'http').reverse(str(data['Latitude'][row])+','+str(data['Longitude'][row])).address
        except: data['Address'][row] = 'No Address Found'
        if row == 0: print('Seraching for Adresses...')
        if (row + 1) % 25 == 0: print(str(int(100*((row + 1)/len(data))))+'% Complete...')

#Print location data
print(data)

#Create data frame for stores per state
stores_per_state = data[['State','Longitude']].groupby('State').count()
stores_per_state.columns = ['Stores']
stores_per_state = stores_per_state.sort_values('Stores', ascending = False)
stores_per_state['Rank'] = stores_per_state.rank(method = 'min', ascending = False).astype(int)

#Print stores per state
print(stores_per_state)

#Save data files
data.to_csv(tkinter.filedialog.asksaveasfilename(title = 'Save Location Data As...'), index = False)
stores_per_state.to_csv(tkinter.filedialog.asksaveasfile(title = 'Save Stores Per Sate Data As...'))