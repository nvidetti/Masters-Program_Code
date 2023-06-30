course_progress <- function(Total_Lessons, Semester_Progress, Progress)
  {On_Time <<- ceiling(Total_Lessons*Semester_Progress)
  
  #Very Ahead is more than 5 lessons ahead, but not completed
  Very_Ahead <<- c((On_Time + 6) : (Total_Lessons - 1))
  
  #Middling is 0 to 5 lessons ahead
  Middling <<- c(On_Time : (On_Time + 5))
                
  #Behind is 1 to 5 lessons behind
  Behind <<- c((On_Time - 5) : (On_Time - 1))
  
  #More Behind is 6 to 10 lessons behind
  More_Behind <<- c((On_Time - 10) : (On_Time - 6))
  
  #Very Behind is more than 10 lessons behind
  Very_Behind <<- c(0 : (On_Time - 11))
  
  #Completed is finished with course
  Completed <<- as.vector(Total_Lessons)}

course_progress(35,3/4)

On_Time
Very_Behind
More_Behind
Behind
Middling
Very_Ahead
Completed

#setwd('C:/Users/nvidetti/Downloads')
data <- read.csv('data-storyteller.csv')
names(data)
names(data)[3:ncol(data)] <- c('Very Ahead','Middling','Behind','More Behind','Very Behind','Completed')
data

# lessons <- as.integer(rnorm(5,mean = On_Time, sd = 5))
# 
# status <- c(0)
# for(i in 1:length(lessons))
#     {if(lessons[i] %in% Completed){status <- c(status,'Completed')}
#     else if(lessons[i] %in% Very_Ahead){status <- c(status,'Very Ahead')}
#     else if(lessons[i] %in% Middling){status <- c(status,'Middling')}
#     else if(lessons[i] %in% Behind){status <- c(status,'Behind')}
#     else if(lessons[i] %in% More_Behind){status <- c(status,'More Behind')} 
#     else if(lessons[i] %in% Very_Behind){status <- c(status,'Very Behind')}}
# status <- status[2:length(status)]
# 
# school <- c('A','B','C','D','E')
# 
# progress_data <- data.frame(school,lessons,status)
# progress_data

schools <- data.frame(
             aggregate(data$Section,list(data$School),length),
             aggregate(data$`Very Ahead`,list(data$School),sum),
             aggregate(data$`Middling`,list(data$School),sum),
             aggregate(data$`Behind`,list(data$School),sum),
             aggregate(data$`More Behind`,list(data$School),sum),
             aggregate(data$`Very Behind`,list(data$School),sum),
             aggregate(data$Completed,list(data$School),sum))
schools <- schools[,c(1,2,4,6,8,10,12,14)]
names(schools) <- names(data)
names(schools)[2] <- 'Sections'
schools$`Total Students` <- schools$`Very Ahead` + schools$Middling + schools$Behind + schools$`More Behind` + schools$`Very Behind` + schools$Completed
schools

schools_prop <- schools
for (school in 1:nrow(schools_prop)){
  for (column in 3:ncol(schools_prop)){
    schools_prop[school,column] <- (100*schools_prop[school,column]) / schools_prop[school,ncol(schools_prop)]}}
schools_prop
             

library(tidyverse)

Very_Behind_Graph <- ggplot(schools_prop,aes(School,`Very Behind`)) + ggtitle('Percentage of Students Very Behind') + stat_identity(geom = 'bar') + aes(fill = School) + geom_text(size = 8, vjust = 1.5, aes(label = gsub(' ','',paste(as.integer(`Very Behind`),'%')))) + ylab('% Very Behind')
Very_Behind_Graph

More_Behind_Graph <- ggplot(schools_prop,aes(School,`More Behind`)) + ggtitle('Percentage of Students More Behind') + stat_identity(geom = 'bar') + aes(fill = School) + geom_text(size = 8, vjust = 1.5, aes(label = gsub(' ','',paste(as.integer(`More Behind`),'%')))) + ylab('% More Behind')
More_Behind_Graph

Behind_Graph <- ggplot(schools_prop,aes(School,Behind)) + ggtitle('Percentage of Students Behind') + stat_identity(geom = 'bar') + aes(fill = School) + geom_text(size = 8, vjust = 1.5, aes(label = gsub(' ','',paste(as.integer(Behind),'%')))) + ylab('% Behind')
Behind_Graph

Middling_Graph <- ggplot(schools_prop,aes(School,Middling)) + ggtitle('Percentage of Students Middling') + stat_identity(geom = 'bar') + aes(fill = School) + geom_text(size = 8, vjust = 1.5, aes(label = gsub(' ','',paste(as.integer(Middling),'%')))) + ylab('% Middling')
Middling_Graph

Very_Ahead_Graph <- ggplot(schools_prop,aes(School,`Very Ahead`)) + ggtitle('Percentage of Students Very Ahead') + stat_identity(geom = 'bar') + aes(fill = School) + geom_text(size = 8, vjust = 1.5, aes(label = gsub(' ','',paste(as.integer(`Very Ahead`),'%')))) + ylab('% Very Ahead')
Very_Ahead_Graph

Completed_Graph <- ggplot(schools_prop,aes(School,Completed)) + ggtitle('Percentage of Students Completed') + stat_identity(geom = 'bar') + aes(fill = School) + geom_text(size = 8, vjust = 1.5, aes(label = gsub(' ','',paste(as.integer(Completed),'%')))) + ylab('% Completed')
Completed_Graph

schools_ranks <- schools_prop
for (column in 3:ncol(schools_ranks) -1 ){as.integer(
      if (names(schools_ranks)[column] %in% c('Very Behind','More Behind','Behind')) {schools_ranks[,column] <- rank(schools_ranks[,column],ties.method = 'max')}
      else if (names(schools_ranks)[column] %in% c('Middling','Very Ahead','Completed')) {schools_ranks[,column] <- rank(-schools_ranks[,column],ties.method = 'max')})}
names(schools_ranks)[3:(ncol(schools_ranks)- 1)] <- gsub(' ','',paste(names(schools_ranks)[3:(ncol(schools_ranks) -1)], 'RANK'))

schools_ranks$RankAnalysis <- schools_ranks$VeryAheadRANK + schools_ranks$MiddlingRANK + schools_ranks$BehindRANK + schools_ranks$MoreBehindRANK + schools_ranks$VeryBehindRANK + schools_ranks$CompletedRANK

schools_ranks

Rank_Analysis_Graph <- ggplot(schools_ranks,aes(School,RankAnalysis)) + ggtitle('School Rank Analysis (Lower Number is Better)') + stat_identity(geom = 'bar') + aes(fill = School) + geom_text(size = 8, vjust = 1.5, aes(label = RankAnalysis)) + ylab('')
Rank_Analysis_Graph
