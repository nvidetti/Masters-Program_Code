data <- read.csv('C:/Users/nvidetti/Downloads/schoolvax.csv')
#Question 1
for (i in 1:nrow(data)){
  if(data$pubpriv[i] == 'PUBLIC'){data$public_dummy[i] <- 1} else if(data$pubpriv[i] == 'PRIVATE'){data$public_dummy[i] <- 0}}
for (i in 1:nrow(data)){
  if(data$religious[i] > 0){data$relig_exempt[i] <- 1} else{data$relig_exempt[i] <- 0}}

#Question 2
for (i in 1:ncol(data))
{if (class(data[,i]) == 'numeric') {print(c(colnames(data[i]),mean(data[,i])))}}

#Question 3
Question3 <- lm(medical ~ pubpriv + enrollment, data = data)
summary(Question3)

#Question 5
Question5 <- glm(relig_exempt ~ public_dummy + enrollment, data = data, family = 'binomial')
summary(Question5)

#Question6
exp(coef(Question5))