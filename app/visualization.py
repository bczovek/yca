import pandas as pd
import matplotlib.pyplot as plt
from preprocessing import Preprocessor
from sentiment import SentimentClassifier
import datetime
import numpy as np

def pie_chart(comments):
    df = pd.DataFrame.from_dict(comments)
    sentiment_classifier = SentimentClassifier()
    df = sentiment_classifier.clear_data_frame(df)
    preprocessor = Preprocessor()
    df = preprocessor.create_sentences_column(df)
    return __create_pie_chart(df, sentiment_classifier)

def __create_pie_chart(sentences, sentiment_classifier):
    sentences['sentiment'], sentences['intensity'] = zip(*sentences['sentences'].apply(sentiment_classifier.score_comment_sentiment))
    labels = ["Positive", "Negative", "Neutral"]
    sum = sentences['sentiment'].count()
    neg_count = sentences[sentences['sentiment'] == 'Negative']['sentiment'].count()
    neu_count = sentences[sentences['sentiment'] == 'Neutral']['sentiment'].count()
    pos_count = sentences[sentences['sentiment'] == 'Positive']['sentiment'].count()
    sizes = [pos_count/sum, neg_count/sum, neu_count/sum]

    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, labels=labels, autopct='%1.1f%%',
            shadow=True, startangle=90)
    ax1.axis('equal')

    plt.savefig("./static/img/"+ sentences['videoId'].values[0]+".png", format='png')

    plt.figure()
    plt.gcf().subplots_adjust(bottom=0.15)
    sentences[sentences["intensity"] > 0.75].groupby('sentiment').intensity.count().plot(kind="bar", xlabel="Sentiment", ylabel="Number of high intensity comments")
    plt.savefig("./static/img/"+ sentences['videoId'].values[0]+"IntensityDist.png")

    sentences["date"] = sentences["publishedAt"].apply(__parse_date)
    del sentences['publishedAt']
    sentences['date'] = pd.to_datetime(sentences['date'], format='%Y-%m-%d')
    fig, ax = plt.subplots(figsize=(7,3))
    plt.gcf().subplots_adjust(bottom=0.1)
    sentences[['date', 'sentiment']][sentences['sentiment'] == 'Positive'].groupby('date').count().plot(ax=ax, color='green')
    sentences[['date', 'sentiment']][sentences['sentiment'] == 'Negative'].groupby('date').count().plot(ax=ax, color='red')
    ax.legend(['Positive', 'Negative'])
    ax.set_xlabel("Date")
    ax.set_ylabel("Number of comments posted")

    plt.savefig("./static/img/"+ sentences['videoId'].values[0]+"Dates.png", format='png')

    plt.figure(figsize=(7,3))
    plt.gcf().subplots_adjust(bottom=0.1)
    sentences.loc[(sentences['sentiment'] == 'Positive') | (sentences['sentiment'] == 'Negative')].groupby('date').filter(lambda x: x['intensity'].count() > 2).groupby('date').intensity.min().plot(xlabel="Date of comments posted", ylabel = "Average intensity of comments", yticks=np.arange(0, 1, 0.1))
    plt.savefig("./static/img/"+ sentences['videoId'].values[0]+"DatesIntesity.png", format='png')

    return "/static/img/"+ sentences['videoId'].values[0]+".png", "/static/img/"+ sentences['videoId'].values[0]+"IntensityDist.png", "/static/img/"+ sentences['videoId'].values[0]+"Dates.png", "/static/img/"+ sentences['videoId'].values[0]+"DatesIntesity.png"

def __parse_date(text):
    dateText = text.split('T')[0]
    return datetime.datetime.strptime(dateText, "%Y-%m-%d").date()