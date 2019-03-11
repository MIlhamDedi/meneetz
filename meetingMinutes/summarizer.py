import nltk
import re
import os
import heapq
from pprint import pprint

def summarize_text(text):
    # Removing Square Brackets and Extra Spaces
    article_text = re.sub(r'\[[0-9]*\]', ' ', text)  
    article_text = re.sub(r'\s+', ' ', article_text)
    
    # Removing special characters and digits
    formatted_article_text = re.sub('[^a-zA-Z]', ' ', article_text )  
    formatted_article_text = re.sub(r'\s+', ' ', formatted_article_text)  

    sentence_list = nltk.sent_tokenize(article_text)
    stopwords = nltk.corpus.stopwords.words("english")
    word_frequencies = {}
    for word in nltk.word_tokenize(formatted_article_text):
        if word not in stopwords:
            if word not in word_frequencies.keys():
                word_frequencies[word] = 1
            else:
                word_frequencies[word] += 1
    maximum_frequncy = max(word_frequencies.values())
    for word in word_frequencies.keys():  
        word_frequencies[word] = (word_frequencies[word]/maximum_frequncy)
    sentence_scores = {}
    for sent in sentence_list:
        for word in nltk.word_tokenize(sent.lower()):
            if word in word_frequencies.keys():
                if len(sent.split(' ')) < 30:
                    if sent not in sentence_scores.keys():
                        sentence_scores[sent] = word_frequencies[word]
                    else:
                        sentence_scores[sent] += word_frequencies[word]
    print(word_frequencies)
    print("\n\n\n")
    print(sentence_scores)
    summary_sentences = heapq.nlargest(3, sentence_scores, key=sentence_scores.get)
    summary = ' '.join(summary_sentences)
    return summary


def main():
    try:
        nltk.find("stopwords")
        nltk.find("punkt")
    except Exception:
        nltk.download("stopwords")
        nltk.download("punkt")
    fName = "test.txt"
    if not os.path.exists(fName):
        print("No tests file!")
        return
    text = ""
    with open(fName, "r", encoding="utf8") as f:
        text = f.read()
    result = summarize_text(text)
    print(result)


if __name__ == "__main__":
    main()
