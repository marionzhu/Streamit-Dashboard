import streamlit as st
import pandas as pd
from textblob import TextBlob
from collections import Counter
from wordcloud import WordCloud
import plotly.express as px
from matplotlib import pyplot as plt

# set the page 
st.set_page_config(
    page_title="Welcome to the Airline Sentiment Analysis",
    page_icon="✈️",
    layout="centered"
)

# set header 
st.header(f"Airline Sentiment Analysis ✈️")
st.header(" ")

# Load your dataset (replace with your path)
data = pd.read_csv("Tweets.csv")
print(data)

# Assuming stopwords are provided in a file or list. For demonstration, using a small sample.
stopwords = set(["the", "and", "to", "of", "a", "in", "for", "on", "is", "that", "with", \
                  "my", "you", "me","was","i","your", "it", "this", "am", "we", "be", "an"])


# User input for filtering data by airline
selected_airline = st.selectbox("Select Airline:", data["airline"].unique())
filtered_data = data[data["airline"] == selected_airline].copy()
st.subheader(" ")

# Preprocess text (lowercase and remove stop words)
def preprocess_text(text):
    words = TextBlob(text).words.lower()
    filtered_words = [word for word in words if word not in stopwords]
    return " ".join(filtered_words)

# Sentiment analysis with TextBlob
filtered_data["sentiment"] = filtered_data["text"].apply(lambda text: TextBlob(text).sentiment.polarity)

# Most used words (excluding stop words)
word_counts = Counter()
for text in filtered_data["text"]:
    processed_text = preprocess_text(text)
    word_counts.update(processed_text.split())

# Generate word cloud
cloudwords = WordCloud(background_color="white", width=800, height=600).generate_from_frequencies(word_counts)
plt.figure(figsize=(10, 7))
plt.imshow(cloudwords, interpolation="bilinear")
plt.axis("off")

st.subheader(f"Cloudwords of Most Used Words for {selected_airline} 🛫")
st.markdown("**Note:** Stop words excluded")
st.pyplot(plt)
st.subheader(" ")

# Treemap for sentiment distribution
sentiment_counts = filtered_data["sentiment"].value_counts().reset_index(name="Count")
sentiment_counts["sentiment_label"] = sentiment_counts["sentiment"].apply(lambda score: "Positive" if score > 0 else ("Negative" if score < 0 else "Neutral"))

sentiment_treemap = px.treemap(
    sentiment_counts,
    path=["sentiment_label"],
    values="Count",
    # title="Sentiment Distribution",
    # color_discrete_sequence=["green", "red","gray"]  # Customize colors for sentiment labels
)
sentiment_treemap.update_layout(margin = dict(t=0, b=25))

st.subheader(f"Treemap of Sentiment Distribution for {selected_airline} 🛩️")
st.plotly_chart(sentiment_treemap)
st.markdown("**Note:** TextBlob's sentiment scores range from -1 (negative) to 1 (positive). The treemap displays the distribution of these scores.")
