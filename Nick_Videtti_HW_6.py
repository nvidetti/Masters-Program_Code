'''
Nick Videtti
Homework 6 - Bernoulli Naive Bayes, Multinomial Naive Bayes, and Decision Trees on Text Data
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

#Clean words - lowercase, remove stopwords, remove phrases with numbers
import re
stopwords = nltk.corpus.stopwords.words('english')
data['cleaned_words'] = [[word.lower() for word in review if word.lower() not in stopwords and not re.match('^.*[0-9]+.*$', word)] for review in data['words']]

#Further cleaning of words - only words at least 3 characters long but no longer than 13 characters
data['cleaned_words'] = [[word for word in document if len(word) >= 3 and len(word) <= 13] for document in data['cleaned_words']]

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
print()
print()
print()
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

#Create function to go through process for one dataframe
def VectorizeModelCrossVal(dataframe, text_column, label_column, num_classes, cross_val_folds = 5):
    #Create Count, Count Binary, TfIdf, and TfIdf Binary vectors
    from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
    from sklearn.naive_bayes import MultinomialNB, BernoulliNB
    from sklearn.tree import DecisionTreeClassifier
    from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
    cnt = CountVectorizer()
    cnt_bool = CountVectorizer(binary = True)
    tfidf = TfidfVectorizer()
    tfidf_bool = TfidfVectorizer(binary = True)

    #Create dataframe
    data = dataframe[[label_column, text_column]]

    #Create Vectorized dataframes
    cnt_data = pandas.DataFrame(cnt.fit_transform(data[text_column]).toarray(), columns = cnt.get_feature_names_out())
    cnt_data = data.join(cnt_data).drop(columns = [text_column]).fillna(0)
    cnt_bool_data = pandas.DataFrame(cnt_bool.fit_transform(data[text_column]).toarray(), columns = cnt_bool.get_feature_names_out())
    cnt_bool_data = data.join(cnt_bool_data).drop(columns = [text_column]).fillna(0)
    tfidf_data = pandas.DataFrame(tfidf.fit_transform(data[text_column]).toarray(), columns = tfidf.get_feature_names_out())
    tfidf_data = data.join(tfidf_data).drop(columns = [text_column]).fillna(0)
    tfidf_bool_data = pandas.DataFrame(tfidf_bool.fit_transform(data[text_column]).toarray(), columns = tfidf_bool.get_feature_names_out())
    tfidf_bool_data = data.join(tfidf_bool_data).drop(columns = [text_column]).fillna(0)
    
    #Perform cross validations
    cnt_data = cnt_data.sample(frac = 1)
    cnt_bool_data = cnt_bool_data.sample(frac = 1)
    tfidf_data = tfidf_data.sample(frac = 1)
    tfidf_bool_data = tfidf_bool_data.sample(frac = 1)
    cnt_mnb_acc = []
    cnt_bool_mnb_acc = []
    tfidf_mnb_acc = []
    tfidf_bool_mnb_acc = []
    cnt_bool_ber_acc = []
    tfidf_bool_ber_acc = []
    cnt_dt_acc = []
    cnt_bool_dt_acc = []
    tfidf_dt_acc = []
    tfidf_bool_dt_acc = []
    cnt_mnb_cnfmat = [[i*0 for i in range(num_classes)]]*num_classes
    cnt_bool_mnb_cnfmat = [[i*0 for i in range(num_classes)]]*num_classes
    tfidf_mnb_cnfmat = [[i*0 for i in range(num_classes)]]*num_classes
    tfidf_bool_mnb_cnfmat = [[i*0 for i in range(num_classes)]]*num_classes
    cnt_bool_ber_cnfmat = [[i*0 for i in range(num_classes)]]*num_classes
    tfidf_bool_ber_cnfmat = [[i*0 for i in range(num_classes)]]*num_classes
    cnt_dt_cnfmat = [[i*0 for i in range(num_classes)]]*num_classes
    cnt_bool_dt_cnfmat = [[i*0 for i in range(num_classes)]]*num_classes
    tfidf_dt_cnfmat = [[i*0 for i in range(num_classes)]]*num_classes
    tfidf_bool_dt_cnfmat = [[i*0 for i in range(num_classes)]]*num_classes
    
    for i in range(cross_val_folds):
        
        try:
            #Multinomial Naive Bayes - Count
            test_start = int(len(cnt_data.index)/cross_val_folds) * i
            test_stop = int(len(cnt_data.index)/cross_val_folds) * (i+1)
            test = cnt_data.iloc[test_start : test_stop]
            test_labels = test[label_column]
            test = test.drop(columns = [label_column])
            train = pandas.concat([cnt_data.iloc[:test_start], cnt_data.iloc[test_stop:]])
            mnb = MultinomialNB()
            mnb.fit(train.drop(columns = [label_column]), train[label_column])
            cnt_mnb_acc.append(mnb.score(test, test_labels))
            pred = mnb.predict(test)
            cnt_mnb_cnfmat += confusion_matrix(test_labels, pred)
                
            #Multinomial Naive Bayes - Count Boolean
            test_start = int(len(cnt_bool_data.index)/cross_val_folds) * i
            test_stop = int(len(cnt_bool_data.index)/cross_val_folds) * (i+1)
            test = cnt_bool_data.iloc[test_start : test_stop]
            test_labels = test[label_column]
            test = test.drop(columns = [label_column])
            train = pandas.concat([cnt_bool_data.iloc[:test_start], cnt_bool_data.iloc[test_stop:]])
            mnb = MultinomialNB()
            mnb.fit(train.drop(columns = [label_column]), train[label_column])
            cnt_bool_mnb_acc.append(mnb.score(test, test_labels))
            pred = mnb.predict(test)
            cnt_bool_mnb_cnfmat += confusion_matrix(test_labels, pred)

            #Multinomial Naive Bayes - TfIdf
            test_start = int(len(tfidf_data.index)/cross_val_folds) * i
            test_stop = int(len(tfidf_data.index)/cross_val_folds) * (i+1)
            test = tfidf_data.iloc[test_start : test_stop]
            test_labels = test[label_column]
            test = test.drop(columns = [label_column])
            train = pandas.concat([tfidf_data.iloc[:test_start], tfidf_data.iloc[test_stop:]])
            mnb = MultinomialNB()
            mnb.fit(train.drop(columns = [label_column]), train[label_column])
            tfidf_mnb_acc.append(mnb.score(test, test_labels))
            pred = mnb.predict(test)
            tfidf_mnb_cnfmat += confusion_matrix(test_labels, pred)

            #Multinomial Naive Bayes - TfIdf Boolean
            test_start = int(len(tfidf_bool_data.index)/cross_val_folds) * i
            test_stop = int(len(tfidf_bool_data.index)/cross_val_folds) * (i+1)
            test = tfidf_bool_data.iloc[test_start : test_stop]
            test_labels = test[label_column]
            test = test.drop(columns = [label_column])
            train = pandas.concat([tfidf_bool_data.iloc[:test_start], tfidf_bool_data.iloc[test_stop:]])
            mnb = MultinomialNB()
            mnb.fit(train.drop(columns = [label_column]), train[label_column])
            tfidf_bool_mnb_acc.append(mnb.score(test, test_labels))
            pred = mnb.predict(test)
            tfidf_bool_mnb_cnfmat += confusion_matrix(test_labels, pred)

            #Bernoulli Naive Bayes - Count Boolean
            test_start = int(len(cnt_bool_data.index)/cross_val_folds) * i
            test_stop = int(len(cnt_bool_data.index)/cross_val_folds) * (i+1)
            test = cnt_bool_data.iloc[test_start : test_stop]
            test_labels = test[label_column]
            test = test.drop(columns = [label_column])
            train = pandas.concat([cnt_bool_data.iloc[:test_start], cnt_bool_data.iloc[test_stop:]])
            ber = BernoulliNB()
            ber.fit(train.drop(columns = [label_column]), train[label_column])
            cnt_bool_ber_acc.append(ber.score(test, test_labels))
            pred = ber.predict(test)
            cnt_bool_ber_cnfmat += confusion_matrix(test_labels, pred)

            #Bernoulli Naive Bayes - TfIdf Boolean
            test_start = int(len(tfidf_bool_data.index)/cross_val_folds) * i
            test_stop = int(len(tfidf_bool_data.index)/cross_val_folds) * (i+1)
            test = tfidf_bool_data.iloc[test_start : test_stop]
            test_labels = test[label_column]
            test = test.drop(columns = [label_column])
            train = pandas.concat([tfidf_bool_data.iloc[:test_start], tfidf_bool_data.iloc[test_stop:]])
            ber = BernoulliNB()
            ber.fit(train.drop(columns = [label_column]), train[label_column])
            tfidf_bool_ber_acc.append(ber.score(test, test_labels))
            pred = ber.predict(test)
            tfidf_bool_ber_cnfmat += confusion_matrix(test_labels, pred)

            #Decision Tree - Count
            test_start = int(len(cnt_data.index)/cross_val_folds) * i
            test_stop = int(len(cnt_data.index)/cross_val_folds) * (i+1)
            test = cnt_data.iloc[test_start : test_stop]
            test_labels = test[label_column]
            test = test.drop(columns = [label_column])
            train = pandas.concat([cnt_data.iloc[:test_start], cnt_data.iloc[test_stop:]])
            dt = DecisionTreeClassifier()
            dt.fit(train.drop(columns = [label_column]), train[label_column])
            cnt_dt_acc.append(dt.score(test, test_labels))
            pred = dt.predict(test)
            cnt_dt_cnfmat += confusion_matrix(test_labels, pred)
                
            #Decision Tree - Count Boolean
            test_start = int(len(cnt_bool_data.index)/cross_val_folds) * i
            test_stop = int(len(cnt_bool_data.index)/cross_val_folds) * (i+1)
            test = cnt_bool_data.iloc[test_start : test_stop]
            test_labels = test[label_column]
            test = test.drop(columns = [label_column])
            train = pandas.concat([cnt_bool_data.iloc[:test_start], cnt_bool_data.iloc[test_stop:]])
            dt = DecisionTreeClassifier()
            dt.fit(train.drop(columns = [label_column]), train[label_column])
            cnt_bool_dt_acc.append(dt.score(test, test_labels))
            pred = dt.predict(test)
            cnt_bool_dt_cnfmat += confusion_matrix(test_labels, pred)

            #Decision Tree - TfIdf
            test_start = int(len(tfidf_data.index)/cross_val_folds) * i
            test_stop = int(len(tfidf_data.index)/cross_val_folds) * (i+1)
            test = tfidf_data.iloc[test_start : test_stop]
            test_labels = test[label_column]
            test = test.drop(columns = [label_column])
            train = pandas.concat([tfidf_data.iloc[:test_start], tfidf_data.iloc[test_stop:]])
            dt = DecisionTreeClassifier()
            dt.fit(train.drop(columns = [label_column]), train[label_column])
            tfidf_dt_acc.append(dt.score(test, test_labels))
            pred = dt.predict(test)
            tfidf_dt_cnfmat += confusion_matrix(test_labels, pred)

            #Decision Tree - TfIdf Boolean
            test_start = int(len(tfidf_bool_data.index)/cross_val_folds) * i
            test_stop = int(len(tfidf_bool_data.index)/cross_val_folds) * (i+1)
            test = tfidf_bool_data.iloc[test_start : test_stop]
            test_labels = test[label_column]
            test = test.drop(columns = [label_column])
            train = pandas.concat([tfidf_bool_data.iloc[:test_start], tfidf_bool_data.iloc[test_stop:]])
            dt = DecisionTreeClassifier()
            dt.fit(train.drop(columns = [label_column]), train[label_column])
            tfidf_bool_dt_acc.append(dt.score(test, test_labels))
            pred = dt.predict(test)
            tfidf_bool_dt_cnfmat += confusion_matrix(test_labels, pred)
                
        #Pass if fails
        except: pass

    
    print('--------------ACCURACY SUMMARY---------------')
    print()
    print('Multinomial Naive Bayes with Count Vectorization -', cross_val_folds, 'FOLD CROSS VALIDATION')
    print('Average Accuracy:', round((sum(cnt_mnb_acc) / cross_val_folds)*100, 2), '%')
    print('Minimum Accuracy:', round(min(cnt_mnb_acc)*100, 2), '%')
    print('Maximum Accuracy:', round(max(cnt_mnb_acc)*100, 2), '%')
    print('Confusion Matrix for Folds Where All', num_classes, 'Classifications are Represented:')
    print(cnt_mnb_cnfmat)
    print()
    print('Multinomial Naive Bayes with Boolean Count Vectorization -', cross_val_folds, 'FOLD CROSS VALIDATION')
    print('Average Accuracy:', round((sum(cnt_bool_mnb_acc) / cross_val_folds)*100, 2), '%')
    print('Minimum Accuracy:', round(min(cnt_bool_mnb_acc)*100, 2), '%')
    print('Maximum Accuracy:', round(max(cnt_bool_mnb_acc)*100, 2), '%')
    print('Confusion Matrix for Folds Where All', num_classes, 'Classifications are Represented:')
    print(cnt_bool_mnb_cnfmat)
    print()
    print('Multinomial Naive Bayes with TfIdf Vectorization -', cross_val_folds, 'FOLD CROSS VALIDATION')
    print('Average Accuracy:', round((sum(tfidf_mnb_acc) / cross_val_folds)*100, 2), '%')
    print('Minimum Accuracy:', round(min(tfidf_mnb_acc)*100, 2), '%')
    print('Maximum Accuracy:', round(max(tfidf_mnb_acc)*100, 2), '%')
    print('Confusion Matrix for Folds Where All', num_classes, 'Classifications are Represented:')
    print(tfidf_mnb_cnfmat)
    print()
    print('Multinomial Naive Bayes with Boolean TfIdf Vectorization -', cross_val_folds, 'FOLD CROSS VALIDATION')
    print('Average Accuracy:', round((sum(tfidf_bool_mnb_acc) / cross_val_folds)*100, 2), '%')
    print('Minimum Accuracy:', round(min(tfidf_bool_mnb_acc)*100, 2), '%')
    print('Maximum Accuracy:', round(max(tfidf_bool_mnb_acc)*100, 2), '%')
    print('Confusion Matrix for Folds Where All', num_classes, 'Classifications are Represented:')
    print(tfidf_bool_mnb_cnfmat)
    print()
    print('Bernoulli Naive Bayes with Boolean Count Vectorization -', cross_val_folds, 'FOLD CROSS VALIDATION')
    print('Average Accuracy:', round((sum(cnt_bool_ber_acc) / cross_val_folds)*100, 2), '%')
    print('Minimum Accuracy:', round(min(cnt_bool_ber_acc)*100, 2), '%')
    print('Maximum Accuracy:', round(max(cnt_bool_ber_acc)*100, 2), '%')
    print('Confusion Matrix for Folds Where All', num_classes, 'Classifications are Represented:')
    print(cnt_bool_ber_cnfmat)
    print()
    print('Bernoulli Naive Bayes with Boolean TfIdf Vectorization -', cross_val_folds, 'FOLD CROSS VALIDATION')
    print('Average Accuracy:', round((sum(tfidf_bool_ber_acc) / cross_val_folds)*100, 2), '%')
    print('Minimum Accuracy:', round(min(tfidf_bool_ber_acc)*100, 2), '%')
    print('Maximum Accuracy:', round(max(tfidf_bool_ber_acc)*100, 2), '%')
    print('Confusion Matrix for Folds Where All', num_classes, 'Classifications are Represented:')
    print(tfidf_bool_ber_cnfmat)
    print()
    print('Decision Tree with Count Vectorization -', cross_val_folds, 'FOLD CROSS VALIDATION')
    print('Average Accuracy:', round((sum(cnt_dt_acc) / cross_val_folds)*100, 2), '%')
    print('Minimum Accuracy:', round(min(cnt_dt_acc)*100, 2), '%')
    print('Maximum Accuracy:', round(max(cnt_dt_acc)*100, 2), '%')
    print('Confusion Matrix for Folds Where All', num_classes, 'Classifications are Represented:')
    print(cnt_dt_cnfmat)
    print()
    print('Decision Tree with Boolean Count Vectorization -', cross_val_folds, 'FOLD CROSS VALIDATION')
    print('Average Accuracy:', round((sum(cnt_bool_dt_acc) / cross_val_folds)*100, 2), '%')
    print('Minimum Accuracy:', round(min(cnt_bool_dt_acc)*100, 2), '%')
    print('Maximum Accuracy:', round(max(cnt_bool_dt_acc)*100, 2), '%')
    print('Confusion Matrix for Folds Where All', num_classes, 'Classifications are Represented:')
    print(cnt_bool_dt_cnfmat)
    print()
    print('Decision Tree with TfIdf Vectorization -', cross_val_folds, 'FOLD CROSS VALIDATION')
    print('Average Accuracy:', round((sum(tfidf_dt_acc) / cross_val_folds)*100, 2), '%')
    print('Minimum Accuracy:', round(min(tfidf_dt_acc)*100, 2), '%')
    print('Maximum Accuracy:', round(max(tfidf_dt_acc)*100, 2), '%')
    print('Confusion Matrix for Folds Where All', num_classes, 'Classifications are Represented:')
    print(tfidf_dt_cnfmat)
    print()
    print('Decision Tree with Boolean TfIdf Vectorization -', cross_val_folds, 'FOLD CROSS VALIDATION')
    print('Average Accuracy:', round((sum(tfidf_bool_dt_acc) / cross_val_folds)*100, 2), '%')
    print('Minimum Accuracy:', round(min(tfidf_bool_dt_acc)*100, 2), '%')
    print('Maximum Accuracy:', round(max(tfidf_bool_dt_acc)*100, 2), '%')
    print('Confusion Matrix for Folds Where All', num_classes, 'Classifications are Represented:')
    print(tfidf_bool_ber_cnfmat)

    #Create and return accuracy dataframe
    model_list = ['Multinomial Naive Bayes']*12 + ['Bernoulli Naive Bayes']*6 + ['Decision Tree']*12
    vectorizer_list = ['Count']*3 + ['Boolean Count']*3 + ['TfIdf']*3 + ['Boolean TfIdf']*3 + ['Boolean Count']*3 + ['Boolean TfIdf']*3 + ['Count']*3 + ['Boolean Count']*3 + ['TfIdf']*3 + ['Boolean TfIdf']*3
    measure_list = ['Average Accuracy', 'Minimum Accuracy', 'Maximum Accuracy']*10
    value_list = [sum(cnt_mnb_acc) / cross_val_folds, min(cnt_mnb_acc), max(cnt_mnb_acc),
                    sum(cnt_bool_mnb_acc) / cross_val_folds, min(cnt_bool_mnb_acc), max(cnt_bool_mnb_acc),
                    sum(tfidf_mnb_acc) / cross_val_folds, min(tfidf_mnb_acc), max(tfidf_mnb_acc),
                    sum(tfidf_bool_mnb_acc) / cross_val_folds, min(tfidf_bool_mnb_acc), max(tfidf_bool_mnb_acc),
                    sum(cnt_bool_ber_acc) / cross_val_folds, min(cnt_bool_ber_acc), max(cnt_bool_ber_acc),
                    sum(tfidf_bool_ber_acc) / cross_val_folds, min(tfidf_bool_ber_acc), max(tfidf_bool_ber_acc),
                    sum(cnt_dt_acc) / cross_val_folds, min(cnt_dt_acc), max(cnt_dt_acc),
                    sum(cnt_bool_dt_acc) / cross_val_folds, min(cnt_bool_dt_acc), max(cnt_bool_dt_acc),
                    sum(tfidf_dt_acc) / cross_val_folds, min(tfidf_dt_acc), max(tfidf_dt_acc),
                    sum(tfidf_bool_dt_acc) / cross_val_folds, min(tfidf_bool_dt_acc), max(tfidf_bool_dt_acc)]
    data_list = [[model_list[i], vectorizer_list[i], measure_list[i], value_list[i]] for i in range(30)]
    return(pandas.DataFrame(data_list, columns = ['Model', 'Vectorizer', 'Measure', 'Value']))

#Run function on all three dataframes
print()
print()
print('LIE MODELS')
lie_acc_df = VectorizeModelCrossVal(dataframe = lie, text_column = 'cleaned_review', label_column = 'lie', num_classes = 2, cross_val_folds = 10)
print()
print('ACCURACY DATAFRAME')
print(lie_acc_df)
print()
print('BEST LIE MODEL (Average Accuracy)')
print(lie_acc_df[lie_acc_df['Value'] == max(lie_acc_df[lie_acc_df['Measure'] == 'Average Accuracy']['Value'])])
print()
print()
print('SENTIMENT MODELS')
sentiment_acc_df = VectorizeModelCrossVal(sentiment, text_column = 'cleaned_review', label_column = 'sentiment', num_classes = 2, cross_val_folds = 10)
print()
print('ACCURACY DATAFRAME')
print(sentiment_acc_df)
print()
print('BEST SENTIMENT MODEL (Average Accuracy)')
print(sentiment_acc_df[sentiment_acc_df['Value'] == max(sentiment_acc_df[sentiment_acc_df['Measure'] == 'Average Accuracy']['Value'])])
print()
print()
print('LIE_SENTIMENT MODELS')
lie_sentiment_acc_df = VectorizeModelCrossVal(lie_sentiment, text_column = 'cleaned_review', label_column = 'lie_sentiment', num_classes = 4, cross_val_folds = 10)
print()
print('ACCURACY DATAFRAME')
print(lie_sentiment_acc_df)
print()
print('BEST LIE_SENTIMENT MODEL (Average Accuracy)')
print(lie_sentiment_acc_df[lie_sentiment_acc_df['Value'] == max(lie_sentiment_acc_df[lie_sentiment_acc_df['Measure'] == 'Average Accuracy']['Value'])])

print()
print()
print()
print('End of Homework 6.')