'''
Nick Videtti
Homework 8 - Latent Dirichlet Allocation for Topic Modeling
IST 736 - Text Mining
Spring 2023
'''

#Print Beginning
print('''
Nick Videtti
Homework 8 - Latent Dirichlet Allocation for Topic Modeling
IST 736 - Text Mining
Spring 2023
''')

#import pandas
import pandas

#Find file paths
import tkinter.filedialog
print('FILE DIALOG IS OPEN. PLEASE USE FILE DIALOG TO CHOOSE APPROPRIATE DATA FILE FOR "110" DATA.')
parent_path = tkinter.filedialog.askdirectory(title = 'Please Choose Appropriate Data File For "110" Data...')
print('FILE SELECTED. FILE DIALOG IS CLOSED.')
paths = [parent_path + '/110-f-d', parent_path + '/110-f-r', parent_path + '/110-m-d', parent_path + '/110-m-r']

#Info for user
print()
print('LOADING DATA...')

#Read in data
import os
datalist = []
for path in paths:
    files = [path + '/' + file for file in os.listdir(path)]
    for file in files[:25]:
        with open(file, 'r') as datafile: datalist.append([path[-3], path[-1], datafile.read()])
    datafile.close()

#PREPARE DATA
#Split docs
datalist = [[sex, party, doc.split('<DOC>')[1:]] for [sex, party, doc] in datalist]
datalist = [[sex, party, doc[i]] for [sex, party, doc] in datalist for i in range(len(doc))]
#Split each doc
datalist = [[sex, party, doc.split('<TEXT>')[0], doc.split('<TEXT>')[1]] for [sex, party, doc] in datalist]
#Trim up <DOCNO>'s
datalist = [[sex, party, ' '.join(docname[8:-9].split()), doc] for [sex, party, docname, doc] in datalist]
#Trim up <TEXT>'s
datalist = [[sex, party, docname, ' '.join(doc[:-17].split())] for [sex, party, docname, doc] in datalist]

#Put list into Pandas DataFrame
data = pandas.DataFrame(datalist, columns = ['SEX', 'POLITICAL_PARTY', 'DOCUMENT_NAME', 'DOCUMENT'])

#Transform SEX and POLTICAL_PARTY
data.SEX = data.SEX.str.replace('f', 'FEMALE').replace('m', 'MALE')
data.POLITICAL_PARTY = data.POLITICAL_PARTY.str.replace('d', 'DEMOCRAT').replace('r', 'REPUBLICAN')

#CLEAN DATA
#Tokenize words
import nltk
data['WORDS'] = [nltk.word_tokenize(doc) for doc in data['DOCUMENT']]

#Clean words - lowercase, remove stopwords, remove phrases with numbers, remove phrases that don't contain letters
import re
stopwords = nltk.corpus.stopwords.words('english')
data['CLEANED_WORDS'] = [[word.lower() for word in doc if word.lower() not in stopwords and not re.match('^.*[0-9]+.*$', word) and re.match('^.*[aA-zZ]+.*$', word)] for doc in data['WORDS']]

#Stem words with Porter Stemmer
stemmer = nltk.stem.PorterStemmer()
data['CLEANED_WORDS'] = [[stemmer.stem(word) for word in doc] for doc in data['CLEANED_WORDS']]

#Create cleaned review
data['CLEANED_DOCUMENT'] = [(' '.join(corpus)).strip() for corpus in data['CLEANED_WORDS']]

#Reorder columns
data = data[['SEX', 'POLITICAL_PARTY', 'DOCUMENT_NAME', 'DOCUMENT', 'WORDS', 'CLEANED_DOCUMENT', 'CLEANED_WORDS']]

#Print dataframe
print()
print('Cleaned DataFrame (First 5 Rows):')
print(data.head())
print()

#Create function to go through process for one dataframe
def VectorizeLDA(dataframe, text_column, n_grams = 1, tfidf = False, boolean = False, vec_in_title = False, title = 'LDA Model Topics', LDA_topics = 5, top_words = 15):

    #Create Count, Count Binary, TfIdf, and TfIdf Binary vectors
    from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
    if (not tfidf) & (not boolean): vec = CountVectorizer(ngram_range = (n_grams, n_grams))
    if (not tfidf) & (boolean): vec = CountVectorizer(binary = True, ngram_range = (n_grams, n_grams))
    if (tfidf) & (not boolean): vec = TfidfVectorizer(ngram_range = (n_grams, n_grams))
    if (tfidf) & (boolean): vec = TfidfVectorizer(binary = True, ngram_range = (n_grams, n_grams))

    #Create dataframe
    data = dataframe[text_column]

    #Create Vectorized dataframes
    print('CREATING VECTORIZED DATAFRAME...')
    vec_data = pandas.DataFrame(vec.fit_transform(data).toarray(), columns = vec.get_feature_names_out())
    print('VECTORIZED DATAFRAME CREATED SUCCESSFULLY.')
    print()

    #Create LDA Models
    from sklearn.decomposition import LatentDirichletAllocation

    print('TRAINING LATENT DIRICHLET ALLOCATION MODEL...')
    lda_model = LatentDirichletAllocation(n_components = LDA_topics)
    lda_model.fit_transform(vec_data)
    print('MODEL TRAINED SUCCESSFULLY.')
    print()

    #VISUALIZATION
    from matplotlib import pyplot
    import numpy

    word_topic = numpy.array(lda_model.components_).transpose()
    num_top_words = top_words
    num_topics = LDA_topics
    vocab = numpy.asarray(vec_data.columns)
    fontsize_base = 20
    for i in range(num_topics):
        pyplot.subplot(1, num_topics, i + 1)
        pyplot.ylim(0, num_top_words + 0.5)
        pyplot.xticks([])
        pyplot.yticks([])
        pyplot.axis('off')
        pyplot.title('Topic #{}'.format(i+1))
        top_words_idx = numpy.argsort(word_topic[:,i])[::-1]
        top_words_idx = top_words_idx[:num_top_words]
        top_words = vocab[top_words_idx]
        top_words_shares = word_topic[top_words_idx, i]
        for j, (word, share) in enumerate(zip(top_words, top_words_shares)):
            pyplot.text(0.3, num_top_words-j-0.5, word, fontsize=fontsize_base)
    
    if vec_in_title:
        if (not tfidf) & (not boolean): vec_title = ' (Count Vectorizer)'
        if (not tfidf) & (boolean): vec_title = ' (Count Boolean Vectorizer)'
        if (tfidf) & (not boolean): vec_title = ' (Tfidf Vectorizer)'
        if (tfidf) & (boolean): vec_title = ' (Tfidf Boolean Vectorizer)'
    else: vec_title = ''

    pyplot.suptitle(title + vec_title)
    pyplot.tight_layout()
    print('DISPLAYING VISUAL. THIS MAY BE IN A SEPARATE WINDOW.')
    print('IF THIS IS IN A SEPARATE WINDOW, CLOSE THE WINDOW TO PROCEED.')
    pyplot.show()
    print('\n\n')

#Run function on a few of the datasets
#All - Count Vectorizer
VectorizeLDA(dataframe = data, text_column = 'CLEANED_DOCUMENT', vec_in_title = True, title = 'All Data')
#Female - Count Vectorizer
VectorizeLDA(dataframe = data[data['SEX'] == 'FEMALE'], text_column = 'CLEANED_DOCUMENT', vec_in_title = True, title = 'All Females')
#Male - Count Vectorizer
VectorizeLDA(dataframe = data[data['SEX'] == 'MALE'], text_column = 'CLEANED_DOCUMENT', vec_in_title = True, title = 'All Males')
#Democrat - Count Vectorizer
VectorizeLDA(dataframe = data[data['POLITICAL_PARTY'] == 'DEMOCRAT'], text_column = 'CLEANED_DOCUMENT', vec_in_title = True, title = 'All Democrats')
#Republican - Count Vectorizer
VectorizeLDA(dataframe = data[data['POLITICAL_PARTY'] == 'REPUBLICAN'], text_column = 'CLEANED_DOCUMENT', vec_in_title = True, title = 'All Republicans')
#Female Democrat - Count Vectorizer
VectorizeLDA(dataframe = data[data['SEX'].isin(['FEMALE']) & data['POLITICAL_PARTY'].isin(['DEMOCRAT'])], text_column = 'CLEANED_DOCUMENT', vec_in_title = True, title = 'Female Democrats')
#Male Democrat - Count Vectorizer
VectorizeLDA(dataframe = data[data['SEX'].isin(['MALE']) & data['POLITICAL_PARTY'].isin(['DEMOCRAT'])], text_column = 'CLEANED_DOCUMENT', vec_in_title = True, title = 'Male Democrats')
#Female Republican - Count Vectorizer
VectorizeLDA(dataframe = data[data['SEX'].isin(['FEMALE']) & data['POLITICAL_PARTY'].isin(['REPUBLICAN'])], text_column = 'CLEANED_DOCUMENT', vec_in_title = True, title = 'Female Republicans')
#Male Republican - Count Vectorizer
VectorizeLDA(dataframe = data[data['SEX'].isin(['MALE']) & data['POLITICAL_PARTY'].isin(['REPUBLICAN'])], text_column = 'CLEANED_DOCUMENT', vec_in_title = True, title = 'Male Republicans')

#All - Tfidf Vectorizer
VectorizeLDA(dataframe = data, text_column = 'CLEANED_DOCUMENT', tfidf = True, vec_in_title = True, title = 'All Data')
#Female - Tfidf Vectorizer
VectorizeLDA(dataframe = data[data['SEX'] == 'FEMALE'], text_column = 'CLEANED_DOCUMENT', tfidf = True, vec_in_title = True, title = 'All Females')
#Male - Tfidf Vectorizer
VectorizeLDA(dataframe = data[data['SEX'] == 'MALE'], text_column = 'CLEANED_DOCUMENT', tfidf = True, vec_in_title = True, title = 'All Males')
#Democrat - Tfidf Vectorizer
VectorizeLDA(dataframe = data[data['POLITICAL_PARTY'] == 'DEMOCRAT'], text_column = 'CLEANED_DOCUMENT', tfidf = True, vec_in_title = True, title = 'All Democrats')
#Republican - Tfidf Vectorizer
VectorizeLDA(dataframe = data[data['POLITICAL_PARTY'] == 'REPUBLICAN'], text_column = 'CLEANED_DOCUMENT', tfidf = True, vec_in_title = True, title = 'All Republicans')
#Female Democrat - Tfidf Vectorizer
VectorizeLDA(dataframe = data[data['SEX'].isin(['FEMALE']) & data['POLITICAL_PARTY'].isin(['DEMOCRAT'])], text_column = 'CLEANED_DOCUMENT', tfidf = True, vec_in_title = True, title = 'Female Democrats')
#Male Democrat - Tfidf Vectorizer
VectorizeLDA(dataframe = data[data['SEX'].isin(['MALE']) & data['POLITICAL_PARTY'].isin(['DEMOCRAT'])], text_column = 'CLEANED_DOCUMENT', tfidf = True, vec_in_title = True, title = 'Male Democrats')
#Female Republican - Tfidf Vectorizer
VectorizeLDA(dataframe = data[data['SEX'].isin(['FEMALE']) & data['POLITICAL_PARTY'].isin(['REPUBLICAN'])], text_column = 'CLEANED_DOCUMENT', tfidf = True, vec_in_title = True, title = 'Female Republicans')
#Male Republican - Tfidf Vectorizer
VectorizeLDA(dataframe = data[data['SEX'].isin(['MALE']) & data['POLITICAL_PARTY'].isin(['REPUBLICAN'])], text_column = 'CLEANED_DOCUMENT', tfidf = True, vec_in_title = True, title = 'Male Republicans')

#Print Ending
print('END OF HOMEWORK 8.')