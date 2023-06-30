'''
Nick Videtti
Homework 4 - Multinomial Naive Bayes on Text Data
IST 736 - Text Mining
Spring 2023
'''

#import pandas
import pandas

#Read in csv file of choice
import tkinter.filedialog
path = tkinter.filedialog.askopenfile(title = 'Please Choose Appropriate Data File...').name

#Read in data
datalist = []
with open(path) as datafile:
    while 1 == 1:
        line = datafile.readline()
        if line == '': break
        else: datalist.append(line)
datafile.close()

#Remove newline characters at end
datalist = [item[:-1] for item in datalist]

#Split into list of lists
datalist = [[item[0], item[2], item[4:]] for item in datalist]

#Fix header row
datalist[0] = ['lie', 'sentiment', 'review']

#Create pandas DataFrame
data = pandas.DataFrame(data = datalist[1:], columns = datalist[0])

#Tokenize words
import nltk
data['words'] = [nltk.word_tokenize(review) for review in data['review']]

#Clean words - lowercase, remove stopwords, only words
import re
stopwords = nltk.corpus.stopwords.words('english')
data['cleaned_words'] = [[word.lower() for word in review if word.lower() not in stopwords and re.match('^[a-z]+$', word)] for review in data['words']]

#Create cleaned review
data['cleaned_review'] = [(' '.join(review)).strip() for review in data['cleaned_words']]

#Create lie_sentiment column
data['lie_sentiment'] = data['lie'] + data['sentiment']

#Reorder columns
data = data[['lie_sentiment', 'lie', 'sentiment', 'review', 'words', 'cleaned_review', 'cleaned_words']]

#Create lie, sentiment, and lie_sentiment pandas DataFrames
lie = data[['lie', 'cleaned_review']]
sentiment = data[['sentiment', 'cleaned_review']]
lie_sentiment = data[['lie_sentiment', 'cleaned_review']]

#Print some information for the user
print('--------------------------SUMMARY OF DATA CLEANING WITH RESULTS--------------------------')
print()
print()
print('COMPREHENSIVE DATAFRAME - FIRST 10 ROWS')
print(data.head(10))
print()
#Lie
print('LIE DATA - FIRST 10 ROWS')
print(lie.head(10))
print()
#Sentiment
print('SENTIMENT DATA - FIRST 10 ROWS')
print(sentiment.head(10))
print()
#Lie_Sentiment
print('LIE_SENTIMENT DATA - FIRST 10 ROWS')
print(lie_sentiment.head(10))
print()

#Create Count Vectors
from sklearn.feature_extraction.text import CountVectorizer
vec = CountVectorizer()

#Count vectors - replace NaN with 0
lie_vecs = pandas.DataFrame(vec.fit_transform(lie['cleaned_review']).toarray(), columns = vec.get_feature_names_out())
lie_vecs = lie.join(lie_vecs).drop(columns = ['cleaned_review']).fillna(0)
sentiment_vecs = pandas.DataFrame(vec.fit_transform(sentiment['cleaned_review']).toarray(), columns = vec.get_feature_names_out())
sentiment_vecs = sentiment.join(sentiment_vecs).drop(columns = ['cleaned_review']).fillna(0)
lie_sentiment_vecs = pandas.DataFrame(vec.fit_transform(lie_sentiment['cleaned_review']).toarray(), columns = vec.get_feature_names_out())
lie_sentiment_vecs = lie_sentiment.join(lie_sentiment_vecs).drop(columns = ['cleaned_review']).fillna(0)

#Create Train and Test Sets
from sklearn.model_selection import train_test_split
lie_train, lie_test = train_test_split(lie_vecs, train_size = 0.7)
sentiment_train, sentiment_test = train_test_split(sentiment_vecs, train_size = 0.7)
lie_sentiment_train, lie_sentiment_test = train_test_split(lie_sentiment_vecs, train_size = 0.7)

#Remove labels from test sets
lie_test_labels = lie_test[['lie']]
lie_test = lie_test.drop(columns = ['lie'])
sentiment_test_labels = sentiment_test[['sentiment']]
sentiment_test = sentiment_test.drop(columns = ['sentiment'])
lie_sentiment_test_labels = lie_sentiment_test[['lie_sentiment']]
lie_sentiment_test = lie_sentiment_test.drop(columns = ['lie_sentiment'])

#Print some more information for the user
print()
print()
print('--------------------------SUMMARY OF DOCUMENT VETCORIZATION WITH RESULTS--------------------------')
print()
print()
#Lie
print('LIE TRAINING VECTORS - FIRST 5 VECTORS')
print(lie_train.head(5))
print()
print('LIE TESTING VECTORS - FIRST 5 VECTORS')
print(lie_test.head(5))
print()
print('LIE TESTING LABELS - FIRST 5 LABELS')
print(lie_test_labels.head(5))
print()
#Sentiment
print('SENTIMENT TRAINING VECTORS - FIRST 5 VECTORS')
print(sentiment_train.head(5))
print()
print('SENTIMENT TESTING VECTORS - FIRST 5 VECTORS')
print(sentiment_test.head(5))
print()
print('SENTIMENT TESTING LABELS - FIRST 5 LABELS')
print(sentiment_test_labels.head(5))
print()
#Lie_Sentiment
print('LIE_SENTIMENT TRAINING VECTORS - FIRST 5 VECTORS')
print(lie_sentiment_train.head(5))
print()
print('LIE_SENTIMENT TESTING VECTORS - FIRST 5 VECTORS')
print(lie_sentiment_test.head(5))
print()
print('LIE_SENTIMENT TESTING LABELS - FIRST 5 LABELS')
print(lie_sentiment_test_labels.head(5))
print()



#Model Training
import sklearn.naive_bayes
from sklearn.metrics import confusion_matrix
MNB = sklearn.naive_bayes.MultinomialNB()

#Print some more information for the user
print()
print()
print('--------------------------SUMMARY OF MULTINIMIAL NAIVE BAYES MODELS WITH RESULTS--------------------------')
print()
print()



#Lie
lie_model = MNB.fit(lie_train.drop(columns = ['lie']), lie_train['lie'])
lie_prediction = MNB.predict(lie_test)
lie_conf = confusion_matrix(lie_test_labels, lie_prediction)
print('LIE MODEL CONFUSION MATRIX')
print(lie_conf)
print('LIE MODEL ACCURACY:', ((lie_conf[0,0] + lie_conf[1,1]) / sum([sum(sublist) for sublist in lie_conf])) * 100, '%')
print()
#Sentiment
sentiment_model = MNB.fit(sentiment_train.drop(columns = ['sentiment']), sentiment_train['sentiment'])
sentiment_prediction = MNB.predict(sentiment_test)
sentiment_conf = confusion_matrix(sentiment_test_labels, sentiment_prediction)
print('SENTIMENT MODEL CONFUSION MATRIX')
print(sentiment_conf)
print('SENTIMENT MODEL ACCURACY:', ((sentiment_conf[0,0] + sentiment_conf[1,1]) / sum([sum(sublist) for sublist in sentiment_conf])) * 100, '%')
print()
#Lie_Sentiment
lie_sentiment_model = MNB.fit(lie_sentiment_train.drop(columns = ['lie_sentiment']), lie_sentiment_train['lie_sentiment'])
lie_sentiment_prediction = MNB.predict(lie_sentiment_test)
lie_sentiment_conf = confusion_matrix(lie_sentiment_test_labels, lie_sentiment_prediction)
print('LIE_SENTIMENT MODEL CONFUSION MATRIX')
print(lie_sentiment_conf)
print('LIE_SENTIMENT MODEL ACCURACY:', ((lie_sentiment_conf[0,0] + lie_sentiment_conf[1,1] + lie_sentiment_conf[2,2] + lie_sentiment_conf[3,3]) / sum([sum(sublist) for sublist in lie_sentiment_conf])) * 100, '%')