#setwd('C:/Users/nvidetti/Downloads/')

library(e1071)

#Read in main training an testing sets, and testing labels
mnist_train <- read.csv('mnist_train.csv')[1:1000,]
mnist_test <- read.csv('mnist_test.csv')
actual_labels <- mnist_test$label

#Remove label from testing data
mnist_test <- mnist_test[,colnames(mnist_test) != 'label']

#Make label factors
mnist_train$label <- as.factor(mnist_train$label)
actual_labels <- as.factor(actual_labels)

#SVM Time!
#SVM w/ linear kernel
#cost = 0.1
SVM_linear_cost_0.1 <- svm(label~., data = mnist_train, kernel = 'linear', cost = 0.1, scale = FALSE)
#cost = 1
SVM_linear_cost_1 <- svm(label~., data = mnist_train, kernel = 'linear', cost = 1, scale = FALSE)
#cost = 10
SVM_linear_cost_10 <- svm(label~., data = mnist_train, kernel = 'linear', cost = 10, scale = FALSE)
#tuned cost
SVM_linear_cost_tuned <- svm(label~., data = mnist_train, kernel = 'linear', scale = FALSE,
                             cost = tune(svm, label~., data = mnist_train, kernel = 'linear', scale = FALSE, 
                                         ranges = list(cost = c(0.001,0.01,0.1,1,10,100,1000)))$best.parameters[1,1])

#SVM w/ polynmial kernel
#cost = 0.1
SVM_polynomial_cost_0.1 <- svm(label~., data = mnist_train, kernel = 'polynomial', cost = 0.1, scale = FALSE)
#cost = 1
SVM_polynomial_cost_1 <- svm(label~., data = mnist_train, kernel = 'polynomial', cost = 1, scale = FALSE)
#cost = 10
SVM_polynomial_cost_10 <- svm(label~., data = mnist_train, kernel = 'polynomial', cost = 10, scale = FALSE)
#tuned cost
SVM_polynomial_cost_tuned <- svm(label~., data = mnist_train, scale = FALSE, kernel = 'polynomial',
                                 cost = tune(svm, label~., data = mnist_train, kernel = 'polynomial', scale = FALSE, 
                                             ranges = list(cost = c(0.001,0.01,0.1,1,10,100,1000)))$best.parameters[1,1])

#SVM w/ radial kernel
#cost = 0.1
SVM_radial_cost_0.1 <- svm(label~., data = mnist_train, kernel = 'radial', cost = 0.1, scale = FALSE)
#cost = 1
SVM_radial_cost_1 <- svm(label~., data = mnist_train, kernel = 'radial', cost = 1, scale = FALSE)
#cost = 10
SVM_radial_cost_10 <- svm(label~., data = mnist_train, kernel = 'radial', cost = 10, scale = FALSE)
#tuned cost
SVM_radial_cost_tuned <- svm(label~., data = mnist_train, scale = FALSE, kernel = 'radial',
                             cost = tune(svm, label~., data = mnist_train, kernel = 'radial', scale = FALSE, 
                                         ranges = list(cost = c(0.001,0.01,0.1,1,10,100,1000)))$best.parameters[1,1])

#SVM w/ sigmoid kernel
#cost = 0.1
SVM_sigmoid_cost_0.1 <- svm(label~., data = mnist_train, kernel = 'sigmoid', cost = 0.1, scale = FALSE)
#cost = 1
SVM_sigmoid_cost_1 <- svm(label~., data = mnist_train, kernel = 'sigmoid', cost = 1, scale = FALSE)
#cost = 10
SVM_sigmoid_cost_10 <- svm(label~., data = mnist_train, kernel = 'sigmoid', cost = 10, scale = FALSE)
#tuned cost
SVM_sigmoid_cost_tuned <- svm(label~., data = mnist_train, scale = FALSE, kernel = 'sigmoid',
                              cost = tune(svm, label~., data = mnist_train, kernel = 'sigmoid', scale = FALSE, 
                                          ranges = list(cost = c(0.001,0.01,0.1,1,10,100,1000)))$best.parameters[1,1])

#Create data frame of predictions
SVM_Predictions <- data.frame(
  c(predict(SVM_linear_cost_0.1, mnist_test, type = 'class')),
  c(predict(SVM_linear_cost_1, mnist_test, type = 'class')),
  c(predict(SVM_linear_cost_10, mnist_test, type = 'class')),
  c(predict(SVM_linear_cost_tuned, mnist_test, type = 'class')),
  c(predict(SVM_polynomial_cost_0.1, mnist_test, type = 'class')),
  c(predict(SVM_polynomial_cost_1, mnist_test, type = 'class')),
  c(predict(SVM_polynomial_cost_10, mnist_test, type = 'class')),
  c(predict(SVM_polynomial_cost_tuned, mnist_test, type = 'class')),
  c(predict(SVM_radial_cost_0.1, mnist_test, type = 'class')),
  c(predict(SVM_radial_cost_1, mnist_test, type = 'class')),
  c(predict(SVM_radial_cost_10, mnist_test, type = 'class')),
  c(predict(SVM_radial_cost_tuned, mnist_test, type = 'class')),
  c(predict(SVM_sigmoid_cost_0.1, mnist_test, type = 'class')),
  c(predict(SVM_sigmoid_cost_1, mnist_test, type = 'class')),
  c(predict(SVM_sigmoid_cost_10, mnist_test, type = 'class')),
  c(predict(SVM_sigmoid_cost_tuned, mnist_test, type = 'class')),
  c(actual_labels))
colnames(SVM_Predictions) <- c('linear_0.1', 'linear_1', 'linear_10', 'linear_tuned',
                               'polynomial_0.1', 'polynomial_1', 'polynomial_10', 'polynomial_tuned',
                               'radial_0.1', 'radial_1', 'radial_10', 'radial_tuned',
                               'sigmoid_0.1', 'sigmoid_1', 'sigmoid_10', 'sigmoid_tuned', 'ACTUAL')

#Create data frame to show each model's accuracy based on SVM_Predictions and actual_labels
SVM_Accuracy <- data.frame(c('linear_0.1', 'linear_1', 'linear_10', 'linear_tuned',
                             'polynomial_0.1', 'polynomial_1', 'polynomial_10', 'polynomial_tuned',
                             'radial_0.1', 'radial_1', 'radial_10', 'radial_tuned',
                             'sigmoid_0.1', 'sigmoid_1', 'sigmoid_10', 'sigmoid_tuned'),
                           c(sum(as.integer(SVM_Predictions$linear_0.1) == as.integer(SVM_Predictions$ACTUAL)) / nrow(SVM_Predictions),
                             sum(as.integer(SVM_Predictions$linear_1) == as.integer(SVM_Predictions$ACTUAL)) / nrow(SVM_Predictions),
                             sum(as.integer(SVM_Predictions$linear_10) == as.integer(SVM_Predictions$ACTUAL)) / nrow(SVM_Predictions),
                             sum(as.integer(SVM_Predictions$linear_tuned) == as.integer(SVM_Predictions$ACTUAL)) / nrow(SVM_Predictions),
                             sum(as.integer(SVM_Predictions$polynomial_0.1) == as.integer(SVM_Predictions$ACTUAL)) / nrow(SVM_Predictions),
                             sum(as.integer(SVM_Predictions$polynomial_1) == as.integer(SVM_Predictions$ACTUAL)) / nrow(SVM_Predictions),
                             sum(as.integer(SVM_Predictions$polynomial_10) == as.integer(SVM_Predictions$ACTUAL)) / nrow(SVM_Predictions),
                             sum(as.integer(SVM_Predictions$polynomial_tuned) == as.integer(SVM_Predictions$ACTUAL)) / nrow(SVM_Predictions),
                             sum(as.integer(SVM_Predictions$radial_0.1) == as.integer(SVM_Predictions$ACTUAL)) / nrow(SVM_Predictions),
                             sum(as.integer(SVM_Predictions$radial_1) == as.integer(SVM_Predictions$ACTUAL)) / nrow(SVM_Predictions),
                             sum(as.integer(SVM_Predictions$radial_10) == as.integer(SVM_Predictions$ACTUAL)) / nrow(SVM_Predictions),
                             sum(as.integer(SVM_Predictions$radial_tuned) == as.integer(SVM_Predictions$ACTUAL)) / nrow(SVM_Predictions),
                             sum(as.integer(SVM_Predictions$sigmoid_0.1) == as.integer(SVM_Predictions$ACTUAL)) / nrow(SVM_Predictions),
                             sum(as.integer(SVM_Predictions$sigmoid_1) == as.integer(SVM_Predictions$ACTUAL)) / nrow(SVM_Predictions),
                             sum(as.integer(SVM_Predictions$sigmoid_10) == as.integer(SVM_Predictions$ACTUAL)) / nrow(SVM_Predictions),
                             sum(as.integer(SVM_Predictions$sigmoid_tuned) == as.integer(SVM_Predictions$ACTUAL)) / nrow(SVM_Predictions)))

colnames(SVM_Accuracy) <- c('Model','Accuracy')
SVM_Accuracy <- data.frame(SVM_Accuracy[order(-SVM_Accuracy$Accuracy),])

#Finally, look at the accuracy of all models
SVM_Accuracy