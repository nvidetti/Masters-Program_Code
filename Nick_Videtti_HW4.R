#Read in fedPapers85.csv
#setwd('C:/Users/nvidetti/Downloads')
papers_csv <- read.csv('fedPapers85.csv')

#Create copy of data set and look at data types
papers <- papers_csv
str(papers)

#Replace period in column names
colnames(papers) <- gsub('[.]','',colnames(papers))

#Check results
str(papers)

#Check different authors, then create new data set using only Hamilton, Madison, and dispt
table(papers$author)
for(i in 1:nrow(papers)){if(papers$author[i] == 'dispt'){papers$author[i] <- papers$filename[i]}}
papers <- papers[!papers$author %in% c('Jay','HM'), colnames(papers) != 'filename']

#Euclidean Distance Hierarchical Clustering
EucClust <- hclust(dist(papers, method = 'euclidean'),method = 'complete')
for(i in 1:nrow(papers)){EucClust$labels[i] <- papers[rownames(papers) == EucClust$labels[i],'author']}
plot(EucClust, main = 'Euclidean')

#Manhattan Distance Hierarchical Clustering
ManhClust <- hclust(dist(papers, method = 'manhattan'),method = 'complete')
for(i in 1:nrow(papers)){ManhClust$labels[i] <- papers[rownames(papers) == ManhClust$labels[i],'author']}
plot(ManhClust, main = 'Manhattan')