from textblob import TextBlob

def forex_sentiment(text):
    """
    Analyzes sentiment of forex-related text.
    Returns polarity score and sentiment label.
    """
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity

    if polarity > 0.1:
        sentiment = "Bullish"
    elif polarity < -0.1:
        sentiment = "Bearish"
    else:
        sentiment = "Neutral"

    return {"polarity": polarity, "sentiment": sentiment}

# Example usage
headline1 = "USD strengthens as Fed signals rate hike"
headline = "The dollar bear market isn’t over, Morgan Stanley says"
result = forex_sentiment(headline)
print(result)