from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline
import torch

# Load FinBERT model
model_name = "ProsusAI/finbert"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSequenceClassification.from_pretrained(model_name)

# Create sentiment analysis pipeline
device = 0 if torch.cuda.is_available() else -1
finbert = pipeline("sentiment-analysis", model=model, tokenizer=tokenizer, device=device)

def analyze_forex_news(news_text):
    """
    Analyze sentiment of forex-related news using FinBERT.
    Returns sentiment label and confidence score.
    """
    result = finbert(news_text)[0]
    return {
        "text": news_text,
        "sentiment": result['label'],
        "confidence": round(result['score'], 4)
    }

# Example usage
headline = """The dollar’s recent resilience should not be mistaken for the end of its downturn, according to Morgan Stanley, which argues that the U.S. currency’s bear market still has further to run.

Despite a slide in front-end Treasury yields and political noise around the Federal Reserve, the greenback has held steady.

Some investors see this as a sign that the dollar’s decline has already played out, supported by U.S. equities outperforming global peers and the perception that the American economy can absorb import tariffs more easily than others.

Yet Morgan Stanley strategist James K. Lord opposes that view.

“We are not convinced that the dollar’s downtrend has run its course – on the contrary, we think its decline is barely halfway through,” he said in a Sunday note.

The bank’s economics team expects U.S. GDP growth to slow to around 1% by the fourth quarter of 2025 and stay only slightly higher in 2026, levels that hardly signal outperformance relative to the rest of the world.

A weaker labor market adds to the downside risks. Lower growth, coupled with the Fed’s readiness to tolerate inflation above target, could push real yields lower. Historically, that has been a headwind for the dollar.

Morgan Stanley’s rates team remains positioned for further easing, holding a long in the five-year Treasury note on expectations that the front end of the curve could price a deeper cycle.

This could reinforce dollar weakness by encouraging foreign investors to hedge their U.S. assets."""
print(analyze_forex_news(headline))
