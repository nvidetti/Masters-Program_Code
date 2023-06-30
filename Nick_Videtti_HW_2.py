'''Nick Videtti
Homework 2 - Text Document Vectorization
IST 736 - Text Mining
Spring 2023'''

#import CountVectorizer and TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer

corpus = '''
    The Knicks are a very very good basketball team. The Celtics are rivals of the knicks. Basketball is a game and a sport. The Knicks are from New York.
    Raptors are from Toronto which is in Ontario and the only NBA squad in Canada. I used to be good at basketball. Well not that good, but better than I am now.
    Right now it is the playoffs and the Knicks are facing Cleveland who are the Cavaliers and they used to have LeBron James a long time ago. Basketball is a good sport but most people like football more
    and they play less games in football. This is just another random sentence that is poorly written grammatically. Food is good to eat while watching the games.
    Chicken Wings are so good, they are sometimes sweet and spicy or both or only one. How many more sentences can I possibly come up with? Let\'s see!
    The Eagles are a very great and amazing football team in the NFL. They are super which is probably why they played in the Super Bowl this year.
    I had sweet honey chicken for dinner but I should\'ve had something better for me but the taste was worth it. Well that is all the thoughts I have on my mind right now. let\'s see how many sentences this was! 
    '''

#Get rid of newlines/returns/tabs and replace with single space
corpus = str(''.join([character for character in corpus if not character in ('\n','\r','\t')])).strip()

#split into sentences using periods, exlamation points, and question marks
docs = corpus.split('.')

docs = [doc.split('!') for doc in docs]
#make sure no list elements are embedded lists
docs = [doc for sublist in docs for doc in sublist][:-1]

docs = [doc.split('?') for doc in docs]
#make sure no list elements are embedded lists
docs = [doc for sublist in docs for doc in sublist]

#trim whitespace at beginning and end of sentences
docs = [' '.join(doc.strip().split()) for doc in docs]

#print the sentences
print()
print(len(docs), 'Documents:')
for doc in docs: print(doc)

#CountVectorizer Raw Documents
import pandas
cntvec = CountVectorizer()
cnt_raw = pandas.DataFrame(cntvec.fit_transform(docs).toarray(), columns = cntvec.get_feature_names_out())
print()
print('RAW DOCUMENTS COUNT VECTORS')
print(cnt_raw)

#CountVectorizer No Stopwords
cntvec_no_stop = CountVectorizer(stop_words = 'english')
cnt_no_stop = pandas.DataFrame(cntvec_no_stop.fit_transform(docs).toarray(), columns = cntvec_no_stop.get_feature_names_out())
print()
print('DOCUMENT COUNT VECTORS WITHOUT STOPWORDS')
print(cnt_no_stop)

#Filter to only words used multiple times in the corpus
filtered_columns = []
for column in list(cnt_no_stop.columns):
    if sum(cnt_no_stop[column]) > 1: filtered_columns.append(column)

cnt_no_stop_multi_corpus = cnt_no_stop[filtered_columns]
print()
print('DOCUMENT COUNT VECTORS WITHOUT STOPWORDS FOR WORDS USED MUTLIPLE TIMES IN THE CORPUS')
print(cnt_no_stop_multi_corpus)

#Generate word clouds
from wordcloud import WordCloud
from matplotlib import pyplot

#Subplots to put all word clouds in one figure
fig, plots = pyplot.subplots(2,3)
fig.suptitle('WORD CLOUDS')

#Raw Word Cloud
cnt_raw_string = [[word]*sum(cnt_raw[word]) for word in list(cnt_raw.columns)]
cnt_raw_string = ' '.join([word for sublist in cnt_raw_string for word in sublist])
plots[0,0].imshow(WordCloud(background_color= 'white').generate(cnt_raw_string))
plots[0,0].set_title('Raw Corpus')
plots[0,0].axis('off')

#No Stopwords Word Cloud
cnt_no_stop_string = [[word]*sum(cnt_no_stop[word]) for word in list(cnt_no_stop.columns)]
cnt_no_stop_string = ' '.join([word for sublist in cnt_no_stop_string for word in sublist])
plots[0,2].imshow(WordCloud(background_color= 'white').generate(cnt_no_stop_string))
plots[0,2].set_title('Corpus Without Stopwords')
plots[0,2].axis('off')

#No Stopwords and Multiple Times in the Corpus Word Cloud
cnt_no_stop_multi_corpus_string = [[word]*sum(cnt_no_stop_multi_corpus[word]) for word in list(cnt_no_stop_multi_corpus.columns)]
cnt_no_stop_multi_corpus_string = ' '.join([word for sublist in cnt_no_stop_multi_corpus_string for word in sublist])
plots[1,1].imshow(WordCloud(background_color= 'white').generate(cnt_no_stop_multi_corpus_string))
plots[1,1].set_title('Corpus Without Stopwords for Words Used Mutiple Times in the Corpus')
plots[1,1].axis('off')

plots[0,1].axis('off')
plots[1,0].axis('off')
plots[1,2].axis('off')

pyplot.show()