'''
Nick Videtti
Homework 7 - Naive Bayes and Support Vector Machines on Corpora
IST 736 - Text Mining
Spring 2023
'''

#import pandas
import pandas

#Read in csv file of choice for negative corpora
import tkinter.filedialog
neg_path = tkinter.filedialog.askdirectory(title = 'Please Choose Appropriate Data File for NEGATIVE Reviews...')
pos_path = tkinter.filedialog.askdirectory(title = 'Please Choose Appropriate Data File for POSITIVE Reviews...')

#Info for user
print('LOADING DATA...')

#Read in negative data
import os
neg_files = [neg_path + '/' + file for file in os.listdir(neg_path)]
neg_datalist = []
for corpus in neg_files[:100]:
    with open(corpus, 'r', encoding = 'utf-8') as datafile: neg_datalist.append(['-', datafile.read()])
    datafile.close()

#Read in positive data
pos_files = [pos_path + '/' + file for file in os.listdir(pos_path)]
pos_datalist = []
for corpus in pos_files[:100]:
    with open(corpus, 'r', encoding = 'utf-8') as datafile: pos_datalist.append(['+', datafile.read()])
    datafile.close()

#Create dataframe
data = pandas.DataFrame(data = neg_datalist + pos_datalist, columns = ['SENTIMENT', 'CORPUS'])

#Tokenize words
import nltk
data['WORDS'] = [nltk.word_tokenize(corpus) for corpus in data['CORPUS']]

#Clean words - lowercase, remove line breaks, remove stopwords, remove phrases with numbers, remove phrases that don't contain letters
import re
stopwords = nltk.corpus.stopwords.words('english')
data['CLEANED_WORDS'] = [[word.lower() for word in corpus if word != 'br' and word.lower() not in stopwords and not re.match('^.*[0-9]+.*$', word) and re.match('^.*[aA-zZ]+.*$', word)] for corpus in data['WORDS']]

#Create cleaned review
data['CLEANED_CORPUS'] = [(' '.join(corpus)).strip() for corpus in data['CLEANED_WORDS']]

#Reorder columns
data = data[['SENTIMENT', 'CORPUS', 'CLEANED_CORPUS', 'WORDS', 'CLEANED_WORDS']]

#Print dataframe
print()
print('Cleaned DataFrame:')
print(data.head())

#Create function to go through process for one dataframe
def VectorizeModelCrossValBEST(dataframe, text_column, label_column, n_grams = 1, cross_val_folds = 5):

    #Create num_classes variable
    num_classes = len(set(dataframe[label_column]))

    #Create Count, Count Binary, TfIdf, and TfIdf Binary vectors
    from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
    from sklearn.naive_bayes import MultinomialNB, BernoulliNB
    from sklearn.svm import SVC, LinearSVC
    from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
    cnt = CountVectorizer(ngram_range = (n_grams, n_grams))
    cnt_bool = CountVectorizer(binary = True, ngram_range = (n_grams, n_grams))
    tfidf = TfidfVectorizer(ngram_range = (n_grams, n_grams))
    tfidf_bool = TfidfVectorizer(binary = True, ngram_range = (n_grams, n_grams))

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
    cnt_polysvm_acc = []
    cnt_bool_polysvm_acc = []
    tfidf_polysvm_acc = []
    tfidf_bool_polysvm_acc = []
    cnt_rbfsvm_acc = []
    cnt_bool_rbfsvm_acc = []
    tfidf_rbfsvm_acc = []
    tfidf_bool_rbfsvm_acc = []
    cnt_linsvm_acc = []
    cnt_bool_linsvm_acc = []
    tfidf_linsvm_acc = []
    tfidf_bool_linsvm_acc = []
    cnt_mnb_cnfmat = [[i*0 for i in range(num_classes)]]*num_classes
    cnt_bool_mnb_cnfmat = [[i*0 for i in range(num_classes)]]*num_classes
    tfidf_mnb_cnfmat = [[i*0 for i in range(num_classes)]]*num_classes
    tfidf_bool_mnb_cnfmat = [[i*0 for i in range(num_classes)]]*num_classes
    cnt_bool_ber_cnfmat = [[i*0 for i in range(num_classes)]]*num_classes
    tfidf_bool_ber_cnfmat = [[i*0 for i in range(num_classes)]]*num_classes
    cnt_polysvm_cnfmat = [[i*0 for i in range(num_classes)]]*num_classes
    cnt_bool_polysvm_cnfmat = [[i*0 for i in range(num_classes)]]*num_classes
    tfidf_polysvm_cnfmat = [[i*0 for i in range(num_classes)]]*num_classes
    tfidf_bool_polysvm_cnfmat = [[i*0 for i in range(num_classes)]]*num_classes
    cnt_rbfsvm_cnfmat = [[i*0 for i in range(num_classes)]]*num_classes
    cnt_bool_rbfsvm_cnfmat = [[i*0 for i in range(num_classes)]]*num_classes
    tfidf_rbfsvm_cnfmat = [[i*0 for i in range(num_classes)]]*num_classes
    tfidf_bool_rbfsvm_cnfmat = [[i*0 for i in range(num_classes)]]*num_classes
    cnt_linsvm_cnfmat = [[i*0 for i in range(num_classes)]]*num_classes
    cnt_bool_linsvm_cnfmat = [[i*0 for i in range(num_classes)]]*num_classes
    tfidf_linsvm_cnfmat = [[i*0 for i in range(num_classes)]]*num_classes
    tfidf_bool_linsvm_cnfmat = [[i*0 for i in range(num_classes)]]*num_classes
    
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

            #Polynomial Support Vector Machine - Count
            test_start = int(len(cnt_data.index)/cross_val_folds) * i
            test_stop = int(len(cnt_data.index)/cross_val_folds) * (i+1)
            test = cnt_data.iloc[test_start : test_stop]
            test_labels = test[label_column]
            test = test.drop(columns = [label_column])
            train = pandas.concat([cnt_data.iloc[:test_start], cnt_data.iloc[test_stop:]])
            polysvm = SVC(kernel = 'poly')
            polysvm.fit(train.drop(columns = [label_column]), train[label_column])
            cnt_polysvm_acc.append(polysvm.score(test, test_labels))
            pred = polysvm.predict(test)
            cnt_polysvm_cnfmat += confusion_matrix(test_labels, pred)
                
            #Polynomial Support Vector Machine - Count Boolean
            test_start = int(len(cnt_bool_data.index)/cross_val_folds) * i
            test_stop = int(len(cnt_bool_data.index)/cross_val_folds) * (i+1)
            test = cnt_bool_data.iloc[test_start : test_stop]
            test_labels = test[label_column]
            test = test.drop(columns = [label_column])
            train = pandas.concat([cnt_bool_data.iloc[:test_start], cnt_bool_data.iloc[test_stop:]])
            polysvm = SVC(kernel = 'poly')
            polysvm.fit(train.drop(columns = [label_column]), train[label_column])
            cnt_bool_polysvm_acc.append(polysvm.score(test, test_labels))
            pred = polysvm.predict(test)
            cnt_bool_polysvm_cnfmat += confusion_matrix(test_labels, pred)

            #Polynomial Support Vector Machine - TfIdf
            test_start = int(len(tfidf_data.index)/cross_val_folds) * i
            test_stop = int(len(tfidf_data.index)/cross_val_folds) * (i+1)
            test = tfidf_data.iloc[test_start : test_stop]
            test_labels = test[label_column]
            test = test.drop(columns = [label_column])
            train = pandas.concat([tfidf_data.iloc[:test_start], tfidf_data.iloc[test_stop:]])
            polysvm = SVC(kernel = 'poly')
            polysvm.fit(train.drop(columns = [label_column]), train[label_column])
            tfidf_polysvm_acc.append(polysvm.score(test, test_labels))
            pred = polysvm.predict(test)
            tfidf_polysvm_cnfmat += confusion_matrix(test_labels, pred)

            #Polynomial Support Vector Machine - TfIdf Boolean
            test_start = int(len(tfidf_bool_data.index)/cross_val_folds) * i
            test_stop = int(len(tfidf_bool_data.index)/cross_val_folds) * (i+1)
            test = tfidf_bool_data.iloc[test_start : test_stop]
            test_labels = test[label_column]
            test = test.drop(columns = [label_column])
            train = pandas.concat([tfidf_bool_data.iloc[:test_start], tfidf_bool_data.iloc[test_stop:]])
            polysvm = SVC(kernel = 'poly')
            polysvm.fit(train.drop(columns = [label_column]), train[label_column])
            tfidf_bool_polysvm_acc.append(polysvm.score(test, test_labels))
            pred = polysvm.predict(test)
            tfidf_bool_polysvm_cnfmat += confusion_matrix(test_labels, pred)

            #RBF Support Vector Machine - Count
            test_start = int(len(cnt_data.index)/cross_val_folds) * i
            test_stop = int(len(cnt_data.index)/cross_val_folds) * (i+1)
            test = cnt_data.iloc[test_start : test_stop]
            test_labels = test[label_column]
            test = test.drop(columns = [label_column])
            train = pandas.concat([cnt_data.iloc[:test_start], cnt_data.iloc[test_stop:]])
            rbfsvm = SVC()
            rbfsvm.fit(train.drop(columns = [label_column]), train[label_column])
            cnt_rbfsvm_acc.append(rbfsvm.score(test, test_labels))
            pred = rbfsvm.predict(test)
            cnt_rbfsvm_cnfmat += confusion_matrix(test_labels, pred)
                
            #RBF Support Vector Machine - Count Boolean
            test_start = int(len(cnt_bool_data.index)/cross_val_folds) * i
            test_stop = int(len(cnt_bool_data.index)/cross_val_folds) * (i+1)
            test = cnt_bool_data.iloc[test_start : test_stop]
            test_labels = test[label_column]
            test = test.drop(columns = [label_column])
            train = pandas.concat([cnt_bool_data.iloc[:test_start], cnt_bool_data.iloc[test_stop:]])
            rbfsvm = SVC()
            rbfsvm.fit(train.drop(columns = [label_column]), train[label_column])
            cnt_bool_rbfsvm_acc.append(rbfsvm.score(test, test_labels))
            pred = rbfsvm.predict(test)
            cnt_bool_rbfsvm_cnfmat += confusion_matrix(test_labels, pred)

            #RBF Support Vector Machine - TfIdf
            test_start = int(len(tfidf_data.index)/cross_val_folds) * i
            test_stop = int(len(tfidf_data.index)/cross_val_folds) * (i+1)
            test = tfidf_data.iloc[test_start : test_stop]
            test_labels = test[label_column]
            test = test.drop(columns = [label_column])
            train = pandas.concat([tfidf_data.iloc[:test_start], tfidf_data.iloc[test_stop:]])
            rbfsvm = SVC()
            rbfsvm.fit(train.drop(columns = [label_column]), train[label_column])
            tfidf_rbfsvm_acc.append(rbfsvm.score(test, test_labels))
            pred = rbfsvm.predict(test)
            tfidf_rbfsvm_cnfmat += confusion_matrix(test_labels, pred)

            #RBF Support Vector Machine - TfIdf Boolean
            test_start = int(len(tfidf_bool_data.index)/cross_val_folds) * i
            test_stop = int(len(tfidf_bool_data.index)/cross_val_folds) * (i+1)
            test = tfidf_bool_data.iloc[test_start : test_stop]
            test_labels = test[label_column]
            test = test.drop(columns = [label_column])
            train = pandas.concat([tfidf_bool_data.iloc[:test_start], tfidf_bool_data.iloc[test_stop:]])
            rbfsvm = SVC()
            rbfsvm.fit(train.drop(columns = [label_column]), train[label_column])
            tfidf_bool_rbfsvm_acc.append(rbfsvm.score(test, test_labels))
            pred = rbfsvm.predict(test)
            tfidf_bool_rbfsvm_cnfmat += confusion_matrix(test_labels, pred)
            
            #Linear Support Vector Machine - Count
            test_start = int(len(cnt_data.index)/cross_val_folds) * i
            test_stop = int(len(cnt_data.index)/cross_val_folds) * (i+1)
            test = cnt_data.iloc[test_start : test_stop]
            test_labels = test[label_column]
            test = test.drop(columns = [label_column])
            train = pandas.concat([cnt_data.iloc[:test_start], cnt_data.iloc[test_stop:]])
            linsvm = LinearSVC()
            linsvm.fit(train.drop(columns = [label_column]), train[label_column])
            cnt_linsvm_acc.append(linsvm.score(test, test_labels))
            pred = linsvm.predict(test)
            cnt_linsvm_cnfmat += confusion_matrix(test_labels, pred)
                
            #Linear Support Vector Machine - Count Boolean
            test_start = int(len(cnt_bool_data.index)/cross_val_folds) * i
            test_stop = int(len(cnt_bool_data.index)/cross_val_folds) * (i+1)
            test = cnt_bool_data.iloc[test_start : test_stop]
            test_labels = test[label_column]
            test = test.drop(columns = [label_column])
            train = pandas.concat([cnt_bool_data.iloc[:test_start], cnt_bool_data.iloc[test_stop:]])
            linsvm = LinearSVC()
            linsvm.fit(train.drop(columns = [label_column]), train[label_column])
            cnt_bool_linsvm_acc.append(linsvm.score(test, test_labels))
            pred = linsvm.predict(test)
            cnt_bool_linsvm_cnfmat += confusion_matrix(test_labels, pred)

            #Linear Support Vector Machine - TfIdf
            test_start = int(len(tfidf_data.index)/cross_val_folds) * i
            test_stop = int(len(tfidf_data.index)/cross_val_folds) * (i+1)
            test = tfidf_data.iloc[test_start : test_stop]
            test_labels = test[label_column]
            test = test.drop(columns = [label_column])
            train = pandas.concat([tfidf_data.iloc[:test_start], tfidf_data.iloc[test_stop:]])
            linsvm = LinearSVC()
            linsvm.fit(train.drop(columns = [label_column]), train[label_column])
            tfidf_linsvm_acc.append(linsvm.score(test, test_labels))
            pred = linsvm.predict(test)
            tfidf_linsvm_cnfmat += confusion_matrix(test_labels, pred)

            #Linear Support Vector Machine - TfIdf Boolean
            test_start = int(len(tfidf_bool_data.index)/cross_val_folds) * i
            test_stop = int(len(tfidf_bool_data.index)/cross_val_folds) * (i+1)
            test = tfidf_bool_data.iloc[test_start : test_stop]
            test_labels = test[label_column]
            test = test.drop(columns = [label_column])
            train = pandas.concat([tfidf_bool_data.iloc[:test_start], tfidf_bool_data.iloc[test_stop:]])
            linsvm = LinearSVC()
            linsvm.fit(train.drop(columns = [label_column]), train[label_column])
            tfidf_bool_linsvm_acc.append(linsvm.score(test, test_labels))
            pred = linsvm.predict(test)
            tfidf_bool_linsvm_cnfmat += confusion_matrix(test_labels, pred)

        #Pass if fails
        except: pass

    #Create accuracy dataframe
    model_list = ['Multinomial Naive Bayes']*12 + ['Bernoulli Naive Bayes']*6 + ['Support Vector Machine (Polynomial Kernel)']*12 + ['Support Vector Machine (RBF Kernel)']*12 + ['Support Vector Machine (Linear Kernel)']*12
    vectorizer_list = ['Count']*3 + ['Boolean Count']*3 + ['TfIdf']*3 + ['Boolean TfIdf']*3 + ['Boolean Count']*3 + ['Boolean TfIdf']*3 + ['Count']*3 + ['Boolean Count']*3 + ['TfIdf']*3 + ['Boolean TfIdf']*3 \
                        + ['Count']*3 + ['Boolean Count']*3 + ['TfIdf']*3 + ['Boolean TfIdf']*3 + ['Count']*3 + ['Boolean Count']*3 + ['TfIdf']*3 + ['Boolean TfIdf']*3
    measure_list = ['Average Accuracy', 'Minimum Accuracy', 'Maximum Accuracy']*18
    value_list = [sum(cnt_mnb_acc) / cross_val_folds, min(cnt_mnb_acc), max(cnt_mnb_acc),
                    sum(cnt_bool_mnb_acc) / cross_val_folds, min(cnt_bool_mnb_acc), max(cnt_bool_mnb_acc),
                    sum(tfidf_mnb_acc) / cross_val_folds, min(tfidf_mnb_acc), max(tfidf_mnb_acc),
                    sum(tfidf_bool_mnb_acc) / cross_val_folds, min(tfidf_bool_mnb_acc), max(tfidf_bool_mnb_acc),
                    sum(cnt_bool_ber_acc) / cross_val_folds, min(cnt_bool_ber_acc), max(cnt_bool_ber_acc),
                    sum(tfidf_bool_ber_acc) / cross_val_folds, min(tfidf_bool_ber_acc), max(tfidf_bool_ber_acc),
                    sum(cnt_polysvm_acc) / cross_val_folds, min(cnt_polysvm_acc), max(cnt_polysvm_acc),
                    sum(cnt_bool_polysvm_acc) / cross_val_folds, min(cnt_bool_polysvm_acc), max(cnt_bool_polysvm_acc),
                    sum(tfidf_polysvm_acc) / cross_val_folds, min(tfidf_polysvm_acc), max(tfidf_polysvm_acc),
                    sum(tfidf_bool_polysvm_acc) / cross_val_folds, min(tfidf_bool_polysvm_acc), max(tfidf_bool_polysvm_acc),
                    sum(cnt_rbfsvm_acc) / cross_val_folds, min(cnt_rbfsvm_acc), max(cnt_rbfsvm_acc),
                    sum(cnt_bool_rbfsvm_acc) / cross_val_folds, min(cnt_bool_rbfsvm_acc), max(cnt_bool_rbfsvm_acc),
                    sum(tfidf_rbfsvm_acc) / cross_val_folds, min(tfidf_rbfsvm_acc), max(tfidf_rbfsvm_acc),
                    sum(tfidf_bool_rbfsvm_acc) / cross_val_folds, min(tfidf_bool_rbfsvm_acc), max(tfidf_bool_rbfsvm_acc),
                    sum(cnt_linsvm_acc) / cross_val_folds, min(cnt_linsvm_acc), max(cnt_linsvm_acc),
                    sum(cnt_bool_linsvm_acc) / cross_val_folds, min(cnt_bool_linsvm_acc), max(cnt_bool_linsvm_acc),
                    sum(tfidf_linsvm_acc) / cross_val_folds, min(tfidf_linsvm_acc), max(tfidf_linsvm_acc),
                    sum(tfidf_bool_linsvm_acc) / cross_val_folds, min(tfidf_bool_linsvm_acc), max(tfidf_bool_linsvm_acc)]
    data_list = [[model_list[i], vectorizer_list[i], measure_list[i], value_list[i]] for i in range(54)]
    acc_df = pandas.DataFrame(data_list, columns = ['Model', 'Vectorizer', 'Measure', 'Value'])

    print('--------------ACCURACY SUMMARY---------------')
    print()
    print('Multinomial Naive Bayes with', str(n_grams)+'-Gram', 'Count Vectorization -', cross_val_folds, 'FOLD CROSS VALIDATION')
    print('Average Accuracy:', round((sum(cnt_mnb_acc) / cross_val_folds)*100, 2), '%')
    print('Minimum Accuracy:', round(min(cnt_mnb_acc)*100, 2), '%')
    print('Maximum Accuracy:', round(max(cnt_mnb_acc)*100, 2), '%')
    print('Confusion Matrix for Folds Where All', num_classes, 'Classifications are Represented:')
    print(cnt_mnb_cnfmat)
    print()
    print('Multinomial Naive Bayes with', str(n_grams)+'-Gram', 'Boolean Count Vectorization -', cross_val_folds, 'FOLD CROSS VALIDATION')
    print('Average Accuracy:', round((sum(cnt_bool_mnb_acc) / cross_val_folds)*100, 2), '%')
    print('Minimum Accuracy:', round(min(cnt_bool_mnb_acc)*100, 2), '%')
    print('Maximum Accuracy:', round(max(cnt_bool_mnb_acc)*100, 2), '%')
    print('Confusion Matrix for Folds Where All', num_classes, 'Classifications are Represented:')
    print(cnt_bool_mnb_cnfmat)
    print()
    print('Multinomial Naive Bayes with', str(n_grams)+'-Gram', 'TfIdf Vectorization -', cross_val_folds, 'FOLD CROSS VALIDATION')
    print('Average Accuracy:', round((sum(tfidf_mnb_acc) / cross_val_folds)*100, 2), '%')
    print('Minimum Accuracy:', round(min(tfidf_mnb_acc)*100, 2), '%')
    print('Maximum Accuracy:', round(max(tfidf_mnb_acc)*100, 2), '%')
    print('Confusion Matrix for Folds Where All', num_classes, 'Classifications are Represented:')
    print(tfidf_mnb_cnfmat)
    print()
    print('Multinomial Naive Bayes with', str(n_grams)+'-Gram', 'Boolean TfIdf Vectorization -', cross_val_folds, 'FOLD CROSS VALIDATION')
    print('Average Accuracy:', round((sum(tfidf_bool_mnb_acc) / cross_val_folds)*100, 2), '%')
    print('Minimum Accuracy:', round(min(tfidf_bool_mnb_acc)*100, 2), '%')
    print('Maximum Accuracy:', round(max(tfidf_bool_mnb_acc)*100, 2), '%')
    print('Confusion Matrix for Folds Where All', num_classes, 'Classifications are Represented:')
    print(tfidf_bool_mnb_cnfmat)
    print()
    print('Bernoulli Naive Bayes with', str(n_grams)+'-Gram', 'Boolean Count Vectorization -', cross_val_folds, 'FOLD CROSS VALIDATION')
    print('Average Accuracy:', round((sum(cnt_bool_ber_acc) / cross_val_folds)*100, 2), '%')
    print('Minimum Accuracy:', round(min(cnt_bool_ber_acc)*100, 2), '%')
    print('Maximum Accuracy:', round(max(cnt_bool_ber_acc)*100, 2), '%')
    print('Confusion Matrix for Folds Where All', num_classes, 'Classifications are Represented:')
    print(cnt_bool_ber_cnfmat)
    print()
    print('Bernoulli Naive Bayes with', str(n_grams)+'-Gram', 'Boolean TfIdf Vectorization -', cross_val_folds, 'FOLD CROSS VALIDATION')
    print('Average Accuracy:', round((sum(tfidf_bool_ber_acc) / cross_val_folds)*100, 2), '%')
    print('Minimum Accuracy:', round(min(tfidf_bool_ber_acc)*100, 2), '%')
    print('Maximum Accuracy:', round(max(tfidf_bool_ber_acc)*100, 2), '%')
    print('Confusion Matrix for Folds Where All', num_classes, 'Classifications are Represented:')
    print(tfidf_bool_ber_cnfmat)
    print()
    print('Support Vector Machine (Polynomial Kernel) with', str(n_grams)+'-Gram', 'Count Vectorization -', cross_val_folds, 'FOLD CROSS VALIDATION')
    print('Average Accuracy:', round((sum(cnt_polysvm_acc) / cross_val_folds)*100, 2), '%')
    print('Minimum Accuracy:', round(min(cnt_polysvm_acc)*100, 2), '%')
    print('Maximum Accuracy:', round(max(cnt_polysvm_acc)*100, 2), '%')
    print('Confusion Matrix for Folds Where All', num_classes, 'Classifications are Represented:')
    print(cnt_polysvm_cnfmat)
    print()
    print('Support Vector Machine (Polynomial Kernel) with', str(n_grams)+'-Gram', 'Boolean Count Vectorization -', cross_val_folds, 'FOLD CROSS VALIDATION')
    print('Average Accuracy:', round((sum(cnt_bool_polysvm_acc) / cross_val_folds)*100, 2), '%')
    print('Minimum Accuracy:', round(min(cnt_bool_polysvm_acc)*100, 2), '%')
    print('Maximum Accuracy:', round(max(cnt_bool_polysvm_acc)*100, 2), '%')
    print('Confusion Matrix for Folds Where All', num_classes, 'Classifications are Represented:')
    print(cnt_bool_polysvm_cnfmat)
    print()
    print('Support Vector Machine (Polynomial Kernel) with', str(n_grams)+'-Gram', 'TfIdf Vectorization -', cross_val_folds, 'FOLD CROSS VALIDATION')
    print('Average Accuracy:', round((sum(tfidf_polysvm_acc) / cross_val_folds)*100, 2), '%')
    print('Minimum Accuracy:', round(min(tfidf_polysvm_acc)*100, 2), '%')
    print('Maximum Accuracy:', round(max(tfidf_polysvm_acc)*100, 2), '%')
    print('Confusion Matrix for Folds Where All', num_classes, 'Classifications are Represented:')
    print(tfidf_polysvm_cnfmat)
    print()
    print('Support Vector Machine (Polynomial Kernel) with', str(n_grams)+'-Gram', 'Boolean TfIdf Vectorization -', cross_val_folds, 'FOLD CROSS VALIDATION')
    print('Average Accuracy:', round((sum(tfidf_bool_polysvm_acc) / cross_val_folds)*100, 2), '%')
    print('Minimum Accuracy:', round(min(tfidf_bool_polysvm_acc)*100, 2), '%')
    print('Maximum Accuracy:', round(max(tfidf_bool_polysvm_acc)*100, 2), '%')
    print('Confusion Matrix for Folds Where All', num_classes, 'Classifications are Represented:')
    print(tfidf_bool_polysvm_cnfmat)
    print()
    print('Support Vector Machine (RBF Kernel) with', str(n_grams)+'-Gram', 'Count Vectorization -', cross_val_folds, 'FOLD CROSS VALIDATION')
    print('Average Accuracy:', round((sum(cnt_rbfsvm_acc) / cross_val_folds)*100, 2), '%')
    print('Minimum Accuracy:', round(min(cnt_rbfsvm_acc)*100, 2), '%')
    print('Maximum Accuracy:', round(max(cnt_rbfsvm_acc)*100, 2), '%')
    print('Confusion Matrix for Folds Where All', num_classes, 'Classifications are Represented:')
    print(cnt_rbfsvm_cnfmat)
    print()
    print('Support Vector Machine (RBF Kernel) with', str(n_grams)+'-Gram', 'Boolean Count Vectorization -', cross_val_folds, 'FOLD CROSS VALIDATION')
    print('Average Accuracy:', round((sum(cnt_bool_rbfsvm_acc) / cross_val_folds)*100, 2), '%')
    print('Minimum Accuracy:', round(min(cnt_bool_rbfsvm_acc)*100, 2), '%')
    print('Maximum Accuracy:', round(max(cnt_bool_rbfsvm_acc)*100, 2), '%')
    print('Confusion Matrix for Folds Where All', num_classes, 'Classifications are Represented:')
    print(cnt_bool_rbfsvm_cnfmat)
    print()
    print('Support Vector Machine (RBF Kernel) with', str(n_grams)+'-Gram', 'TfIdf Vectorization -', cross_val_folds, 'FOLD CROSS VALIDATION')
    print('Average Accuracy:', round((sum(tfidf_rbfsvm_acc) / cross_val_folds)*100, 2), '%')
    print('Minimum Accuracy:', round(min(tfidf_rbfsvm_acc)*100, 2), '%')
    print('Maximum Accuracy:', round(max(tfidf_rbfsvm_acc)*100, 2), '%')
    print('Confusion Matrix for Folds Where All', num_classes, 'Classifications are Represented:')
    print(tfidf_rbfsvm_cnfmat)
    print()
    print('Support Vector Machine (RBF Kernel) with', str(n_grams)+'-Gram', 'Boolean TfIdf Vectorization -', cross_val_folds, 'FOLD CROSS VALIDATION')
    print('Average Accuracy:', round((sum(tfidf_bool_rbfsvm_acc) / cross_val_folds)*100, 2), '%')
    print('Minimum Accuracy:', round(min(tfidf_bool_rbfsvm_acc)*100, 2), '%')
    print('Maximum Accuracy:', round(max(tfidf_bool_rbfsvm_acc)*100, 2), '%')
    print('Confusion Matrix for Folds Where All', num_classes, 'Classifications are Represented:')
    print(tfidf_bool_rbfsvm_cnfmat)
    print()
    print('Support Vector Machine (Linear Kernel) with', str(n_grams)+'-Gram', 'Count Vectorization -', cross_val_folds, 'FOLD CROSS VALIDATION')
    print('Average Accuracy:', round((sum(cnt_linsvm_acc) / cross_val_folds)*100, 2), '%')
    print('Minimum Accuracy:', round(min(cnt_linsvm_acc)*100, 2), '%')
    print('Maximum Accuracy:', round(max(cnt_linsvm_acc)*100, 2), '%')
    print('Confusion Matrix for Folds Where All', num_classes, 'Classifications are Represented:')
    print(cnt_linsvm_cnfmat)
    print()
    print('Support Vector Machine (Linear Kernel) with', str(n_grams)+'-Gram', 'Boolean Count Vectorization -', cross_val_folds, 'FOLD CROSS VALIDATION')
    print('Average Accuracy:', round((sum(cnt_bool_linsvm_acc) / cross_val_folds)*100, 2), '%')
    print('Minimum Accuracy:', round(min(cnt_bool_linsvm_acc)*100, 2), '%')
    print('Maximum Accuracy:', round(max(cnt_bool_linsvm_acc)*100, 2), '%')
    print('Confusion Matrix for Folds Where All', num_classes, 'Classifications are Represented:')
    print(cnt_bool_linsvm_cnfmat)
    print()
    print('Support Vector Machine (Linear Kernel) with', str(n_grams)+'-Gram', 'TfIdf Vectorization -', cross_val_folds, 'FOLD CROSS VALIDATION')
    print('Average Accuracy:', round((sum(tfidf_linsvm_acc) / cross_val_folds)*100, 2), '%')
    print('Minimum Accuracy:', round(min(tfidf_linsvm_acc)*100, 2), '%')
    print('Maximum Accuracy:', round(max(tfidf_linsvm_acc)*100, 2), '%')
    print('Confusion Matrix for Folds Where All', num_classes, 'Classifications are Represented:')
    print(tfidf_linsvm_cnfmat)
    print()
    print('Support Vector Machine (Linear Kernel) with', str(n_grams)+'-Gram', 'Boolean TfIdf Vectorization -', cross_val_folds, 'FOLD CROSS VALIDATION')
    print('Average Accuracy:', round((sum(tfidf_bool_linsvm_acc) / cross_val_folds)*100, 2), '%')
    print('Minimum Accuracy:', round(min(tfidf_bool_linsvm_acc)*100, 2), '%')
    print('Maximum Accuracy:', round(max(tfidf_bool_linsvm_acc)*100, 2), '%')
    print('Confusion Matrix for Folds Where All', num_classes, 'Classifications are Represented:')
    print(tfidf_bool_linsvm_cnfmat)
    print()
    print()
    print('ACCURACY DATAFRAME')
    print(acc_df)
    print()
    print('BEST MODEL(S) (Average Accuracy)')
    print(acc_df[acc_df['Value'] == max(acc_df[acc_df['Measure'] == 'Average Accuracy']['Value'])])
    return acc_df[acc_df['Value'] == max(acc_df[acc_df['Measure'] == 'Average Accuracy']['Value'])]

#Use data and function
print()
print('UNIGRAMS...')
print()
print()
BEST_UNIGRAM = VectorizeModelCrossValBEST(data, text_column = 'CLEANED_CORPUS', label_column = 'SENTIMENT')
print()
print()
print()
print('BIGRAMS...')
print()
print()
BEST_BIGRAM = VectorizeModelCrossValBEST(data, text_column = 'CLEANED_CORPUS', label_column = 'SENTIMENT', n_grams = 2)
print()
print()
print()
print('Best Model(s) Using UNIGRAMS:')
print('(Based On Average Accuracy During Cross Validations)')
print()
print(BEST_UNIGRAM)
print()
from sklearn.feature_extraction.text import CountVectorizer
uni_vec = CountVectorizer()
uni_data = pandas.DataFrame(uni_vec.fit_transform(data['CLEANED_CORPUS']).toarray(), columns = uni_vec.get_feature_names_out())
uni_data = data[['SENTIMENT']].join(uni_data).fillna(0)
top_10_pos = uni_data[uni_data['SENTIMENT'] == '+'].drop(columns = ['SENTIMENT']).sum().sort_values(ascending = False)[:10].index
print('"Most Positive" Features:')
for feature in top_10_pos: print(feature)
print()
top_10_neg = uni_data[uni_data['SENTIMENT'] == '-'].drop(columns = ['SENTIMENT']).sum().sort_values(ascending = False)[:10].index
print('"Most Negative" Features:')
for feature in top_10_neg: print(feature)
print()
print()
print()
print('Best Model(s) Using BIGRAMS:')
print('(Based On Average Accuracy During Cross Validations)')
print()
print(BEST_BIGRAM)
print()
bi_vec = CountVectorizer(ngram_range = (2,2))
bi_data = pandas.DataFrame(bi_vec.fit_transform(data['CLEANED_CORPUS']).toarray(), columns = bi_vec.get_feature_names_out())
bi_data = data[['SENTIMENT']].join(bi_data).fillna(0)
top_10_pos = bi_data[bi_data['SENTIMENT'] == '+'].drop(columns = ['SENTIMENT']).sum().sort_values(ascending = False)[:10].index
print('"Most Positive" Features:')
for feature in top_10_pos: print(feature)
print()
top_10_neg = bi_data[bi_data['SENTIMENT'] == '-'].drop(columns = ['SENTIMENT']).sum().sort_values(ascending = False)[:10].index
print('"Most Negative" Features:')
for feature in top_10_neg: print(feature)
print()
print()
print()
print('End of Homework 7.')