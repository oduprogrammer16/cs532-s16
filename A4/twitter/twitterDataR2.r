pdf("KevinTwitterPlot.pdf")
x_range <- c(1,53)
y_range <- c(1,963391)

x <- c(1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53)
y <- c(1,6,9,9,17,19,19,26,39,52,69,73,80,88,92,104,107,114,132,135,166,188,190,239,248,265,271,287,289,299,333,379,413,493,493,693,957,983,1026,1033,1520,3542,3877,9074,13043,16206,18991,36776,47135,75874,202649,605566,963391)

plot(x_range,y_range,type="n",xlab="Follower Id", ylab="Number of Followers in Log Scale",log="y")

points(x,y,col='blue',pch=1,lwd=1)
kevinX <- c(10)
kevinY <- c(52)

points(kevinX,kevinY,type="b",lty=5,col='red',pch=16);
legend(1,35000,c("Number of Followers for KevinClemmons"),pch=c(16),cex=.8,col=c("Red"))
title("Twitter Follower Counts")
dev.off()

paste("Mean:",mean(y))
paste("Standard Deviation: ",sd(y))
paste("Median: ",median(y))
paste("Number of Followers for KevinClemmons: ",kevinY)
paste("Number of Followers Who have More Followers than KevinClemmons: ", sum(y > kevinY[1] ))
paste("Number of Followers Who have Less Followers than KevinClemmons: ", sum(y < kevinY[1]))
