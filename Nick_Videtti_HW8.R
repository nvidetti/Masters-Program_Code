#READ IN AND CLEAN DATA
#setwd('C:/Users/nvidetti/Downloads/')
data <- read.csv('deception_data_converted_final.csv', col.names = c('lie','sentiment','review',4:24))
for(column in 4:ncol(data)){data[,3] <- paste(data[,3], data[,column])}
data <- data[,1:3]

#Make data a document term matrix
library(tm)
DTM <- data.frame(as.matrix(DocumentTermMatrix(Corpus(VectorSource(data[,3]))),
                               control = list(
                                 stopwords = TRUE,
                                 wordLengths=c(4, 10),
                                 removePunctuation = TRUE,
                                 removeNumbers = TRUE,
                                 tolower=TRUE,
                                 remove_separators = TRUE)))


data <- data.frame(data[,1:2],DTM)

#Make lie and sentiment factor variables
data$lie <- as.factor(data$lie)
data$sentiment <- as.factor(data$sentiment)
for(column in 1:ncol(data)){data[,column] <- as.factor(data[,column])}

#Create two separate data sets, truth and sentiment
truth <- data[,colnames(data) != 'sentiment']
sentiment <- data[,colnames(data) != 'lie']

#1) Run NB on the sentiment dataset (the one with only p and n labels. ) See how it does.
library(e1071)
library(caret)

#Create separate data frames for training and testing and leave labels out of testing set
set.seed(1)
trainrows <- sample(1:nrow(data), as.integer(nrow(data)*(2/3)), replace = FALSE)
sent_train <- sentiment[trainrows,]
sent_test <- data.frame(sentiment[-trainrows,colnames(sentiment) != 'sentiment'])
sent_test_sentiment <- sentiment[-trainrows,'sentiment']

#Naive Bayes with Prediction and Comparison to actual labels
set.seed(1)
nb <- naiveBayes(sent_train, sent_train$sentiment, laplace = 1)
nbpred <- confusionMatrix(predict(nb, sent_test), sent_test_sentiment)

#Show confusion matrix and accuracy
nbpred$table
nbpred$overall['Accuracy']



#2) Run SVMs on the sentiment dataset (the one with only p and n labels. ) See how it does.
#SVM Time!
#SVM w/ linear kernel
#cost = 0.1
SVM_linear_cost_0.1 <- svm(sentiment~., data = sent_train, kernel = 'linear', cost = 0.1, scale = FALSE)
#cost = 1
SVM_linear_cost_1 <- svm(sentiment~., data = sent_train, kernel = 'linear', cost = 1, scale = FALSE)
#cost = 10
SVM_linear_cost_10 <- svm(sentiment~., data = sent_train, kernel = 'linear', cost = 10, scale = FALSE)

#SVM w/ polynmial kernel
#cost = 0.1
SVM_polynomial_cost_0.1 <- svm(sentiment~., data = sent_train, kernel = 'polynomial', cost = 0.1, scale = FALSE)
#cost = 1
SVM_polynomial_cost_1 <- svm(sentiment~., data = sent_train, kernel = 'polynomial', cost = 1, scale = FALSE)
#cost = 10
SVM_polynomial_cost_10 <- svm(sentiment~., data = sent_train, kernel = 'polynomial', cost = 10, scale = FALSE)

#SVM w/ radial kernel
#cost = 0.1
SVM_radial_cost_0.1 <- svm(sentiment~., data = sent_train, kernel = 'radial', cost = 0.1, scale = FALSE)
#cost = 1
SVM_radial_cost_1 <- svm(sentiment~., data = sent_train, kernel = 'radial', cost = 1, scale = FALSE)
#cost = 10
SVM_radial_cost_10 <- svm(sentiment~., data = sent_train, kernel = 'radial', cost = 10, scale = FALSE)

#SVM w/ sigmoid kernel
#cost = 0.1
SVM_sigmoid_cost_0.1 <- svm(sentiment~., data = sent_train, kernel = 'sigmoid', cost = 0.1, scale = FALSE)
#cost = 1
SVM_sigmoid_cost_1 <- svm(sentiment~., data = sent_train, kernel = 'sigmoid', cost = 1, scale = FALSE)
#cost = 10
SVM_sigmoid_cost_10 <- svm(sentiment~., data = sent_train, kernel = 'sigmoid', cost = 10, scale = FALSE)

#Create data frame of predictions
SVM_Predictions <- data.frame(
  c(predict(SVM_linear_cost_0.1, sent_test, type = 'class')),
  c(predict(SVM_linear_cost_1, sent_test, type = 'class')),
  c(predict(SVM_linear_cost_10, sent_test, type = 'class')),
  c(predict(SVM_polynomial_cost_0.1, sent_test, type = 'class')),
  c(predict(SVM_polynomial_cost_1, sent_test, type = 'class')),
  c(predict(SVM_polynomial_cost_10, sent_test, type = 'class')),
  c(predict(SVM_radial_cost_0.1, sent_test, type = 'class')),
  c(predict(SVM_radial_cost_1, sent_test, type = 'class')),
  c(predict(SVM_radial_cost_10, sent_test, type = 'class')),
  c(predict(SVM_sigmoid_cost_0.1, sent_test, type = 'class')),
  c(predict(SVM_sigmoid_cost_1, sent_test, type = 'class')),
  c(predict(SVM_sigmoid_cost_10, sent_test, type = 'class')),
  c(sent_test_sentiment))
colnames(SVM_Predictions) <- c('linear_0.1', 'linear_1', 'linear_10',
                               'polynomial_0.1', 'polynomial_1', 'polynomial_10',
                               'radial_0.1', 'radial_1', 'radial_10',
                               'sigmoid_0.1', 'sigmoid_1', 'sigmoid_10', 'ACTUAL')

#Create data frame to show each model's accuracy based on SVM_Predictions and actual sentiment
SVM_Accuracy <- data.frame(c('linear_0.1', 'linear_1', 'linear_10',
                             'polynomial_0.1', 'polynomial_1', 'polynomial_10',
                             'radial_0.1', 'radial_1', 'radial_10',
                             'sigmoid_0.1', 'sigmoid_1', 'sigmoid_10'),
                           c(sum(as.integer(SVM_Predictions$linear_0.1) == as.integer(SVM_Predictions$ACTUAL)) / nrow(SVM_Predictions),
                             sum(as.integer(SVM_Predictions$linear_1) == as.integer(SVM_Predictions$ACTUAL)) / nrow(SVM_Predictions),
                             sum(as.integer(SVM_Predictions$linear_10) == as.integer(SVM_Predictions$ACTUAL)) / nrow(SVM_Predictions),
                             sum(as.integer(SVM_Predictions$polynomial_0.1) == as.integer(SVM_Predictions$ACTUAL)) / nrow(SVM_Predictions),
                             sum(as.integer(SVM_Predictions$polynomial_1) == as.integer(SVM_Predictions$ACTUAL)) / nrow(SVM_Predictions),
                             sum(as.integer(SVM_Predictions$polynomial_10) == as.integer(SVM_Predictions$ACTUAL)) / nrow(SVM_Predictions),
                             sum(as.integer(SVM_Predictions$radial_0.1) == as.integer(SVM_Predictions$ACTUAL)) / nrow(SVM_Predictions),
                             sum(as.integer(SVM_Predictions$radial_1) == as.integer(SVM_Predictions$ACTUAL)) / nrow(SVM_Predictions),
                             sum(as.integer(SVM_Predictions$radial_10) == as.integer(SVM_Predictions$ACTUAL)) / nrow(SVM_Predictions),
                             sum(as.integer(SVM_Predictions$sigmoid_0.1) == as.integer(SVM_Predictions$ACTUAL)) / nrow(SVM_Predictions),
                             sum(as.integer(SVM_Predictions$sigmoid_1) == as.integer(SVM_Predictions$ACTUAL)) / nrow(SVM_Predictions),
                             sum(as.integer(SVM_Predictions$sigmoid_10) == as.integer(SVM_Predictions$ACTUAL)) / nrow(SVM_Predictions)))

colnames(SVM_Accuracy) <- c('Model','Accuracy')
SVM_Accuracy <- data.frame(SVM_Accuracy[order(-SVM_Accuracy$Accuracy),])

#Finally, look at the accuracy of all models
SVM_Accuracy



#REPEAT WITH truth
#Create separate data frames for training and testing and leave labels out of testing set
set.seed(1)
trainrows <- sample(1:nrow(data), as.integer(nrow(data)*(2/3)), replace = FALSE)
truth_train <- truth[trainrows,]
truth_test <- data.frame(truth[-trainrows,colnames(truth) != 'lie'])
truth_test_truth <- truth[-trainrows,'lie']

#Naive Bayes with Prediction and Comparison to actual labels
set.seed(1)
nb <- naiveBayes(truth_train, truth_train$lie, laplace = 1)
nbpred <- confusionMatrix(predict(nb, truth_test), truth_test_truth)

#Show confusion matrix and accuracy
nbpred$table
nbpred$overall['Accuracy']



#2) Run SVMs on the truth dataset (the one with only p and n labels. ) See how it does.
#SVM Time!
#SVM w/ linear kernel
#cost = 0.1
SVM_linear_cost_0.1 <- svm(lie~., data = truth_train, kernel = 'linear', cost = 0.1, scale = FALSE)
#cost = 1
SVM_linear_cost_1 <- svm(lie~., data = truth_train, kernel = 'linear', cost = 1, scale = FALSE)
#cost = 10
SVM_linear_cost_10 <- svm(lie~., data = truth_train, kernel = 'linear', cost = 10, scale = FALSE)

#SVM w/ polynmial kernel
#cost = 0.1
SVM_polynomial_cost_0.1 <- svm(lie~., data = truth_train, kernel = 'polynomial', cost = 0.1, scale = FALSE)
#cost = 1
SVM_polynomial_cost_1 <- svm(lie~., data = truth_train, kernel = 'polynomial', cost = 1, scale = FALSE)
#cost = 10
SVM_polynomial_cost_10 <- svm(lie~., data = truth_train, kernel = 'polynomial', cost = 10, scale = FALSE)

#SVM w/ radial kernel
#cost = 0.1
SVM_radial_cost_0.1 <- svm(lie~., data = truth_train, kernel = 'radial', cost = 0.1, scale = FALSE)
#cost = 1
SVM_radial_cost_1 <- svm(lie~., data = truth_train, kernel = 'radial', cost = 1, scale = FALSE)
#cost = 10
SVM_radial_cost_10 <- svm(lie~., data = truth_train, kernel = 'radial', cost = 10, scale = FALSE)

#SVM w/ sigmoid kernel
#cost = 0.1
SVM_sigmoid_cost_0.1 <- svm(lie~., data = truth_train, kernel = 'sigmoid', cost = 0.1, scale = FALSE)
#cost = 1
SVM_sigmoid_cost_1 <- svm(lie~., data = truth_train, kernel = 'sigmoid', cost = 1, scale = FALSE)
#cost = 10
SVM_sigmoid_cost_10 <- svm(lie~., data = truth_train, kernel = 'sigmoid', cost = 10, scale = FALSE)

#Create data frame of predictions
SVM_Predictions <- data.frame(
  c(predict(SVM_linear_cost_0.1, truth_test, type = 'class')),
  c(predict(SVM_linear_cost_1, truth_test, type = 'class')),
  c(predict(SVM_linear_cost_10, truth_test, type = 'class')),
  c(predict(SVM_polynomial_cost_0.1, truth_test, type = 'class')),
  c(predict(SVM_polynomial_cost_1, truth_test, type = 'class')),
  c(predict(SVM_polynomial_cost_10, truth_test, type = 'class')),
  c(predict(SVM_radial_cost_0.1, truth_test, type = 'class')),
  c(predict(SVM_radial_cost_1, truth_test, type = 'class')),
  c(predict(SVM_radial_cost_10, truth_test, type = 'class')),
  c(predict(SVM_sigmoid_cost_0.1, truth_test, type = 'class')),
  c(predict(SVM_sigmoid_cost_1, truth_test, type = 'class')),
  c(predict(SVM_sigmoid_cost_10, truth_test, type = 'class')),
  c(truth_test_truth))
colnames(SVM_Predictions) <- c('linear_0.1', 'linear_1', 'linear_10',
                               'polynomial_0.1', 'polynomial_1', 'polynomial_10',
                               'radial_0.1', 'radial_1', 'radial_10',
                               'sigmoid_0.1', 'sigmoid_1', 'sigmoid_10', 'ACTUAL')

#Create data frame to show each model's accuracy based on SVM_Predictions and actual truth
SVM_Accuracy <- data.frame(c('linear_0.1', 'linear_1', 'linear_10',
                             'polynomial_0.1', 'polynomial_1', 'polynomial_10',
                             'radial_0.1', 'radial_1', 'radial_10',
                             'sigmoid_0.1', 'sigmoid_1', 'sigmoid_10'),
                           c(sum(as.integer(SVM_Predictions$linear_0.1) == as.integer(SVM_Predictions$ACTUAL)) / nrow(SVM_Predictions),
                             sum(as.integer(SVM_Predictions$linear_1) == as.integer(SVM_Predictions$ACTUAL)) / nrow(SVM_Predictions),
                             sum(as.integer(SVM_Predictions$linear_10) == as.integer(SVM_Predictions$ACTUAL)) / nrow(SVM_Predictions),
                             sum(as.integer(SVM_Predictions$polynomial_0.1) == as.integer(SVM_Predictions$ACTUAL)) / nrow(SVM_Predictions),
                             sum(as.integer(SVM_Predictions$polynomial_1) == as.integer(SVM_Predictions$ACTUAL)) / nrow(SVM_Predictions),
                             sum(as.integer(SVM_Predictions$polynomial_10) == as.integer(SVM_Predictions$ACTUAL)) / nrow(SVM_Predictions),
                             sum(as.integer(SVM_Predictions$radial_0.1) == as.integer(SVM_Predictions$ACTUAL)) / nrow(SVM_Predictions),
                             sum(as.integer(SVM_Predictions$radial_1) == as.integer(SVM_Predictions$ACTUAL)) / nrow(SVM_Predictions),
                             sum(as.integer(SVM_Predictions$radial_10) == as.integer(SVM_Predictions$ACTUAL)) / nrow(SVM_Predictions),
                             sum(as.integer(SVM_Predictions$sigmoid_0.1) == as.integer(SVM_Predictions$ACTUAL)) / nrow(SVM_Predictions),
                             sum(as.integer(SVM_Predictions$sigmoid_1) == as.integer(SVM_Predictions$ACTUAL)) / nrow(SVM_Predictions),
                             sum(as.integer(SVM_Predictions$sigmoid_10) == as.integer(SVM_Predictions$ACTUAL)) / nrow(SVM_Predictions)))

colnames(SVM_Accuracy) <- c('Model','Accuracy')
SVM_Accuracy <- data.frame(SVM_Accuracy[order(-SVM_Accuracy$Accuracy),])

#Finally, look at the accuracy of all models
SVM_Accuracy