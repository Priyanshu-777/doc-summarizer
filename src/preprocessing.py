import re
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer



def download_nltk_data():
    
    resources = ["punkt", "punkt_tab", "stopwords", "wordnet"]
    for resource in resources:
        nltk.download(resource, quiet=True)



def preprocess_text(text):
   
    # Convert to lowercase
    text = text.lower()

    # Remove special characters (keep alphanumeric and spaces)
    text = re.sub(r"[^a-zA-Z0-9\s]", "", text)

    # Remove extra whitespace
    text = re.sub(r"\s+", " ", text).strip()

    return text



def tokenize_sentences(text):
    
    if not text or not text.strip():
        return []
    return sent_tokenize(text)


def tokenize_words(text):
    
    if not text or not text.strip():
        return []
    return word_tokenize(text)



def remove_stopwords(words):
   
    stop_words = set(stopwords.words("english"))
    return [word for word in words if word.lower() not in stop_words]


def lemmatize_words(words):
    
    lemmatizer = WordNetLemmatizer()
    return [lemmatizer.lemmatize(word) for word in words]



def preprocess_sentence(sentence):
    
    # Clean the text(lowercase + remove special chars)
    cleaned = preprocess_text(sentence)

    # Tokenize into words
    words = tokenize_words(cleaned)

    # Remove stopwords
    filtered_words = remove_stopwords(words)
    
    lemmatized_words = lemmatize_words(filtered_words)


    
    return " ".join(lemmatized_words)
