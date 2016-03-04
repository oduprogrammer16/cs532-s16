# Datafile obtained from http://networkdata.ics.uci.edu/data/karate/

# repeat loop
library(igraph)

karate_network <- read.graph('karate.gml',format='gml')
# Get list communities
communityList <- leading.eigenvector.community(karate_network,steps=1)

# Vertex Coloring
V(karate_network)$color <- ifelse(communityList$membership==1,"orange","yellow")

# Deterline scale of graph 
scale_graph <- function(vertex,alpha,beta){
	vertex <- vertex-min(vertex); vertex <-vertex/max(vertex); vertex <- vertex * (beta-alpha); vertex+alpha
}

# Get the scale of the plot
#V(karate_network)$size <- scale(abs(scale_graph$eigenvectors[[1]]),10,20)

E(karate_network)$color <- "grey"

# Color all edges that connect one cluster to another one 
#E(karate_network)[V(karate_network)[color=="orange"] %--% V(karate_network)[color=="yellow"]]$color <-"red"
tkplot(karate_network,layout=layout.kamada.kawai,vertex.label.font=2)


# Perform the girvan-neumam algorithm 
repeat{

	# Calculate betweeness of all edges 
	edgeBetweeness <- edge.betweenness(karate_network)

	# determine the highest edge betweeness 
	highestEdgeBetweeness <- max(edgeBetweeness)

	# Find the index with the highest edge betweeness
	edgeToDelete <- match(c(highestEdgeBetweeness),edgeBetweeness)

	# Delete the edge with the highest edgebetweeness 

	# Get the start and end nodes
	start <- get.edgelist(karate_network)[edgeToDelete,1] # The starting vertex
	end <- get.edgelist(karate_network)[edgeToDelete,2]# The ending 
	
	# Prints a list of edges to be deleted in the format start,end,highestEdgebet
	print(paste(paste(paste(start,","),end),paste(",",highestEdgeBetweeness)))

	# Delete the edge with the highest edgebetweeness 
	karate_network <- delete.edges(karate_network,E(karate_network,P=c(start,end)))

	# Get the number of groups of nodes
	numberOfClusters <- clusters(karate_network)['no']

	# If two groups of nodes are found, break the loop
	if(numberOfClusters == 2){
		break
	}

	# Get list communities
	communityList <- leading.eigenvector.community(karate_network,steps=1)

	# Vertex Coloring
	#paste(communityList)
	V(karate_network)$color <- ifelse(communityList$membership==1,"orange","yellow")

	# Deterline scale of graph 
	scale_graph <- function(vertex,alpha,beta){
		vertex <- vertex-min(vertex); vertex <-vertex/max(vertex); vertex <- vertex * (beta-alpha); vertex+alpha
	}

	# Get the scale of the plot
	#V(karate_network)$size <- scale(abs(scale_graph$eigenvectors[[1]]),10,20)

	E(karate_network)$color <- "grey"

	# Color all edges that connect one cluster to another one 
	#E(karate_network)[V(karate_network)[color=="orange"] %--% V(karate_network)[color=="yellow"]]$color <-"red"
	tkplot(karate_network,layout=layout.kamada.kawai,vertex.label.font=2)
}





# Get list communities
communityList <- leading.eigenvector.community(karate_network,steps=1)

# Vertex Coloring
V(karate_network)$color <- ifelse(communityList$membership==1,"orange","yellow")

# Deterline scale of graph 
scale_graph <- function(vertex,alpha,beta){
	vertex <- vertex-min(vertex); vertex <-vertex/max(vertex); vertex <- vertex * (beta-alpha); vertex+alpha
}


E(karate_network)$color <- "grey"

tkplot(karate_network,layout=layout.kamada.kawai,vertex.label.font=2)
