from collections import Counter
import numpy as np

class SentimentAggregator:
    @staticmethod
    def aggregate_sentiment(sentiment_results):
        """Aggregate sentiment results from multiple news items."""
        if not sentiment_results:
            return {"overall_sentiment": "neutral", "confidence": 0.0, "details": {}}
            
        # Count sentiment labels
        sentiment_counts = Counter([result["label"] for result in sentiment_results])
        
        # Calculate average scores for each sentiment
        sentiment_scores = {
            "positive": [],
            "neutral": [],
            "negative": []
        }
        
        for result in sentiment_results:
            for label in sentiment_scores.keys():
                if label in result["scores"]:
                    sentiment_scores[label].append(result["scores"][label])
        
        # Calculate average scores
        avg_scores = {
            label: np.mean(scores) if scores else 0.0 
            for label, scores in sentiment_scores.items()
        }
        
        # Get the most frequent sentiment label
        most_common_sentiment = sentiment_counts.most_common(1)[0][0]
        
        # Calculate confidence (percentage of items with the most common sentiment)
        confidence = sentiment_counts[most_common_sentiment] / len(sentiment_results)
        
        return {
            "overall_sentiment": most_common_sentiment,
            "confidence": float(confidence),
            "distribution": {label: count/len(sentiment_results) for label, count in sentiment_counts.items()},
            "average_scores": avg_scores,
            "item_count": len(sentiment_results)
        }