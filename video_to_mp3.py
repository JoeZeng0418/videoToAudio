from bs4 import BeautifulSoup as bs
import requests
from pytube import YouTube
import pytube
import re
import subprocess
import sys

search_base = "https://www.youtube.com/results?search_query="
search_string = "made in china"
request_string = search_base + re.sub("\s+", "+", search_string.strip())
filename_string = re.sub("\s+", "_", search_string.strip())

# get the list of video urls with the current search

video_list=[]
soup=bs(requests.get(request_string).text,'html.parser')
videos = soup.findAll('a',attrs={'class':'yt-uix-tile-link'})
f= open("test.txt","w+")
for video in videos:
	video_list.append('https://www.youtube.com' + video['href'])
	f.write('https://www.youtube.com' + video['href']+"\n")
f.close()

#download videos according to urls

count=0
for item in video_list:
    if count==1:
        break
    # increment counter:
    count+=1
    yt = YouTube(item)

    # download the video:
    yt.streams.filter(mime_type="video/mp4").first().download('vids',filename=filename_string+'_'+str(count))

    command = "ffmpeg -i vids/"+filename_string+"_"+str(count)+".mp4"+" -f mp3 -ab 192000 -vn "+filename_string+"_"+str(count)+".mp3"
    subprocess.call(command, shell=True)
