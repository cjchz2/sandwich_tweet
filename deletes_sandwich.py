import glob
import os

file_path = glob.glob('/home/ec2-user/sandwich_tweet%*')

for file in file_path:
    os.remove(file)
