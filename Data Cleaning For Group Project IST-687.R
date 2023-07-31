Import = function(data){
CSV <- read.csv(data,header = FALSE)
Data <- CSV[-(1:21),-c(1,2,5,6,7,8,10)]
colnames(Data) <- CSV[21,-c(1,2,5,6,7,8,10)]
rownames(Data) <- rownames(CSV)[1:nrow(Data)]
colnames(Data)[6:15] <- CSV[19,13:22]
for (x in 6:17) {Data[,x] <- as.numeric(Data[,x])* (if (x >= 6 & x <= 15) 1000 else 1)}
Data[,"MedAge"] <- as.numeric(Data[,"MedAge"])
for (x in 1:nrow(Data)) {Data[x,"MedAge"] <- if (is.na(Data[x,"MedAge"])) 0 else Data[x,"MedAge"]}
for (x in 1:nrow(Data)) {Data[x,"DaysFixed"] <- paste(
    if (substr(Data[x,"Days"],1,1) == "M") "Mon",
    if (substr(Data[x,"Days"],2,2) == "T") "Tue",
    if (substr(Data[x,"Days"],3,3) == "W") "Wed",
    if (substr(Data[x,"Days"],4,4) == "T") "Thu",
    if (substr(Data[x,"Days"],5,5) == "F") "Fri",
    if (substr(Data[x,"Days"],6,6) == "S") "Sat",
    if (substr(Data[x,"Days"],7,7) == "S") "Sun")}
for (x in 1:nrow(Data)) {Data[x,"Days"] <- gsub(" ","",Data[x,"DaysFixed"])}
Data <- Data[,colnames(Data) != "DaysFixed"]
Data$Period <- gsub("!","",Data$Period)
Data$StartOfPeriod <- as.Date(substr(Data$Period,1,8),"%m/%d/%y")
Data$EndOfPeriod <- as.Date(substr(Data$Period,10,17),"%m/%d/%y")
Data$LengthOfPeriod <- Data$EndOfPeriod - Data$StartOfPeriod
colnames(Data)[colnames(Data) == "T/C"] <- "Times Aired"
colnames(Data)[colnames(Data) == "Duration"] <- "Minutes Aired"
colnames(Data)[colnames(Data) == "MedAge"] <- "Median Age"
colnames(Data)[colnames(Data) == "StartOfPeriod"] <- "Start Of Period"
colnames(Data)[colnames(Data) == "EndOfPeriod"] <- "End Of Period"
colnames(Data)[colnames(Data) == "LengthOfPeriod"] <- "Length Of Period"
for (x in 7:16) {
    if (substr(colnames(Data)[x],1,1) == "P") colnames(Data)[x] <- gsub("P","People",colnames(Data)[x])
    colnames(Data)[x] <- gsub("M","Men",colnames(Data)[x])
    colnames(Data)[x] <- gsub("W","Women",colnames(Data)[x])}
CSV <<- CSV
Data <<- Data}
Import("C:/Users/nvidetti/Downloads/2021 L3 PROGRAM RANKS.L3D.csv")


#What are the most popular and least popular awards shows for each demographic, as well as overall?

library(readxl)
AwardsShows <- read_excel("C:/Users/nvidetti/Downloads/Awards Shows.xlsx")[,3]

AwardsShows <- merge(AwardsShows,Data,by = "Program")

library(tidyverse)

ImpressionsByAwardShow <- as.data.frame(AwardsShows %>% group_by(Program) %>% summarize(`People 18-34` = sum(`P 18-34`), `Men 18-34` = sum(`Men 18-34`), `Women 18-34` = sum(`Women 18-34`), `People 18-49` = sum(`People 18-49`), `Men 18-49` = sum(`Men 18-49`), `Women 18-49` = sum(`Women 18-49`), `People 25-54` = sum(`People 25-54`), `Men 25-54` = sum(`Men 25-54`), `Women 25-54` = sum(`Women 25-54`), `People 2+` = sum(`People 2+`)))

Top_People_18_34 <- ImpressionsByAwardShow[ImpressionsByAwardShow$`People 18-34` == max(ImpressionsByAwardShow$`People 18-34`),1]
Top_Men_18_34 <- ImpressionsByAwardShow[ImpressionsByAwardShow$`Men 18-34` == max(ImpressionsByAwardShow$`Men 18-34`),1]
Top_Women_18_34 <- ImpressionsByAwardShow[ImpressionsByAwardShow$`Women 18-34` == max(ImpressionsByAwardShow$`Women 18-34`),1]
Top_People_18_49 <- ImpressionsByAwardShow[ImpressionsByAwardShow$`People 18-49` == max(ImpressionsByAwardShow$`People 18-49`),1]
Top_Men_18_49 <- ImpressionsByAwardShow[ImpressionsByAwardShow$`Men 18-49` == max(ImpressionsByAwardShow$`Men 18-49`),1]
Top_Women_18_49 <- ImpressionsByAwardShow[ImpressionsByAwardShow$`Women 18-49` == max(ImpressionsByAwardShow$`Women 18-49`),1]
Top_People_25_54 <- ImpressionsByAwardShow[ImpressionsByAwardShow$`People 25-54` == max(ImpressionsByAwardShow$`People 25-54`),1]
Top_Men_25_54 <- ImpressionsByAwardShow[ImpressionsByAwardShow$`Men 25-54` == max(ImpressionsByAwardShow$`Men 25-54`),1]
Top_Women_25_54 <- ImpressionsByAwardShow[ImpressionsByAwardShow$`Women 25-54` == max(ImpressionsByAwardShow$`Women 25-54`),1]
Top_People_2_Plus <- ImpressionsByAwardShow[ImpressionsByAwardShow$`People 2+` == max(ImpressionsByAwardShow$`People 2+`),1]

TopShows <- data.frame(c("People 18-34","Men 18-34","Women 18-34","People 18-49","Men 18-49","Women 18-49","People 25-54","Men 25-54","Women 25-54","People 2+"),c(Top_People_18_34,Top_Men_18_34,Top_Women_18_34,Top_People_18_49,Top_Men_18_49,Top_Women_18_49,Top_People_25_54,Top_Men_25_54,Top_Women_25_54,Top_People_2_Plus))
names(TopShows) <- c("Demographic","Awards Show")

Bottom_People_18_34 <- ImpressionsByAwardShow[ImpressionsByAwardShow$`People 18-34` == min(ImpressionsByAwardShow$`People 18-34`),1]
Bottom_Men_18_34 <- ImpressionsByAwardShow[ImpressionsByAwardShow$`Men 18-34` == min(ImpressionsByAwardShow$`Men 18-34`),1]
Bottom_Women_18_34 <- ImpressionsByAwardShow[ImpressionsByAwardShow$`Women 18-34` == min(ImpressionsByAwardShow$`Women 18-34`),1]
Bottom_People_18_49 <- ImpressionsByAwardShow[ImpressionsByAwardShow$`People 18-49` == min(ImpressionsByAwardShow$`People 18-49`),1]
Bottom_Men_18_49 <- ImpressionsByAwardShow[ImpressionsByAwardShow$`Men 18-49` == min(ImpressionsByAwardShow$`Men 18-49`),1]
Bottom_Women_18_49 <- ImpressionsByAwardShow[ImpressionsByAwardShow$`Women 18-49` == min(ImpressionsByAwardShow$`Women 18-49`),1]
Bottom_People_25_54 <- ImpressionsByAwardShow[ImpressionsByAwardShow$`People 25-54` == min(ImpressionsByAwardShow$`People 25-54`),1]
Bottom_Men_25_54 <- ImpressionsByAwardShow[ImpressionsByAwardShow$`Men 25-54` == min(ImpressionsByAwardShow$`Men 25-54`),1]
Bottom_Women_25_54 <- ImpressionsByAwardShow[ImpressionsByAwardShow$`Women 25-54` == min(ImpressionsByAwardShow$`Women 25-54`),1]
Bottom_People_2_Plus <- ImpressionsByAwardShow[ImpressionsByAwardShow$`People 2+` == min(ImpressionsByAwardShow$`People 2+`),1]

BottomShows <- data.frame(c("People 18-34","Men 18-34","Women 18-34","People 18-49","Men 18-49","Women 18-49","People 25-54","Men 25-54","Women 25-54","People 2+"),c(Bottom_People_18_34,Bottom_Men_18_34,Bottom_Women_18_34,Bottom_People_18_49,Bottom_Men_18_49,Bottom_Women_18_49,Bottom_People_25_54,Bottom_Men_25_54,Bottom_Women_25_54,Bottom_People_2_Plus))
names(BottomShows) <- c("Demographic","Awards Show")

TopBottomByDemo <- merge(TopShows,BottomShows,by = "Demographic")
names(TopBottomByDemo) <- c("Demographic","Most Popular Awards Show","Least Popular Awards Show")

TopShowsOverall <- ImpressionsByAwardShow[order(-ImpressionsByAwardShow$`People 2+`),c("Program","People 2+")]
names(TopShowsOverall) <- c("Awards Show",'Impressions')
rownames(TopShowsOverall) <- c(1:nrow(TopShowsOverall))


BottomShowsOverall <- ImpressionsByAwardShow[order(ImpressionsByAwardShow$`People 2+`),c("Program","People 2+")]
names(BottomShowsOverall) <- c("Awards Show",'Impressions')
rownames(BottomShowsOverall) <- c(1:nrow(BottomShowsOverall))

View(TopBottomByDemo)
View(TopShowsOverall)
View(BottomShowsOverall)