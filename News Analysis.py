import pandas as pd
import re
from textblob import TextBlob
from collections import Counter

# Function to clean up articles
def clean_article(article):
    cleaned_article = re.sub(r'[^\w\s]', '', article.lower())  # Remove punctuation and convert to lowercase
    cleaned_article = ' '.join([word for word in cleaned_article.split() if word not in stopwords])
    return cleaned_article

# Function to check mood
def check_mood(article):
    analysis = TextBlob(article)
    if analysis.sentiment.polarity > 0:
        return "Positive"
    elif analysis.sentiment.polarity < 0:
        return "Negative"
    else:
        return "Neutral"

# Function to find connections
def find_connections(articles):
    themes = Counter()
    for article in articles:
        for theme in themes_list:
            if theme in article:
                themes[theme] += 1
    return themes.most_common()

# Function for aspect analysis
def aspect_analysis(article):
    aspects = {}
    for aspect in aspects_list:
        if aspect in article:
            sentiments = [check_mood(sentence) for sentence in article.split('.') if aspect in sentence]
            aspects[aspect] = Counter(sentiments)
    return aspects

# Load articles from CSV file
articles_df = pd.read_csv('Assignment.csv')

# List of common words to remove
stopwords = ['a', 'an', 'the', 'is', 'was', 'were', 'and', 'or', 'but', 'on', 'in', 'at', 'to', 'of', 'for', 'by', 'with']

# List of possible themes
themes_list = ['technology', 'artificial intelligence', 'cybersecurity', 'healthcare','development']

# List of possible aspects for aspect analysis
aspects_list = ['cost', 'innovation', 'impact', 'traffic']

# Clean up articles
articles_df['Cleaned_Article'] = articles_df['Article'].apply(clean_article)

# Check mood
articles_df['Mood'] = articles_df['Cleaned_Article'].apply(check_mood)

# Find connections
common_themes = find_connections(articles_df['Cleaned_Article'])

#Aspect Analysis (Optional)
articles_df['Aspect_Sentiments'] = articles_df['Article'].apply(aspect_analysis)

# Output results
print("Cleaned Articles:")
print(articles_df[['Article', 'Cleaned_Article']])
print("\nMood Ratings:")
print(articles_df[['Article', 'Mood']])
print("\nCommon Themes:")
print(common_themes)
print("\nAspect Analysis:")
print(articles_df[['Article', 'Aspect_Sentiments']])