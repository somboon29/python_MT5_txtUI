# Install required packages if you haven't:
# pip install transformers torch pandas

import pandas as pd
from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline
import torch

# Load FinBERT model
model_name = "ProsusAI/finbert"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSequenceClassification.from_pretrained(model_name)

# Create sentiment analysis pipeline
device = 0 if torch.cuda.is_available() else -1
finbert = pipeline("sentiment-analysis", model=model, tokenizer=tokenizer, device=device)

# Sample forex headlines
data = {
    "headline": [
        "Dollar weakens as inflation slows",
        "Euro rises amid ECB rate hike speculation",
        "Yen tumbles after BoJ maintains ultra-loose policy",
        "US PPI expected to highlight sticky inflation before crucial CPI report",
        "EUR: Dollar story dominates over French politics – ING"
    ]
}

# Create DataFrame
df = pd.DataFrame(data)

# Apply FinBERT sentiment analysis
def get_sentiment(text):
    result = finbert(text)[0]
    return pd.Series([result['label'], round(result['score'], 4)])

# Add sentiment columns
df[['sentiment', 'confidence']] = df['headline'].apply(get_sentiment)

# Display results
print(df)
