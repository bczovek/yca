import pandas as pd
from sentiment import SentimentClassifier
from preprocessing import Preprocessor
import nltk
import numpy as np
import json

def words(comments):
    df = pd.DataFrame.from_dict(comments)
    sentiment_classifier = SentimentClassifier()
    df = sentiment_classifier.clear_data_frame(df)
    preprocessor = Preprocessor()
    df = preprocessor.create_sentences_column(df)
    df['sentiment'], df['intensity'] = zip(*df['sentences'].apply(sentiment_classifier.score_comment_sentiment))
    df = preprocessor.preprocess_sentences(df)
    words = __word_sentiments(df)
    word_pairs = __word_pair_sentiments(df)
    return json.dumps({"words": words,
    "word_pairs": word_pairs}, indent=4)

def __word_sentiments(df):
    df = __create_context_sentiment(df)
    del df['frequencies']

    return {"top5MostlyPositive": df[df['context_sentiment'] == 'Mostly positive'].head(5).to_dict(orient='records'),
    "top5SlightlyPositive": df[df['context_sentiment'] == 'Slightly positive'].head(5).to_dict(orient='records'),
    "top3Controversial": df[df['context_sentiment'] == 'Controversial'].head(3).to_dict(orient='records'),
    "top5SlightlyNegative": df[df['context_sentiment'] == 'Slightly negative'].head(5).to_dict(orient='records'),
    "top5MostlyNegative": df[df['context_sentiment'] == 'Mostly negative'].head(5).to_dict(orient='records')}

def __word_pair_sentiments(df):
    df = __create_context_sentiment_bigram(df)
    del df['frequencies']

    return {"top3MostlyPositive": df[df['context_sentiment'] == 'Mostly positive'].head(3).to_dict(orient='records'),
    "top3SlightlyPositive": df[df['context_sentiment'] == 'Slightly positive'].head(3).to_dict(orient='records'),
    "top3Controversial": df[df['context_sentiment'] == 'Controversial'].head(3).to_dict(orient='records'),
    "top3SlightlyNegative": df[df['context_sentiment'] == 'Slightly negative'].head(3).to_dict(orient='records'),
    "top3MostlyNegative": df[df['context_sentiment'] == 'Mostly negative'].head(3).to_dict(orient='records')}

def __create_context_sentiment(df):
    pos_tokens = __create_token_array(df[df['sentiment'] == 'Positive']['keywords'].values)
    neg_tokens = __create_token_array(df[df['sentiment'] == 'Negative']['keywords'].values)
    neu_tokens = __create_token_array(df[df['sentiment'] == 'Neutral']['keywords'].values)
    pos_freq = __create_frequency_map(pos_tokens)
    neg_freq = __create_frequency_map(neg_tokens)
    neu_freq = __create_frequency_map(neu_tokens)
    context_sentiment_dict = __context_sentiment(pos_freq, neg_freq, neu_freq)
    df_words = __convert_dict_to_dataframe(context_sentiment_dict)
    df_words['compound'] = df_words['frequencies'].apply(__normalize)
    df_words['context_sentiment'] = df_words['compound'].apply(__score_context_sentiment)
    return df_words

def __create_context_sentiment_bigram(df):
    pos_tokens = __create_token_array(df[df['sentiment'] == 'Positive']['keywords'].values)
    neg_tokens = __create_token_array(df[df['sentiment'] == 'Negative']['keywords'].values)
    neu_tokens = __create_token_array(df[df['sentiment'] == 'Neutral']['keywords'].values)
    pos_bigrams = nltk.bigrams(pos_tokens)
    neg_bigrams = nltk.bigrams(neg_tokens)
    neu_bigrams = nltk.bigrams(neu_tokens)
    pos_freq = __create_frequency_map(pos_bigrams)
    neg_freq = __create_frequency_map(neg_bigrams)
    neu_freq = __create_frequency_map(neu_bigrams)
    context_sentiment_dict = __context_sentiment(pos_freq, neg_freq, neu_freq)
    df_words = __convert_dict_to_dataframe(context_sentiment_dict)
    df_words['compound'] = df_words['frequencies'].apply(__normalize)
    df_words['context_sentiment'] = df_words['compound'].apply(__score_context_sentiment)
    return df_words

def __create_token_array(values):
    tokens = []
    for tokenizedSentece in values:
        for token in tokenizedSentece:
            tokens.append(token)
    return tokens

def __create_frequency_map(tokens):
    fdist = nltk.FreqDist(tokens)
    return fdist.most_common(50)

def __context_sentiment(pos_freq, neg_freq, neu_freq):
    result = dict()
    for k, v in pos_freq:
        result[k] = [v, 0, 0]
    for k,v in neu_freq:
        try:
            result[k][1] = v
        except:
            result[k] = [0, v, 0]
    for k,v in neg_freq:
        try:
            result[k][2] = v
        except:
            result[k] = [0, 0, v]
    return result

def __convert_dict_to_dataframe(dict):
    df = pd.DataFrame(dict.items(), columns=['word','frequencies'])
    df[['positive', 'neutral', 'negative']] = pd.DataFrame(df['frequencies'].tolist(), index=df.index)
    return df

def __normalize(frequencies):
    v = np.array(frequencies)
    v = v / np.linalg.norm(v)
    return v[0] * 1 + v[1] * 0.01 + v[2] * (-1)

def __score_context_sentiment(compound):
    if compound == 0.01:
        result = "Neutral"
    elif compound > 0.5:
        result = "Mostly positive"
    elif compound > 0.1:
        result = "Slightly positive"
    elif compound > -0.1:
        result = "Controversial"
    elif compound > -0.5:
        result = "Slightly negative"
    else:
        result = "Mostly negative"
    return result