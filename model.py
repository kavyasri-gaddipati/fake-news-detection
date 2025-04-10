import pickle
import re
import string
from sklearn.feature_extraction.text import TfidfVectorizer

# Load your saved model
with open('fake_news_model.pkl', 'rb') as model_file:
    model = pickle.load(model_file)

# Load the vectorizer
with open('vectorizer.pkl', 'rb') as vectorizer_file:
    vectorizer = pickle.load(vectorizer_file)

# Preprocess text (same as in your model training code)
def preprocess_text(text):
    text = text.lower()
    text = re.sub(r'\[.*?\}', '', text)
    text = re.sub(r"\\W", " ", text)
    text = re.sub(r'https?://\S+|www\.\S+', '', text)
    text = re.sub(r'<.*?>+', '', text)
    text = re.sub(r'[%s]' % re.escape(string.punctuation), '', text)
    text = re.sub(r'\n', '', text)
    text = re.sub(r'\w*\d\w*', '', text)
    return text

# Prediction function
def predict_news(news_text):
    processed_text = preprocess_text(news_text)
    vectorized_text = vectorizer.transform([processed_text])
    prediction = model.predict(vectorized_text)
    return "Fake News" if prediction[0] == 0 else "Not a Fake News"
