from nltk.sentiment.vader import SentimentIntensityAnalyzer
from collections import deque

# VADER Sentiment Analysis
sia = SentimentIntensityAnalyzer()

# Deque to store the last three sentiment scores
sentiment_history = deque(maxlen=3)


# Get sentiment score. Unweighted. Only considers the most sentiment of most recent text input
def get_sentiment(text):
    """
    'neg' = The proportion of negative sentiment in the text
    'neu' = The proportion of neutral sentiment in the text
    'pos' = The proportion of positive sentiment in the text
    'compound' = The overall sentiment score, which is a weighted sum of all the individual sentiment scores
    'compound' ranges from [-1, 1]. 1 = highly pos, -1 = highly neg, 0 = neutral
    """
    sentiment = sia.polarity_scores(text)
    return sentiment


# Get weighted sentiment score. Considers the three most recent sentiment scores. Greater weight for more recent sentiments.
def get_weighted_sentiment(text):
    global sentiment_history
    sentiment = get_sentiment(text)
    # Append the new sentiment score (automatically removes oldest if more than 3)
    sentiment_history.append(sentiment)
    # Calculate weighted sentiment
    weighted_sentiment = calculate_weighted_sentiment()
    return weighted_sentiment


# Function to calculate weighted sentiment
def calculate_weighted_sentiment():
    global sentiment_history
    total_weight = 0
    weighted_sum = {"neg": 0, "neu": 0, "pos": 0, "compound": 0}

    # Define weights (most recent has highest weight)
    weights = [3, 2, 1]  # Adjust these weights as necessary

    for i, sentiment in enumerate(reversed(sentiment_history)):
        weight = weights[i]
        total_weight += weight
        weighted_sum["neg"] += sentiment["neg"] * weight
        weighted_sum["neu"] += sentiment["neu"] * weight
        weighted_sum["pos"] += sentiment["pos"] * weight
        weighted_sum["compound"] += sentiment["compound"] * weight

    # Normalize the weighted sum by the total weight to get the average
    if total_weight == 0:
        return {"neg": 0, "neu": 0, "pos": 0, "compound": 0}
    weighted_sentiment = {k: v / total_weight for k, v in weighted_sum.items()}
    return weighted_sentiment


if __name__ == "__main__":
    # Example usage
    text = "Python is good but not that good. I don't mind it."
    user_sentiment = get_sentiment(text)
    print(user_sentiment)
    print()

    text1 = "I love python"
    user_sentiment = get_sentiment(text1)
    print(user_sentiment)
    print()

    text2 = "I am not sure about Python"
    user_sentiment = get_sentiment(text2)
    print(user_sentiment)
    print()

    text3 = "I hate bugs in the code"
    user_sentiment = get_sentiment(text3)
    print(user_sentiment)
