import os
from datetime import datetime, timedelta
from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import re
from api_client import FinancialNewsClient
from preprocessor import TextPreprocessor
from sentiment_analyzer import FinBERTSentimentAnalyzer
from aggregator import SentimentAggregator

app = FastAPI(title="Financial Sentiment Analysis API")

# Initialize components
news_client = FinancialNewsClient()
preprocessor = TextPreprocessor()
sentiment_analyzer = FinBERTSentimentAnalyzer()
aggregator = SentimentAggregator()

@app.get("/")
def read_root():
    return {"message": "Financial Sentiment Analysis API"}

# Updated app.py with better error handling
@app.get("/sentiment")
async def get_sentiment(
    ticker: str = Query(..., description="Company ticker symbol (e.g., AAPL)"),
    days: int = Query(7, description="Number of days to look back for news", ge=1, le=30)
):
    # Validate ticker format
    ticker = ticker.strip().upper()
    if not re.match(r'^[A-Z]{1,5}$', ticker):
        return JSONResponse(
            content={
                "error": "Invalid ticker format",
                "message": "Please provide a valid stock ticker symbol (e.g., AAPL, MSFT, TSLA)",
                "example": "/sentiment?ticker=AAPL&days=7"
            },
            status_code=400
        )
    
    try:
        # Calculate date range
        today = datetime.now()
        from_date = (today - timedelta(days=days)).strftime("%Y-%m-%d")
        to_date = today.strftime("%Y-%m-%d")
        
        # Get news data
        try:
            news_items = news_client.get_company_news(ticker, from_date, to_date)
        except Exception as e:
            if "API request failed" in str(e):
                return JSONResponse(
                    content={
                        "error": "API request failed",
                        "message": f"Could not retrieve news for ticker {ticker}. The ticker may not exist or there could be an issue with the API.",
                        "details": str(e)
                    },
                    status_code=404
                )
            raise
        
        if not news_items:
            return JSONResponse(
                content={
                    "ticker": ticker,
                    "message": f"No news found for {ticker} in the last {days} days",
                    "period": {"from": from_date, "to": to_date},
                    "sentiment": {
                        "overall_sentiment": "neutral",
                        "confidence": 0.0,
                        "distribution": {},
                        "average_scores": {"positive": 0.0, "neutral": 0.0, "negative": 0.0},
                        "item_count": 0
                    }
                },
                status_code=200  # Changed from 404 to 200 as this is a valid result
            )
        
        # Process each news item
        sentiment_results = []
        processed_items = []
        
        for item in news_items:
            # Extract and preprocess headline and summary
            headline = preprocessor.preprocess(item.get("headline", ""))
            summary = preprocessor.preprocess(item.get("summary", ""))
            
            # Combine headline and summary for analysis
            text = f"{headline} {summary}".strip()
            if not text:
                continue
                
            # Analyze sentiment
            sentiment = sentiment_analyzer.analyze(text)
            sentiment_results.append(sentiment)
            
            # Store processed item
            processed_items.append({
                "datetime": item.get("datetime"),
                "headline": headline,
                "sentiment": sentiment["label"],
                "score": sentiment["score"]
            })
        
        # Aggregate results
        aggregated_sentiment = aggregator.aggregate_sentiment(sentiment_results)
        
        return {
            "ticker": ticker,
            "period": {"from": from_date, "to": to_date},
            "sentiment": aggregated_sentiment,
            "news_items": processed_items[:10]  # Return only first 10 for brevity
        }
        
    except Exception as e:
        # Log the detailed error for debugging
        import traceback
        print(f"Error processing request: {str(e)}")
        print(traceback.format_exc())
        
        # Return a user-friendly error
        return JSONResponse(
            content={
                "error": "Internal server error",
                "message": "An unexpected error occurred while processing your request.",
                "ticker": ticker,
                "days": days
            },
            status_code=500
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)