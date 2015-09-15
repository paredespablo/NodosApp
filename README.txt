NodosApp v0.9
NodosChile Ltda. 2012-2015
PPN <s1339439@sms.ed.ac.uk>

*********************************************

NodosApp is a lightweight application written in Python 2.7 for social network analysis based on twitter data.
The capabilities of NodosApp can be divided in three groups of functions:

Downloading of data from Twitter
- Search API
- Streaming and Georeferenced Streaming API
- Timeline from a specific user

Social Network and Media Analysis
- Building of GEXF files
- Social network's indicators
- Sentiment Analysis (spanish and english)
- Gender analysis (spanish and english)
- Ranking of most popular hashtags
- Ranking of most active users
- Ranking of most mentioned users

Data visualization
- Georeferencing of tweets in Google maps
- Networks in Sigma.js
- Networks in D3.js

For a better understanding of these functions, read the Wiki

## INSTALL ##

NodosApp is written in Python 2.7, hence you need to install this package in order to use it

[Download Python 2.7](https://www.python.org/download/releases/2.7/)

Once installed, you should go to the Python27/Scripts folder, and run the next commands:

* pip install networkx
* pip install tweepy

These commands (either run by windows console or linux terminal) will install the required libraries to run NodosApp. Otherwise, you will have to download them manually.