from data_access import find_comments, open_comments, save_comments
from flask import Flask, render_template, request, redirect, url_for, send_file, make_response
from visualization import pie_chart
from words import words
from yt import get_all_comments
import json

app = Flask(__name__)
app.static_folder = 'static'

@app.route('/', methods=["GET", "POST"])
def index():

    if request.method == "POST":
        video_id = request.form.get("videoId")
        
        if not find_comments(video_id):
            comments = get_all_comments(video_id)
            if len(comments) > 100:
                save_comments(comments, video_id)
            else:
                return render_template("index.html")

        return redirect(url_for('video') + '?videoId=' + video_id)

    return render_template("index.html")

@app.route('/video')
def video():
    video_id = request.args.get("videoId")
    if not find_comments(video_id):
        save_comments(get_all_comments(video_id), video_id)
    
    return render_template("video.html", comment_number = len(open_comments(video_id)), video_id = video_id)

@app.route('/graphs')
def comments():
    video_id = request.args.get("videoId")
    comments = None
    if find_comments(video_id):
        comments = open_comments(video_id)
    else:
        save_comments(get_all_comments(video_id), video_id)
        comments = open_comments(video_id)

    image1, image2, image3, image4 = pie_chart(comments)
    
    return json.dumps({"image1": image1, "image2": image2, "image3": image3, "image4": image4})

@app.route('/words')
def words_table():
    video_id = request.args.get("videoId")
    words_json = None
    if find_comments(video_id):
        words_json = words(open_comments(video_id))
    else:
        save_comments(get_all_comments(video_id), video_id)
        words_json = words(open_comments(video_id))

    return words_json

if __name__ == "__main__":
    app.run()
