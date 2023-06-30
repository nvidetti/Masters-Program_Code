print('''
Nick Videtti
nvidetti@syr.edu
IST 736 - Text Mining
Spring 2023
Homework 1 - Sentiment Analysis Classification Tools
''')

#Imports
import nltk
import pandas
from nltk.sentiment import SentimentAnalyzer
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

#Create lists and integers for compared and average accuracies
NLTK_list = []
VADER_list = []
NLTK_win = 0
VADER_win = 0

#Create loop variable
i = 0

#Put tests in a loop to repeat 5 times
while i < 10:
    #Get data set of tweet examples for setiment analysis
    pos_list = nltk.corpus.twitter_samples.strings('positive_tweets.json')
    neg_list = nltk.corpus.twitter_samples.strings('negative_tweets.json')
    tweet_list = pos_list + neg_list
    pos_tup = [(poslistitem, 'pos') for poslistitem in pos_list]
    neg_tup = [(neglistitem, 'neg') for neglistitem in neg_list]
    pos_neg = pos_tup + neg_tup
    #Store tweet and "true" sentiment in a pandas DataFrame
    tweets = pandas.DataFrame(data = pos_neg, columns = ['Tweet', 'Sentiment'])
    #Shuffle up DataFrame and rests indices.
    tweets = tweets.sample(frac = 1).reset_index().drop(columns = 'index')


    #NLTK Sentiment Analyzer
    tweets['Features'] = [({'Tweet': tweets['Tweet'][row]}, tweets['Sentiment'][row]) for row in range(len(tweets.index))]
    NLTK_analyzer = SentimentAnalyzer()
    NLTK_analyzer.train(nltk.classify.NaiveBayesClassifier.train, tweets['Features'][ : int(len(tweets['Features'])*0.8)])
    NLTK_accuracy = NLTK_analyzer.evaluate(tweets['Features'][int(len(tweets['Features'])*0.8) : ])


    #VADER Sentiment Intensity Analyzer
    VADER_analyzer = SentimentIntensityAnalyzer()
    #Compound Scores and Sentiment
    tweets['VADER Compound Score'] = [VADER_analyzer.polarity_scores(tweets['Tweet'][row])['compound'] for row in range(len(tweets.index))]
    tweets['VADER Sentiment'] = ['pos' if row > 0.5 else 'neg' if row < -0.5 else 'neutral' for row in tweets['VADER Compound Score']]
    if i == 0: print('First Example of "tweets" DataFrame\n', tweets)
    #VADER Sentiment Accuracy
    VADER_accuracy = sum([1 if tweets['VADER Sentiment'][row] == tweets['Sentiment'][row] else 0 for row in range(len(tweets.index))]) / len(tweets.index)

    #Compare NLTK and VADER
    print('NLTK Model:', NLTK_accuracy)
    print('NLTK Accuracy:', NLTK_accuracy['Accuracy']*100, '%')
    print('VADER Accuracy:', VADER_accuracy*100, '%')
    if NLTK_accuracy['Accuracy'] > VADER_accuracy: print('NLTK was more accurate!'); NLTK_win += 1
    elif NLTK_accuracy['Accuracy'] < VADER_accuracy: print('VADER was more accurate!'); VADER_win += 1
    elif NLTK_accuracy['Accuracy'] == VADER_accuracy: print('Both NLTK and VADER were equally accurate!')

    #Append to lists
    NLTK_list.append(NLTK_accuracy['Accuracy'])
    VADER_list.append(VADER_accuracy)

    #Increment loop variable
    i += 1
    print('\n\n')

#Final Summary
print('FINAL SUMMARY:')
print('NLTK was more accurate', NLTK_win, '/ 10 times')
print('VADER was more accurate', VADER_win, '/ 10 times')
print('\nAverage Accuracies: NLTK -', round(sum(NLTK_list) / len(NLTK_list)*100, 2), '% ', 'VADER -', round(sum(VADER_list) / len(VADER_list)*100, 2), '%')
if sum(NLTK_list) > sum(VADER_list): print('NLTK was better on average!')
elif sum(NLTK_list) < sum(VADER_list): print('VADER was better on average!')
elif sum(NLTK_list) == sum(VADER_list): print('NLTK and VADER were equally accurate on average!')

#End
print('\n\nEnd of Homework 1.')