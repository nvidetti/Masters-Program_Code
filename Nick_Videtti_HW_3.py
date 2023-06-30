'''
Nick Videtti
Homework 3 - CSV File to Pandas DataFrame with Labels
IST 736 - Text Mining
Spring 2023
'''

#import pandas, CountVectorizer, and TfidfVectorizer
import pandas
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer

#import nltk for data
import nltk

#Get data
categories = nltk.corpus.brown.categories()
data = [[category,' '.join(document)] for category in categories for document in nltk.corpus.brown.sents(categories = category)]

#Create csv file of choice
import tkinter
path = tkinter.filedialog.asksaveasfile(title = 'Save Data As...').name

#Write data to file
with open(path, 'w') as datafile:
    datafile.write('CATEGORY' + ', ' + 'DOCUMENT' + '\n')
    for category, document in data:
        datafile.write(category + ', ' + document + '\n')

#Close data file
datafile.close()

#Read in data file and store in dataframe
print('Reading in Data...')

read_in_data = []

with open(path, 'r') as datafile:
    while 1 == 1:
        line = datafile.readline()
        #read in line and trim off newline character
        if line != '': read_in_data.append(line[:-1].split(',', 1))
        else: break

#Close data file
datafile.close()

print('Processing Data...')

#Create pandas DataFrame
dataframe = pandas.DataFrame(data = read_in_data[1:], columns = read_in_data[0])
#Trim column names
dataframe.columns = [column.strip() for column in dataframe.columns]

#Tokenize words
dataframe['WORDS'] = [nltk.word_tokenize(words) for words in dataframe['DOCUMENT']]

#Convert to lowercase
dataframe['CLEANED WORDS'] = [[word.lower() for word in row] for row in dataframe['WORDS']]

#Keep only words
import re
dataframe['CLEANED WORDS'] = [[word for word in row if re.match('^[a-z]+$', word)] for row in dataframe['CLEANED WORDS']]

#Remove stopwords
stopwords = nltk.corpus.stopwords.words('english')
dataframe['CLEANED WORDS'] = [[word for word in row if not word in stopwords] for row in dataframe['CLEANED WORDS']]

#Create text from cleaned words
dataframe['CLEANED DOCUMENT'] = [' '.join(words) for words in dataframe['CLEANED WORDS']]

#Create Count Vectors with 3 random categories
import random
random.shuffle(categories)

print('Vectorizing Documents...')

#First category
#Count Vectors
category = categories[0]
v1_data = dataframe['CLEANED DOCUMENT'][dataframe['CATEGORY'] == category]
cnt_vec_1 = CountVectorizer()
cnt_vecs_1 = pandas.DataFrame(cnt_vec_1.fit_transform(v1_data).toarray(), columns = cnt_vec_1.get_feature_names_out())
cnt_vecs_1.insert(0, 'CATEGORY', category)
#Tfidf Vectors
tfidf_vec_1 = TfidfVectorizer()
tfidf_vecs_1 = pandas.DataFrame(tfidf_vec_1.fit_transform(v1_data).toarray(), columns = tfidf_vec_1.get_feature_names_out())
tfidf_vecs_1.insert(0, 'CATEGORY', category)

#Second category
#Count Vectors
category = categories[1]
v2_data = dataframe['CLEANED DOCUMENT'][dataframe['CATEGORY'] == category]
cnt_vec_2 = CountVectorizer()
cnt_vecs_2 = pandas.DataFrame(cnt_vec_2.fit_transform(v2_data).toarray(), columns = cnt_vec_2.get_feature_names_out())
cnt_vecs_2.insert(0, 'CATEGORY', category)
#Tfidf Vectors
tfidf_vec_2 = TfidfVectorizer()
tfidf_vecs_2 = pandas.DataFrame(tfidf_vec_2.fit_transform(v2_data).toarray(), columns = tfidf_vec_2.get_feature_names_out())
tfidf_vecs_2.insert(0, 'CATEGORY', category)

#Third category
#Count Vectors
category = categories[2]
v3_data = dataframe['CLEANED DOCUMENT'][dataframe['CATEGORY'] == category]
cnt_vec_3 = CountVectorizer()
cnt_vecs_3 = pandas.DataFrame(cnt_vec_3.fit_transform(v3_data).toarray(), columns = cnt_vec_3.get_feature_names_out())
cnt_vecs_3.insert(0, 'CATEGORY', category)
#Tfidf Vectors
tfidf_vec_3 = TfidfVectorizer()
tfidf_vecs_3 = pandas.DataFrame(tfidf_vec_3.fit_transform(v3_data).toarray(), columns = tfidf_vec_3.get_feature_names_out())
tfidf_vecs_3.insert(0, 'CATEGORY', category)



#Generate word clouds
from wordcloud import WordCloud
from matplotlib import pyplot

print('Generating Word Clouds...')

#Subplots to put all word clouds in one figure
fig, plots = pyplot.subplots(2,3)
fig.suptitle('Word Clouds Using Count Vectorizers and TFIDF Vectorizers\nBrown Corpus by Category', fontsize = 16)

#Category 1 Word Cloud - Count Vectorizer
plots[0,0].set_title(max(cnt_vecs_1['CATEGORY']).upper() + ' - COUNT')
cnt_vecs_1 = cnt_vecs_1.drop(columns = 'CATEGORY')
cnt_1_string = [[word]*sum(cnt_vecs_1[word]) for word in list(cnt_vecs_1.columns)]
cnt_1_string = ' '.join([word for sublist in cnt_1_string for word in sublist])
plots[0,0].imshow(WordCloud(background_color= 'white').generate(cnt_1_string))
plots[0,0].axis('off')
#Category 1 Word Cloud - TFIDF Vectorizer
plots[1,0].set_title(max(tfidf_vecs_1['CATEGORY']).upper() + ' - TFIDF')
tfidf_vecs_1 = tfidf_vecs_1.drop(columns = 'CATEGORY')
tfidf_1_string = [[word]*int(1000*sum(tfidf_vecs_1[word])) for word in list(tfidf_vecs_1.columns)]
tfidf_1_string = ' '.join([word for sublist in tfidf_1_string for word in sublist])
plots[1,0].imshow(WordCloud(background_color= 'white').generate(tfidf_1_string))
plots[1,0].axis('off')

#Category 2 Word Cloud - Count Vectorizer
plots[0,1].set_title(max(cnt_vecs_2['CATEGORY']).upper() + ' - COUNT')
cnt_vecs_2 = cnt_vecs_2.drop(columns = 'CATEGORY')
cnt_2_string = [[word]*sum(cnt_vecs_2[word]) for word in list(cnt_vecs_2.columns)]
cnt_2_string = ' '.join([word for sublist in cnt_2_string for word in sublist])
plots[0,1].imshow(WordCloud(background_color= 'white').generate(cnt_2_string))
plots[0,1].axis('off')
#Category 2 Word Cloud - TFIDF Vectorizer
plots[1,1].set_title(max(tfidf_vecs_2['CATEGORY']).upper() + ' - TFIDF')
tfidf_vecs_2 = tfidf_vecs_2.drop(columns = 'CATEGORY')
tfidf_2_string = [[word]*int(1000*sum(tfidf_vecs_2[word])) for word in list(tfidf_vecs_2.columns)]
tfidf_2_string = ' '.join([word for sublist in tfidf_2_string for word in sublist])
plots[1,1].imshow(WordCloud(background_color= 'white').generate(tfidf_2_string))
plots[1,1].axis('off')

#Category 3 Word Cloud - Count Vectorizer
plots[0,2].set_title(max(cnt_vecs_3['CATEGORY']).upper() + ' - COUNT')
cnt_vecs_3 = cnt_vecs_3.drop(columns = 'CATEGORY')
cnt_3_string = [[word]*sum(cnt_vecs_3[word]) for word in list(cnt_vecs_3.columns)]
cnt_3_string = ' '.join([word for sublist in cnt_3_string for word in sublist])
plots[0,2].imshow(WordCloud(background_color= 'white').generate(cnt_3_string))
plots[0,2].axis('off')
#Category 3 Word Cloud - TFIDF Vectorizer
plots[1,2].set_title(max(tfidf_vecs_3['CATEGORY']).upper() + ' - TFIDF')
tfidf_vecs_3 = tfidf_vecs_3.drop(columns = 'CATEGORY')
tfidf_3_string = [[word]*int(1000*sum(tfidf_vecs_3[word])) for word in list(tfidf_vecs_3.columns)]
tfidf_3_string = ' '.join([word for sublist in tfidf_3_string for word in sublist])
plots[1,2].imshow(WordCloud(background_color= 'white').generate(tfidf_3_string))
plots[1,2].axis('off')

plots[0,1].axis('off')
plots[1,0].axis('off')
plots[1,2].axis('off')

print('Displaying Word Clouds in a separate window. Close the window when ready.')
pyplot.show()

print()
print('END OF HOMEWORK 3.')