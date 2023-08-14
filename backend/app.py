import os
from flask import Flask, render_template,Response
from googleapiclient.discovery import build
from dotenv import load_dotenv
import isodate
import datetime

app = Flask(__name__)

load_dotenv()
api_key = os.getenv('YOUTUBE_API_KEY')
# print(api_key)

youtube = build('youtube', 'v3', developerKey=api_key)



@app.route('/hey/<playlist_id>')
def get_playlist_info(playlist_id):
    video_list=[]
    next_page_token = None
    while True:
        request = youtube.playlistItems().list(
        part="contentDetails",
        maxResults=50,
        playlistId=playlist_id,
        pageToken=next_page_token
        )   
        response = request.execute()
        videoDetails = response['items']
        for i in range(len(videoDetails)):
            video_list.append(videoDetails[i]['contentDetails']['videoId'])
        
        next_page_token = response.get('nextPageToken')
        if not next_page_token:
            break
        
    time=0
    for i in (video_list):
        time+=videoDuration(i)[0]
    ans = []
    # [ total_time | at 1.25x | at 1.5x | at 2x | Average duration ]
    ans.append(str(datetime.timedelta(seconds=time)))
    ans.append(str(datetime.timedelta(seconds=time/1.25)))
    ans.append(str(datetime.timedelta(seconds=time/1.5)))
    ans.append(str(datetime.timedelta(seconds=time/1.75)))
    ans.append(str(datetime.timedelta(seconds=time/2)))
    ans.append(str(datetime.timedelta(seconds=time/len(video_list))))
    return ans


@app.route('/may/<id>')
def videoDuration(id):
    request = youtube.videos().list(
        part="contentDetails",
        id=id,
    )
    response = request.execute()
    items = response['items']
    duration = items[0]['contentDetails']['duration']
    durationObj = isodate.parse_duration(duration)
    totalSeconds = durationObj.total_seconds()
    return [totalSeconds]


if __name__=="__main__":
    app.run(debug=True)
