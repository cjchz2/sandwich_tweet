import boto3
from datetime import date, timedelta, datetime
from pytz import timezone
import settings
import psycopg2
import glob

class tweet_etl:
    def __init__(self):
        pass

    def db_credential_setter(self, database_name, user_name, password, host_name, port):
        self.database_name = database_name
        self.user_name = user_name
        self.password = password
        self.host_name = host_name
        self.port = port

    def db_connect(self):
        self.conn = psycopg2.connect(database = self.database_name,
                                user = self.user_name,
                                password = self.password,
                                host_name = self.host_name,
                                port = self.port)
        print("Database successfully connected to.")

    def insert_fact_sql_creator(self, schema, fact_table):
        self.schema = schema
        self.fact_table = fact_table
        fact_insert_statement = """INSERT INTO {schema}.{fact_table} (ID,TEXT,USERNAME,TWEET_DATE,PULLED_DATE)
                                   VALUES (%s, %s, %s, %s, %s)
                                   ON CONFLICT DO NOTHING""".format(schema = self.schema,
                                                                    fact_table = self.fact_table)

    def s3_bucket_connect(self, s3_bucket_name):
        self.s3_bucket_name = s3_bucket_name
        self.s3_bucket_obj = s3_resource.Bucket(self.s3_bucket_name)

    def s3_file_puller(self, s3_bucket_name, hour_time_range):
        self.s3_bucket_name = s3_bucket_name
        self.s3_bucket_obj = s3_resource.Bucket(self.s3_bucket_name)

        now_datetime = datetime.now()

        #Grabbing all files from the within the time range specified in hour_time_range
        for bucket in self.s3_bucket_obj.objects.all():
            file_datetime_str = bucket.key[15:34]
            file_datetime = datetime.strptime(file_datetime_str, "%Y-%m-%d %H:%M:%S")
            if file_datetime > now_datetime - timedelta(hours = hour_time_range):
                s3_resource.Object(self.bucket_name,
                                   bucket.key).download_file(Filename = bucket.key)

    def insert_facts(self, local_file_path, tweet_topic):
        cur = self.conn.cursor()

        file_path_collection = glob.glob(local_file_path + tweet_topic + " %*")

        for file_path in file_path_collection:
            with open(file_path) as file:
                print("about to read file")
                tweet_info = file.read()
                print("About to split file")
                tweet_list = tweet_info.split('^&*>*&^')
                print("about to convert id to int")
                tweet_list[0] = int(tweet_list[0])
                print("About to execute SQL")
                cur.execute(sql_statement, tweet_list)
                print("about to write a record")
                conn.commit()
        cur.close()

