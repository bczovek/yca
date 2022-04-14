from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import pandas as pd
import numpy as np

class SentimentClassifier:

    def __init__(self):
        self.sid_obj = SentimentIntensityAnalyzer()

    def clear_data_frame(self, df):
        del df['authorDisplayName']
        del df['authorProfileImageUrl']
        del df['authorChannelUrl']
        del df['canRate']
        del df['viewerRating']
        del df['authorChannelId']
        del df['updatedAt']
        del df['textDisplay']
        del df['likeCount']
        return df

    def score_comment_sentiment(self, sentences):
        compounds = []
        intensities = []
        for sentence in sentences:
            sentiment_dict = self.sid_obj.polarity_scores(sentence)
            if sentiment_dict['compound'] >= 0.05 :
                intensities.append(sentiment_dict["pos"])
            elif sentiment_dict['compound'] <= - 0.05 :
                intensities.append(sentiment_dict["neg"])
            compounds.append(sentiment_dict['compound'])

        comment_compound = np.average(compounds)
        intesity_average = np.average(intensities)
        
        if comment_compound >= 0.05:
            sentiment = "Positive"
        elif comment_compound <= -0.05:
            sentiment = "Negative"
        else:
            sentiment = "Neutral"

        if np.isnan(intesity_average):
            intesity_average = 0.0

        return sentiment, intesity_average