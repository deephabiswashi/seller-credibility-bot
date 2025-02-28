import nltk
from transformers import pipeline

# Download required NLTK data (vader lexicon) if not already present
nltk.download('vader_lexicon', quiet=True)
from nltk.sentiment.vader import SentimentIntensityAnalyzer

def analyze_sentiment(text: str) -> dict:
    """
    Analyze sentiment using NLTK VADER.
    Returns a dictionary with sentiment scores.
    """
    sia = SentimentIntensityAnalyzer()
    sentiment = sia.polarity_scores(text)
    return sentiment

def analyze_with_llm(text: str) -> str:
    """
    Use a transformer-based sentiment analysis as a proxy for credibility detection.
    Here, we use a pre-trained sentiment analysis model from Hugging Face.
    In a real application, you might use a more specialized/fine-tuned model.
    """
    classifier = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")
    # For inference speed, we limit the input to the first 512 characters.
    result = classifier(text[:512])
    label = result[0]['label']
    score = result[0]['score']
    if label == "NEGATIVE" and score > 0.7:
        return "The seller seems to have negative signals. Exercise caution."
    elif label == "POSITIVE" and score > 0.7:
        return "The seller appears credible based on the sentiment of the content."
    else:
        return "The seller's credibility is uncertain. Further review may be necessary."

def combined_analysis(text: str) -> str:
    """
    Combine analyses from NLTK and the transformer model to provide a final suggestion.
    """
    nltk_sentiment = analyze_sentiment(text)
    llm_analysis = analyze_with_llm(text)
    
    # A simple heuristic: if the compound sentiment is strongly negative, warn the user.
    compound = nltk_sentiment.get("compound", 0)
    if compound < -0.2:
        final = "Based on NLTK sentiment analysis, there are negative signals. " + llm_analysis
    elif compound > 0.2:
        final = "Based on NLTK sentiment analysis, the signals are positive. " + llm_analysis
    else:
        final = "The sentiment analysis is neutral. " + llm_analysis
    return final
