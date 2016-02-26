pdf("KevinTwitterPlot.pdf")
x_range <- c(1,52)
y_range <- c(1,963486)

x <- c(1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52)
y <- c(1,5,9,9,19,19,26,39,51,69,73,80,88,92,104,107,114,132,135,166,188,190,239,248,264,269,287,289,299,332,380,413,492,494,693,957,984,1026,1033,1446,3542,3864,9072,13041,16210,18990,36774,47138,75786,202680,605634,963486)

plot(x_range,y_range,type="n",xlab="Follower Id", ylab="Number of Followers in Log Scale",log="y")

points(x,y,col='blue',pch=1,lwd=1)
kevinX <- c(9)
kevinY <- c(51)

points(kevinX,kevinY,type="b",lty=5,col='red',pch=16);
legend(1,35000,c("Number of Followers for KevinClemmons"),pch=c(16),cex=.8,col=c("Red"))
title("Twitter Follower Counts")
dev.off()