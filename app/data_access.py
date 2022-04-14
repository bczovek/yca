from os.path import exists
import io
import json

def find_comments(video_id):
    return exists("./data/"+ str(video_id) +".json")

def open_comments(video_id): 
    with open("./data/"+ str(video_id) +".json") as file:
        return json.load(file)

def save_comments(comments, video_id):
    with open("./data/"+ str(video_id) +".json", 'w+') as outfile:
        json.dump(comments, outfile)
