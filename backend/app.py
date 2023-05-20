import os
from flask import Flask, render_template
from googleapiclient.discovery import build
from dotenv import load_dotenv
app = Flask(__name__)

load_dotenv()
api_key = os.getenv('YOUTUBE_API_KEY')
# print(api_key)

youtube = build('youtube', 'v3', developerKey=api_key)

@app.route('/<playlist_id>')
def get_playlist_info(playlist_id):
    response = youtube.playlists().list(
        part='snippet',
        maxResults =25,
        id=playlist_id
    ).execute()
    # playlist_info = response['items'][0]['contentDetails']
    # print(playlist_info)
    return response
    # return render_template('playlist.html', playlist=playlist_info)

# get_playlist_info("PLxCzCOWd7aiHMonh3G6QNKq53C6oNXGrX")
if __name__=="__main__":
    app.run(debug=True)
