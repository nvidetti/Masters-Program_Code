#Read in fedPapers85.csv
#setwd('C:/Users/nvidetti/Downloads')
papers_csv <- read.csv('fedPapers85.csv')

#Create copy of data set and look at data types
papers <- papers_csv
str(papers)

#Replace period in column names
colnames(papers) <- gsub('[.]','',colnames(papers))

#Discretize every column (except author and filename) to 0 or 1
for(column in colnames(papers)[3:length(papers)]){
  for(row in rownames(papers)){if(papers[row,column] == 0){papers[row,column] <- 0} else{papers[row,column] <- 1}}}

#Check results
str(papers)

#Create training data set using only Hamilton, Madison, and create testing data set using only dispt
papers_train <- papers[papers$author %in% c('Hamilton','Madison'), colnames(papers) != 'filename']
rownames(papers_train) <- c(1:length(rownames(papers_train)))
papers_test <- papers[papers$author == 'dispt', colnames(papers) != 'author']
rownames(papers_test) <- papers_test$filename
papers_test <- papers_test[,colnames(papers_test) != 'filename']

#Look at the results
papers_train[1:10,1:10]
papers_test[1:10,1:10]

#Make all variables factors
for(column in colnames(papers_train)){papers_train[,column] <- as.factor(papers_train[,column])}
for(column in colnames(papers_test)){papers_test[,column] <- as.factor(papers_test[,column])}


#Decision Tree Time!! Library necessary packages
library(rpart)
library(rattle)

#Create decision tree
set.seed(1)
Papers_Tree <- rpart(author~.,papers_train)
fancyRpartPlot(Papers_Tree)

#Predict disputed papers with decision tree
set.seed(1)
Disputed <- data.frame(predict(Papers_Tree, papers_test, type = 'class'))
colnames(Disputed) <- 'Predicted Author'
View(Disputed)