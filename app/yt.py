import os

import googleapiclient.discovery

def __make_request(video_id, pageToken=""):
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    api_service_name = "youtube"
    api_version = "v3"
    DEVELOPER_KEY = "AIzaSyBus7NEgJerHPvIgvzxAubbEcQMtrTA4Cs"

    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, developerKey = DEVELOPER_KEY)

    request = youtube.commentThreads().list(
        part="snippet",
        pageToken=pageToken,
        maxResults=100,
        videoId=video_id
    )

    response = request.execute()

    return response

def get_all_comments(video_id):
    
    commentList = []
    data = __make_request(video_id)
    i = 0
    for item in data["items"]:
        commentList.append(item["snippet"]["topLevelComment"]["snippet"])
    while("nextPageToken" in data and i <= 100):
        i = i+1
        data = __make_request(video_id, pageToken=data["nextPageToken"])
        for item in data["items"]:
            commentList.append(item["snippet"]["topLevelComment"]["snippet"])

    return commentList