import psycopg2
import boto3
#Grabbing credentials from a text file so they aren't hardcoded in script.

credential_list = []

with open("sandwich_db_credentials.txt") as file:
	lines = file.readlines()
	for line in lines:
		 credential_list.append(line)

user_name_str = credential_list[0]
password_str = credential_list[1]
#Creating connection to the PostgreSQL database.
conn = psycopg2.connect(database = "sandwich_tweets",
 	user = user_name_str.strip(),
	password = password_str.strip(),
	host = "sandwich-tweets.cxors8ly0k2i.us-east-2.rds.amazonaws.com", 
	port = "5432" )

sql_statement = """SELECT TEXT,TWEET_DATE FROM SANDWICH_TWEETS.TWEETS WHERE INSERT_DATE = (SELECT MAX(INSERT_DATE) FROM SANDWICH_TWEETS.TWEETS)"""

cur = conn.cursor()

cur.execute(sql_statement)

row = cur.fetchone()

text = row[0]

date_tweeted = row[1]

website_string = """<!DOCTYPE html>
<html>
  <body>
  Here is a tweet with the word sandwich:
  {0}
  It was posted on:
  {1}
  </body>
</html>""".format(text, date_tweeted)

with open("index.html","w+") as f:
    f.write(website_string)

s3_resource = boto3.resource("s3")
s3_resource.Object("sandwich-website", "index.html").upload_file("index.html", ExtraArgs = {"ContentType":"application/html"})



#client = boto3.client("s3")
#client.put_object(Body = website_string, Bucket = "sandwich-website", key = "html.index")
