import re
import spacy
from nltk.tokenize import word_tokenize, sent_tokenize

class Preprocessor:

    nlp = spacy.load('en_core_web_sm')
    STOPWORDS = nlp.Defaults.stop_words
    print("loaded en_core_web_sm")

    def preprocess_sentences(self, sentences):
        sentences['cleanSentence'] = sentences['textOriginal'].str.lower()
        sentences['cleanSentence'] = sentences['cleanSentence'].apply(self.__clean_punctuation)
        sentences['cleanSentence'] = sentences['cleanSentence'].apply(self.__remove_adjectives_adverbs_verbs)
        sentences['cleanSentence'] = sentences['cleanSentence'].apply(self.__remove_stopwords)
        sentences['cleanSentence'] = sentences['cleanSentence'].apply(self.__lemmatization)
        sentences['cleanSentence'] = sentences['cleanSentence'].apply(self.__remove_common_words)
        sentences['cleanSentence'].replace('', float("NaN"), inplace=True)
        sentences.dropna(subset=['cleanSentence'], inplace=True)
        sentences['keywords'] = sentences['cleanSentence'].apply(word_tokenize)
        del sentences['cleanSentence']
        return sentences

    def __remove_common_words(self, text):
        common_words = ['wow', 'xd', 'lol','wtf','lmao','wow','omg','nvm','idk','idc','guy','people','de','na','fuck','shit','damn','year','world','thing','like','fact','oh']
        tokenized_text = text.split(' ')
        return ' '.join([w for w in tokenized_text if not w in common_words])

    def __replace_newline(self, text):
        text = text.replace('\n', '. ')
        return text

    def __clean_punctuation(self, text):
        text = re.sub(r'\d+', '', text)
        text = str(text)
        text = re.sub(r'[^\w\s]', '', text)
        return text

    def __remove_stopwords(self, text):
        tokenized_text = text.split(' ')
        return ' '.join([w for w in tokenized_text if not w in Preprocessor.STOPWORDS and len(w) > 1])

    def __lemmatization(self, text):
        doc = Preprocessor.nlp(text)
        return ' '.join([w.lemma_ for w in doc])

    def __remove_adjectives_adverbs_verbs(self, text):
        return ' '.join(word.text for word in Preprocessor.nlp(text) if not (word.pos_ == 'VERB'  or word.pos_ == 'ADJ') and not (word.text == "nt" or word.text == "ve"))

    def create_sentences_column(self, df):
        df["textOriginal"] = df["textOriginal"].apply(self.__replace_newline)
        df['sentences'] = df['textOriginal'].apply(sent_tokenize)
        return df