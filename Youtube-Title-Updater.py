from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from time import sleep
from requests import get
from lxml.html import fromstring
import json

def scrap_video_url(video_url):
    try:
        return get(video_url).content
    except Exception as e:
        raise e

def convert_raw_data_to_html(video_url):
    try:
        return fromstring(scrap_video_url(video_url))
    except Exception as e:
        raise e

def get_information_in_json(video_url):
    tree = convert_raw_data_to_html(video_url)
    try:
        for x in tree.xpath("//script"):
            if x.text and "ytInitialPlayerResponse" in x.text:
                return json.loads(x.text.split("= ")[1][:-1])
    except Exception as e:
        raise e

def get_view_count(video_url):
    return get_information_in_json(video_url)["videoDetails"]["viewCount"]


if __name__ == "__main__":

    '''
    Things You will require
    '''
    # You will require to create YouTube Data API v3 OAuth 2.0 Client IDs Client ID for Desktop
    CLIENT_SECRETS_FILE = "client_secret.json"
    # Add Your Video URL here
    video_url = "https://www.youtube.com/watch?v=6VU0h-pfibQ"
    # Add Your Channel ID here
    channel_id = "UCxqQq91PUgR7RqseFpkSMLw"



    SCOPES = ["https://www.googleapis.com/auth/youtube"]
    API_SERVICE_NAME = "youtube"
    API_VERSION = "v3"
    youtube_id = video_url.split("v=")[1]

    flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
    credentials = flow.run_console()
    youtube = build(API_SERVICE_NAME, API_VERSION, credentials=credentials)

    
    while True:
        try:
            view_count = get_view_count(video_url)
            title = f"This Video has {view_count} views."   # Add Your title here
            # Change This based on your Video. Check Videos-list-snippet-Example File for more info or
            # you can generate it yourself by Following https://github.com/youtube/api-samples/blob/master/python/update_video.py example
            # I have done this because it will also consume 1 unit everytime. So I probably saved it into a variable. 
            videos_list_snippet = {
                "publishedAt": "2020-05-25T09:40:58Z",
                "channelId": channel_id,
                "title": title,
                "description": "**So I have Exhausted the daily Quota and this wont work now! ** Apologies.\n\n\nThis video will update the title automatically according to views, comments and likes.\nSubscribe to see the tutorial for the following video.\n\nThank You for watching...\nCode will be updated on GitHub soon.",
                "thumbnails": {
                    "default": {
                        "url": "https://i.ytimg.com/vi/6VU0h-pfibQ/default.jpg",
                        "width": 120,
                        "height": 90,
                    },
                    "medium": {
                        "url": "https://i.ytimg.com/vi/6VU0h-pfibQ/mqdefault.jpg",
                        "width": 320,
                        "height": 180,
                    },
                    "high": {
                        "url": "https://i.ytimg.com/vi/6VU0h-pfibQ/hqdefault.jpg",
                        "width": 480,
                        "height": 360,
                    },
                    "standard": {
                        "url": "https://i.ytimg.com/vi/6VU0h-pfibQ/sddefault.jpg",
                        "width": 640,
                        "height": 480,
                    },
                    "maxres": {
                        "url": "https://i.ytimg.com/vi/6VU0h-pfibQ/maxresdefault.jpg",
                        "width": 1280,
                        "height": 720,
                    },
                },
                "channelTitle": "Dhruv Padhiyar",
                "categoryId": "28",
                "liveBroadcastContent": "none",
                "localized": {
                    "title": "This Video has 139 views, 17 comments and 12 likes.",
                    "description": "**So I have Exhausted the daily Quota and this wont work now! ** Apologies.\n\n\nThis video will update the title automatically according to views, comments and likes.\nSubscribe to see the tutorial for the following video.\n\nThank You for watching...\nCode will be updated on GitHub soon.",
                },
                "defaultAudioLanguage": "en-US",
            }
            videos_update_response = (
                youtube.videos()
                .update(
                    part="snippet", body=dict(snippet=videos_list_snippet, id=youtube_id)
                )
                .execute()
            )
            print("Video Updated")
        except Exception as e:
            print(e)
        # Updating Title every 10 mins due to Quota Restrictions for Youtube API v3. 10000 Per day and Update Operation cost 50 units. 
        sleep(10*60)
    
