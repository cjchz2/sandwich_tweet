This is the first version of the project! It is quite rudimentary. The code is very rough and will be refactored in subsequent analysis.

In version 2, I will be refactoring the script to OOP principles of encapsulation and modularity. In addition, I will be conforming to PEP8 standards. Finally I will be adding an error table to track failed loads into the TWEETS table.


This project pulls down a tweet every hour involving the word tweet. It is then saved in the tweet datalake (an s3 bucket), then the most recent tweet is written to the database. The most recent tweet written to the database is then posted on the website sandwich.xyz.

The development was mostly done in a linux ec2 instance. 

