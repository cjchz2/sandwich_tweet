This project pulls down a tweet every hour involving the word tweet. It is then saved in the tweet datalake (an s3 bucket), then the most recent tweet is written to the database. The most recent tweet written to the database is then posted on the website sandwich.xyz.

The development was mostly done in a linux ec2 instance. 

Skills learned:

1) How to do get around in linux.
2) How to use git to push to a remote repository. How to pull down new versions of the remote repository.
3) SQL stuff?
4) Python stuff?
5) Practiced OOP skills? Originally everything (as of writing now) is written as functions. Wanted to use the principles of encapsulation and modularity to make code easier to reason about and change.
6) Learned how to use HTML a little.
7) Learned the basics of crontab.
8)

Next changes:
1) Change python scripts to OOP. Increase modularity.
2) Create error table.
3) Create a docker image of this first iteration? That way we can quickly see the development. Experiment with getting this whole setup spun up from scratch, at least the ec2 instance.
4) read pep8 and make sure you have a consistent style.

Next iteration:
Going to publish a new repository using a streaming software. Either EMR or kafka, might try both for fun. Will use this for the hourly load. 
Going to add a error table for when rows are not inserted correctly.
Going to create a partitioned table by date.
Going to create an etl process that reloads everything from the previous day.
Create a viz that helps track the findings in the error table.
Incorporate airflow?
Make the website look nicer.

Things to improve:
What is the best way to do time comparisons?

Notes for you later:

Come up with a better way to do local time conversion on current_timestamp() in POSTGRESQL.
