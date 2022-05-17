#!/usr/bin/env python
# coding: utf-8

# Membuat Akun Twitter Developer

# In[ ]:


#Import library yang dibutuhkan
import tweepy
import sys
import jsonpickle
import time
from datetime import datetime
from datetime import timedelta


# In[ ]:


# Menggunakan google drive sebagai storage
from google.colab import drive
drive.mount("/content/gdrive")


# In[ ]:


#Memasukan consumer key dan secret untuk akses API Twitter
consumer_key = ''
consumer_secret = ''

auth = tweepy.AppAuthHandler(consumer_key,consumer_secret)


# In[ ]:


#Mengisi parameter pencarian
since =(datetime.now() + timedelta(days=-30)).strftime("%Y-%m-%d")
qry='kebijakan miras  since:'+since +' lang:in -filter:url -filter:images'
maxTweets = 100000 # Isi sesuai dengan kebutuhan anda
tweetsPerQry = 100  # dibatasi Twitter maksimum 100
fName='/content/gdrive/MyDrive/Data_Tweet_'+datetime.now().strftime("%Y%m%d%H%M%S")+'.json' # Nama file hasil scraping

api = tweepy.API(auth, wait_on_rate_limit=True,wait_on_rate_limit_notify=True)


# In[ ]:


sinceId, max_id, tweetCount = None, -1, 0 

print("Mulai mengunduh maksimum {0} tweets".format(maxTweets))
with open(fName,'w') as f:
    while tweetCount < maxTweets:
        try:
            if (max_id <= 0):
                if (not sinceId):
                    new_tweets=api.search(q=qry,count=tweetsPerQry, tweet_mode='extended')
                else:
                    new_tweets=api.search(q=qry,count=tweetsPerQry,since_id=sinceId, tweet_mode='extended')
            else:
                if (not sinceId):
                    new_tweets=api.search(q=qry,count=tweetsPerQry,max_id=str(max_id - 1), tweet_mode='extended')
                else:
                    new_tweets=api.search(q=qry,count=tweetsPerQry,max_id=str(max_id - 1),since_id=sinceId, tweet_mode='extended')
            if not new_tweets:
                print(' Tidak ada lagi Tweet ditemukan dengan Query="{0}"'.format(qry));break
            for tweet in new_tweets:
                #if(tweet.created_at.date() < datetime.now().date()) :
                f.write(jsonpickle.encode(tweet._json,unpicklable=False)+'\n')
            tweetCount+=len(new_tweets)
            sys.stdout.write("\r");sys.stdout.write("Jumlah Tweets telah tersimpan: %.0f" %tweetCount);sys.stdout.flush()
            max_id=new_tweets[-1].id
        except tweepy.TweepError as e:
            print("some error : " + str(e));break 
print ('\nSelesai! {0} tweets tersimpan di "{1}"'.format(tweetCount,fName))


# Menulis data tweet ke dalam file csv

# In[ ]:


import json
import csv
with open('/content/gdrive/MyDrive/Data_Tweet_20220321020604.json', 'r') as f:
    #mengambil tweet pada x baris pertama
    data = [next(f) for x in range(100)]

    csvFile = open('Dataset tweet.csv', 'a', newline='', encoding='utf8')
    csvWriter = csv.writer(csvFile)
    csvWriter.writerow(['id','userid','name','date','location','tweet',])

    for dt in data :
      tweet = json.loads(dt)
      csvWriter.writerow([tweet['id'],tweet['user']['id'],tweet['user']['screen_name'],tweet['created_at'],tweet['user']['location'],tweet['full_text'].replace('\n', ' ')])
    csvFile.close() 

