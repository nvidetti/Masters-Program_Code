#Homework 3 - IST 707 - Summer 2022
#Association Rule Mining
#setwd('C:/Users/nvidetti/Downloads')

#Read in data
data <- read.csv('bankdata_csv_all.csv')

#Structure of data
str(data)

#Create copy of data
ARMdata <- data 

#set index to id and remove id column
rownames(ARMdata) <- ARMdata$id
ARMdata <- ARMdata[colnames(ARMdata) != 'id']

#Discretize age
for(i in 1:nrow(ARMdata)){
  if(ARMdata$age[i] < 18){ARMdata$age_group[i] <- 'Minor'}
    if(ARMdata$age[i] >= 18 & ARMdata$age[i] <= 24){ARMdata$age_group[i] <- '18-24'}
    if(ARMdata$age[i] >= 25 & ARMdata$age[i] <= 39){ARMdata$age_group[i] <- '25-39'}
    if(ARMdata$age[i] >= 40 & ARMdata$age[i] <= 49){ARMdata$age_group[i] <- '40-49'}
    if(ARMdata$age[i] >= 50 & ARMdata$age[i] <= 59){ARMdata$age_group[i] <- '50-59'}
    if(ARMdata$age[i] >= 60 & ARMdata$age[i] <= 69){ARMdata$age_group[i] <- '60-69'}
    if(ARMdata$age[i] >= 70 & ARMdata$age[i] <= 79){ARMdata$age_group[i] <- '70-79'}
    if(ARMdata$age[i] >= 80){ARMdata$age_group[i] <- '80+'}}

#Make age_group a factor and remove age from ARMdata
ARMdata$age_group <- as.factor(ARMdata$age_group)
ARMdata <- ARMdata[colnames(ARMdata) != 'age']

#Make sex,region,married,children,car,save_act,current_act,mortgage, and pep factors
ARMdata$sex <- as.factor(ARMdata$sex)
ARMdata$region <- as.factor(ARMdata$region)
ARMdata$married <- as.factor(ARMdata$married)
ARMdata$children <- as.factor(ARMdata$children)
ARMdata$car <- as.factor(ARMdata$car)
ARMdata$save_act <- as.factor(ARMdata$save_act)
ARMdata$current_act <- as.factor(ARMdata$current_act)
ARMdata$mortgage <- as.factor(ARMdata$mortgage)
ARMdata$pep <- as.factor(ARMdata$pep)

#Discretize income

for(i in 1:nrow(ARMdata)){
  if(ARMdata$income[i] < 10000){ARMdata$income_group[i] <- '< $10,000'}
  if(ARMdata$income[i] >= 10000 & ARMdata$income[i] < 20000){ARMdata$income_group[i] <- '$10,000 - $20,000'}
  if(ARMdata$income[i] >= 20000 & ARMdata$income[i] < 30000){ARMdata$income_group[i] <- '$20,000 - $30,000'}
  if(ARMdata$income[i] >= 30000 & ARMdata$income[i] < 40000){ARMdata$income_group[i] <- '$30,000 - $40,000'}
  if(ARMdata$income[i] >= 40000 & ARMdata$income[i] < 50000){ARMdata$income_group[i] <- '$40,000 - $50,000'}
  if(ARMdata$income[i] >= 50000 & ARMdata$income[i] < 60000){ARMdata$income_group[i] <- '$50,000 - $60,000'}
  if(ARMdata$income[i] >= 60000 & ARMdata$income[i] < 70000){ARMdata$income_group[i] <- '$60,000 - $70,000'}
  if(ARMdata$income[i] >= 70000){ARMdata$income_group[i] <- '$70,000+'}}

#Make income_group a factor and remove income from ARMdata
ARMdata$income_group <- as.factor(ARMdata$income_group)
ARMdata <- ARMdata[colnames(ARMdata) != 'income']

#Structure of ARMdata
str(ARMdata)

library(arules)
library(arulesViz)

rules <- apriori(ARMdata)#, parameter = list(support = 0.3, confidence = 0.7, maxlen = 70))
sorted_rules <- sort(rules, by = 'lift',decreasing = TRUE)
rulelist <- inspect(sorted_rules)[inspect(sorted_rules)[,'lift'] > 1,]
rulelist <- inspect(sorted_rules)[inspect(sorted_rules)[,'rhs'] == '{pep=YES}',]
rulelist





