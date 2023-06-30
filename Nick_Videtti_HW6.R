library(e1071)
library(caret)
library(rpart)
library(rattle)

#setwd("C:/Users/nvidetti/Downloads")

mnist_train <- read.csv('mnist_train.csv')
mnist_test <- read.csv('mnist_test.csv')

#Make label factors
mnist_train$label <- as.factor(mnist_train$label)
mnist_test$label <- as.factor(mnist_test$label)

#Create separate data frames for Naive Bayes
nb_train <- mnist_train
nb_test <- mnist_test

#Make rest of variables factors for Naive Bayes
for(column in colnames(nb_train)){nb_train[,column] <- as.factor(mnist_train[,column])}
for(column in colnames(nb_train)){nb_test[,column] <- as.factor(mnist_test[,column])}

#Remove label from testing data
nb_test <- nb_test[,colnames(nb_test) != 'label']

#Naive Bayes
set.seed(1)
nb <- naiveBayes(nb_train, nb_train$label, laplace = 1)

#Naive Bayes Prediction and Comparison to actual labels
nb_prediction <- predict(nb, nb_test)

nb_accuracy <- confusionMatrix(nb_prediction, mnist_test$label)$overall['Accuracy']

#Create separate data frames for decision trees
dt_train <- mnist_train
dt_test <- mnist_test

#Remove label from testing data
dt_test <- dt_test[,colnames(dt_test) != 'label']

#Decision Tree
set.seed(1)
dt <- rpart(label~.,dt_train)
fancyRpartPlot(dt)

#Decision Tree Prediction and Comparison
dt_prediction <- data.frame(predict(dt, dt_test, type = 'class'))

#Calculate Accuracy for Decision Tree
comparison <- data.frame(dt_prediction,mnist_test$label)
colnames(comparison) <- c('prediction','actual')
dt_accuracy <- sum(comparison$prediction == comparison$actual)/nrow(comparison)

#Compare models
Accuracy <- data.frame(nb_accuracy,dt_accuracy)
colnames(Accuracy) = c('Naive Bayes Accuracy', 'Decision Tree Accuracy')
Accuracy