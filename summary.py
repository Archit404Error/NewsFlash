'''
This script utilizes natural language processing via the nltk module to
summarize the news articles. These summaries are more relavant/useful to the
topic at hand compared to the newspaper3k summaries, as newspaper doesn't use
optimal analyses
'''

# importing libraries
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize

def summarize_text(text):

    # Tokenizing the text
    stopWords = set(stopwords.words("english"))
    words = word_tokenize(text)

    # Creating a frequency table to keep the score of each word
    freqTable = dict()
    for word in words:
        word = word.lower()
        if word in stopWords:
            continue
        if word in freqTable:
            freqTable[word] += 1
        else:
            freqTable[word] = 1

    # Creating a dictionary to keep the score of each sentence
    sentences = sent_tokenize(text)
    sentenceValue = dict()

    for sentence in sentences:
        for word, freq in freqTable.items():
            if word in sentence.lower():
                if sentence in sentenceValue:
                    sentenceValue[sentence] += freq
                else:
                    sentenceValue[sentence] = freq

    sumValues = 0
    for sentence in sentenceValue:
        sumValues += sentenceValue[sentence]

    # Average value of a sentence from the original text
    if len(sentenceValue) == 0:
        return ''
    average = int(sumValues / len(sentenceValue))

    # Storing sentences into our summary.
    summary = ''
    for sentence in sentences:
        #Set sentence value to be greater than 1.5 * average to create relatively short summaries
        if (sentence in sentenceValue) and (sentenceValue[sentence] > (1.5 * average)):
            summary += " " + sentence
    return summary
