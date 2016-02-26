# Submission for Assignment 4

## Folders 
### twitter 
 * Contains source code for the twitter portion of the assignment. 

### facebook 
 * Contains source code for the facebook portion of the assignment 

### reports
* Contains report for assignment 4 and the graphs produced. 

## Twitter Program 
* Located in folder called twitter
### Setup 
* Ensure that you have tweepy api installed 
* Enter your twitter api access information in the twitter_config.json 
### Running 
1) Run the command "python twitterFriendData.py", a json file will be created.
2) Run the command "python createRScript.py <json-file-name> <output-r-script-file>", an r-script will be generated 
3) Run the command "Rscript <output-r-script-file>" to generate the graph, a pdf will be generated. 

## Facebook Program 
### Running 
1) Run the command "python extractFacebookFriendData.py <optional-facebook-file>", an r-script will be generated. 
2) Run the command "Rscript <output-r-script-file>" to generate the graph, a pdf will be generated. 
